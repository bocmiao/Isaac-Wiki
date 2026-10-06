"""Build offline lookup facts from pinned enum definitions and reviewed site guides.
Usage: python3 scripts/generate-save-progress-data.py ISAACSCRIPT_CHECKOUT
"""
import json
import re
import runpy
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
GEN = runpy.run_path(str(ROOT / 'scripts/generate-entry-pages.py'))
reference = Path(sys.argv[1])
enums = reference / 'packages/isaac-typescript-definitions-repentogon/src/enums'
def enum(file):
    return {name: int(value) for name, value in re.findall(r'^  ([A-Z0-9_]+) = (-?\d+),', (enums / file).read_text(), re.M)}
events = enum('EventCounter.ts')
ach_ids = enum('Achievement.ts')
def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'\{#[^}]+\}|\{\.ach-links\}|<[^>]+>|[*`]', '', text)
    text = re.sub(r'(?m)^:::.*$', '', text)
    return '\n'.join(line.rstrip() for line in text.splitlines()).strip()
achievements = json.loads((DOCS / '.vitepress/theme/data/achievements.json').read_text())
for achievement in achievements:
    source = (DOCS / ('achievements/' + achievement['page'] + '.md')).read_text()
    part = re.split(r'(?m)^## ', source.split('{#achievement-' + str(achievement['id']) + '}', 1)[1], 1)[0]
    achievement['tutorial'] = plain(part.split('相关：', 1)[0])
items = []
for item in GEN['ITEMS'].values():
    key = item['key']
    page = (DOCS / ('items/' + key + '.md')).read_text()
    acquisition = page.split('## 解锁与获取', 1)[1].split('## 使用与取舍', 1)[0]
    effects = page.split('## 效果与数值', 1)[1].split('## 解锁与获取', 1)[0]
    items.append({'key': key, 'kind': item['kind'], 'id': item['id'], 'name': GEN['SPECIAL_NAMES'].get(key, item['name']),
                  'en': item['en'], 'unlocks': [row['id'] for row in GEN['unlocks'](item)],
                  'collection': item['kind'] == 'c' and item['metadata'].get('hidden') != 'true',
                  'hidden': item['metadata'].get('hidden') == 'true',
                  'group': GEN['KIND_NAMES'][item['metadata'].get('type', item['kind'])],
                  'effects': plain(effects), 'acquisition': plain(acquisition)})
profiles = json.loads((DOCS / '.vitepress/theme/data/catalog/characters.json').read_text())
names = ['ISAAC','MAGDALENE','CAIN','JUDAS','BLUE_BABY','EVE','SAMSON','AZAZEL','LAZARUS','EDEN','THE_LOST','LILITH','KEEPER','APOLLYON','THE_FORGOTTEN','BETHANY','JACOB_AND_ESAU']
targets = {'heart':'KILL_MOMS_HEART','isaac':'KILL_ISAAC','satan':'KILL_SATAN','bluebaby':'KILL_BLUE_BABY','lamb':'KILL_THE_LAMB','megasatan':'KILL_MEGA_SATAN','bossrush':'BOSSRUSH_CLEARED','hush':'KILL_HUSH','greed':'GREED_MODE_CLEARED','delirium':'KILL_DELIRIUM','mother':'KILL_MOTHER','beast':'KILL_BEAST'}
mark_names = dict(re.findall(r"\{ id: '([^']+)', name: '([^']+)'", (DOCS / '.vitepress/theme/data/characters.ts').read_text()))
characters = []
for index, profile in enumerate(profiles):
    code = names[index % 17]
    tainted = index >= 17
    unlock_code = ('TAINTED_' if tainted else '') + code.replace('THE_', '')
    event_code = ('T_' if tainted else '') + code
    marks = [{'id': ident, 'name': mark_names[ident], 'counter': events['PROGRESSION_' + target + '_WITH_' + event_code]} for ident, target in targets.items()]
    donation_code = 'GREED_MODE_COINS_DONATED_WITH_' + event_code
    if code == 'BLUE_BABY' and not tainted: donation_code = 'GREED_MODE_COINS_DONATED_WITH_BLUE'
    if code == 'THE_FORGOTTEN' and not tainted: donation_code = 'GREED_MODE_COINS_DONATED_WITH_FORGOTTEN'
    characters.append({'id': profile['id'], 'name': profile['name'], 'en': profile['en'], 'group': profile['group'],
                       'achievement': 0 if unlock_code == 'ISAAC' else ach_ids[unlock_code],
                       'marks': marks, 'donationCounter': events[donation_code]})
result = {'isaacScriptCommit': subprocess.check_output(['git','-C',str(reference),'rev-parse','HEAD'], text=True).strip(),
          'achievements': achievements, 'items': items, 'characters': characters,
          'challenges': json.loads((DOCS / '.vitepress/theme/data/challenges.json').read_text()),
          'donations': {'normal': events['DONATION_MACHINE_COUNTER'], 'greed': events['GREED_DONATION_MACHINE_COUNTER']}}
out = ROOT / 'local-tools/progress/data.json'
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
print('Offline lookup generated:', len(achievements), 'achievements,', len(items), 'items,', len(characters), 'characters.')
