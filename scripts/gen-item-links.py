"""从 EID 中文名称表生成道具外链数据：docs/.vitepress/theme/data/item-reference-links.json

用法：python3 scripts/gen-item-links.py <EID 仓库路径>
EID 仓库：https://github.com/wofsauge/External-Item-Descriptions（MIT）
每条记录：英文名（小写，作键）→ [中文名, 类型, 游戏内 ID, 英文原名]。类型 c=道具 t=饰品 k=卡牌/符文 p=胶囊，
与 IsaacGuru 的地址前缀一致（https://isaacguru.com/wiki/isaac/c1 = 悲伤洋葱）。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KINDS = {'collectibles': 'c', 'trinkets': 't', 'cards': 'k', 'pills': 'p'}
out, kind = {}, None
for line in open(f'{sys.argv[1]}/descriptions/names/zh_cn.lua', encoding='utf-8'):
    k = re.search(r'local (collectibles|trinkets|cards|pills)', line)
    if k:
        kind = KINDS[k.group(1)]
    r = re.search(r'\[\w+ \.\. (\d+)\]\s*=\s*"([^"]+)",\s*--\s*(.+?)\s*$', line)
    if r and kind:
        out.setdefault(r.group(3).lower().replace('’', "'"), [r.group(2), kind, int(r.group(1)), r.group(3)])
path = ROOT / 'docs/.vitepress/theme/data/item-reference-links.json'
path.write_text(json.dumps(out, ensure_ascii=False, separators=(',', ':')) + '\n', encoding='utf-8')
print(f'{len(out)} 条 → {path.relative_to(ROOT)}')
