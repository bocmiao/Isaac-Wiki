"""Generate combat and pickup guides from reviewed records and pinned facts."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];DOCS=ROOT/'docs';DATA=DOCS/'.vitepress/theme/data/catalog'
BOSS_SOURCE=json.loads((ROOT/'data/boss-state-source.json').read_text())
ENUM_SOURCE=json.loads((ROOT/'data/pickup-enum-source.json').read_text())
ITEM_SOURCE=json.loads((ROOT/'data/item-source.json').read_text())
ITEMS=ITEM_SOURCE['entries']
def achievement_link(ident):
 return f'/achievements/ids-{((ident-1)//100)*100+1:03d}-{min(((ident-1)//100+1)*100,641)}#achievement-{ident}'
def cell(value):return value.replace('|','\\|').replace('\n',' ')
for family,file,heading,icon in [('bosses','boss-guides','常见 Boss 图鉴','skull'),('pickups','pickup-guides','拾取物与宝箱','chest')]:
 rows=json.loads((ROOT/f'data/{file}.json').read_text());entries=[];known={r['id'] for r in rows}
 for row in rows:
  searchable=' '.join([row['summary'],row['approach'],row['pitfall'],*row.get('steps',[]),*[part for attack in row.get('attacks',[]) for part in attack.values()]])
  entry=dict(id=row['id'],name=row['name'],en=row['en'],group=row['group'],summary=row['summary'],icon=icon,link=f'/{family}/{row["id"]}',aliases=row.get('aliases',[]),search=searchable)
  if 'entity' in row:entry['entity']=row['entity']
  entries.append(entry)
  text='---\ntitle: '+json.dumps(row['name'],ensure_ascii=False)+'\n---\n# '+row['name']+'\n\n<VersionBadge checked="2026-10" />\n\n'+row['summary']+'\n\n'
  if family=='bosses':
   text+='## 招式、前摇与应对\n\n| 招式 | 看什么 | 怎么躲 |\n| --- | --- | --- |\n'
   for attack in row['attacks']:text+='| '+' | '.join(cell(attack[k]) for k in ['attack','tell','response'])+' |\n'
   text+='\n## 安全站位与打法\n\n'+row['approach']+'\n\n## 最容易受伤的地方\n\n'+row['pitfall']+'\n\n精英与变体可能改变速度、弹幕或召唤；进入战斗先看实际外观和攻击，不能只靠名称套用一个节奏。\n\n'
   if row.get('unlockAdvice'):text+='## 特殊奖励怎么取\n\n'+row['unlockAdvice']+f' 对应[成就 #{row["achievement"]}]({achievement_link(row["achievement"])})。\n\n'
   if row.get('related'):
    assert all(id in known for id in row['related'])
    names={r['id']:r['name'] for r in rows}
    text+='## 不要混淆\n\n'+' · '.join(f'[{names[id]}](/bosses/{id})' for id in row['related'])+'。不同 Boss 的击杀记录不互相替代。\n\n'
   source=BOSS_SOURCE['bosses'][row['id']]
   assert source['file']==row['sourceFile']
   text+='## 来源与相关攻略\n\n打法是本站走位建议，不提供未核实的血量、伤害或触发帧。招式类型对照固定 IsaacDocs 状态资料：'
   text+='、'.join(f'[{block["label"]}](https://github.com/wofsauge/IsaacDocs/blob/{BOSS_SOURCE["isaacDocsCommit"]}/docs/entities/bosses/{source["file"]}#L{block["startLine"]}-L{block["endLine"]})' for block in source['blocks'])
   text+='。状态表只证明已记录招式，不能证明当前客户端所有精英变化；章节分组也不是完整的楼层解锁必需名单。\n\n[常见敌人与地形](/strategy/enemies) · [楼层图鉴](/floors/) · [终局 Boss](/strategy/bosses) · [Boss 总览](/bosses/)。\n'
  else:
   text+='## 获取与使用\n\n'+row['approach']+'\n\n## 操作顺序\n\n'+''.join(f'{n}. {step}\n' for n,step in enumerate(row['steps'],1))+'\n## 限制与特殊角色\n\n'+row['pitfall']+'\n\n'
   if row['achievement']:
    ident=row['achievement'];text+=f'## 永久解锁\n\n先满足[成就 #{ident}]({achievement_link(ident)})；解锁后才可能在对应来源生成，不保证这一局掉落。\n\n'
   if row.get('pool'):
    pool=[r for r in ITEMS if row['pool'] in r['poolsRepSnapshot']]
    assert pool
    text+=f'## 道具来源池参考\n\n固定**忏悔** XML 快照的 `{row["pool"]}` 道具池收录 {len(pool)} 件；以下列出前 {min(12,len(pool))} 件供认道具。池内候选不等于一次开箱必出道具，也不是当前忏悔+完整奖池或掉率表。\n\n'
    text+='、'.join(f'[{r["name"]}](/items/{r["key"]})' for r in pool[:12])+'。\n\n'
   if row.get('entity'):
    entity=row['entity'];tables=ENUM_SOURCE['enums']
    assert entity['variant'] in tables['PickupVariant'].values()
    assert tables[entity['source']][entity['enum']]==entity['subtype']
    text+=f'## 控制台练习\n\n```text\nspawn 5.{entity["variant"]}.{entity["subtype"]}\n```\n\n只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。'
    if row['id']=='troll-bomb':text+=' 即爆炸弹会爆炸，先准备安全距离。'
    text+=f' [打开命令生成器](/tools/console-generator?pickup={row["id"]})，开启控制台见[控制台教程](/topics/debug-console)。\n\n编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/{ENUM_SOURCE["isaacDocsCommit"]}/docs/enums/PickupVariant.md) 与 [{entity["source"]}](https://github.com/wofsauge/IsaacDocs/blob/{ENUM_SOURCE["isaacDocsCommit"]}/docs/enums/{entity["source"]}.md)；枚举不证明开启成本与掉率。\n\n'
   text+='## 相关机制与来源\n\n[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。\n\n解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/'+ITEM_SOURCE['isaacDocsCommit']+'/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。\n'
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

按名称、英文、旧称或打法关键词搜索。当前收录 {len(rows)} 项，每个条目都有操作、危险与相关攻略入口；不宣称覆盖全部游戏内部变体。

<EntryCatalog :entries="entries" label="{heading}" />

'''
 index+=('[终局 Boss](/strategy/bosses) · [常见敌人与地形](/strategy/enemies) · [楼层解锁检查](/strategy/floor-unlocks)。\n' if family=='bosses' else '[机器与乞丐](/strategy/machines) · [生命与资源教程](/guide/first-win/pickups)。\n')
 (DOCS/family/'index.md').write_text(index)
print('Generated',len(json.loads((DATA/'bosses.json').read_text())),'Boss guides and',len(json.loads((DATA/'pickups.json').read_text())),'pickup guides')
