"""Generate combat and pickup guides from reviewed records and pinned facts."""
import json
import re
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
   text+='\n## 站位与打法\n\n'+row['approach']+'\n\n## 容易受伤的地方\n\n'+row['pitfall']+'\n\n'
   if row.get('unlockAdvice'):text+='## 特殊奖励怎么取\n\n'+row['unlockAdvice']+f' 对应[成就 #{row["achievement"]}]({achievement_link(row["achievement"])})。\n\n'
   if row.get('related'):
    assert all(id in known for id in row['related'])
    names={r['id']:r['name'] for r in rows}
    text+='## 不要混淆\n\n'+' · '.join(f'[{names[id]}](/bosses/{id})' for id in row['related'])+'。不同 Boss 的击杀记录不互相替代。\n\n'
   source=BOSS_SOURCE['bosses'][row['id']]
   assert source['file']==row['sourceFile']
   text+='## 来源与相关攻略\n\n::: details 查看招式出处\n招式类型参考 IsaacDocs：'
   text+='、'.join(f'[{block["label"]}](https://github.com/wofsauge/IsaacDocs/blob/{BOSS_SOURCE["isaacDocsCommit"]}/docs/entities/bosses/{source["file"]}#L{block["startLine"]}-L{block["endLine"]})' for block in source['blocks'])
   text+='。打法由本站整理；精英招式可能不同，见[核实记录](/about-verification)。\n:::\n\n[常见敌人与地形](/strategy/enemies) · [楼层图鉴](/floors/) · [终局 Boss](/strategy/bosses) · [Boss 总览](/bosses/)。\n'
  else:
   text+='## 怎么用\n\n'+row['approach']+'\n\n'+''.join(f'- {step}\n' for step in row['steps'])+'\n## 要注意什么\n\n'+row['pitfall']+'\n\n'
   if row['achievement']:
    ident=row['achievement'];text+=f'## 解锁条件\n\n先完成[成就 #{ident}]({achievement_link(ident)})，之后才可能出现。\n\n'
   if row.get('pool'):
    pool=[r for r in ITEMS if row['pool'] in r['poolsRepSnapshot']]
    assert pool
    text+=f'## 可能开出的道具\n\n忏悔版资料中，这类箱子的道具池收录 {len(pool)} 件，以下举出 {min(12,len(pool))} 件。开箱也可能只给拾取物；忏悔+ 的池表可能有调整。\n\n'
    text+='、'.join(f'[{r["name"]}](/items/{r["key"]})' for r in pool[:12])+'。\n\n'
   if row.get('entity'):
    entity=row['entity'];tables=ENUM_SOURCE['enums']
    assert entity['variant'] in tables['PickupVariant'].values()
    assert tables[entity['source']][entity['enum']]==entity['subtype']
    text+=f'::: details 用控制台生成它\n\n```text\nspawn 5.{entity["variant"]}.{entity["subtype"]}\n```\n\n这条命令会把它放在地上，不会解锁对应成就。'
    if row['id']=='troll-bomb':text+=' 即爆炸弹会爆炸，先准备安全距离。'
    text+=f' [打开命令生成器](/tools/console-generator?pickup={row["id"]}) · [开启控制台](/topics/debug-console)。\n\n编号：[PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/{ENUM_SOURCE["isaacDocsCommit"]}/docs/enums/PickupVariant.md) / [{entity["source"]}](https://github.com/wofsauge/IsaacDocs/blob/{ENUM_SOURCE["isaacDocsCommit"]}/docs/enums/{entity["source"]}.md)。\n:::\n\n'
   text+='## 相关攻略与来源\n\n[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。\n\n::: details 查看出处\n解锁条件见对应成就页，使用规则见资源指南。箱子池表：[IsaacDocs 忏悔版 XML](https://github.com/wofsauge/IsaacDocs/tree/'+ITEM_SOURCE['isaacDocsCommit']+'/scripts/data)。版本与待核实规则见[资料记录](/about-verification)。\n:::\n'
  out=DOCS/family/f'{row["id"]}.md';out.parent.mkdir(exist_ok=True);out.write_text(re.sub(r"\n{3,}", "\n\n", text))
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

按名称、英文或关键词搜索，点卡片看打法和注意事项。当前收录 {len(rows)} 项。

<EntryCatalog :entries="entries" label="{heading}" />

'''
 index+=('[终局 Boss](/strategy/bosses) · [常见敌人与地形](/strategy/enemies) · [楼层解锁检查](/strategy/floor-unlocks)。\n' if family=='bosses' else '[机器与乞丐](/strategy/machines) · [生命与资源教程](/guide/first-win/pickups)。\n')
 (DOCS/family/'index.md').write_text(index)
print('Generated',len(json.loads((DATA/'bosses.json').read_text())),'Boss guides and',len(json.loads((DATA/'pickups.json').read_text())),'pickup guides')
