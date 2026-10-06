"""Render the 45 challenge guides from reviewed rules and separately authored tactics.

Rules remain owned by strategy/challenges.md + generate-tool-data.py; do not infer
Repentance+ rules from older third-party challenge XML snapshots.
"""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DATA = DOCS / '.vitepress/theme/data'
rules = json.loads((DATA / 'challenges.json').read_text())
guides = json.loads((ROOT / 'data/challenge-guides.json').read_text())
assert [r['id'] for r in rules] == [g['id'] for g in guides] == list(range(1, 46))
achievements = json.loads((ROOT / 'data/achievement-source.json').read_text())
profiles = json.loads((DATA / 'catalog/characters.json').read_text())
characters = {p['name']: p['link'] for p in profiles}
characters['里雅各'] = '/characters/tainted-jacob'
rewards = {}
for achievement in achievements:
    # #29/#30 swapped rewards after Afterbirth. Read the current-version branch
    # rather than the first challenge number in a versioned condition.
    condition = achievement['condition']
    if '[(except in Rebirth and Afterbirth)] ' in condition:
        condition = condition.split('[(except in Rebirth and Afterbirth)] ', 1)[1]
    match = re.search(r'challenge #(\d+)', condition, re.I)
    if match and condition.startswith('Complete'):
        rewards[int(match[1])] = achievement
assert set(rewards) == set(range(1, 46))

def achievement_link(a):
    start = ((a['id'] - 1) // 100) * 100 + 1
    end = min(start + 99, 641)
    return f"/achievements/ids-{start:03}-{end}#achievement-{a['id']}"

def normalize(name):
    return re.sub(r'[^a-z0-9]', '', name.lower())

routes = {
    '妈妈': '地下室 → 洞穴 → 深处 II 的妈妈。终点就在妈妈战，不需要继续打子宫。',
    '妈妈的心脏': '地下室 → 洞穴 → 深处 → 子宫 II 的妈妈的心脏 / 它活着。',
    '撒但': '打完子宫 II 的心脏 / 它活着，走向下的入口到阴间，击败撒但。',
    '以撒（Boss）': '打完子宫 II 的心脏 / 它活着，走光柱到教堂，击败以撒。',
    '???（Boss）': '妈妈时拿全家福，心脏后走教堂，再进宝箱层击败 ???。',
    '超级撒但': '妈妈时拿底片，心脏后走阴间到暗室，用开局的两块钥匙碎片开超级撒但门。',
    '母亲': '走下水道 / 污水渠 → 矿洞 / 灰坑 → 陵墓 / 炼狱 → 尸宫 II，完成路线需要的刀片流程，击败母亲。',
    '地下室 I': '开局先打超级撒但，随后沿反向楼层出口上行，最终到地下室 I。',
}
catalog = []
folder = DOCS / 'challenges'
folder.mkdir(exist_ok=True)
for rule, guide in zip(rules, guides):
    ident = rule['id']
    reward = rewards[ident]
    unlocked = next((a for a in achievements if normalize(a['name']) == normalize(rule['name'])
                     and not a['condition'].startswith('Complete')), None)
    default_open = rule['unlock'] == '默认开放'
    if not default_open and unlocked is None:
        raise ValueError(f"No verified opening achievement for challenge #{ident}: {rule['name']}")
    opening = '默认开放，可直接从 Challenges 菜单选择。' if default_open else f"{rule['unlock']}。[逐步解锁教程]({achievement_link(unlocked)})。"
    treasure = '有常规宝箱房' if '有宝箱房' in rule['rules'] else '不生成常规宝箱房'
    if ident == 39:
        treasure = '常规宝箱房不生成；下水道 II / 污水渠 II 的刀片房例外'
    group = '默认开放' if rule['unlock'] == '默认开放' else '需要解锁'
    character = f"[{rule['character']}]({characters[rule['character']]})"
    def adjacent(n):
        return json.dumps({'text': f"#{n} {rules[n - 1]['name']}", 'link': f'/challenges/{n}'}, ensure_ascii=False)
    route = routes[rule['target']]
    if ident == 44:
        route = '沿本挑战各层的 Boss 与出口推进，最终到尸宫 II 打母亲。红房间地图按挑战自身流程处理，不直接套用正常局分支的门票与开门条件。'
    content = f'''---
title: {json.dumps(f"#{ident} {rule['name']}", ensure_ascii=False)}
description: {json.dumps(guide['focus'] + '开放条件、奖励、路线与逐阶段打法。', ensure_ascii=False)}
prev: {adjacent(ident - 1) if ident > 1 else 'false'}
next: {adjacent(ident + 1) if ident < 45 else 'false'}
---
# #{ident} {rule['name']}

<EntryHeader en="Challenge #{ident}" category="编号挑战 · {group}" icon="trophy" />

<VersionBadge checked="2026-10" />

{guide['focus']}

## 开局与规则

| 项目 | 内容 |
| --- | --- |
| 指定角色 | {character} |
| 终点 | {rule['target']} |
| 宝箱房 | {treasure} |
| 商店 | {'不生成' if ident == 1 else '可生成，受本挑战的替换与价格规则影响'} |
| 难度 | {'困难' if ident == 26 else '普通（挑战自带的特殊限制另算）'} |
| 开局 / 特殊规则 | {rule['rules']} |

挑战按上表的固定开局玩。蒙眼时不能发射普通泪弹，主要靠跟班、主动或特殊攻击。[查看挑战通用规则](/strategy/challenges#挑战模式是什么)。

## 开放条件与完成奖励

**开放条件**：{opening}

**完成奖励**：{rule['reward']}。[奖励成就 #{reward['id']} 的条件]({achievement_link(reward)})。

“挑战已开放”与“挑战已完成”是两个进度。达成前置只是让它出现在菜单里；本局到达终点并碰到奖杯，才领取完成奖励。编号挑战不用于刷普通角色标记或其他普通成就。

## 前期怎么打

{guide['early']}

## 中期拿什么道具

{guide['middle']}

## 路线与终点打法

{route}

{guide['boss']}

打完后领取终点奖杯，再回菜单检查完成状态。[主线路线与前置](/guide/unlocks/endings) · [终局 Boss 打法](/strategy/bosses) · [母亲与其他终局打法](/strategy/bosses-2)。

## 最容易失败的地方

{guide['pitfall']}

## 记录进度与相关攻略

[返回 45 个挑战图鉴](/challenges/) · [挑战推荐顺序](/strategy/challenges#先做哪些) · [记录本挑战进度](/tools/challenges?q={ident}) · [读取本地存档进度](/tools/local-progress) · [全部模式](/modes/)。

角色的常规发育可参考 {character}，实际操作以本挑战的开局与限制为准。

## 资料来源

::: details 查看出处
规则见[全部挑战总表](/strategy/challenges#全部挑战总表)；开放与奖励对照[成就数据](/achievements/)。[Challenges](https://bindingofisaacrebirth.wiki.gg/wiki/Challenges) · [{rule['name']}](https://bindingofisaacrebirth.wiki.gg/wiki/{quote(rule['name'].replace(' ', '_'), safe='_')})。数字编号核对 [IsaacDocs Challenge 枚举](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/Challenge.md)。基于 wiki 条件的翻译与改编按 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)发布；打法由本站整理，推荐道具并非通关必需品。
:::
'''
    (folder / f'{ident}.md').write_text(content)
    catalog.append({'id': f'challenge-{ident}', 'gameId': ident, 'name': f'#{ident} {rule["name"]}',
                    'en': rule['description'], 'group': group, 'summary': guide['focus'],
                    'icon': 'trophy', 'link': f'/challenges/{ident}', 'aliases': [],
                    'search': ' '.join(str(v) for v in rule.values()) + ' ' + guide['focus']})
(DATA / 'catalog/challenges.json').write_text(json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
print(f'Generated {len(catalog)} challenge pages and catalog entries.')
