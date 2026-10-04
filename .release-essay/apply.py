"""Transport fixed reviewed attestations; do not calculate approval or review status."""
from pathlib import Path
import json,hashlib,shutil,copy
root=Path(__file__).resolve().parents[1]
stage=root/'.release-essay'
fixed=json.loads((stage/'review.json').read_text())
assert len(fixed['hashes'])==12
sources=root/'content/essays/not-necessarily-an-order-2026'
assert {p.stem for p in sources.glob('*.md')}=={'nb','en','fr','zh-Hans','ja','es','de','pt','ko','ar'}
rows={}
for rel,expected in fixed['hashes'].items():
    assert hashlib.sha256((root/rel).read_bytes()).hexdigest()==expected,rel
    row=copy.deepcopy(fixed['common'])
    row['sha256']=expected
    row['publication_approval']={**fixed['approval'],'sha256':expected}
    rows[rel]=row
p=root/'docs/editorial/language-reviews.json'
before=json.loads(p.read_text());before.update(rows)
p.write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
p=root/'scripts/approved_norwegian_phrases.json'
before=json.loads(p.read_text());delta=json.loads((stage/'phrase-delta.json').read_text())
for key,phrases in delta.items():
    assert key in fixed['hashes']
    before[key]=list(dict.fromkeys(before.get(key,[])+phrases))
p.write_text(json.dumps(before,ensure_ascii=False,indent=2)+'\n')
shutil.rmtree(stage)
print('Fixed attestations matched all 12 page hashes; ten source languages verified; temporary helpers removed.')
