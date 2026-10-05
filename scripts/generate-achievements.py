"""Regenerate achievement guides from the reviewed wiki snapshot. No network access.
Source facts and derived translations: CC BY-SA 4.0, see data/achievement-source.README.md.
"""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'data/achievement-source.json').read_text())
assert sorted(x['id'] for x in source)==list(range(1,642))
actors=[('Isaac','以撒','isaac'),('Magdalene','抹大拉','magdalene'),('Cain','该隐','cain'),('Judas','犹大','judas'),('???','小蓝人','bluebaby'),('Eve','夏娃','eve'),('Samson','参孙','samson'),('Azazel','阿撒泻勒','azazel'),('Lazarus','拉撒路','lazarus'),('Eden','伊甸','eden'),('The Lost','游魂','lost'),('Lilith','莉莉丝','lilith'),('Keeper','店主','keeper'),('Apollyon','亚玻伦','apollyon'),('The Forgotten','遗骸','forgotten'),('Bethany','伯大尼','bethany'),('Jacob and Esau','雅各与以扫','jacob')]
ACTORS={a:(b,c,False)for a,b,c in actors}
for a,b,c in actors:ACTORS['Tainted '+a.removeprefix('The ')]=('里'+('雅各'if c=='jacob'else b),c,True)
ACTORS['Tainted Jacob']=('里雅各','jacob',True)
BOSSES={'Mom':'妈妈',"Mom's Heart":'妈妈的心脏','It Lives!':'它活着','Isaac':'以撒（Boss）','???':'小蓝人（Boss）','Satan':'撒但','The Lamb':'羔羊','Mega Satan':'超级撒但','Hush':'死寂','Delirium':'精神错乱','Mother':'母亲','The Beast':'祸兽','Ultra Greed':'究极贪婪','Ultra Greedier':'究极贪婪加强版','Lokii':'Lokii','Gish':'Gish','Steven':'Steven','C.H.A.D.':'C.H.A.D.','Krampus':'Krampus','a Harbinger':'一位天启骑士'}
ROUTES={
'Mom':('主线 / Boss','地下室 I 开始正常清层，走到深牢 II；保留足够血量进入妈妈战并击败她。','/guide/first-win/mom'),
"Mom's Heart":('主线 / Boss','先击败妈妈开放子宫，再到子宫 II 击败妈妈的心脏；已替换为它活着时注意条目的累计计数。','/guide/unlocks/endings'),
'It Lives!':('主线 / Boss','累计击败妈妈的心脏 11 次后到子宫 II，击败替代 Boss 它活着。','/guide/unlocks/endings'),
'Isaac':('角色标记','先开放教堂路线，从子宫 II 的光柱进入教堂；击败以撒。想继续宝箱层，妈妈处需带全家福。','/guide/unlocks/endings'),
'???':('角色标记','先解锁全家福（以撒 Boss 累计 5 次），妈妈处拿它；走教堂打以撒，再碰终点箱子进入宝箱层击败小蓝人。','/guide/unlocks/endings'),
'Satan':('角色标记','先开放阴间路线，从子宫 II 的活板门进阴间，击败撒但；需要继续暗室时妈妈处拿底片。','/guide/unlocks/endings'),
'The Lamb':('角色标记','先解锁底片（撒但累计 5 次），妈妈处拿它；走阴间打撒但，再碰箱子进入暗室击败羔羊。','/guide/unlocks/endings'),
'Mega Satan':('角色标记','规划宝箱层或暗室路线；同局击败两位天使拿齐钥匙碎片，或准备爸爸的钥匙等替代开门手段，打开起始房金门并击败超级撒但。','/guide/unlocks/endings'),
'Hush':('限时 / Boss','先累计击败妈妈的心脏 10 次开放蓝子宫；通常 30 分钟内击败心脏 / 它活着，进入限时门并击败死寂。','/strategy/bosses-2'),
'Delirium':('角色标记','先击败死寂开放虚空；已开放后死寂战后虚空入口适合稳定规划。进入虚空探索各 Boss 房，找到并击败精神错乱。','/strategy/bosses-2'),
'Mother':('角色标记','先累计击败死寂 3 次开放替代路线；下水道 II 取镜世界刀片，矿井 II 完成追逐取第二片，陵墓 II 击败妈妈后用完整刀进入尸宫，击败母亲。','/guide/unlocks/endings'),
'The Beast':('角色标记','先击败母亲开放奇怪的门；深牢 II 带全家福 / 底片传出妈妈房并开门，取爸爸的便条上行回家，打 Dogma 后完成祸兽战。','/guide/unlocks/endings'),
'Ultra Greed':('贪婪 / 捐款','选人时进入贪婪模式，前六层完成按钮波次、购买补强，第七层击败究极贪婪；留钱可顺便捐贪婪捐款机。','/strategy/greed'),
'Ultra Greedier':('贪婪 / 捐款','先向贪婪捐款机累计捐 500 枚开放极贪；选极贪模式到第七层，完成究极贪婪与加强版两个阶段。普通贪婪不满足此项。','/strategy/greed'),
}
def route(b):
 if b in ROUTES:return ROUTES[b]
 return ('探索 / 累计',f'在正常局探索对应楼层的 Boss 房，遇到并击败 {BOSSES.get(b,b)}；避免只打名称相似的另一位 Boss。','/strategy/bosses')
def actor_steps(a):
 zh,key,t=ACTORS[a];page='tainted'if t else'characters'
 return zh,[f'在选人菜单选择{zh}，确认当前局允许解锁。角色机制与开局配置见[{zh}攻略](/strategy/{page}#{key})。']
def finish(group,zh,steps,guide=None):
 if guide:steps.append(f'路线、机制与操作细节见[对应攻略]({guide})。')
 return group,zh,steps
# Explicit translations for irregular and version-specific conditions. Each includes actionable advice.
SPECIAL={
19:('探索 / 单局','同局拾取 4 个绷带球，组成超级绷带女孩。','利用启示录增加天启骑士出现机会，但掉肉块还是绷带球不能保证。若取得怪物手册，可对照专门机制累积临时跟班形态；不要把四个普通跟班当成四级绷带女孩。','https://bindingofisaacrebirth.wiki.gg/wiki/Unlocking_Super_Meat_Boy_%26_Super_Bandage_Girl'),
22:('探索 / 累计','累计击败七宗罪的全部 7 种。','记录 Pride、Wrath、Gluttony、Greed、Lust、Envy、Sloth；在小头目房和普通房继续补缺，不要求同一局。','/guide/first-win/rooms'),
27:('探索 / 单局','用圣经，或忏悔起的逆位恶魔卡，击败妈妈、妈妈的心脏或它活着之一。','带圣经到相应 Boss 房，在战斗中使用。不要带着圣经在撒但战中照做，它对撒但有致死惩罚。','/strategy/items'),
31:('探索 / 单局','同局拾取 2 件带 dead 标签的道具（忏悔 / 忏悔+）。','按当前版本道具标签判断，不照搬旧版仅四件的名单。收集道具要亲自拾取；名称里看似“死亡”的物品不一定具有该标签。','https://bindingofisaacrebirth.wiki.gg/wiki/Item_Tags_dead'),
35:('探索 / 单局','同局获得 3 件妈妈变身（Yes Mother?）组件。','逐件记录实际拿到的组件，达到三件时确认变身。物品带 Mom 名称并不自动表示计入，按变身组件表选择。','https://bindingofisaacrebirth.wiki.gg/wiki/Yes_Mother%3F'),
41:('主线 / Boss','击败小蓝人（Boss）和羔羊。','分别走全家福 → 教堂 → 宝箱层、底片 → 阴间 → 暗室；两条路线可分局完成。','/guide/unlocks/endings'),
42:('角色获取','连续两层不拾取任何心。','用以撒等容错较高角色清两层，避开红心、魂心、黑心等所有地上心；允许受伤不代表允许补心。','/guide/unlocks/order#unlock-eve'),
58:('探索 / 单局','同局从天使获得两块钥匙碎片。','先开放可炸醒天使雕像的条件，到天使房炸醒雕像并击杀天使；继续找到另一位天使，亲自拿齐两个不同碎片。献祭房也能提供天使。','/strategy/mechanics'),
64:('探索 / 累计','累计玩猜壳游戏或忏悔起的 Hell Game 100 次。','找到对应摊位并准备硬币，多次互动累积；普通赌博机与献血机不是这两个摊位。','/strategy/mechanics'),
65:('探索 / 单局','达成嗝屁猫（Guppy）变身。','同局收集 3 件不同嗝屁猫组件，检查变身；主动组件也需实际拾取。不是只拿三个外观像猫的道具。','https://bindingofisaacrebirth.wiki.gg/wiki/Guppy_(Transformation)'),
67:('角色获取','连续完成两层且不受伤。','用阿撒泻勒等清房快的角色练开局；红心、魂心伤害都应避免，不把“无红心伤害”当作无伤。','/guide/unlocks/order#unlock-samson'),
69:('收集 / 全成就','收集重生本体道具，完成本体秘密与结局；不包含游魂及其 6 件专属解锁。','这是旧版白金成就，不是 Dead God；按本体收集范围逐项补，别用当前 641 项总数推算。','/guide/platinum/#remaining'),
77:('主线 / Boss','任意角色击败 Ultra Pride，或用犹大击败小蓝人（Boss）。','可在小头目房找 Ultra Pride；更容易规划的是犹大带全家福走教堂 → 宝箱层。两条任选一条。','/guide/unlocks/endings'),
79:('角色获取','同局完成 3 次恶魔交易。','保护魂心，尽量稳定开交易门，先算支付后能否活着；只是进房或捡黑心不算交易。','/guide/unlocks/order#unlock-azazel'),
82:('角色获取','携带寻人启事，在献祭房内死亡（胎衣以后，包括忏悔）。','先用以撒击败羔羊解锁寻人启事，再实际拿到并携带它；确保死亡位置仍在献祭房内。旧重生的四段死亡解锁法不适用于这里。','/guide/unlocks/order#hidden-lost'),
84:('收集 / 全成就','收集全部重生本体道具，完成全部本体秘密与结局。','与 #69 相比还包括游魂及其本体专属解锁；确认是物品收集页已记录，不是道具已经解锁就算。','/guide/platinum/#remaining'),
86:('探索 / 累计','击败所有地下室章节 Boss；忏悔起不要求 Baby Plum。','按该章节 Boss 名单补缺，在其他区域击败同一 Boss 也可计入，不必只在名为 Basement 的层打。','https://bindingofisaacrebirth.wiki.gg/wiki/The_Cellar'),
87:('探索 / 累计','击败所有洞穴章节 Boss；忏悔起不要求 Bumbino。','记录尚未打过的 Boss，继续正常局补缺；不要求它们全部出现在 Caves 本层。','https://bindingofisaacrebirth.wiki.gg/wiki/The_Catacombs'),
88:('探索 / 累计','击败所有深牢章节 Boss；忏悔起不要求 Reap Creep。','按章节 Boss 名单补齐，替代楼层或其他区域击败相同 Boss 也可计入。','https://bindingofisaacrebirth.wiki.gg/wiki/Necropolis'),
144:('探索 / 单局','同局拾取 4 个肉块，组成超级肉块男孩。','启示录可帮助遇到天启骑士，但不保证掉落全部是肉块；不要混用绷带球进度。怪物手册辅助方法见专门教程。','https://bindingofisaacrebirth.wiki.gg/wiki/Unlocking_Super_Meat_Boy_%26_Super_Bandage_Girl'),
146:('探索 / 单局','同局拾取 2 件带 syringe 标签的道具。','寻找当前版本针剂组件，如成长激素等；按标签确认，不把旧版限定名单当成当前全部候选。','https://bindingofisaacrebirth.wiki.gg/wiki/Item_Tags_syringe'),
156:('角色标记','用游魂完成全部 12 格困难标记，贪婪格为极贪（忏悔 / 忏悔+）。','先完成贪婪捐款 879 枚拿开局神圣屏障；主线用困难、贪婪用极贪，逐格检查。旧版只需 6 / 9 / 10 格的说法不适用于忏悔。','/strategy/character-roster#marks'),
157:('挑战开放','累计击败妈妈的心脏 11 次，并用夏娃击败小蓝人（Boss）。','先开放它活着与宝箱层，再用夏娃带全家福走宝箱层。这里只开放挑战 #4，奖励还需完成挑战本身。','/strategy/challenges'),
160:('挑战开放','累计击败妈妈的心脏 11 次，并解锁拉撒路。','先累计主线击杀，再同一时间持有至少 4 颗魂心解锁拉撒路；菜单检查挑战 #7 是否开放。','/strategy/challenges'),
164:('挑战开放','完成挑战 #19、击败 Lokii，并解锁犹大与它活着。','逐项补前置：Family Man 奖杯、Lokii 击杀、撒但击杀解锁犹大、心脏累计 11 次。不是满足其中一项即可。','/strategy/challenges'),
172:('角色标记','用拉撒路在困难模式击败心脏 / 它活着（胎衣+以后）。','选拉撒路与困难模式完成子宫 II；旧重生 / 胎衣把此奖励归给阿撒泻勒，不照搬旧表。','/strategy/characters#lazarus'),
173:('角色标记','用阿撒泻勒在困难模式击败心脏 / 它活着（胎衣+以后）。','选阿撒泻勒与困难模式完成子宫 II；旧重生 / 胎衣把此奖励归给拉撒路。','/strategy/characters#azazel'),
178:('探索 / 单局','达成苍蝇王（Beelzebub）变身。','同局收集 3 件不同苍蝇王组件，查看变身是否发生；跟班数量不是组件数量。','https://bindingofisaacrebirth.wiki.gg/wiki/Beelzebub'),
232:('挑战奖励','完成 Onan’s Streak，挑战 #29（胎衣+以后）。','在挑战菜单选择 #29，按其泪弹命中规则打到终点并拾取奖杯；旧重生 / 胎衣奖励与 #30 对调。','/strategy/challenges'),
233:('挑战奖励','完成 The Guardian，挑战 #30（胎衣+以后）。','在挑战菜单选择 #30，保护目标到终点并拾取奖杯；不要按旧版本把奖励归给 #29。','/strategy/challenges'),
235:('收集 / 全成就','忏悔起：解锁任意 275 项成就，收集页记录至少 510 件道具。','先补容易的成就，再实际拾取未收集道具。旧胎衣要求其全部秘密、结局与道具，两个版本的条件不同。','/guide/platinum/#remaining'),
258:('探索 / 单局','持有太阳卡时使用空白卡牌。','先拿 Blank Card 与 XIX - The Sun，把太阳卡放在消耗品槽，等主动充满后使用空白卡牌；不是直接使用太阳卡。','/strategy/items'),
267:('挑战开放','炸毁 10 个标记石头，并累计击败妈妈的心脏 11 次。','两项可跨局推进；用带炸弹的角色找带 X 的石头，之后检查挑战 #23 是否开放。','/strategy/challenges'),
270:('挑战开放','击败超级撒但，并解锁底片（忏悔 / 忏悔+）。','撒但累计击败 5 次拿底片，准备金门钥匙走暗室或宝箱层击败超级撒但；这里只开放 #26。','/strategy/challenges'),
273:('挑战开放','解锁犹大和它活着（忏悔 / 忏悔+）。','击败撒但解锁犹大；妈妈的心脏累计 11 次开放它活着，再去挑战菜单找 #29。','/strategy/challenges'),
277:('挑战开放','击败超级撒但，并解锁底片（忏悔 / 忏悔+）。','逐项完成两个前置，挑战 #31 才能选；完成该挑战才会给拉撒路开局贫血。','/strategy/challenges'),
280:('挑战开放','击败超级撒但，并解锁底片（忏悔 / 忏悔+）。','先完成两个前置再尝试 #34 Ultra Hard；开放挑战不等于拿到参孙强化奖励。','/strategy/challenges'),
321:('胜利圈 / 连胜','完成 1 个胜利圈：在胜利圈里击败羔羊。','先正常局击败羔羊，接受 Victory Lap，再通关至羔羊；最初进入胜利圈前的正常局不算一圈。','/achievements/special#victory'),
322:('胜利圈 / 连胜','获得连续 3 局胜利。','用熟悉角色进行可计数的正常局，完成胜利终点；途中死亡或重开会破坏连胜，不用胜利圈代替独立三局。','/achievements/special#streak'),
323:('胜利圈 / 连胜','连续 5 局获胜，每局用不同角色。','用五个不同的表角色连赢五局。表角色和对应的里角色只算一个；部分表、里角色因计数 bug 共用同一位，混用会清零连胜，详见特殊成就教程。','/achievements/special#streak'),
324:('收集 / 全成就','收集怪物图鉴全部条目。','正常探索各楼层、特殊房与模式，补没有遇到的敌人和 Boss。公开表记录旧 v1.9.0 计数 bug，不将 bug 当作稳定捷径。','/achievements/special#collection'),
325:('每日 / 联机','参与 31 次每日挑战，不要求连续日期。','每日关闭模组与控制台后进入实际挑战；开局死亡也计参与，查看排行榜不算。无需为此追求全胜，但同一天重练不能当作多天官方参与。','/achievements/special#daily'),
326:('限时 / Boss','20 分钟内击败羔羊。','准备已解锁的底片，选择清房快的角色，尽量少回头；妈妈处拿底片走阴间 → 暗室，计时是整局时间，不是暗室用时。','/achievements/special#lamb'),
327:('探索 / 单局','整局不拾取心、硬币、炸弹，最后击败羔羊。','钥匙可以拿；避开三类地上资源，不带自动捡这些资源的乞丐跟班或 Lil Portal，也避开 Bumbino 等代捡情况。走底片路线，胜利圈不作为解锁途径。','/achievements/special#lamb'),
328:('胜利圈 / 连胜','PC 连续重开 7 次；部分主机版改为 -10 连败。','PC 在对局中连续重开七次，不把退出菜单当重开；Switch / PS4 按公开表的平台条件核对，不照搬 PC。','/achievements/special#streak'),
329:('探索 / 单局','地下室之后的一个完整章节，两层从头到尾总血量仅半颗心；可用游魂。','最稳按游魂机制完成一个后续章节，或普通角色控总血量到半颗并保持两层；只有红心半颗但另有魂心不满足。','/achievements/special#no-hit'),
330:('探索 / 单局','同局获得 50 件道具。','多层积累道具，利用能增加底座或道具的构筑；同一被动 / 跟班重复份数计入，例如多个早餐。不要按“50种不同道具”误算。','/strategy/items'),
336:('每日 / 联机','每日挑战连续 5 次获胜；不要求连续日历天。','只参加把握较高的每日，完整碰终点奖杯。可以隔日参加，已参加的局死亡会断连胜；练习模式不计正式胜利。','/achievements/special#daily'),
337:('胜利圈 / 连胜','完成 3 个胜利圈，均以击败羔羊结束。','正常局击败羔羊后接受胜利圈，再连续完成三圈；后期圈会变为游魂，规划保命。三圈后按提示继续以触发 RERUN 条件。','/achievements/special#victory'),
339:('收集 / 全成就','忏悔起：解锁任意 402 项成就，收集页记录至少 510 件道具。','先用角色标记、挑战与累计目标补成就数，再拾取未收集道具；旧胎衣+全道具 / 图鉴条件不能直接套用。','/guide/platinum/#remaining'),
354:('每日 / 联机','完成 7 次每日挑战，需触碰终点奖杯。','这项按胜利计，不是参与七次；逐日完成正式 Daily Run，不用练习模式或普通种子复现代替。','/achievements/special#daily'),
355:('探索 / 单局','同局拾取 5 个跟班。','选择跟班资源较多的路线，记录实际拾取的跟班；公开资料中的临时效果计数 bug 不作为计划依据。','/strategy/items'),
358:('探索 / 累计','使用小电池充能 20 次。','持有未满充能主动再拾取小电池，多局继续积累；满充时无法正常拾取不能当充能次数。','/guide/first-win/pickups'),
359:('探索 / 累计','睡一次床。','找到卧室、按床的互动规则睡眠；只是看见床不够。','/guide/first-win/rooms'),
360:('胜利圈 / 连胜','完成 2 个胜利圈，均击败羔羊。','首次正常局不算一圈，接受并完成两次 Victory Lap；顺路继续第三圈可推进 RERUN。','/achievements/special#victory'),
361:('探索 / 单局','体型达到初始的 3 倍；按效果倍率通常需要 5–7 次增大。','收集 One Makes You Larger 等真正增大体型的效果，多次使用；不要仅按拿到“大个子外观”判断。','/strategy/items'),
362:('探索 / 累计','使用卡牌和符文累计 20 次。','实际按消耗品键使用，不是只拾取；在允许解锁的局中逐步积累。','/guide/first-win/pickups'),
363:('收集 / 全成就','收集页同时记录损坏的怀表与怀表。','先完成普通捐款 999 枚解锁怀表，再实际拾取两件；不要求两件同局持有。','/achievements/special#collection'),
364:('探索 / 累计','在商店、恶魔房和 / 或黑市累计购买 50 次。','购买道具或拾取物逐渐累积，三种场所合计；单纯进入房间不算购买。','/strategy/mechanics'),
366:('探索 / 单局','在暗室使用潘多拉魔盒。','先获得 Pandora’s Box，带到暗室再使用；在阴间或宝箱层开不满足地点要求。','/guide/unlocks/endings'),
367:('探索 / 单局','同局拾取 2 件带 battery 标签的道具。','按当前道具标签找电池相关道具；地上普通小电池不是两件收藏道具。','https://bindingofisaacrebirth.wiki.gg/wiki/Item_Tags_battery'),
369:('探索 / 单局','同局拾取 2 件带 tech 标签的道具。','按科技道具标签判断，分别实际拾取；不以外观有激光就认定计入。','https://bindingofisaacrebirth.wiki.gg/wiki/Item_Tags_tech'),
370:('探索 / 单局','获得钥匙碎片 1 和钥匙碎片 2。','通过天使房或献祭房击败两位天使并拿碎片；直接用爸爸的钥匙开金门不会替你取得碎片。','/strategy/mechanics'),
372:('探索 / 累计','击败全部 5 位天启骑士。','记录 Famine、Pestilence、War、Death 与 Conquest，持续探索对应章节；祸兽路线强化骑士不应自动当作同一原版名单。','/strategy/bosses'),
375:('探索 / 累计','累计炸开门与隐藏房墙壁 50 次。','用炸弹对准可炸开的出口或隐藏房候选墙，成功开口才按目标计；随意在房中央放炸弹不是开门。','/strategy/mechanics'),
377:('探索 / 累计','累计获得血块（Blood Clot）10 次。','反复正常局在 Boss 等池取得该道具；不是击杀十个名字相似的敌人。','/strategy/items'),
378:('探索 / 单局','同局获得 10 个射速上升道具或胶囊。','寻找明确 Tears Up 的道具与胶囊效果，累计十次；射速属性已到上限不等于目标次数够了。','/strategy/items'),
379:('探索 / 单局','同局进入 6 个商店。','前六层逐层进商店，带钥匙；若商店被贪婪替换或路线改变要继续寻找有效商店，不是同一房进出六次。','/strategy/mechanics'),
381:('收集 / 全成就','收集页记录蓄电池、9伏特与车载电池。','分别实际拾取 The Battery、9 Volt、Car Battery，跨局补齐三件，不要求同时持有。','/achievements/special#collection'),
382:('探索 / 累计','累计获得橡胶胶水（Rubber Cement）5 次。','先累计击败妈妈的心脏 2 次解锁，再在正常局实际拾取该道具累积。','/strategy/items'),
384:('探索 / 单局','死于自己造成的爆炸毒泪弹。','最直接是拿吐根酊后，让自己的爆炸造成致命伤；也可用原文列出的爆炸与毒组合。先确认当前局允许解锁。','/strategy/items'),
385:('探索 / 累计','累计睡 10 次床。','探索卧室并实际完成睡眠，多局累积；床出现但没睡不计。','/guide/first-win/rooms'),
386:('探索 / 单局','同局使用 5 次 Gulp! 胶囊；安慰剂使用计入。','先完成相关胶囊前置，寻找咕噜并使用；可保留给安慰剂重复复制，记的是使用次数不是拾取次数。','/strategy/items'),
387:('探索 / 单局','同一房间生成 3 个被魅惑的敌人。','使用能魅惑敌人的效果，在同一房内让三只同时满足；蓝苍蝇与普通跟班不是被魅惑敌人。','/strategy/items'),
388:('探索 / 单局','同时拥有 20 只蓝苍蝇。','用嗝屁猫的头等生成蓝苍蝇的手段，在不消耗它们的空房积累到二十只。','/strategy/items'),
389:('探索 / 单局','已经有追踪泪弹时，使用魔术师卡或傻瓜心灵感应。','先拿追踪效果，再用 I - The Magician 或 Telepathy For Dummies，顺序不能反过来只等其效果结束。','/strategy/items'),
390:('角色获取','完成铲子任务，解锁遗骸。','先击败羔羊；首层 Boss 一分钟内击败，炸起始房拿碎铲，完成 Boss Rush 合铲，带到底片暗室路线挖坟。','/guide/unlocks/order#hidden-forgotten'),
391:('角色获取','解锁遗骸，同时开放骨心。','与 #390 同一铲子任务触发，不是先捡到一颗骨心才解锁；完整准备与失败检查见遗骸教程。','/guide/unlocks/order#hidden-forgotten'),
404:('角色获取','用拉撒路在困难模式击败心脏 / 它活着，全程不死亡。','这项开放伯大尼，连拉撒路自身复活都不能触发；别按平时每层主动死亡换属性的玩法做。','/guide/unlocks/order#伯大尼-困难模式与不死要求'),
406:('探索 / 单局','同局收集 3 件带 stars 标签的道具，开放星象房。','按当前 stars 标签找星座或天体组件，例如星座道具、星球跟班等；不是进三次宝箱房。开放后生成仍受概率规则影响。','https://bindingofisaacrebirth.wiki.gg/wiki/Planetarium'),
408:('探索 / 单局','击败塞壬后炸毁她留下的头骨。','在陵墓等对应区域遇到 The Siren，战后别马上离开；用炸弹炸地上的头骨。','https://bindingofisaacrebirth.wiki.gg/wiki/The_Siren'),
410:('探索 / 单局','让 Baby Plum 逃走，不击杀她。','进入战斗后停止输出，以走位躲招等待约 30 秒，直到她离场；避免伤害跟班、毒或自动攻击误杀。','https://bindingofisaacrebirth.wiki.gg/wiki/Baby_Plum'),
411:('主线 / Boss','第一次进入尸宫。','按母亲路线收齐刀片，陵墓 II 击败妈妈后开肉门，通过心脏战进入尸宫；只在下水道或陵墓不算。','/guide/unlocks/endings'),
412:('探索 / 累计','击败下水道的全部 Boss。','先开放替代路线，按 Downpour 的 Boss 名单跨局补缺；不要把“下水道通关一次”当作全 Boss。','https://bindingofisaacrebirth.wiki.gg/wiki/Dross'),
413:('探索 / 累计','击败矿井的全部 Boss。','正常母亲路线中记录矿井 Boss，跨局补齐后开放灰坑。','https://bindingofisaacrebirth.wiki.gg/wiki/Ashpit'),
414:('探索 / 累计','击败陵墓的全部 Boss。','继续母亲路线并核对 Mausoleum Boss 名单，补缺后开放 Gehenna 变体。','https://bindingofisaacrebirth.wiki.gg/wiki/Gehenna'),
415:('主线 / Boss','打开家里妈妈卧室的箱子。','完成上行回家，进入妈妈卧室打开 Mom’s Chest；首次取得红钥匙后可顺路开里角色。','/guide/unlocks/order#tainted-route'),
508:('挑战开放','解锁伯大尼、血袋和它活着。','伯大尼用拉撒路困难不死通关；血袋需献血机累计使用 30 次；它活着需心脏累计 11 次。三项都满足才开放 #37。','/strategy/challenges'),
512:('挑战开放','心脏累计击败 11 次，并解锁弹珠（Marbles）。','先完成同局五次 Gulp! 的 #386，再确认主线次数；这里只开放挑战 #41。','/strategy/challenges'),
513:('挑战开放','解锁里遗骸。','用表遗骸上行回家开隐藏房；这里只开放挑战 #42 Hot Potato，完成奖杯是另一项奖励。','/guide/unlocks/order#tainted-forgotten'),
514:('挑战开放','解锁里该隐。','用表该隐回家开隐藏房，之后从挑战菜单选 #43；不需要先用里该隐打祸兽。','/guide/unlocks/order#tainted-cain'),
515:('挑战开放','解锁里雅各。','用雅各与以扫回家开隐藏房，之后检查 #44；没有另一个“表里以扫”可选角色。','/guide/unlocks/order#tainted-jacob'),
516:('挑战开放','解锁里伊甸。','用表伊甸回家开隐藏房；#45 在挑战菜单是一行无文字的条目，不是菜单漏加载。','/guide/unlocks/order#tainted-eden'),
523:('探索 / 累计','给电池乞丐捐钱，累计使其给出道具 5 次。','准备硬币，保持有可充能主动，让 Battery Bum 正常结算直到给出道具；捐五枚硬币不等于五次道具结算。','/strategy/mechanics'),
545:('探索 / 累计','击杀 10 个电池乞丐。','找到 Battery Bum 后用炸弹等击杀，跨局积累；不是向其捐钱十次。','/strategy/mechanics'),
546:('探索 / 单局','打破 Hornfel 矿车后，在他逃走前击杀他。','到矿井相应 Boss 房，保留爆发输出；矿车破坏后快速击杀本体，别只击毁车就离开。','https://bindingofisaacrebirth.wiki.gg/wiki/Hornfel'),
547:('收集 / 全成就','17 个表角色完成全部困难标记，贪婪格为极贪。','按表角色逐行补十二格；不要求里角色，但也不是只打困难心脏即可。','/strategy/character-roster#marks'),
582:('探索 / 单局','同一间商店消费至少 40 枚硬币。','准备 40+ 钱，在同一商店多次购买，可用补货辅助；不同楼层商店花钱相加不满足。','/strategy/mechanics'),
583:('探索 / 单局','同局先持有 99 枚硬币，再把它们全部花光。','先把显示的钱攒到 99，再通过购物、机器等消费降到 0；仅累计捡到 99 枚但从未同时持有不够。','/strategy/mechanics'),
636:('收集 / 全成就','34 个表 / 里角色完成全部困难标记，贪婪格为极贪。','先解锁全部里角色；每行十二格补齐困难状态，包括极贪，才能开放死亡证明。它仍不是 Dead God。','/strategy/character-roster#marks'),
637:('收集 / 全成就','解锁其余全部成就，并收集全部要求的道具；忏悔+包括新增四项。','先清角色标记与挑战，再补每日 / 特殊条件，最后检查物品收集页；已经解锁但没有实际拾取的道具仍要补。','/achievements/special#collection'),
638:('每日 / 联机','参加一次官方在线游戏（仅忏悔+）。','关闭全部模组并重启，使用游戏官方在线入口从头开始参与；不是 Steam 远程同乐或本地双人。','/topics/coop'),
639:('每日 / 联机','赢得一次官方在线游戏（仅忏悔+）。','从开局加入官方在线局，和队友打到正常胜利终点；中途加入不能按同样规则判断解锁。','/topics/coop'),
640:('每日 / 联机','赢得一次官方在线每日挑战（仅忏悔+）。','关闭模组与控制台，使用在线每日入口，与队友完整打到每日终点；普通在线局和离线每日不替代它。','/topics/coop'),
}
SPECIAL[268]=('挑战开放','用该隐击败以撒（Boss）；忏悔非加号还要求炸 10 个标记石头。','先开放教堂，用该隐击败以撒；忏悔+取消标记石头这一额外前置。这里只开放挑战 #24，完成奖励另计。','/strategy/challenges')
SPECIAL[276]=('角色标记','全部 17 个表角色分别击败超级撒但；忏悔起不包含里角色。','逐个表角色规划宝箱层或暗室金门路线，补齐超级撒但格；角色列表完整解锁后再查缺，不把里角色击杀代替表角色。','/strategy/character-roster#marks')
for ident,count in [(346,3),(347,6)]:SPECIAL[ident]=('探索 / 累计',f'用 {count} 个不同角色击败小蓝人（Boss）。','每次换未计入的角色，带全家福走教堂 → 宝箱层击败小蓝人；反复使用同一角色不增加不同角色数量。','/guide/unlocks/endings')
SPECIAL[509]=('挑战开放','用伯大尼击败撒但，心脏累计 11 次，并解锁抹大拉的信仰。','伯大尼走阴间击败撒但；另用抹大拉带底片击败羔羊解锁 Maggy’s Faith。三个前置都满足，才开放挑战 #38。','/strategy/challenges')
# Same conditions share a reviewed translation, with the entry name still identifying each reward.
for dst,src in {161:65,165:58,352:178}.items():SPECIAL[dst]=SPECIAL[src]
def translate(x):
 n,c=x['id'],x['condition']
 if n in SPECIAL:
  group,zh,tip,guide=SPECIAL[n]
  return finish(group,zh,['准备可解锁的目标存档，并按本条检查指定版本、角色、模式或道具前置。',tip,'完成后回到 Stats → Secrets 检查本编号；若是道具奖励，解锁与物品实际收集是两件事。'],guide)
 # Composite tainted rewards must be completed by the same character across separate runs.
 if ' as ' in c:
  task,a=c.rsplit(' as ',1)
  zh,steps=actor_steps(a)
  if task=='Defeat Isaac , ??? , Satan , and The Lamb':
   return finish('里角色合并奖励',f'用{zh}分别击败以撒、小蓝人、撒但、羔羊，四项齐全。',steps+['至少按两条分支规划：全家福 → 教堂 → 宝箱层，以及底片 → 阴间 → 暗室。可以分局完成，必须由这同一个里角色补齐四格。','单个 Boss 击杀不会单独发这组奖励；建议全部用困难模式完成，避免为死亡证明返工。'],'/strategy/character-roster#marks')
  if task=='Defeat Hush and Boss Rush':
   return finish('里角色合并奖励',f'用{zh}完成 Boss Rush 与死寂，两项齐全。',steps+['通常 20 分钟内击败妈妈进 Boss Rush，30 分钟内击败心脏进死寂门。可以分两局完成，两项必须属于同一里角色。','不要只打其中一个就期待奖励；建议用困难模式补齐。'],'/strategy/character-roster#marks')
  if task in ['Complete the Boss Rush','Complete Boss Rush']:
   return finish('限时 / Boss',f'用{zh}完成 Boss Rush。',steps+['通常 20 分钟内击败深牢 II 的妈妈，进入 Boss Rush 门；选取奖励后开始并打完全部波次。','进入过房间或只拿道具后传走不算完成；妈妈的心脏不是这扇门的触发 Boss。'],'/strategy/bosses')
  if task.startswith('Earn all Hard mode Completion Marks'):
   return finish('角色标记',f'用{zh}完成全部困难标记，贪婪格按极贪。',steps+['选择困难模式完成普通主线的全部目标；另开极贪补最高贪婪状态。','检查角色这一行十二格，不要把普通完成图标或其他角色的格子算进去。'],'/strategy/character-roster#marks')
  if task.lower()=="defeat mom's heart or it lives! on hard mode":
   return finish('角色标记',f'用{zh}在困难模式击败妈妈的心脏 / 它活着。',steps+['选人时确认 Hard，走普通主线至子宫 II。','击败心脏或它活着任一个即可；普通模式、挑战模式和别的角色不替代此条件。'],'/guide/unlocks/endings')
  if task.startswith('Use Red Key'):
   return finish('角色获取',f'用{zh}回家，开启隐藏房并解锁对应里角色。',steps+['先击败母亲开放回家路线；取便条前在宝箱房 / Boss 房丢饰品，上行回程捡红钥匙碎片；首次回家箱子保证有红钥匙。','在家左侧走廊对应墙使用红钥匙 / 碎片等开隐藏房，接触里角色；本局不要求再击败祸兽。'],f'/guide/unlocks/order#tainted-{ACTORS[a][1]}')
  if task.startswith('Defeat '):
   b=task.removeprefix('Defeat ');group,tip,guide=route(b)
   return finish(group,f'用{zh}击败{BOSSES[b]}。',steps+[tip,'本条未额外写困难要求时，普通模式也可解锁；为全困难标记规划可直接用困难。极贪奖励必须选择极贪。'],guide)
 if c.startswith('Complete ') and '(challenge #'in c:
  m=re.fullmatch(r'Complete (.*?) \(challenge #(\d+)\)',c);assert m,c
  name,num=m.groups()
  return finish('挑战奖励',f'完成挑战 #{num} {name}。',[f'在 Challenges 菜单选 #{num}；若尚未开放，先查[挑战总表](/strategy/challenges#全部挑战总表)的开放条件。','按该挑战的固定角色、装备与终点规则推进；打完目标 Boss 后亲自拾取奖杯。','普通局用类似装备击败同一 Boss 不算完成挑战；奖励道具开放后还要实际拾取才能记入收集页。'],'/strategy/challenges')
 m=re.fullmatch(r'Donate (\d+) [Cc]oins to the (Greed Donation Machine|Donation Machine)',c)
 if m:
  num,machine=m.groups();greed=machine.startswith('Greed');where='贪婪捐款机'if greed else'普通捐款机'
  return finish('贪婪 / 捐款'if greed else'探索 / 累计',f'向{where}累计捐 {num} 枚硬币。',[('通关贪婪 / 极贪模式，击败终点 Boss 后保留硬币给捐款机。'if greed else'在正常局商店找到普通捐款机，保留硬币投入。'),f'跨局积累直到机器显示达到 {num}；机器卡住后本局不强行继续，换局再捐。','两种捐款机的累计数互相独立；只是口袋里有同样钱数不等于已捐。'],('/strategy/greed'if greed else'/strategy/mechanics'))
 m=re.fullmatch(r"Defeat (Mom's Heart(?: / It Lives!)?|Isaac|Satan|Hush|Baby Plum|Little Horn) (\d+) times",c)
 if m:
  b,num=m.groups();group,tip,guide=route(b.split(' / ')[0]);label='妈妈的心脏 / 它活着'if b.startswith("Mom's Heart")else BOSSES.get(b,b)
  return finish('探索 / 累计',f'累计击败{label} {num} 次。',[tip,f'以有效正常局继续重复，累计达到 {num} 次；不要求一局打这么多次，也不要求连续胜利。','相关挑战开放和角色奖励可能同时推进；完成后按本编号检查秘密页。'],guide)
 if c.startswith('Defeat '):
  b=c[7:]
  if b=='Delirium for the 1st time':b='Delirium'
  if b in BOSSES:
   group,tip,guide=route(b)
   return finish(group,f'击败{BOSSES[b]}。',['先确认对应路线已开放，选择可解锁的普通局。',tip,'本条没有限定角色；若同场还要拿角色专属奖励，再按其他成就选择角色。'],guide)
 m=re.fullmatch(r'(?:Beat|Complete) Chapter ([1-6])( without taking damage| (\d+) times)?',c)
 if m:
  chapter,extra,num=m.groups();chapter=int(chapter);label={1:'地下室章节',2:'洞穴章节',3:'深牢章节',4:'子宫章节',6:'宝箱层 / 暗室'}[chapter]
  if extra==' without taking damage':
   return finish('探索 / 无伤',f'完成{label}且不受伤。',['选熟悉的角色，优先魂心、护盾与安全输出；护盾替你挡伤不代表可以随意碰撞。',f'在{label}从进入到结束保持无伤。前四章包含 I / II 两层，不能只完成第二层；自伤与特殊扣血按保守无伤策略避开。','“不掉红心”并不等于不受伤，魂心受伤也应避免；无需整局所有其他章节一起无伤。'],'/achievements/special#no-hit')
  return finish('主线 / Boss',f'完成{label}'+(f'累计 {num} 次。'if num else'。'),[f'正常路线推进到{label}，完成章节终点 Boss。','若有累计次数，跨有效局补齐；前四章正常走完 II 层才算章节通关。','替代楼层属于相应章节，但特殊模式的计数不要未经核对当作普通局。'],'/guide/unlocks/endings')
 m=re.fullmatch(r'Destroy (\d+) (Tinted Rocks|rocks|poops|rainbow poops)',c)
 if m:
  num,obj=m.groups();zh={'Tinted Rocks':'标记石头','rocks':'石头','poops':'大便','rainbow poops':'彩虹大便'}[obj]
  return finish('探索 / 累计',f'累计破坏 {num} 个{zh}。',[f'探索房间找到{zh}；石头用炸弹等破坏，大便可射击。','有效正常局中跨局逐步积累，不要求同一层完成。','标记石头需辨认 X 标记，普通石头不能替代；彩虹大便也不是普通大便。'],'/guide/first-win/pickups')
 simple={
 'Have 7 or more Red Heart Containers at one time':('角色获取','同时有至少 7 个红心容器。','用以撒等已解锁角色收集加上限道具，容器可以是空的；魂心、黑心不是红心容器。'),
 'Hold 55 Coins at one time':('角色获取','同时持有 55 枚硬币。','开局攒钱到显示 55，先不购物；累计捡 55 但已经花掉不满足。'),
 'Have 4 or more Soul Hearts at one time':('角色获取','同时持有至少 4 颗魂心。','保留魂心拾取到四颗，同时持有而非累计拿四颗；不是四个半心。'),
 'Beat Basement 40 times':('探索 / 累计','累计完成地下室 40 次。','反复正常局完成地下室，推进自然计数；其他章节通关数不替代。'),
 'Visit 10 Arcades':('探索 / 累计','累计进入 10 个赌博房。','带钥匙与至少少量硬币探索对应层，发现 Arcade 后实际进入，不必消费十次。'),
 'Die 100 times':('探索 / 累计','累计死亡 100 次。','随正常学习过程累计，无需为了此项消耗昂贵练习局；重开与正常死亡是不同事件。'),
 'Use XIII - Death 4 times':('探索 / 累计','累计使用死亡卡 4 次。','拿到 XIII - Death 后实际使用，多局继续；仅拾取不计使用。'),
 'Blow up 20 Shopkeepers':('探索 / 累计','累计炸掉 20 个房间里的店主。','用炸弹炸 Shopkeeper 尸体，和可选角色店主不是同一个对象。'),
 'Take 10 Angel Room items':('探索 / 累计','累计拿 10 件天使房道具。','优先跳过首个恶魔房，提高下一次天使机会；进入房间后实际拿道具，不只是开门。'),
 'Take 20 items from Devil Rooms':('探索 / 累计','累计从恶魔房取得 20 件道具。','正常交易路线拿道具，逐次算血避免死亡；进房次数不等于道具数量。'),
 'Use the Blood Donation Machine 30 times':('探索 / 累计','累计使用献血机 30 次。','准备红心与回血，以血换钱；一次互动扣血计一次，普通捐款机投钱不是献血。'),
 'Blow up 30 Slot Machine':('探索 / 累计','累计炸掉 30 个赌博机。','找到 Slot Machine 后炸毁，多局累积；投币三十次不是炸机三十台。'),
 'Defeat 20 Portals':('探索 / 累计','击败 20 个传送门敌人。','寻找会生成敌人的 Portal 并击杀，地上通往虚空的出口不是这类敌人。'),
 'Open 20 Locked Chests':('探索 / 累计','累计打开 20 个上锁箱子。','留钥匙开金色上锁箱，不把普通木箱或没真正打开的箱子计入。'),
 'Defeat an Angel 10 times':('探索 / 累计','累计击败天使 10 次。','炸天使雕像或用献祭房生成天使并击败，跨局累积；一局只碰雕像不算击败。'),
 'Take 25 Deals with the Devil':('探索 / 累计','累计完成 25 次恶魔交易。','实际拿交易道具而非捡免费黑心或仅进房，多局补；先算付费后的血量。'),
 'Take 50 Deals with the Devil':('探索 / 累计','累计完成 50 次恶魔交易。','继续在可解锁正常局购买，先保证存活；天使房选道具不是恶魔交易。'),
 'Take 25 Angel Rooms items':('探索 / 累计','累计取得 25 件天使房道具。','走天使路线并实际拾取道具，多局补到二十五件，不要求同局。'),
 }
 if c in simple:
  group,zh,tip=simple[c];return finish(group,zh,['在可解锁的正常局准备所需资源与目标房间。',tip,'单局目标必须同局完成；标成“累计”的目标可以跨正常局推进。'],'/strategy/mechanics')
 raise ValueError(f'Untranslated #{n}: {c}')
records=[]
for x in source:
 group,zh,steps=translate(x)
 if x['id'] in {*range(157,167), *range(265,275), *range(277,282), *range(508,517)}:
  group='挑战开放'
  steps.append('此项只开放同名挑战；还要在 Challenges 菜单完成该挑战并拿奖杯，才得到其完成奖励。')
 if x['id'] in {1,2,3,32,42,67,79,80,81,82,199,251,340,390,404,405,*range(474,491)}:
  group='角色获取'
 minimum=next(label for end,label in [(178,'重生'),(276,'胎衣'),(403,'胎衣+'),(637,'忏悔'),(641,'忏悔+')]if x['id']<=end)
 r={**x,'conditionZh':zh,'steps':steps,'group':group,'minimum':minimum,'page':f"ids-{((x['id']-1)//100)*100+1:03d}-{min(((x['id']-1)//100+1)*100,641):03d}"}
 records.append(r)
# 页面只保留每条特有的信息；通用提醒集中写在索引页「使用前先确认」，避免 641 条重复同样的话。
GENERIC={
 '准备可解锁的目标存档，并按本条检查指定版本、角色、模式或道具前置。',
 '完成后回到 Stats → Secrets 检查本编号；若是道具奖励，解锁与物品实际收集是两件事。',
 '按该挑战的固定角色、装备与终点规则推进；打完目标 Boss 后亲自拾取奖杯。',
 '普通局用类似装备击败同一 Boss 不算完成挑战；奖励道具开放后还要实际拾取才能记入收集页。',
 '本条未额外写困难要求时，普通模式也可解锁；为全困难标记规划可直接用困难。极贪奖励必须选择极贪。',
 '先确认对应路线已开放，选择可解锁的普通局。',
 '本条没有限定角色；若同场还要拿角色专属奖励，再按其他成就选择角色。',
 '相关挑战开放和角色奖励可能同时推进；完成后按本编号检查秘密页。',
 '在可解锁的正常局准备所需资源与目标房间。',
 '单局目标必须同局完成；标成“累计”的目标可以跨正常局推进。',
 '此项只开放同名挑战；还要在 Challenges 菜单完成该挑战并拿奖杯，才得到其完成奖励。',
}
PAGE_NAMES={'/guide/unlocks/endings':'结局与路线','/guide/unlocks/order':'角色解锁步骤','/guide/first-win/mom':'第一次打妈妈',
 '/guide/first-win/rooms':'房间类型','/guide/first-win/pickups':'心、钱、炸弹、钥匙','/guide/platinum/':'白金神收尾检查',
 '/strategy/challenges':'挑战模式','/strategy/items':'道具取舍','/strategy/mechanics':'机制详解','/strategy/character-roster':'角色标记',
 '/strategy/greed':'贪婪模式','/strategy/bosses':'Boss 打法（一）','/strategy/bosses-2':'Boss 打法（二）','/strategy/characters':'表角色攻略',
 '/strategy/tainted':'里角色攻略','/achievements/special':'特殊成就教程','/topics/coop':'联机专题'}
GUIDE_RE=re.compile(r'^路线、机制与操作细节见\[对应攻略\]\(([^)]+)\)。$')
ACTOR_RE=re.compile(r'^在选人菜单选择(.+?)，确认当前局允许解锁。角色机制与开局配置见(\[[^]]+\]\([^)]+\))。$')
def render(r):
 links,steps=[],[]
 for st in r['steps']:
  if st in GENERIC:continue
  if m:=GUIDE_RE.match(st):
   url=m[1];links.append(f"[{PAGE_NAMES.get(url.split('#')[0],'相关攻略')}]({url})");continue
  if m:=ACTOR_RE.match(st):
   links.insert(0,m[2]);continue
  steps.append(st)
 tags=f"<Badge type=\"info\" text=\"{r['group']}\" /> <Badge type=\"tip\" text=\"{r['minimum']}\" />"
 out=[f"## #{r['id']} · {r['name']} {{#achievement-{r['id']}}}",f"**条件**：{r['conditionZh']} {tags}"]
 if steps:out.append('\n'.join(f'- {s}' for s in steps))
 links.append(f"[wiki 原条目]({r['source']})")
 out.append('相关：'+' · '.join(links)+' {.ach-links}')
 return out
for start in range(1,642,100):
 end=min(start+99,641);subset=[r for r in records if start<=r['id']<=end]
 jumps=' · '.join(f'[#{i}](#achievement-{i})' for i in range(start,end+1,10))
 lines=[f'---\ntitle: 全成就 #{start}–{end}\noutline: false\n---',f'# 全成就 #{start}–{end}','<VersionBadge checked="2026-10" />',
  f'[← 返回搜索](/achievements/) · 编号对应游戏内 Stats → Secrets。做之前先看[通用规则](/achievements/#rules)：哪些局不能解锁、困难与普通的区别、挑战开放和完成是两回事。',
  f'跳到：{jumps} {{.ach-jump}}']
 for r in subset:lines.extend(render(r))
 lines.extend(['## 来源与授权','成就编号、名称、条件事实来自 [The Binding of Isaac: Rebirth Wiki · Achievements](https://bindingofisaacrebirth.wiki.gg/wiki/Achievements)，2026-10-05 保存的修订版 269014。本文对其条件进行翻译并补充操作说明，按 [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)发布，此页适用该授权而非站点默认的非商业授权。未在云环境逐项运行游戏解锁。'])
 (ROOT/f"docs/achievements/{subset[0]['page']}.md").write_text('\n\n'.join(lines)+'\n')
# The UI uses only searchable fields; source facts stay in data/achievement-source.json.
ui=[{k:r[k]for k in ['id','name','conditionZh','group','minimum','page']}for r in records]
(ROOT/'docs/.vitepress/theme/data/achievements.json').write_text(json.dumps(ui,ensure_ascii=False,indent=2)+'\n')
print(f'Generated {len(records)} individually anchored tutorials across 7 pages.')
