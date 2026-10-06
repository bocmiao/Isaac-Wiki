"""Import factual item descriptions and metadata without executing upstream Lua.

Usage: python3 scripts/import-item-source.py EID_CHECKOUT ISAACDOCS_CHECKOUT
All inputs are pinned in data/item-source.README.md. Site generation is offline.
"""
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRING = r'"(?:[^"\\]|\\.)*"'
ROW = re.compile(r'(?m)^\s*(?:\[(\d+)\]\s*=\s*)?\{\s*(' + STRING + r')\s*,\s*(' + STRING + r')\s*,\s*(' + STRING + r')\s*\}')
TABLES = {
    'ab+': ['EID.descriptions[languageCode].collectibles', 'EID.descriptions[languageCode].trinkets', 'EID.descriptions[languageCode].cards', 'EID.descriptions[languageCode].pills'],
    'rep': ['local repCollectibles', 'local repTrinkets', 'local repCards', 'local repPills'],
    'rep+': ['local collectibles', 'local trinkets', 'local cards', 'local pills'],
}


def read_table(path, key):
    text = path.read_text(encoding='utf-8')
    found = re.search(re.escape(key) + r'\s*=\s*\{\s*\n(.*?)\n\}', text, re.S)
    if not found:
        return {}
    result = {}
    for row in ROW.finditer(found[1]):
        ident, name, desc = (json.loads(value) for value in row.groups()[1:])
        # Pills' Lua array keys are offset by one; the explicit first string is the effect ID.
        ident = int(ident) if ident.isdigit() else int(row[1]) if row[1] else None
        if ident is not None:
            if ident in result:
                raise ValueError(f'Duplicate ID {ident} in {path}:{key}')
            result[ident] = {'name': name, 'description': desc}
    return result


def commit(path):
    return subprocess.check_output(['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True).strip()


def load_names(path):
    prefixes = {'C_ID': 'c', 'T_ID': 't', 'Card_ID': 'k', 'Pill_ID': 'p'}
    entries = {}
    pattern = re.compile(r'\[(C_ID|T_ID|Card_ID|Pill_ID)[ \t]*\.\.[ \t]*(\d+)\][ \t]*=[ \t]*(' + STRING + r'),?[ \t]*--[ \t]*(.*)$')
    # Parse one line at a time: an empty English comment must not consume the following entry.
    for line in path.read_text(encoding='utf-8').splitlines():
        match = pattern.search(line)
        if not match:
            continue
        name, en = json.loads(match[3]), match[4].strip()
        if not name:
            continue  # unused IDs, not missing pages
        kind, ident = prefixes[match[1]], int(match[2])
        key = f'{kind}{ident}'
        if key in entries or not en:
            raise ValueError(f'Invalid name entry: {key}')
        entries[key] = {'key': key, 'kind': kind, 'id': ident, 'name': name, 'en': en}
    return entries


def main():
    eid, isaac = map(Path, sys.argv[1:3])
    names = load_names(eid / 'descriptions/names/zh_cn.lua')
    descriptions = {kind: {} for kind in 'ctkp'}
    for folder in ['ab+', 'rep']:
        for kind, key in zip('ctkp', TABLES[folder]):
            descriptions[kind].update(read_table(eid / f'descriptions/{folder}/zh_cn.lua', key))
    rep = {kind: dict(values) for kind, values in descriptions.items()}
    for kind, key in zip('ctkp', TABLES['rep+']):
        descriptions[kind].update(read_table(eid / 'descriptions/rep+/zh_cn.lua', key))
    horse_rep = read_table(eid / 'descriptions/rep/zh_cn.lua', 'EID.descriptions[languageCode].horsepills')
    horse_plus = dict(horse_rep)
    horse_plus.update(read_table(eid / 'descriptions/rep+/zh_cn.lua', 'local horsepills'))
    metadata = {}
    for entry in ET.parse(isaac / 'scripts/data/items.xml').getroot():
        if entry.tag not in ['active', 'passive', 'familiar', 'trinket']:
            continue
        kind = 't' if entry.tag == 'trinket' else 'c'
        key = f'{kind}{entry.attrib["id"]}'
        fields = {field: entry.attrib[field] for field in ['achievement', 'maxcharges', 'chargetype', 'hidden'] if field in entry.attrib}
        metadata[key] = {'type': entry.tag, **fields}
    pools = {}
    for pool in ET.parse(isaac / 'scripts/data/itempools.xml').getroot():
        for item in pool:
            key = f'c{item.attrib["Id"]}'
            if float(item.attrib.get('Weight', '1')) > 0:
                pools.setdefault(key, []).append(pool.attrib['Name'])
    entries = []
    for key, row in names.items():
        kind, ident = row['kind'], row['id']
        if ident not in descriptions[kind] or not descriptions[kind][ident]['description']:
            raise ValueError(f'Missing description: {key}')
        row['rep'] = rep[kind].get(ident, {}).get('description', '')
        row['repPlus'] = descriptions[kind][ident]['description']
        if kind == 'p' and ident in horse_plus:
            row['horseRep'] = horse_rep.get(ident, {}).get('description', '')
            row['horseRepPlus'] = horse_plus[ident]['description']
        row['metadata'] = metadata.get(key, {})
        row['poolsRepSnapshot'] = sorted(set(pools.get(key, [])))
        entries.append(row)
    entries.sort(key=lambda row: ('ctkp'.index(row['kind']), row['id']))
    result = {'eidCommit': commit(eid), 'isaacDocsCommit': commit(isaac), 'entries': entries}
    (ROOT / 'data/item-source.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Imported {len(entries)} unique kind/ID entries; no Lua executed.')


if __name__ == '__main__':
    main()
