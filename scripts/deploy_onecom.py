#!/usr/bin/env python3
"""Deploy a checked _site over pinned SFTP, with private backup and readback."""
import argparse
import base64
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import stat
import zipfile

HOST = 'ssh.cyi2nwq1l.service.one'
USER = 'cyi2nwq1l_ssh'
# First connection observed 2026-11-03; later changes fail closed.
KEY = 'AAAAC3NzaC1lZDI1NTE5AAAAIHqIQzp1R9ZzoL0Mw4ERjRBsiHP10j8LkY8ch8C/vtyt'
ROOTS = {'staging': '/webroots/8582494d', 'production': '/webroots/79f29e95'}
MANIFEST = '.onecom-manifest.json'

def safe_name(name):
    path = PurePosixPath(name)
    if not name or name == '.' or path.is_absolute() or '..' in path.parts or str(path) != name or any(ord(c) < 32 for c in name):
        raise ValueError('Unsafe deployment path')
    return name

def digest(data):
    return hashlib.sha256(data).hexdigest()

def payload(directory, staging=False):
    result = {}
    for path in sorted(Path(directory).rglob('*')):
        if path.is_symlink():
            raise ValueError('Deployment input must not contain symlinks')
        if path.is_file():
            name = safe_name(path.relative_to(directory).as_posix())
            result[name] = path.read_bytes()
    if not result.get('index.html') or len(result) < 50:
        raise ValueError('Incomplete public build')
    # Hosting-only controls; preserve checked public HTML byte for byte.
    result['.htaccess'] = (b'Options -Indexes\nRewriteEngine On\n'
        b'RewriteCond %{HTTP_HOST} ^www\\.experimentalnewsroom\\.org$ [NC]\n'
        b'RewriteRule ^ https://experimentalnewsroom.org%{REQUEST_URI} [R=301,L]\n'
        b'RewriteCond %{HTTPS} !=on\n'
        b'RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]\n'
        b'<Files ".onecom-manifest.json">\nRequire all denied\n</Files>\n'
        + (b'Header set X-Robots-Tag "noindex, nofollow"\n' if staging else b''))
    result[MANIFEST] = json.dumps({name: digest(data) for name, data in result.items()},
                                  sort_keys=True).encode()
    return result

def read_optional(sftp, path):
    try:
        with sftp.open(path, 'rb') as f:
            f.prefetch()
            return f.read()
    except OSError as error:
        if error.errno == 2:
            return None
        raise

def mkdirs(sftp, path, mode=0o755):
    parent = str(PurePosixPath(path).parent)
    try:
        item = sftp.stat(path)
        if not stat.S_ISDIR(item.st_mode):
            raise ValueError('Expected directory')
    except OSError as error:
        if error.errno != 2:
            raise
        if parent != path:
            mkdirs(sftp, parent, mode)
        sftp.mkdir(path, mode)

def put_bytes(sftp, path, data, mode=0o644):
    mkdirs(sftp, str(PurePosixPath(path).parent))
    sftp.putfo(io.BytesIO(data), path, file_size=len(data), confirm=True)
    sftp.chmod(path, mode)

def deploy(sftp, root, files, run_id):
    old_manifest = read_optional(sftp, root + '/' + MANIFEST)
    previous_names = set(json.loads(old_manifest)) if old_manifest else set()
    for name in previous_names:
        safe_name(name)
    names = set(files) | previous_names
    originals = {name: read_optional(sftp, root + '/' + name) for name in names}
    changed = {name: data for name, data in files.items() if originals[name] != data}
    print('Compared existing files; changed=' + str(len(changed)), flush=True)
    home = sftp.normalize('.')
    backup_dir = home + '/onecom-deploy-backups'
    mkdirs(sftp, backup_dir, 0o700)
    sftp.chmod(backup_dir, 0o700)
    backup = io.BytesIO()
    with zipfile.ZipFile(backup, 'w', zipfile.ZIP_DEFLATED) as z:
        for name, data in originals.items():
            if data is not None:
                z.writestr(name, data)
        z.writestr('_rollback.json', json.dumps({'root': root, 'absent': [n for n, d in originals.items() if d is None]}))
    backup_path = backup_dir + '/' + run_id + '.zip'
    put_bytes(sftp, backup_path, backup.getvalue(), 0o600)
    if read_optional(sftp, backup_path) != backup.getvalue():
        raise RuntimeError('Backup verification failed; no public files changed')
    stage = root + '/.onecom-stage-' + run_id
    mkdirs(sftp, stage)
    # Upload and verify every candidate before touching an existing public file.
    for name, data in changed.items():
        put_bytes(sftp, stage + '/' + name, data)
        if read_optional(sftp, stage + '/' + name) != data:
            raise RuntimeError('Staged file readback failed')
    touched = []
    try:
        # Assets first, index and manifest last. Rename is atomic per file.
        ordered = sorted(changed, key=lambda n: (n == MANIFEST, n == 'index.html', n.endswith('.html'), n))
        for name in ordered:
            mkdirs(sftp, str(PurePosixPath(root + '/' + name).parent))
            sftp.posix_rename(stage + '/' + name, root + '/' + name)
            touched.append(name)
        for name in previous_names - set(files):
            sftp.remove(root + '/' + name)
            touched.append(name)
        for name, data in changed.items():
            if read_optional(sftp, root + '/' + name) != data:
                raise RuntimeError('Published file readback failed')
    except Exception:
        for name in reversed(touched):
            old = originals[name]
            if old is None:
                sftp.remove(root + '/' + name)
            else:
                put_bytes(sftp, root + '/' + name, old)
        raise
    # Only empty staging directories are removed; private backup is retained.
    dirs = {stage}
    for name in changed:
        parent = PurePosixPath(stage + '/' + name).parent
        while str(parent).startswith(stage):
            dirs.add(str(parent))
            if str(parent) == stage:
                break
            parent = parent.parent
    for path in sorted(dirs, key=len, reverse=True):
        sftp.rmdir(path)
    print(json.dumps({'target': root, 'verified_files': len(files), 'backup': backup_path}))

def preserve_copy(sftp, source, destination):
    """Cross-filesystem move: verify a private copy before removing its source."""
    info = sftp.lstat(source)
    if stat.S_ISLNK(info.st_mode):
        raise ValueError('Refusing symlink in migration artifacts')
    if stat.S_ISDIR(info.st_mode):
        mkdirs(sftp, destination, 0o700)
        for child in sftp.listdir(source):
            safe_name(child)
            if '/' in child:
                raise ValueError('Invalid directory entry')
            preserve_copy(sftp, source + '/' + child, destination + '/' + child)
        sftp.rmdir(source)
        return
    if not stat.S_ISREG(info.st_mode):
        raise ValueError('Unsupported migration artifact')
    data = read_optional(sftp, source)
    existing = read_optional(sftp, destination)
    if existing is not None and existing != data:
        raise ValueError('Existing private archive differs; preserving both')
    if existing is None:
        put_bytes(sftp, destination, data, 0o600)
    if read_optional(sftp, destination) != data:
        raise RuntimeError('Private artifact copy failed verification')
    sftp.remove(source)

def preserve_migration_artifacts(sftp, root):
    """Move only the eight known migration leftovers out of the public webroot."""
    destination = sftp.normalize('.') + '/onecom-migration-artifacts'
    mkdirs(sftp, destination, 0o700)
    sftp.chmod(destination, 0o700)
    for name in ('expnr-pages', 'expnr-probe', 'expnr-stage', 'expnr-complete.zip',
                 'expnr-onecom-164dc038.zip', 'expnr-pages.zip',
                 'expnr-portable.zip', 'expnr-probe.zip'):
        try:
            sftp.lstat(root + '/' + name)
        except OSError as error:
            if error.errno == 2:
                continue
            raise
        preserve_copy(sftp, root + '/' + name, destination + '/' + name)
        print('Preserved migration artifact outside webroot: ' + name)

def main():
    import paramiko
    parser = argparse.ArgumentParser()
    parser.add_argument('target', choices=ROOTS)
    args = parser.parse_args()
    run_id = safe_name(os.environ['GITHUB_RUN_ID'] + '-' + os.environ['GITHUB_RUN_ATTEMPT'])
    if '/' in run_id:
        raise ValueError('Invalid run ID')
    files = payload('_site', args.target == 'staging')
    client = paramiko.SSHClient()
    client.get_host_keys().add(HOST, 'ssh-ed25519', paramiko.Ed25519Key(data=base64.b64decode(KEY)))
    client.set_missing_host_key_policy(paramiko.RejectPolicy())
    client.connect(HOST, username=USER, password=os.environ['ONECOM_SFTP_PASSWORD'],
                   allow_agent=False, look_for_keys=False, timeout=20, auth_timeout=20)
    try:
        with client.open_sftp() as sftp:
            sftp.get_channel().settimeout(60)
            deploy(sftp, ROOTS[args.target], files, run_id)
            if args.target == 'production':
                preserve_migration_artifacts(sftp, ROOTS[args.target])
    finally:
        client.close()

if __name__ == '__main__':
    main()
