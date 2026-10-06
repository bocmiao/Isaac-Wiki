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

看两件或多件道具配在一起会发生什么，再看使用提醒。已有这些道具时，可用[组合查询工具](/tools/synergies)找还缺的那件。

'''
for row in combos:
 text+=f'## {row["title"]} {{#{row["id"]}}}\n\n'
 text+=' + '.join(f'[{items[id]["name"]}](/items/c{id})' for id in row['items'])+'\n\n'
 text+=row['individual']+'\n\n'+row['effect']+'\n\n'
 text+=f'**要注意**：{row["limits"]}\n\n**版本**：{row["version"]}。\n\n'
text+='''## 资料来源

效果参考 EID 及[道具取舍](/strategy/items#常见组合)的资料；具体版本差异见每件道具页。嗝屁猫变身条件见 EID 说明。出处与仍待核实的规则见[资料记录](/about-verification)。
'''
(ROOT/'docs/strategy/synergies.md').write_text(text)
print('Generated',len(combos),'combination guides with canonical item links')
