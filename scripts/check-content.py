"""Check reviewed IDs and cross-page claims that a normal link check cannot catch."""
import json,re,runpy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs'
GEN=runpy.run_path(str(ROOT/'scripts/generate-entry-pages.py'));errors=[]
for row in json.loads((DOCS/'.vitepress/theme/data/catalog/items.json').read_text()):
 item=GEN['ITEMS'][row['id']];expected=GEN['SPECIAL_NAMES'].get(row['id'],item['name'])
 if row['name']!=expected:errors.append(f'Wrong canonical name: {row["id"]}')
for path in DOCS.rglob('*.md'):
 text=path.read_text()
 if '在线联机的胜利圈不受影响' in text:errors.append(f'Unsupported eligibility: {path}')
 if '[网页图鉴](/about)' in text:errors.append(f'Wrong catalog destination: {path}')
 if '弹珠（Marbles）' in text:errors.append(f'Noncanonical Marbles: {path}')
 if '注意：：' in text:errors.append(f'Doubled warning punctuation: {path}')
 if path.name=='console-generator.md' and '不含模组道具、饰品、卡牌和胶囊' in text:errors.append(f'Stale console capabilities: {path}')
 for old in ['水潭','水牢','深牢','矿井']:
  if old in text:errors.append(f'Outdated floor name {old}: {path}')
for family in ['boss','pickup']:
 rows=json.loads((ROOT/f'data/{family}-guides.json').read_text())
 if len({x['id'] for x in rows})!=len(rows):errors.append(f'Duplicate {family} keys')
 known={x['id'] for x in json.loads((ROOT/'data/achievement-source.json').read_text())}
 for row in rows:
  if row.get('achievement') and row['achievement'] not in known:errors.append(f'Unknown unlock: {row["id"]}')
for row in json.loads((DOCS/'.vitepress/theme/data/synergies.json').read_text()):
 if not all('c'+str(id) in GEN['ITEMS'] for id in row['items']):errors.append(f'Unknown combo ID: {row["id"]}')
 if not row.get('limits') or not row.get('version'):errors.append(f'Unqualified combo: {row["id"]}')
if errors:raise SystemExit('\n'.join(errors))
print('PASS canonical item names, eligibility claims, catalog destinations and reviewed guide IDs')
