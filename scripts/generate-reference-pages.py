"""Generate practical combat and pickup catalogs from reviewed authoring records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';DATA=DOCS/'.vitepress/theme/data/catalog'
for family,file,heading,icon in [('bosses','boss-guides','前中期 Boss 图鉴','skull'),('pickups','pickup-guides','拾取物与宝箱','chest')]:
 rows=json.loads((ROOT/f'data/{file}.json').read_text());entries=[]
 for row in rows:
  entry=dict(id=row['id'],name=row['name'],en=row['en'],group=row['group'],summary=row['summary'],icon=icon,link=f'/{family}/{row["id"]}',aliases=[])
  entries.append(entry)
  text='---\ntitle: '+json.dumps(row['name'],ensure_ascii=False)+'\n---\n# '+row['name']+'\n\n<VersionBadge checked="2026-10" />\n\n'+row['summary']+'\n\n'
  if family=='bosses':
   text+='## 招式与观察\n\n'+row['summary']+'\n\n## 安全站位与打法\n\n'+row['approach']+'\n\n## 最容易受伤的地方\n\n'+row['pitfall']+'\n\n精英与变体可能改变速度、弹幕或召唤；进入战斗先看实际外观和攻击，不能只靠名称套用一个节奏。\n\n'
   text+='## 来源与相关攻略\n\n打法是本站走位建议，不提供未核实的血量、伤害或触发帧。招式参照 [IsaacDocs 的 Boss 状态资料](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/entities/bosses)；章节分组用于查询，不承诺只在一个楼层出现。\n\n[常见敌人与地形](/strategy/enemies) · [楼层图鉴](/floors/) · [终局 Boss](/strategy/bosses) · [Boss 总览](/bosses/)。\n'
  else:
   text+='## 获取与使用\n\n'+row['approach']+'\n\n'
   if row['achievement']:
    ident=row['achievement'];page=f'ids-{((ident-1)//100)*100+1:03d}-{min(((ident-1)//100+1)*100,641)}'
    text+=f'## 永久解锁\n\n先满足[成就 #{ident}](/achievements/{page}#achievement-{ident})；解锁后才可能在对应来源生成，不保证这一局掉落。\n\n'
   text+='## 相关机制与来源\n\n[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。\n\n类别核对 [IsaacDocs 的 PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md)。解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南；不补未核实的掉率、伤害量或完整奖池。\n'
  out=DOCS/family/f'{row["id"]}.md';out.parent.mkdir(exist_ok=True);out.write_text(text)
 (DATA/f'{family}.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2)+'\n')
 index=f'''---
title: {heading}
aside: false
---
<script setup lang="ts">
import entries from '../.vitepress/theme/data/catalog/{family}.json'
</script>
# {heading}

<VersionBadge checked="2026-10" />

按名称、英文或关键词搜索。每个条目有使用、危险与相关攻略入口。

<EntryCatalog :entries="entries" label="{heading}" />

'''
 index+=('[终局 Boss](/strategy/bosses) · [常见敌人与地形](/strategy/enemies) · [楼层解锁检查](/strategy/floor-unlocks)。\n' if family=='bosses' else '[机器与乞丐](/strategy/machines) · [生命与资源教程](/guide/first-win/pickups)。\n')
 (DOCS/family/'index.md').write_text(index)
print('Generated',len(json.loads((DATA/'bosses.json').read_text())),'Boss guides and',len(json.loads((DATA/'pickups.json').read_text())),'pickup guides')
