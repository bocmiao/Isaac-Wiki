"""检查文章里「中文（English）」写法的译名是否与 EID 中文版一致。

用法：python3 scripts/check-names.py <EID 仓库路径> 文件1.md [文件2.md ...]
EID 仓库：https://github.com/wofsauge/External-Item-Descriptions
只检查 EID 收录的道具、饰品、卡牌、胶囊；其他名字（敌人、楼层等）原样列出供人工判断。
"""
import re
import sys

strict='--strict' in sys.argv
args=[x for x in sys.argv[1:] if x!='--strict']
if len(args)<2:
    raise SystemExit("Usage: check-names.py [--strict] <EID repository> <markdown file> [...] ")
eid_root, files=args[0],args[1:]
errors=0
names = {}
kind = None
for line in open(f'{eid_root}/descriptions/names/zh_cn.lua', encoding='utf-8'):
    k = re.search(r'local (collectibles|trinkets|cards|pills)', line)
    if k:
        kind = k.group(1)
    r = re.search(r'\]\s*=\s*"([^"]*)",\s*--\s*(.+?)\s*$', line)
    if r and kind:
        names.setdefault(r.group(2).lower().replace('’', "'"), r.group(1))

pair = re.compile(r'([一-鿿「」·0-9A-Za-z\-？?！!.…]{1,16})[（(]([A-Za-z0-9][A-Za-z0-9 .,\'’!?&+\-]+?)[）)]')
for f in files:
    text = open(f, encoding='utf-8').read()
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)  # 跳过待核实注释
    print(f'== {f}')
    seen = set()
    for zh, en in pair.findall(text):
        key = en.strip().lower().replace('’', "'")
        if key in seen:
            continue
        seen.add(key)
        cand = [key, 'the ' + key, key.removeprefix('the ')]
        eid = next((names[c] for c in cand if c in names), None)
        if key=='the soul' and '遗骸之魂' in zh:continue  # A character form, not the same-named collectible.
        if eid is None:
            print(f'   [未收录] {zh}（{en}）')
        elif eid.replace('-', '') not in zh.replace('-', '').replace(' ', ''):
            errors+=1
            print(f'   [不一致] {zh}（{en}） → EID：{eid}')

if strict and errors:raise SystemExit(1)
