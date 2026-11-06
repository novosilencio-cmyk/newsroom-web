import importlib.util
import io
import stat
import unittest
from pathlib import Path
from types import SimpleNamespace

spec = importlib.util.spec_from_file_location('onecom', Path(__file__).resolve().parents[1] / 'scripts/deploy_onecom.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class RemoteFile(io.BytesIO):
    def prefetch(self):
        pass

class FakeSFTP:
    def __init__(self, fail=False):
        self.files = {'/site/index.html': b'old', '/site/asset.css': b'oldcss'}
        self.fail = fail
    def open(self, path, mode):
        if path not in self.files:
            raise FileNotFoundError(2, 'absent')
        return RemoteFile(self.files[path])
    def normalize(self, path):
        return '/private'
    def stat(self, path):
        return SimpleNamespace(st_mode=stat.S_IFDIR | 0o755)
    def lstat(self, path):
        if path not in self.files:
            raise FileNotFoundError(2, 'absent')
        return SimpleNamespace(st_mode=stat.S_IFREG | 0o644)
    def chmod(self, *args):
        pass
    def putfo(self, source, target, **kwargs):
        self.files[target] = source.read()
    def posix_rename(self, source, target):
        if self.fail and target == '/site/index.html':
            raise OSError('simulated promotion failure')
        self.files[target] = self.files.pop(source)
    def remove(self, path):
        del self.files[path]
    def rmdir(self, path):
        pass

class DeploymentTests(unittest.TestCase):
    def test_private_copy_preserves_bytes_before_source_removal(self):
        remote = FakeSFTP()
        module.preserve_copy(remote, '/site/index.html', '/private/index.html')
        self.assertEqual(remote.files['/private/index.html'], b'old')
        self.assertNotIn('/site/index.html', remote.files)
    def test_archive_collision_preserves_both_originals(self):
        remote = FakeSFTP()
        remote.files['/private/index.html'] = b'different'
        with self.assertRaises(ValueError):
            module.preserve_copy(remote, '/site/index.html', '/private/index.html')
        self.assertEqual(remote.files['/site/index.html'], b'old')
        self.assertEqual(remote.files['/private/index.html'], b'different')
    def test_rejects_escaping_and_ambiguous_paths(self):
        for path in ('../x', '/x', '.', 'x/../y', 'x//y', 'x\ny'):
            with self.assertRaises(ValueError):
                module.safe_name(path)
    def test_failed_promotion_restores_prior_assets(self):
        remote = FakeSFTP(fail=True)
        with self.assertRaises(OSError):
            module.deploy(remote, '/site', {'asset.css': b'newcss', 'index.html': b'new'}, '1-1')
        self.assertEqual(remote.files['/site/asset.css'], b'oldcss')
        self.assertEqual(remote.files['/site/index.html'], b'old')
        self.assertIn('/private/onecom-deploy-backups/1-1.zip', remote.files)
    def test_success_verifies_and_preserves_backup(self):
        remote = FakeSFTP()
        module.deploy(remote, '/site', {'asset.css': b'newcss', 'index.html': b'new'}, '2-1')
        self.assertEqual(remote.files['/site/index.html'], b'new')
        self.assertIn('/private/onecom-deploy-backups/2-1.zip', remote.files)

if __name__ == '__main__':
    unittest.main()
