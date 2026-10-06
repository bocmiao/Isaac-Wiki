"""Generate the four catalogs and standalone guides from reviewed offline snapshots.

python3 scripts/generate-entry-pages.py
Authoring inputs: data/entry-guides/*.md and data/item-source.json.
"""
import html
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DATA = DOCS / '.vitepress/theme/data/catalog'
SOURCES = ROOT / 'data/entry-guides'
ITEM_SOURCE = json.loads((ROOT / 'data/item-source.json').read_text())
ITEMS = {item['key']: item for item in ITEM_SOURCE['entries']}
ACHIEVEMENTS = {row['id']: row for row in json.loads((DOCS / '.vitepress/theme/data/achievements.json').read_text())}
RAW_ACHIEVEMENTS = json.loads((ROOT / 'data/achievement-source.json').read_text())
KIND_NAMES = {'active': '主动道具', 'passive': '被动道具', 'familiar': '跟班', 'trinket': '饰品', 'k': '卡牌 / 符文', 'p': '胶囊'}
CATALOGS = {family: [] for family in ['characters', 'rooms', 'floors', 'items']}
LEGACY = {}
GENERATED = []
MARKUP = re.compile(r'{{([^{}]+)}}')


def plain(text):
    text = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<[^>]*>|\{#[^}]+\}|[*`#]', '', text)
    return re.sub(r'\s+', ' ', html.unescape(text)).strip()


def yaml(value):
    return json.dumps(value, ensure_ascii=False)


def mdtext(value):
    return html.escape(value, quote=False).replace('|', '\\|').replace('[', '\\[').replace(']', '\\]')


def front(title, description, prev=None, next=None):
    rows = ['---', f'title: {yaml(title)}', f'description: {yaml(description)}']
    for key, entry in [('prev', prev), ('next', next)]:
        if entry:
            rows.append(f'{key}: {yaml({"text": entry["name"], "link": entry["link"]})}')
    return '\n'.join(rows + ['---', ''])


def hero(entry, code=''):
    attrs = {'en': entry['en'], 'category': entry['group'], 'icon': entry['icon'], 'code': code}
    return '<EntryHeader ' + ' '.join(f'{key}="{html.escape(value, quote=True)}"' for key, value in attrs.items() if value) + ' />\n'


def write(path, content):
    path = DOCS / path
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + '\n', encoding='utf-8')
    GENERATED.append(str(path.relative_to(DOCS)))


def remember(family, entry, old_path=None):
    CATALOGS[family].append(entry)
    if old_path:
        for anchor in entry['aliases']:
            LEGACY[f'{old_path}#{anchor}'] = entry['link'] + ('#' + anchor if anchor in entry.get('detailAnchors', []) else '')


def rewrite_links(text, source=''):
    def replace(match):
        target = match[1]
        # Relative links from the old room/floor source articles.
        if target.startswith('./floors'):
            target = target.replace('./floors', '/strategy/floors', 1)
        elif target.startswith('./rooms'):
            target = target.replace('./rooms', '/strategy/rooms', 1)
        if target.startswith('#') and source:
            target = source + target
        return '](' + LEGACY.get(target, target) + ')'
    return re.sub(r'\]\(([^\s)]+)\)', replace, text)


def sections(text):
    """H3 profiles stop at the next H2/H3; preceding compatibility spans travel with their profile."""
    starts = list(re.finditer(r'(?m)(?:<span id="[^"]+"></span>\n\n)?^### (.+?) \{#([^}]+)\}\s*\n', text))
    result = []
    for i, match in enumerate(starts):
        stop = starts[i + 1].start() if i + 1 < len(starts) else len(text)
        higher = re.search(r'(?m)^## ', text[match.end():stop])
        if higher:
            stop = match.end() + higher.start()
        prefix = re.sub(r'###[^\n]+\n', '', match[0]).strip()
        result.append({'title': match[1], 'id': match[2], 'body': text[match.end():stop].strip(), 'prefix': prefix})
    return result


def excerpt(body):
    first = next((line for line in body.splitlines() if line.strip() and not line.startswith(('<', '|', '#', ':::'))), '')
    first = re.sub(r'^\*\*[^*]+\*\*[：:]?', '', first)
    return plain(first)[:110]


def split_title(title):
    match = re.match(r'(.+?)（(.+)）$', title)
    return (match[1], match[2]) if match else (title, '')


def guide_headings(body):
    """Turn the original guide's paragraph labels into the detail-page outline."""
    return re.sub(r'(?m)^\*\*([^*\n]+)\*\*[：:]\s*',
                  lambda match: '' if match[1] == '共通规则' else '## ' + match[1] + '\n\n', body)


def make_profiles():
    for variant, file in [(False, 'characters'), (True, 'tainted')]:
        text = (SOURCES / f'{file}.md').read_text()
        profiles = sections(text)
        if len(profiles) != 17:
            raise ValueError(f'{file}: expected 17 characters, found {len(profiles)}')
        stats = {}
        for line in text.splitlines():
            if line.startswith('| ['):
                cells = [cell.strip() for cell in line.split('|')[1:-1]]
                ident = re.search(r'\(#([^)]*)\)', cells[0])
                if ident:
                    stats[ident[1]] = cells[1:]
        for profile in profiles:
            slug = ('tainted-' if variant else '') + profile['id']
            name, en = split_title(profile['title'])
            anchors = re.findall(r'\{#([^}]+)\}|<span id="([^"]+)"', profile['body'] + '\n' + profile['prefix'])
            aliases = [profile['id']] + [a or b for a, b in anchors]
            entry = {'id': slug, 'name': name, 'en': en, 'group': '里角色' if variant else '表角色', 'summary': excerpt(profile['body']), 'icon': 'face-dark' if variant else 'face', 'link': f'/characters/{slug}', 'aliases': aliases, 'detailAnchors': [profile['id']] + re.findall(r'\{#([^}]+)\}', profile['body'])}
            remember('characters', entry, f'/strategy/{file}')
            counterpart = profile['id'] if variant else 'tainted-' + profile['id']
            body = re.sub(r'(?m)^#### ', '## ', profile['body'])
            for label, heading in [('机制', '核心机制'), ('要注意', '风险与练习')]:
                body = body.replace(f'**{label}**\n', f'## {heading}\n\n')
            body = re.sub(r'(?m)^\*\*获取方式\*\*[：:]\s*', '## 获取方式\n\n', body)
            info = stats[profile['id']]
            lead = '\n## 开局速查\n\n| 血量 | 初始道具 / 能力 | 特点 | 难点 |\n| --- | --- | --- | --- |\n| ' + ' | '.join(info) + ' |\n\n'
            page = front(name, f'{name}的独立攻略：获取方式、开局、发育、清房、Boss 打法和路线。')
            page += f'# {name} {{#{profile["id"]}}}\n\n' + hero(entry) + '\n<VersionBadge checked="2026-10" />\n\n'
            page += profile['prefix'] + lead + body
            page += f'\n\n## 相关条目\n\n- [对应{"表" if variant else "里"}角色](/characters/{counterpart})\n- [全部角色](/characters/) · [开局强化与完成标记](/strategy/character-roster#upgrades)\n- [角色解锁步骤](/guide/unlocks/order) · [路线规划](/tools/routes) · [道具图鉴](/items/)\n'
            title = ('Tainted_' if variant else '') + en.replace('Tainted ', '').replace(' (Blue Baby)', '').replace(' ', '_')
            page += '\n## 参考资料\n\n- [角色资料](https://bindingofisaacrebirth.wiki.gg/wiki/' + quote(title, safe='_') + ')\n- [长子名分](https://bindingofisaacrebirth.wiki.gg/wiki/Birthright)\n- 本页的机制与分阶段打法保留自站内已校对角色攻略，适用单人忏悔 / 忏悔+。\n'
            entry['_body'] = page


ROOM_GROUPS = {
 '基础与发育': ['normal','treasure','shop','boss','miniboss'],
 '隐藏与交易': ['secret','supersecret','ultrasecret','devil','angel'],
 '资源与挑战': ['curse','challenge','boss-challenge','sacrifice','library','arcade','vault','dice'],
 '特殊奖励': ['clean-bedroom','dirty-bedroom','crawlspace','black-market','planetarium'],
 '路线与特殊区域': ['boss-rush','error','secret-exit','greed-exit','blue','red','mirror','minecart','strange-door','home-closet','genesis','grave'],
}
ROOM_ICONS = {'treasure':'crown','shop':'coin','boss':'skull','miniboss':'skull','secret':'bomb','supersecret':'bomb','ultrasecret':'key','devil':'heart','angel':'soul','curse':'heart','challenge':'trophy','boss-challenge':'skull','sacrifice':'heart','library':'card','arcade':'coin','vault':'chest','dice':'dice','clean-bedroom':'heart','dirty-bedroom':'heart','crawlspace':'rock','black-market':'coin','planetarium':'eye','boss-rush':'trophy','error':'dice','secret-exit':'key','greed-exit':'coin','blue':'key'}
FLOOR_GROUPS = {'第一章':['basement','cellar','burning-basement'],'第二章':['caves','catacombs','flooded-caves'],'第三章':['depths','necropolis','dank-depths'],'第四章':['womb','utero','scarred-womb'],'母亲路线':['downpour','dross','mines','ashpit','mausoleum','gehenna','corpse'],'终局与上行':['blue-womb','sheol','cathedral','dark-room','chest','void','ascent','home','xl'],'贪婪模式':['greed-basement','greed-caves','greed-depths','greed-womb','greed-sheol','greed-shop','ultra-greed']}


def group_for(ident, groups):
    return next(group for group, ids in groups.items() if ident in ids)


def make_rooms_floors():
    for family, groups in [('rooms', ROOM_GROUPS), ('floors', FLOOR_GROUPS)]:
        text = (SOURCES / f'{family}.md').read_text()
        for profile in sections(text):
            if profile['id'] == 'route-map':
                continue
            name, en = split_title(profile['title'])
            if family == 'floors':
                en = en.replace(' I / II', '')
            entry = {'id':profile['id'], 'name':name, 'en':en, 'group':group_for(profile['id'],groups), 'summary':excerpt(profile['body']), 'icon':ROOM_ICONS.get(profile['id'],'map' if family=='floors' else 'lock'), 'link':f'/{family}/{profile["id"]}', 'aliases':[profile['id']], 'detailAnchors':[]}
            remember(family,entry,f'/strategy/{family}')
            shared = ''
            if family == 'floors':
                previous = list(re.finditer(r'(?m)^## .+\n', text[:text.index('### '+profile['title'])]))[-1]
                context = text[previous.end():].split('### ',1)[0].strip()
                if context:
                    shared = '\n## 本章共通规则\n\n'+context+'\n'
            page = front(name,f'{name}的进入条件、奖励、风险、打法和路线出口。') + f'# {name} {{#{profile["id"]}}}\n\n' + hero(entry) + '\n<VersionBadge checked="2026-10" />\n\n'
            page += guide_headings(profile['body'] + shared)
            entry['_body'] = page
    # Special layouts have their own pages too; their walkthroughs draw on the reviewed route guides.
    extras = [
      ('red','红房间','Red Room','红钥匙等效果在正常地图之外开出的房间，是找究极隐藏房与里角色衣柜的基础。',
       '使用红钥匙、红钥匙碎片、水晶钥匙或该隐的魂石等，在符合条件的墙面拓出新房。红房的来源不决定用途，里面仍可能是普通战斗或特殊奖励。\n\n不要把红房间与究极隐藏房混用：开出相邻红房后，究极隐藏房才可能自动开门。普通炸弹不能从原地图直接炸出究极隐藏房。\n\n每次拓图前观察候选空格与充能余量，优先覆盖更多候选位置。到 Home 开衣柜是固定位置的特殊用途，不能靠随便开一间红房完成。', [('究极隐藏房','/rooms/ultrasecret'),('Home 衣柜','/rooms/home-closet'),('找房规则','/strategy/mechanics#究极隐藏房-忏悔起')]),
      ('mirror','镜面世界','Mirror World','下水道 / 污水渠 II 的特殊区域，临时游魂进入镜子后取得刀片 1。',
       '先在下水道 / 污水渠 II 找到白火和镜子，触碰白火进入临时游魂状态，再穿镜子。刀片 1 在镜面宝箱房，拿到后原路穿镜子返回。\n\n临时游魂的圣斗篷与游魂开局强化有关，不能假定未完成强化也能安全挨一下。镜面 Boss 是可选额外奖励，母亲路线不要求击败它。\n\n进门先观察危险物与敌人，刀片到手就优先安全返回；不要为多拿一个可选奖励把整条路线断掉，也不要打碎镜子后再计划返回。',[('下水道 II','/floors/downpour'),('污水渠 II','/floors/dross'),('刀片 1','/items/c626')]),
      ('minecart','矿车与逃亡区域','Mines Escape','矿洞 / 灰坑 II 的三个黄按钮与矿车区域，取刀片 2 后躲避妈妈的影子。',
       '前提是已经持有刀片 1。找到并按下三个黄色按钮，再乘矿车进入特殊区域；没拿第一块刀片就不能指望在这里补齐完整刀片。\n\n取得刀片 2 后妈妈的影子开始追击，按安全路线返回矿车。先看坑与可走通道，再躲它的冲锋；特殊段落会暂时限制能力，不能按平时飞行或主动联动估算容错。\n\n回到原楼层后确认两块刀片已经合成，再规划陵墓门的两心入门成本与后续血量。',[('矿洞 II','/floors/mines'),('灰坑 II','/floors/ashpit'),('刀片 2','/items/c627')]),
      ('strange-door','奇怪的门与便条房','A Strange Door','深处 II 以照片开门的回家路线，特殊陵墓 II 拿爸爸的便条后上行。',
       '先击败母亲解锁奇怪的门。深处 II 去妈妈前准备可靠传送，常见方法是炸本层带记号的骷髅取得愚者。\n\n击败妈妈后拿全家福或底片，传送回起点，用照片打开奇怪的门，开门消耗照片。不要提前跳普通子宫出口，也不要把传送卡用掉。\n\n门后是特殊陵墓 II，终点为爸爸的便条；拿便条开始上行。这里与母亲路线用刀片开肉门的陵墓 II 不同，计划解锁里角色时先在宝箱房或 Boss 房留下饰品。',[('深处 II','/floors/depths'),('上行','/floors/ascent'),('爸爸的便条','/items/c668')]),
      ('home-closet','Home 隐藏衣柜','Home Closet','妈妈卧室前走廊左侧墙后的隐藏房，接触对应里角色才能解锁。',
       '先走奇怪的门、爸爸的便条与上行路线到家，再在妈妈卧室前走廊左侧墙的对应位置使用红钥匙或红钥匙碎片等开门。\n\n第一次到家打开妈妈卧室箱子保证给红钥匙；以后优先提前留饰品，上行取红钥匙碎片。该隐的魂石也是可用方式，不必依赖随机拿到它。\n\n开门后进隐藏衣柜，接触里面的对应里角色并确认解锁提示。只是到家、只是开门、或者用其他表角色到家，都不能代替目标角色的解锁。先做完衣柜，再睡床触发终局战。',[('家','/floors/home'),('红钥匙','/items/c580'),('红钥匙碎片','/items/k78'),('17 个里角色获取步骤','/guide/unlocks/order#tainted-list')]),
      ('genesis','创世记卧室','Genesis Room','使用创世记后移除原道具并逐件选择替代道具的特殊卧室。',
       '使用创世记会移除原道具和掉落物，并将角色带到特殊卧室。每移除一件道具，可以从同一道具池的三个选项中选一件，逐步重建组合。\n\n先把输出、防御与可持续发育的需求列好，再比较每组选择；不能把前三个选项当成全部可选道具，也不能认为会保留原组合或主动。\n\n这里不是普通睡床回血房，退出也不是原地图的一扇普通门。使用前完成当前楼层的刀片、交易和路线事项，离场按创世记所在章节的出口规则继续。',[('创世记','/items/c622'),('干净卧室','/rooms/clean-bedroom'),('路线规划','/tools/routes')]),
      ('grave','遗骸坟墓房','Forgotten Grave','暗室的土堆布局，需要完整妈妈的铲子及前置任务来解锁遗骸。',
       '先击败过羔羊，再开始遗骸的铲子任务：首层限时击败 Boss，拿铲子碎片，带着它完成 Boss Rush 得到完整妈妈的铲子。\n\n之后去暗室找到带土堆的房间，在土堆上使用完整铲子并确认解锁。只有铲子碎片、只打完 Boss Rush 或只抵达暗室，都不算完成任务。\n\n遗骸与遗骸之魂是同一个角色的两种形态，不需要各找一间坟墓解锁；详细时间要求与路线准备按完整教程执行。',[('遗骸完整解锁','/guide/unlocks/order#hidden-forgotten'),('暗室','/floors/dark-room'),('妈妈的铲子','/items/c552'),('遗骸攻略','/characters/forgotten')]),
    ]
    for ident,name,en,summary,body,related in extras:
        entry={'id':ident,'name':name,'en':en,'group':group_for(ident,ROOM_GROUPS),'summary':summary,'icon':'key' if ident in ['red','home-closet','strange-door'] else 'map','link':f'/rooms/{ident}','aliases':[],'detailAnchors':[]}
        remember('rooms',entry)
        first, _, rest = body.partition('\n\n')
        entry['_body']=front(name,summary)+f'# {name}\n\n'+hero(entry)+'\n<VersionBadge checked="2026-10" />\n\n'+summary+'\n\n## 进入与机制\n\n'+first+'\n\n## 推进与注意事项\n\n'+rest+'\n\n## 相关条目\n\n'+'\n'.join(f'- [{label}]({target})' for label,target in related)
    # XL is a map modifier, with its own guide, not a new chapter.
    entry={'id':'xl','name':'XL 与迷宫诅咒','en':'Curse of the Labyrinth','group':'终局与上行','summary':'同章两层合并，两个宝箱房与两个 Boss；交易门和章终点看第二个 Boss。','icon':'map','link':'/floors/xl','aliases':[],'detailAnchors':[]}
    remember('floors',entry)
    entry['_body']=front(entry['name'],entry['summary'])+'# XL 与迷宫诅咒\n\n'+hero(entry)+'\n<VersionBadge checked="2026-10" />\n\n迷宫诅咒把同章 I / II 合为一张大地图，通常两个宝箱房和两个 Boss。第一章的两间宝箱房通常都免费；不能据此推导成两家免费商店。\n\n## 推进与打法\n\n两层已经合并，不要打完第一个 Boss 就当作章终点。交易门和妈妈等章终点机制看第二个 Boss，资源与路线准备也要在整张地图上做完。\n\n地图更大，迷路和回头都更耗时。先确定本局是否赶 Boss Rush / 死寂，再规划支路；母亲刀片与回家照片仍要按实际出现的路线结构处理，XL 不会自动送路线物品。\n\n## 相关条目\n\n- [诅咒规则](/strategy/mechanics#诅咒)\n- [全部楼层](/floors/) · [路线检查](/tools/routes)\n'
    floor_text=(SOURCES/'floors.md').read_text()
    greed_table=floor_text.split('## 贪婪 / 极贪的七层',1)[1].split('普通贪婪为',1)[0]
    rows=[line for line in greed_table.splitlines() if re.match(r'\| [1-7] ',line)]
    greed_ids=FLOOR_GROUPS['贪婪模式']
    if len(rows)!=7:raise ValueError('Expected seven Greed stages')
    shared=floor_text.split('普通贪婪为',1)[1].split('## 下层之前',1)[0].strip()
    for i,(ident,row) in enumerate(zip(greed_ids,rows),1):
        cells=[x.strip() for x in row.split('|')[1:-1]]
        title=cells[0][2:];name,en=split_title(title);name='贪婪 · '+name
        entry={'id':ident,'name':name,'en':en,'group':'贪婪模式','summary':plain(cells[1]),'icon':'coin','link':f'/floors/{ident}','aliases':[],'detailAnchors':[]}
        remember('floors',entry)
        rooms='前五层通常有中央竞技场、商店、银门免费宝箱房、金门上锁宝箱房、诅咒房、交易房与出口。银门通常给 Boss 池道具，金门给宝箱房池道具。' if i<=5 else '第六层没有前五层的双宝箱房，重点是战斗与最后购物。' if i==6 else '第七层依次经过起始房、小头目房与究极贪婪 Boss 房。极贪模式还有金色第二阶段。'
        body=f'# {name}（{en}）\n\n'+hero(entry)+f'\n<VersionBadge checked="2026-10" />\n\n这是贪婪 / 极贪模式的**第 {i} 层**，使用模式自己的楼层顺序，不能套用普通主线同名楼层的终点与伤害规则。\n\n## 房间与发育\n\n{rooms}\n\n{cells[1]}。\n\n## 下楼前\n\n{cells[2]}。\n\n## 前六层的波次与模式规则\n\n普通贪婪为{shared}\n\n## 相关条目\n\n- [贪婪模式完整攻略](/strategy/greed) · [捐款进度](/tools/donations)\n- [全部楼层](/floors/) · [贪婪出口房](/rooms/greed-exit)\n'
        if i<7:body+=f'- [下一层](/floors/{greed_ids[i]})\n'
        entry['_body']=front(name,entry['summary'])+body


# Icon markup is presentation, except named entities / stats / statuses. Those become explicit text or links.
STAT_LABELS={'Damage':'伤害','Tears':'射速','Speed':'移速','Range':'射程','Shotspeed':'弹速','Luck':'幸运','Tearsize':'泪弹尺寸','Heart':'红心容器','EmptyHeart':'空红心容器','HealingRed':'恢复红心','SoulHeart':'魂心','HalfSoulHeart':'半魂心','BlackHeart':'黑心','HalfBlackHeart':'半黑心','HalfHeart':'半红心','EternalHeart':'永恒之心','GoldenHeart':'金心','BoneHeart':'骨心','EmptyBoneHeart':'空骨心','RottenHeart':'腐心','BrokenHeart':'碎心','UnknownHeart':'随机心','Coin':'硬币','Bomb':'炸弹','Key':'钥匙','GoldenBomb':'金炸弹','GoldenKey':'金钥匙','Battery':'电池','Pill':'胶囊','Card':'卡牌','Rune':'符文','Trinket':'饰品','Chest':'箱子','GoldenChest':'金箱子','RedChest':'红箱子','DirtyChest':'脏箱子','GrabBag':'福袋','AngelChance':'天使房概率','DevilChance':'恶魔房概率','AngelDevilChance':'恶魔 / 天使房概率','PlanetariumChance':'星象房概率'}
ROOM_MARKS={'Room':('普通房间','normal'),'Shop':('商店','shop'),'TreasureRoom':('宝箱房','treasure'),'RedTreasureRoom':('宝箱房','treasure'),'BossRoom':('Boss 房','boss'),'MiniBoss':('小头目房','miniboss'),'SecretRoom':('隐藏房','secret'),'SuperSecretRoom':('超级隐藏房','supersecret'),'UltraSecretRoom':('究极隐藏房','ultrasecret'),'ArcadeRoom':('赌博房','arcade'),'CursedRoom':('诅咒房','curse'),'ChallengeRoom':('挑战房','challenge'),'Library':('图书馆','library'),'SacrificeRoom':('献祭房','sacrifice'),'DevilRoom':('恶魔房','devil'),'AngelRoom':('天使房','angel'),'LadderRoom':('夹层','crawlspace'),'BossRushRoom':('Boss Rush','boss-rush'),'IsaacsRoom':('干净卧室','clean-bedroom'),'BarrenRoom':('肮脏卧室','dirty-bedroom'),'ChestRoom':('宝库','vault'),'DiceRoom':('骰子房','dice'),'Planetarium':('星象房','planetarium'),'ErrorRoom':('错误房','error')}
OTHER_MARKS={'Warning':'注意：','Shrink':'缩小','Poison':'中毒','Fear':'恐惧','Petrify':'石化','Slow':'减速','Confusion':'混乱','Charm':'魅惑','Friendly':'友好','Magnetize':'磁力','Freezing':'冰冻','Burning':'燃烧','BleedingOut':'流血','Bait':'诱饵','DeathMark':'死亡标记','Chained':'锁链','BrimstoneCurse':'硫磺火诅咒','Chargeable':'蓄力','Throwable':'投掷','HolyMantle':'圣斗篷','Guppy':'嗝屁猫','Leviathan':'利维坦','Beggar':'乞丐','DemonBeggar':'恶魔乞丐','Slotmachine':'赌博机','FortuneTeller':'预言机','CraneGame':'夹娃娃机','BloodDonationMachine':'献血机','DonationMachine':'捐款机','RestockMachine':'补货机','MomsHeart':'妈妈的心脏','ButtonRT':'RT','CurseBlind':'致盲诅咒','CurseDarkness':'黑暗诅咒','CurseLost':'迷失诅咒','CurseMaze':'混乱诅咒','CurseCursed':'诅咒'}
PLAYERS={4:('???','bluebaby'),7:('阿撒泻勒','azazel'),10:('游魂','lost'),11:('复活的拉撒路','lazarus'),12:('犹大之影','judas'),14:('店主','keeper'),16:('遗骸','forgotten'),20:('以扫','jacob')}


def render_effect(raw, markdown=True):
    def replace(match):
        tag=match[1]; tail=raw[match.end():].lstrip()
        if tag in ['Blank','NoLB','CR','Timer'] or tag.startswith('Color'):
            return ''
        entity=re.fullmatch(r'(Collectible|Trinket|Card)(\d+)',tag)
        if entity:
            key={'Collectible':'c','Trinket':'t','Card':'k'}[entity[1]]+entity[2]
            if key not in ITEMS:raise ValueError('Unknown entity markup '+tag)
            name=ITEMS[key]['name']
            if tail.startswith(name):return ''
            return f'[{mdtext(name)}](/items/{key}) ' if markdown else name+' '
        player=re.fullmatch(r'Player(\d+)',tag)
        if player:
            name,slug=PLAYERS[int(player[1])]
            if tail.startswith(name):return ''
            return f'[{name}](/characters/{slug}) ' if markdown else name+' '
        quality=re.fullmatch(r'Quality([0-4])',tag)
        if quality:return '品质 '+quality[1]+' '
        if tag in ROOM_MARKS:
            name,slug=ROOM_MARKS[tag]
            if tail.startswith(name):return ''
            return f'[{name}](/rooms/{slug}) ' if markdown else name+' '
        label=STAT_LABELS.get(tag,OTHER_MARKS.get(tag))
        if label is None:raise ValueError('Unreviewed markup '+tag)
        # Icons before already written words are decorative, not an extra effect.
        if tail.startswith(label) or (tag in ['Heart','EmptyHeart','HealingRed'] and ('心' in tail[:5] or tail.startswith('回满血'))):return ''
        return label+'：'
    result=MARKUP.sub(replace,raw)
    result=result.replace('<道具不存在>','未使用的道具编号')
    if re.search(r'\{\d+\}|{{',result):raise ValueError('Unresolved effect value: '+result)
    return re.sub(r'(?<=\d)x|x(?=\d)', '×', re.sub(r'[ \t]{2,}', ' ', result))


def effect_bullets(raw):
    return '\n'.join(dict.fromkeys('- '+render_effect(part).strip() for part in raw.split('#') if part.strip()))


def norm(value):
    # A question mark distinguishes reversed tarot cards from ordinary cards.
    return re.sub(r'[^a-z0-9?]', '',unicodedata.normalize('NFKD',unquote(value).lower()))


def unlocks(item):
    direct=item['metadata'].get('achievement')
    if direct:
        ident=int(direct)
        if ident not in ACHIEVEMENTS:raise ValueError('Unknown achievement '+str(ident))
        return [ACHIEVEMENTS[ident]]
    if item['kind'] not in ['k','p']:return []
    # Each of these challenge rewards unlocks TWO pills; the source record
    # anchors only the first one. A literal ??? pill must never match the
    # source's generic "???" reward-message placeholders for tainted rewards.
    paired_pills={'p28':227,'p29':227,'p30':228,'p31':228}
    if item['key'] in paired_pills:return [ACHIEVEMENTS[paired_pills[item['key']]]]
    if item['key']=='k75':return [ACHIEVEMENTS[542]]  # reversed Sun and Moon share one unlock
    if item['key']=='p9999':return [ACHIEVEMENTS[603]]
    title=norm(item['en'])
    result=[]
    for row in RAW_ACHIEVEMENTS:
        source=urlsplit(row['source']); source_title=unquote(source.fragment or source.path.rsplit('/',1)[-1]).replace('_',' ')
        source_title=re.sub(r' \(Card\)$','',source_title)
        candidates=[norm(row['name']),norm(source_title)]
        # Some records name the entity only in the reward message (e.g. the
        # reversed Magician). Keep real names, exclude bare ??? placeholders.
        reward_name=norm(row['reward'])
        if re.search(r'[a-z0-9]',reward_name):candidates.append(reward_name)
        if item['kind']=='k':candidates.append(norm(re.sub(r'^Rune of ','',row['name'])))
        if title not in candidates:continue
        group=ACHIEVEMENTS[row['id']]['group']
        if group in ['角色获取','挑战开放','开局强化']:continue
        result.append(ACHIEVEMENTS[row['id']])
    return result


POOLS={'treasure':'宝箱房','shop':'商店','boss':'Boss 房','devil':'恶魔房','angel':'天使房','secret':'隐藏房','library':'图书馆','shellGame':'壳游戏','goldenChest':'金箱子','redChest':'红箱子','beggar':'普通乞丐','demonBeggar':'恶魔乞丐','curse':'诅咒房','keyMaster':'钥匙大师','batteryBum':'电池乞丐','momsChest':'妈妈的箱子','greedTreasure':'贪婪宝箱房','greedBoss':'贪婪银门 / Boss 池','greedShop':'贪婪商店','greedCurse':'贪婪诅咒房','greedDevil':'贪婪恶魔房','greedAngel':'贪婪天使房','greedSecret':'贪婪隐藏房','craneGame':'夹娃娃机','ultraSecret':'究极隐藏房','bombBum':'炸弹乞丐','planetarium':'星象房','oldChest':'旧箱子','babyShop':'里店主商店','woodenChest':'木箱子','rottenBeggar':'腐烂乞丐'}
SPECIAL_NAMES={'c59':'彼列之书（被动形态）','c551':'铲子碎片（第二块）','c656':'达摩克里斯之剑（悬剑形态）'}
SPECIAL_ACQUISITION={
 'c59':'犹大 / 犹大之影取得长子名分后，彼列之书转为可搭配其他主动的被动形态。它不是另一件正常宝箱房主动道具，参见[犹大机制](/characters/judas)。',
 'c238':'炸天使房的天使雕像并击败相应天使取得，用于与另一块钥匙碎片合成超级撒但门的钥匙。参见[天使房](/rooms/angel)。',
 'c239':'炸天使房的天使雕像并击败相应天使取得，用于与另一块钥匙碎片合成超级撒但门的钥匙。参见[天使房](/rooms/angel)。',
 'c550':'遗骸铲子任务的第一部分，先满足首层限时 Boss 与炸出生房等前置。具体按[遗骸完整解锁](/guide/unlocks/order#hidden-forgotten)执行。',
 'c551':'带第一块铲子碎片完成 Boss Rush，取得第二块并合成妈妈的铲子。参见[遗骸完整解锁](/guide/unlocks/order#hidden-forgotten)。',
 'c552':'铲子任务中两部分合成后的完整铲子，暗室土堆解锁遗骸需要它。永久解锁与本局任务获取是不同事项，参见[坟墓房](/rooms/grave)。',
 'c626':'下水道 / 污水渠 II 触碰白火后穿镜子，在镜面宝箱房取得。参见[镜面世界](/rooms/mirror)。',
 'c627':'先持有刀片 1，在矿洞 / 灰坑 II 按三个黄按钮、乘矿车取得，再躲妈妈的影子返回。参见[矿车逃亡](/rooms/minecart)。',
 'c656':'使用主动版[达摩克里斯之剑](/items/c577)后形成的悬剑状态，不是额外掉落的常规跟班。',
 'c668':'已解锁奇怪的门后，深处 II 用照片开门进入特殊陵墓 II，在终点取得并开始上行。参见[奇怪的门](/rooms/strange-door)。',
 'k78':'拿爸爸的便条前，在宝箱房 / Boss 房留下饰品，上行时回收转换出的碎片。参见[上行](/floors/ascent)与[Home 衣柜](/rooms/home-closet)。',
}


def corrected_effect(item, field):
    if item['key']=='c59':
        return '彼列之书转为被动形态，可搭配另一件主动道具#使用搭配的主动时获得伤害加成，加成随该主动的充能量变化#部分主动搭配有特殊效果'
    raw=item[field]
    if item['key']=='c120' and field=='repPlus':
        # EID rep+/item_data.lua updates Tears to FireRate: a flat increase that can exceed the normal cap.
        raw=raw.replace('射速+1.7','射速修正+1.7（可突破常规射速上限）')
    return raw


def make_items():
    synergies=json.loads((DOCS/'.vitepress/theme/data/synergies.json').read_text())
    for item in ITEMS.values():
        key=item['key']; kind=item['kind']; typ=item['metadata'].get('type',kind); group=KIND_NAMES[typ]
        current=corrected_effect(item,'repPlus'); base=corrected_effect(item,'rep')
        parts=[part for part in current.split('#') if part.strip()]
        core=next((part for part in parts if not re.match(r'^[↑↓]',part.strip())),parts[0])
        summary=plain(render_effect(core,False))[:110]
        entry={'id':key,'name':SPECIAL_NAMES.get(key,item['name']),'en':item['en'],'group':group,'summary':summary,'icon':{'active':'battery','passive':'crown','familiar':'face','trinket':'key','k':'card','p':'pill'}.get(typ,'crown'),'link':f'/items/{key}','aliases':[],'detailAnchors':[],'gameId':item['id'],'search':item['name']+' '+plain(render_effect(current,False)).replace('#',' ')}
        # GameIcon has no battery icon; the existing key/coin/card vocabulary is reused.
        if entry['icon']=='battery':entry['icon']='dice'
        remember('items',entry)
        page=front(entry['name'],summary)+f'# {mdtext(entry["name"])}\n\n'+hero(entry,key)+'\n<VersionBadge checked="2026-10" />\n\n'
        info=[('类型',group)]
        if key=='p9999':
            info.append(('形态','金胶囊：随机效果的特殊胶囊颜色'))
            entry.pop('gameId',None)
        else:
            info.append(('胶囊效果 ID' if kind=='p' else '游戏内 ID',str(item['id'])))
        if typ=='active':
            charge=item['metadata'].get('maxcharges'); charge_type=item['metadata'].get('chargetype','0')
            value='计时恢复' if charge_type=='1' else '特殊充能' if charge_type=='2' else f'{charge} 格常规充能' if charge and charge!='0' else '无需常规清房充能'
            info.append(('基础充能方式',value))
        if item['metadata'].get('hidden')=='true' or key in SPECIAL_NAMES:
            info.append(('形态','剧情 / 特殊形态，获取方式见下文'))
        page+='## 基本信息\n\n| 项目 | 内容 |\n| --- | --- |\n'+'\n'.join(f'| {k} | {v} |' for k,v in info)+'\n\n'
        page+='## 效果与数值\n\n'+effect_bullets(current)+'\n\n'
        if base and base!=current:
            page+='::: details 忏悔版的效果差异\n以下为忏悔基础说明；上方为忏悔+说明。\n\n'+effect_bullets(base)+'\n:::\n\n'
        if kind=='p' and item.get('horseRepPlus'):
            page+='## 巨型胶囊\n\n'+effect_bullets(item['horseRepPlus'])+'\n\n'
            if item.get('horseRep') and item['horseRep']!=item['horseRepPlus']:
                page+='::: details 忏悔版巨型胶囊差异\n'+effect_bullets(item['horseRep'])+'\n:::\n\n'
        page+='## 解锁与获取\n\n'
        linked=unlocks(item)
        if linked:
            for achievement in linked:
                page+=f'- **解锁条件**：{achievement["conditionZh"]} [详细教程：成就 {achievement["id"]}](/achievements/{achievement["page"]}#achievement-{achievement["id"]})。\n'
            collection = '要收集记录还需实际取得对应道具。' if item['kind']=='c' else '饰品、卡牌与胶囊不计入普通道具收藏页，解锁条件与是否实际用过要分开看。'
            page+='\n解锁表示之后可以正常参与生成，不等于本局一定出现；'+collection+'\n\n'
        if key in SPECIAL_ACQUISITION:page+=SPECIAL_ACQUISITION[key]+'\n\n'
        pool_list=item['poolsRepSnapshot']
        if pool_list:
            page+='**常见来源池（忏悔快照）**：'+'、'.join(POOLS[pool] for pool in pool_list)+'。\n\n'
            page+='道具池不是掉落保证；解锁、难度、角色、模式和模组会改变可用项与生成方式。池表保留 IsaacDocs 的忏悔快照，忏悔+效果变化在上方单列。\n\n'
        elif key not in SPECIAL_ACQUISITION:
            if kind=='k':page+='通过卡牌 / 符文 / 魂石的生成与掉落机制取得；商店、箱子及特定道具也可能提供。不同种类与解锁条件分别判断。\n\n'
            elif kind=='p':page+='通过胶囊生成与掉落取得。普通胶囊的颜色与效果按本局分配，不能只凭颜色认定是这个效果；识别、博士证等还会改变实际效果。\n\n'
            elif kind=='t':page+='通过饰品掉落、箱子、机器及相关道具取得；看到本条目并不代表它在每种来源中都有相同机会。\n\n'
            else:page+='取得方式受道具自身与当前模式规则影响；本快照未列出常规来源池，特殊形态按对应机制生成。\n\n'
        if not linked and key not in SPECIAL_ACQUISITION:
            if kind in ['c','t'] and item['metadata']:
                page+='无需单独成就解锁；能否在本局取得仍按来源与模式规则判断。\n\n'
            elif kind=='k' and item['id']<=26:
                page+='基础塔罗牌 / 花色牌，无需单独成就解锁。\n\n'
            else:
                page+='本条目未关联独立成就条件；特殊生成前置按道具与模式机制判断。\n\n'
        page+='## 使用与取舍\n\n'
        if typ=='active':page+='先比较本主动能解决的短板与现有主动。涉及“当前房间”的增益通常在危险房或 Boss 战前使用；传送、重置和开洞类效果应先确认本层路线事项已完成。充能、临时电量和道具自身冷却按实际状态判断。\n\n'
        elif kind=='p':page+='普通与巨型效果分开看；效果编号与胶囊颜色编号不同，不能直接互换控制台参数。在 Boss 战、低血或限时路线中使用未识别胶囊有额外风险。加减血、传送、加速等效果先与当前角色生命规则和路线目标核对。\n\n'
        elif kind=='k':page+='先确认它是直接消耗的卡牌、符文还是魂石，再规划使用地点。传送与开门效果可以承担路线任务，别提前用掉留给妈妈房、隐藏衣柜或终局入口的消耗品。\n\n'
        elif kind=='t':page+='按当前构筑比较饰品效果与槽位价值。金饰品、妈妈的盒子和叠加效果会改变部分数值，有些改动是特殊规则，不能一律把基础说明乘二。\n\n'
        else:page+='先看当前缺输出、生存还是资源，再判断本条目的效果。箭头、倍率与触发条件要一起读；已有泪弹替换、爆炸、自伤等组合时，先核对效果如何叠加，再决定是否交易或重置掉现有奖励。\n\n'
        combos=[row for row in synergies if kind=='c' and item['id'] in row['items']]
        if combos:
            page+='## 已核对的组合\n\n'
            for row in combos:
                links=' + '.join(f'[{ITEMS[f"c{ident}"]["name"]}](/items/c{ident})' for ident in row['items'])
                page+=f'- **{links}**：{row["effect"]}。\n'
            page+='\n'
        refs=sorted(set(re.findall(r'{{(Collectible|Trinket|Card)(\d+)}}',current)),key=lambda row:(row[0],int(row[1])))
        related=[]
        for tag,ident in refs:
            target={'Collectible':'c','Trinket':'t','Card':'k'}[tag]+ident
            if target!=key:related.append(f'- [{ITEMS[target]["name"]}](/items/{target})')
        if key=='c59':related+=['- [主动版彼列之书](/items/c34)','- [长子名分](/items/c619)','- [犹大](/characters/judas)']
        if key=='c551':related+=['- [第一块铲子碎片](/items/c550)','- [妈妈的铲子](/items/c552)']
        if key=='c656':related+=['- [主动版达摩克里斯之剑](/items/c577)']
        page+='## 相关条目\n\n'+'\n'.join(dict.fromkeys(related))+'\n- [返回道具图鉴](/items/) · [道具取舍与流派](/strategy/items)\n- [道具组合查询](/tools/synergies) · [控制台命令生成器](/tools/console-generator)\n\n'
        wiki='https://bindingofisaacrebirth.wiki.gg/zh/index.php?search='+quote(item['name'])+'&go=Go'
        page+='## 资料来源\n\n'
        page+=f'- 效果与译名：[EID 中文基础说明及忏悔 / 忏悔+更新](https://github.com/wofsauge/External-Item-Descriptions/tree/{ITEM_SOURCE["eidCommit"]}/descriptions)，条目 `{key}`；数值为基础说明，角色与联动按具体机制处理。\n'
        if item['metadata'] or pool_list:page+=f'- 类型、基础充能与池表：[IsaacDocs 数据快照](https://github.com/wofsauge/IsaacDocs/tree/{ITEM_SOURCE["isaacDocsCommit"]}/scripts/data)。\n'
        if linked:
            page+='- 解锁条件：[站内已校对成就表](/achievements/)。条件译文改编自 wiki.gg 贡献者资料，按 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) 发布；原出处见对应成就教程。\n'
        page+=f'- [wiki.gg 中文]({wiki}) · [IsaacGuru](https://isaacguru.com/wiki/isaac/{key})\n'
        entry['_body']=page


def catalog_page(family, legacy=False, subset=''):
    names={'characters':'人物图鉴','rooms':'房间图鉴','floors':'楼层图鉴','items':'道具图鉴'}
    name=names[family]
    selected=CATALOGS[family]
    if subset:selected=[entry for entry in selected if entry['group']==subset]
    import_path='../.vitepress/theme/data/catalog/'+family+'.json'
    selected_expr='(allEntries as CatalogEntry[]).filter(entry => entry.group === '+yaml(subset)+')' if subset else 'allEntries as CatalogEntry[]'
    page='---\ntitle: '+yaml((subset+'攻略') if subset else name)+'\naside: false\n---\n\n<script setup lang="ts">\nimport type { CatalogEntry } from "../.vitepress/theme/data/catalog"\nimport allEntries from '+yaml(import_path)+'\nconst entries = '+selected_expr+'\n</script>\n\n# '+((subset+'攻略') if subset else name)+'\n\n'
    page+='<VersionBadge checked="2026-10" />\n\n'
    descriptions={'characters':'每个角色都有独立页，包含开局、获取方式、核心机制、分阶段发育、清房与 Boss 操作、路线与标记建议。表角色与对应里角色互相链接。','rooms':'每种房间独立说明进入条件、奖励、资源消耗与打法；镜面世界、矿车逃亡、红房间等特殊区域也有单独入口。','floors':'每种楼层独立说明前置、危险与路线出口，I / II 同页讲清；贪婪同名楼层分开列出，避免混用模式规则。','items':'按中文名、英文名、游戏内 ID 或效果关键词搜索。每个道具、饰品、卡牌 / 符文和胶囊都有独立页，包含效果、数值、版本差异、来源及已关联的解锁教程。'}
    page+=descriptions[family]+'\n\n'
    anchors={'characters':'catalog','rooms':'room-index','floors':'floor-index','items':'catalog'}
    page+='## 按名称与类型查找 {#'+anchors[family]+'}\n\n<EntryCatalog :entries="entries" label="'+name+'"'+(' legacy' if legacy else '')+' />\n\n'
    if family=='characters':
        page+='## 解锁与练习\n\n- [角色解锁步骤](/guide/unlocks/order) · [全部里角色获取方式](/guide/unlocks/order#tainted-list)\n- [开局强化](/strategy/character-roster#upgrades) · [完成标记](/strategy/character-roster#marks)\n- [新手练习建议](/strategy/characters#新手先练哪个) · [角色解锁清单](/tools/tracker)\n'
        if legacy:
            page+='\n## 总表\n\n原来的角色总表已整理为上方卡片；点击名字进入完整独立攻略。\n\n## 逐个'+('里角色' if subset=='里角色' else '角色')+'\n\n各角色的发育、打法与路线段落完整保留在独立页中。\n'
            source=(SOURCES/('tainted.md' if subset=='里角色' else 'characters.md')).read_text()
            if subset=='表角色':page+='\n'+'## 新手先练哪个'+source.split('## 新手先练哪个',1)[1].split('## 参考资料',1)[0]
            else:
                page+='\n## 解锁和切换\n\n'+source.split('## 解锁和切换',1)[1].split('## 总表',1)[0]
                page+='\n## 先练哪个里角色'+source.split('## 先练哪个里角色',1)[1].split('## 参考资料',1)[0]
    if family=='rooms':
        text=(SOURCES/'rooms.md').read_text()
        page+='## 每层怎样安排顺序 {#room-order}\n\n'+text.split('## 每层怎样安排顺序',1)[1].split('## 数据依据',1)[0].split('\n',1)[1]+'\n'
        for anchor,label in [('basic','基础战斗与发育'),('hidden-deals','隐藏与交易'),('resource-rooms','用生命和资源换奖励'),('special-rewards','特殊奖励'),('route-rooms','路线功能房'),('special-areas','红房间与路线区域')]:
            page+=f'\n## {label} {{#{anchor}}}\n\n'
            group={'basic':'基础与发育','hidden-deals':'隐藏与交易','resource-rooms':'资源与挑战','special-rewards':'特殊奖励'}.get(anchor,'路线与特殊区域')
            page+=' · '.join(f'[{entry["name"]}]({entry["link"]})' for entry in selected if entry['group']==group)+'\n'
        page+='\n开发枚举中的传送入口 / 出口当前标为未使用；死亡竞赛标识不代表普通单人路线，内部占位值也不计为可探索房间。\n'
    if family=='floors':
        text=(SOURCES/'floors.md').read_text()
        page+='\n### 四条路线怎么选 {#route-map}\n\n'+text.split('### 四条路线怎么选',1)[1].split('## 第一章',1)[0].split('\n',1)[1]
        for anchor,label,group in [('chapter-one','第一章','第一章'),('chapter-two','第二章','第二章'),('chapter-three','第三章','第三章'),('chapter-four','第四章','第四章'),('alt-path','母亲替代路线','母亲路线'),('late-floors','终局楼层','终局与上行'),('home-path','回家路线','终局与上行'),('greed-floors','贪婪七层','贪婪模式')]:
            page+=f'\n## {label} {{#{anchor}}}\n\n'+' · '.join(f'[{entry["name"]}]({entry["link"]})' for entry in selected if entry['group']==group)+'\n'
        curse=text.split('## XL、诅咒与特殊地图怎么处理',1)[1].split('## 贪婪 / 极贪',1)[0].split('\n',1)[1]
        page+='\n## XL、诅咒与特殊地图 {#curses}\n\n'+curse
        page+='\n## 下层之前的检查单 {#before-exit}\n\n'+text.split('## 下层之前的检查单',1)[1].split('## 数据依据',1)[0].split('\n',1)[1]
    page+='\n<span id="参考资料"></span>\n\n## 数据依据 {#sources}\n\n[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。\n'
    return page


def finish():
    for family,entries in CATALOGS.items():
        for i,entry in enumerate(entries):
            if family in ['rooms','floors']:
                related=[row for row in entries if row['group']==entry['group'] and row['id']!=entry['id']][:5]
                entry['_body']+='\n\n## 同类条目\n\n'+' · '.join(f'[{row["name"]}]({row["link"]})' for row in related)+f'\n\n[返回{"房间" if family=="rooms" else "楼层"}图鉴](/{family}/) · [路线与结局](/guide/unlocks/endings) · [机制详解](/strategy/mechanics)\n\n## 资料来源\n\n本站已校对的房间 / 楼层攻略、路线与角色解锁教程；分类核对 [IsaacDocs](https://github.com/wofsauge/IsaacDocs/tree/{ITEM_SOURCE["isaacDocsCommit"]}/docs/enums)。具体数值沿用[机制详解](/strategy/mechanics)及[成就条件](/achievements/)。\n'
            body=rewrite_links(entry['_body'], f'/strategy/{family}' if family in ['rooms','floors'] else '/strategy/tainted' if entry['group']=='里角色' else '/strategy/characters' if family=='characters' else '')
            # Explicit neighbors keep navigation compact rather than putting 1,000 links in the sidebar.
            close=body.index('\n---\n',4)
            nav='\nprev: '+yaml({'text':entries[i-1]['name'],'link':entries[i-1]['link']}) if i else '\nprev: false'
            nav+='\nnext: '+yaml({'text':entries[i+1]['name'],'link':entries[i+1]['link']}) if i+1<len(entries) else '\nnext: false'
            body=body[:close]+nav+body[close:]
            write(f'{family}/{entry["id"]}.md',body)
        DATA.mkdir(parents=True,exist_ok=True)
        data=[{key:value for key,value in entry.items() if not key.startswith('_') and key!='detailAnchors'} for entry in entries]
        (DATA/f'{family}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
        write(f'{family}/index.md',rewrite_links(catalog_page(family)))
    for family in ['rooms','floors']:
        write(f'strategy/{family}.md',rewrite_links(catalog_page(family,legacy=True)))
    for group,file in [('表角色','characters'),('里角色','tainted')]:
        write(f'strategy/{file}.md',rewrite_links(catalog_page('characters',legacy=True,subset=group),f'/strategy/{file}'))
    (DATA/'legacy-links.json').write_text(json.dumps(LEGACY,ensure_ascii=False,indent=2)+'\n')
    (ROOT/'data/entry-pages-manifest.json').write_text(json.dumps({'pages':sorted(GENERATED),'counts':{k:len(v) for k,v in CATALOGS.items()}},ensure_ascii=False,indent=2)+'\n')
    print('Generated standalone pages:', {k:len(v) for k,v in CATALOGS.items()})


if __name__=='__main__':
    make_profiles()
    make_rooms_floors()
    make_items()
    finish()
