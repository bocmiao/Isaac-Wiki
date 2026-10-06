"""Keep combination page labels, IDs and text aligned with the tool's single source."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/'docs/.vitepress/theme/data'
items={row['gameId']:row for row in json.loads((DATA/'catalog/items.json').read_text()) if row['id'].startswith('c')}
combos=json.loads((DATA/'synergies.json').read_text())
text='''---
title: 道具组合与负面联动
---
# 道具组合与负面联动

<VersionBadge checked="2026-10" />

组合是取舍建议，不保证任何角色都同样生效。先检查攻击形态、生命机制、主动容量与版本。[组合查询工具](/tools/synergies)。

'''
for row in combos:
 text+=f'## {row["title"]} {{#{row["id"]}}}\n\n'
 text+=' + '.join(f'[{items[id]["name"]}](/items/c{id})' for id in row['items'])+'\n\n'
 text+=row['individual']+'\n\n'+row['effect']+'\n\n'
 text+=f'**版本**：{row["version"]}。\n\n**适用与风险**：{row["limits"]}\n\n'
text+='''## 来源与核对范围

单件机制使用本站固定 EID 快照，具体版本差异见各道具页；原有八组保留[道具取舍](/strategy/items#常见组合)的来源。新增条目以已知单件能力解释发育、操作与风险，不补未经核实的复合倍率。嗝屁猫组件依据 EID 的变身说明，圣经与撒但的风险依据[Boss 指南](/strategy/bosses)。
'''
(ROOT/'docs/strategy/synergies.md').write_text(text)
print('Generated',len(combos),'combination guides with canonical item links')
