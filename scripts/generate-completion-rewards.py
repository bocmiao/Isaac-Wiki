"""Join reviewed achievement conditions to character completion marks.

No completion states are inferred from achievement flags. Combined tainted
rewards keep their full mark requirements; version-specific rewards use the
Repentance/Repentance+ branch explicitly.
"""
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'docs/.vitepress/theme/data'
GEN = runpy.run_path(str(ROOT / 'scripts/generate-entry-pages.py'))
MODE = runpy.run_path(str(ROOT / 'scripts/generate-mode-rewards.py'))
SOURCE = json.loads((ROOT / 'data/achievement-source.json').read_text())
BY_ID = {row['id']: row for row in SOURCE}
CONDITIONS = {}
for row in SOURCE:
    CONDITIONS.setdefault(row['condition'], []).append(row)

MARKS = ['heart', 'isaac', 'satan', 'bluebaby', 'lamb', 'megasatan',
         'bossrush', 'hush', 'greed', 'delirium', 'mother', 'beast']
NORMAL = [
    ('heart', '困难心脏 / 它活着', "Defeat Mom's Heart or It Lives! on Hard mode", ['heart'], 2),
    ('isaac', '以撒', 'Defeat Isaac', ['isaac'], 1),
    ('satan', '撒但', 'Defeat Satan', ['satan'], 1),
    ('bluebaby', '???（Boss）', 'Defeat ???', ['bluebaby'], 1),
    ('lamb', '羔羊', 'Defeat The Lamb', ['lamb'], 1),
    ('megasatan', '超级撒但', 'Defeat Mega Satan', ['megasatan'], 1),
    ('bossrush', 'Boss Rush', 'Complete the Boss Rush', ['bossrush'], 1),
    ('hush', '死寂', 'Defeat Hush', ['hush'], 1),
    ('greed', '普通贪婪', 'Defeat Ultra Greed', ['greed'], 1),
    ('greedier', '极贪', 'Defeat Ultra Greedier', ['greed'], 2),
    ('delirium', '精神错乱', 'Defeat Delirium', ['delirium'], 1),
    ('mother', '母亲', 'Defeat Mother', ['mother'], 1),
    ('beast', '祸兽', 'Defeat The Beast', ['beast'], 1),
    ('all-hard', '全部十二格困难 / 极贪', 'Earn all Hard mode Completion Marks', MARKS, 2),
]
TAINTED = [
    ('main-four', '以撒＋???＋撒但＋羔羊', 'Defeat Isaac , ??? , Satan , and The Lamb', ['isaac','bluebaby','satan','lamb'], 1),
    ('timed-pair', 'Boss Rush＋死寂', 'Defeat Hush and Boss Rush', ['bossrush','hush'], 1),
    *[row for row in NORMAL if row[0] in ['megasatan','greedier','delirium','mother','beast']],
]
NOTES = {
    29: '开放六面骰，同时让表以撒开局携带它；这是用 ??? 打以撒，不是用以撒本人。',
    77: '也可用任意角色击败超级傲慢开放；左手已解锁时，犹大的 ??? 标记仍可能未完成。',
    156: '忏悔 / 忏悔+ 要十二格全困难 / 极贪；旧版六格、九格、十格条件不适用。',
    172: '胎衣+、忏悔 / 忏悔+ 对应拉撒路；旧重生 / 胎衣对应阿撒泻勒。',
    173: '胎衣+、忏悔 / 忏悔+ 对应阿撒泻勒；不要沿用旧版的拉撒路条件。',
    191: '强化店主的开局硬币；忏悔 / 忏悔+ 还开放第三个硬币心。',
    199: '开放角色莉莉丝；这项奖励不是一件收集页道具。',
    236: '让店主开局带木制镍币；不代表解锁木制镍币这个道具本身。',
    237: '让店主开局带商店钥匙。',
    542: '反向月亮与反向太阳两张牌共用这一个成就。',
}
LINK_EXCEPTIONS = {
    191: [{'name':'店主开局硬币 / 第三个硬币心', 'link':'/characters/keeper'}],
    236: [{'name':'店主开局木制镍币', 'link':'/items/c349'}],
    237: [{'name':'店主开局商店钥匙', 'link':'/items/t83'}],
}

def items_by_achievement():
    result = {}
    for item in GEN['ITEMS'].values():
        if item['metadata'].get('hidden') == 'true':
            continue
        for achievement in GEN['unlocks'](item):
            result.setdefault(achievement['id'], []).append({
                'name': GEN['SPECIAL_NAMES'].get(item['key'],item['name']),
                'link': '/items/' + item['key'],
            })
    result[199] = [{'name':'角色莉莉丝', 'link':'/characters/lilith'}]
    for pickup in json.loads((ROOT / 'data/pickup-guides.json').read_text()):
        ident = pickup['achievement']
        if ident and ident not in result:
            result[ident] = [{'name':pickup['name'], 'link':'/pickups/' + pickup['id']}]
    result.update(LINK_EXCEPTIONS)
    return result

def collect_rewards():
    item_links = items_by_achievement()
    result = []
    for tainted, file in [(False,'characters'),(True,'tainted')]:
        profiles = GEN['sections']((ROOT / f'data/entry-guides/{file}.md').read_text())
        if len(profiles) != 17:
            raise ValueError(f'Expected 17 profiles in {file}')
        for index, profile in enumerate(profiles):
            english = MODE['NAMES'][index]
            if tainted:
                english = 'Tainted ' + english.removeprefix('The ').replace('Jacob and Esau','Jacob')
            slug = ('tainted-' if tainted else '') + profile['id']
            row = {'id':slug, 'name':GEN['split_title'](profile['title'])[0],
                   'en':english, 'group':'里角色' if tainted else '表角色', 'rewards':[]}
            for kind, label, task, marks, minimum in TAINTED if tainted else NORMAL:
                condition = f'{task} as {english}'
                if profile['id']=='jacob' and kind=='bossrush':
                    condition = condition.replace('Complete the Boss Rush','Complete Boss Rush')
                # These pinned records contain two historical branches; select
                # the current branch, never the first name in the source text.
                override = None
                if not tainted and kind=='heart' and profile['id'] in ['azazel','lazarus']:
                    override = 173 if profile['id']=='azazel' else 172
                if not tainted and kind=='all-hard' and profile['id']=='lost':
                    override = 156
                if not tainted and kind=='bluebaby' and profile['id']=='judas':
                    override = 77
                matches = [BY_ID[override]] if override else CONDITIONS.get(condition,[])
                if len(matches) != 1:
                    raise ValueError(f'Expected one condition for {slug}/{kind}: {condition}; got {len(matches)}')
                achievement = matches[0]
                ident = achievement['id']
                items = item_links.get(ident,[])
                mechanism = ident in [240,593] or (tainted and kind=='megasatan')
                if not items and not achievement['name'].endswith('Baby') and not mechanism:
                    raise ValueError(f'Unreviewed non-item reward #{ident}: {achievement["name"]}')
                translated = GEN['ACHIEVEMENTS'][ident]
                row['rewards'].append({'id':ident, 'name':achievement['name'], 'kind':kind,
                    'label':label, 'marks':marks, 'minimum':minimum,
                    'condition':achievement['condition'], 'conditionZh':translated['conditionZh'],
                    'achievementLink':MODE['achievement_link'](ident), 'items':items,
                    'notes':NOTES.get(ident,'奖励为掉落物、箱子或机器，不计入普通道具收藏。' if mechanism else '奖励为本地合作宝宝，不计入道具收藏。' if not items else '')})
            result.append(row)
    if len(result)!=34 or sum(len(r['rewards']) for r in result)!=357:
        raise ValueError('Expected 34 characters and 357 character-specific rewards')
    if len({a['id'] for r in result for a in r['rewards']}) != 357:
        raise ValueError('A reward was assigned to multiple characters')
    return result

if __name__=='__main__':
    rows=collect_rewards()
    (DATA/'completion-rewards.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print('Generated 357 character-specific reward conditions: 17 × 14 normal + 17 × 7 tainted.')
