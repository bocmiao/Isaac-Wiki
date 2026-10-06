"""Map all 34 characters' Greed rewards from pinned achievement conditions.

Use exact boss/character conditions; reversed cards and the shared Sun/Moon
achievement are resolved by the existing item generator's reviewed ID mapping.
"""
import json
import re
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/.vitepress/theme/data'
SOURCE = json.loads((ROOT / 'data/achievement-source.json').read_text())
PROFILES = json.loads((DATA / 'catalog/characters.json').read_text())
GEN = runpy.run_path(str(ROOT / 'scripts/generate-entry-pages.py'))
NAMES = ['Isaac', 'Magdalene', 'Cain', 'Judas', '???', 'Eve', 'Samson', 'Azazel',
         'Lazarus', 'Eden', 'The Lost', 'Lilith', 'Keeper', 'Apollyon',
         'The Forgotten', 'Bethany', 'Jacob and Esau']

def achievement_link(ident):
    start = ((ident - 1) // 100) * 100 + 1
    return f'/achievements/ids-{start:03}-{min(start + 99, 641)}#achievement-{ident}'

def collect_rewards():
    conditions = {}
    for achievement in SOURCE:
        match = re.fullmatch(r'Defeat (Ultra Greed(?:ier)?) as (.+)', achievement['condition'])
        if match:
            key = (match[1], match[2])
            if key in conditions:
                raise ValueError(f'Duplicate reward condition: {key}')
            conditions[key] = achievement
    by_achievement = {}
    for item in GEN['ITEMS'].values():
        if item['metadata'].get('hidden') == 'true':
            continue
        for achievement in GEN['unlocks'](item):
            by_achievement.setdefault(achievement['id'], []).append({
                'name': GEN['SPECIAL_NAMES'].get(item['key'], item['name']),
                'en': item['en'], 'link': '/items/' + item['key'],
            })
    by_achievement[199] = [{'name': '角色莉莉丝', 'en': 'Lilith', 'link': '/characters/lilith'}]
    rows = []
    for index, profile in enumerate(PROFILES):
        tainted = index >= 17
        english = NAMES[index % 17]
        if tainted:
            english = 'Tainted ' + english.removeprefix('The ').replace('Jacob and Esau', 'Jacob')
        row = {'id': profile['id'], 'name': profile['name'], 'characterLink': profile['link'],
               'group': profile['group'], 'en': english, 'greed': None, 'greedier': None}
        for boss, mode in [('Ultra Greed', 'greed'), ('Ultra Greedier', 'greedier')]:
            achievement = conditions.get((boss, english))
            if achievement is None:
                if tainted and mode == 'greed':
                    continue
                raise ValueError(f'Missing {mode} reward for {english}')
            items = by_achievement.get(achievement['id'])
            if not items:
                raise ValueError(f'Missing item/character link for reward #{achievement["id"]}')
            row[mode] = {'id': achievement['id'], 'en': achievement['name'],
                         'achievementLink': achievement_link(achievement['id']), 'items': items}
        rows.append(row)
    assert len(rows) == 34
    assert sum(row['greed'] is not None for row in rows) == 17
    assert sum(row['greedier'] is not None for row in rows) == 34
    return rows

def reward_cell(reward):
    if reward is None:
        return '无专属奖励'
    names = '、'.join(f"[{item['name']}]({item['link']})" for item in reward['items'])
    return f"{names}<br>[成就 #{reward['id']}]({reward['achievementLink']})"

def render(rows):
    introduction = '''---
title: 全角色贪婪与极贪奖励对照
description: 34 个表角色与里角色的贪婪、极贪完成奖励、解锁教程及捐款进度区别。
---
# 全角色贪婪与极贪奖励对照

<VersionBadge checked="2026-10" />

按角色找奖励，点道具名查看效果与获取方式，点成就编号查看详细条件。以下以忏悔+ 为准，区分普通贪婪的究极贪婪与极贪的金色二阶段。

## 先分清三种进度

| 进度 | 要做什么 | 不能替代它的事 |
| --- | --- | --- |
| 普通贪婪完成 | 用指定角色打通 Greed | 用别的角色捐足硬币 |
| 极贪完成 | 先累计捐 500 枚，再用指定角色打通 Greedier 两阶段 | 只打普通贪婪或只打完极贪第一阶段 |
| 贪婪捐款里程碑 | 通关后向贪婪捐款机实际投币，累计达到对应数量 | 仅击败 Boss，或向商店的普通捐款机投币 |

极贪会同时满足同角色的普通贪婪完成，给红边贪婪标记。里角色没有单独的“普通贪婪通关专属奖励”，但可以记录普通标记、参加捐款；其表角色的奖励不会因为使用里角色而自动获得。

## 表角色 {#normal}

| 角色 | 贪婪奖励 | 极贪奖励 |
| --- | --- | --- |
'''
    lines = [introduction.rstrip()]
    for row in rows[:17]:
        lines.append(f"| <span id=\"reward-{row['id']}\"></span>[{row['name']}]({row['characterLink']}) | {reward_cell(row['greed'])} | {reward_cell(row['greedier'])} |")
    lines.extend(['', '## 里角色 {#tainted}', '', '| 角色 | 普通贪婪 | 极贪奖励 |', '| --- | --- | --- |'])
    for row in rows[17:]:
        lines.append(f"| <span id=\"reward-{row['id']}\"></span>[{row['name']}]({row['characterLink']}) | {reward_cell(row['greed'])} | {reward_cell(row['greedier'])} |")
    lines.append('''
## 反向塔罗牌与合并奖励

里角色极贪奖励中的塔罗牌是**反向牌**，不是同名正向牌。里雅各的 [#542](/achievements/ids-501-600#achievement-542)同时开放反向太阳与反向月亮，两张牌是两件物品，但共用一个成就条件；不要只补其中一张或把它们当成两个通关目标。

## 解锁后怎么拿到

通关解锁后，道具、饰品和卡牌只是加入可用范围，需要之后实际捡到，才会记入对应收藏记录。点击物品查看可出现的来源；反向牌、饰品与收集页道具的记录方式不同。[读取本地存档对照](/tools/local-progress)。

## 推荐推进方式

还没开极贪时，用已熟悉且尚未捐过很多钱的角色轮换通关，保留终点资金推进 500 枚里程碑。极贪开放后，有把握可以直接打极贪，一局补同角色普通与极贪奖励；没有把握时先拿普通奖励，再练金色二阶段。

冲全困难标记时，贪婪那格必须红边；普通贪婪标记不够。做完 Boss 后另外检查捐款进度，机器卡住不影响已经取得的通关奖励。[捐款表与概率](/strategy/greed#贪婪捐款机) · [捐款进度工具](/tools/donations)。

## 相关攻略与来源

[贪婪玩法](/modes/greed) · [极贪玩法](/modes/greedier) · [详细机制表](/strategy/greed) · [全部模式](/modes/) · [全成就查询](/achievements/)。

奖励关系逐条来自[成就条件](/achievements/)的指定角色 / Boss 记录，原始数据为 [Achievements](https://bindingofisaacrebirth.wiki.gg/wiki/Achievements) revision 269014，2026-10-05 快照。物品链接使用本站已校对的道具与反向牌 ID 映射。条件翻译与改编按 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)发布。
'''.rstrip())
    return '\n'.join(lines) + '\n'

if __name__ == '__main__':
    rows = collect_rewards()
    (DATA / 'mode-rewards.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'docs/modes/greed-rewards.md').write_text(render(rows))
    print('Generated 34 character rows: 17 Greed + 34 Greedier rewards.')
