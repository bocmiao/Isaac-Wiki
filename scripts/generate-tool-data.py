"""Extract tool lookup data from the reviewed repository tables and local upstream snapshots."""
import argparse,json,re
from pathlib import Path
root=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--isaacdocs',type=Path,required=True);p.add_argument('--eid',type=Path,required=True);args=p.parse_args()
text=(root/'docs/strategy/challenges.md').read_text()
def clean(s):return re.sub(r'\[([^\]]+)\]\([^)]+\)',r'\1',re.sub('<[^>]+>',' ',s)).strip()
rows=[]
for line in text.splitlines():
 cells=[c.strip()for c in line.strip('|').split('|')]
 if len(cells)==7 and cells[0].isdigit():
  num=int(cells[0]);rows.append(dict(id=num,name=clean(cells[1].split('<br>')[0]),description=clean(cells[1]),character=cells[2],target=cells[3],rules=clean(cells[4]),reward=clean(cells[5]),unlock=clean(cells[6])))
assert [r['id']for r in rows]==list(range(1,46))
folder=root/'docs/.vitepress/theme/data'
(folder/'challenges.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
names={'en':{},'zh':{}}
for version in ['ab+','rep','rep+']:
 for lang,key in [('en_us','en'),('zh_cn','zh')]:
  text=(args.eid/f'descriptions/{version}/{lang}.lua').read_text().split('---------- Trinkets')[0]
  for ident,name in re.findall(r'\{\s*"(\d+)"\s*,\s*"([^"\n]+)"',text):names[key][int(ident)]=name
items=[]
for n,enum in re.findall(r'\|(\d+)\s*\|COLLECTIBLE_([A-Z0-9_]+)',(args.isaacdocs/'docs/enums/CollectibleType.md').read_text()):
 ident=int(n)
 if ident>0 and ident in names['en'] and ident in names['zh']:
  items.append(dict(id=ident,en=names['en'][ident],name=names['zh'][ident],enum='COLLECTIBLE_'+enum))
assert len(items)>700 and len({x['id']for x in items})==len(items)
assert next(x for x in items if x['id']==105)['en']=='The D6'
(folder/'item-links.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
source=json.loads((root/'data/achievement-source.json').read_text());normal=[]
for r in source:
 m=re.fullmatch(r'Donate (\d+) [Cc]oins to the Donation Machine',r['condition'])
 if m:normal.append(dict(coins=int(m[1]),id=r['id'],name=r['name']))
normal.sort(key=lambda x:x['coins'])
(folder/'normal-donations.json').write_text(json.dumps(normal,ensure_ascii=False,indent=2)+'\n')
print(f'Extracted {len(rows)} challenges, {len(items)} verified collectible IDs, {len(normal)} normal donation milestones')
