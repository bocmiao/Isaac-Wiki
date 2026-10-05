---
title: 道具取舍与流派
---

# <GameIcon name="crown" :size="36" style="vertical-align: -6px; margin-right: 6px" />道具取舍与流派

<VersionBadge checked="2026-10" />

挑道具先看品质。品质分 0–4 五档，3 和 4 是最高的两档。恶魔交易拿不拿，先算付完之后还剩什么血：还剩红心容器、魂心或黑心，就可以拿品质 3–4 的道具；付完什么都不剩，就会死。想要天使房或钥匙碎片（Key Piece），就一次都别买。组合只看英文 wiki 道具页「Synergies」段落里写明的，本页列了 8 组。最后一节是每层的资源取舍清单。

::: info 版本
本页以忏悔+（Repentance+）为准。忏悔+ 改过不少道具的品质和效果，有差别的地方会标出「忏悔」和「忏悔+」两个数值。
:::

## 道具品质：粗略的强弱刻度

品质是忏悔（Repentance）加入的隐藏数值，每个道具都有，从 0 到 4，写在游戏文件 `items_metadata.xml` 里。游戏本身不显示品质。装了 [EID](/topics/mods) 的话，道具名后面会有品质图标（设置项 `ShowQuality`，忏悔版默认开）。EID 也能显示道具来自哪个道具池，这项默认关。

品质只能粗看。它不管你已经有什么道具、玩什么角色。两件道具二选一，又没有明确的组合关系时，先选品质高的。恶魔房还有一个参照：wiki 说恶魔房道具卖 1 或 2 个红心容器，价格大致和强度对应。

下面这些机制会直接看品质：

| 道具 / 角色 | 和品质的关系 |
| --- | --- |
| 十字圣球（Sacred Orb） | 品质 0–1 的道具自动重置，品质 2 的有 33% 概率重置。任务道具不受影响 |
| 里游魂（Tainted Lost） | 只会遇到带 offensive 标签的道具；品质 2 及以下的道具有 20% 概率被重置 |
| 不！（NO!）饰品 | 叠加持有、持有金色版本或配合妈妈的盒子（Mom's Box）时，品质 0 的道具会被重置 |
| 筹码（Poker Chip）饰品，忏悔+ | 箱子里如果是品质 0–2 的道具，会重置并获得 +1 品质加成 |
| 长子名分（Birthright），里伯大尼（Tainted Bethany） | 所罗门魔典（Lemegeton）召唤的魂火必定是品质 3 以上的道具 |
| 合成宝袋（Bag of Crafting） | 放进去的掉落物决定做出什么档次的道具 |
| 无底坑（Abyss），忏悔+ | 吞掉道具变成蝗虫，蝗虫伤害按道具品质算：0 档 0.5 倍，1 档 0.75 倍，2 档 1 倍，3 档 1.5 倍，4 档 2 倍 |

wiki 品质页列出的机制里，没有只出低品质道具的。

::: tip 忏悔+ 改过的品质（举例）
撒但圣经（Satanic Bible）、虚空（Void）、无底坑：4 → 3。达摩克里斯之剑（Damocles）、光环（The Halo）、内眼（The Inner Eye）：2 → 3。鲁多维科科技（The Ludovico Technique）：2 → 1。亡者之书（Book of the Dead）、炼金硫磺（Sulfur）：3 → 2。看老攻略时注意版本。
:::

## 恶魔交易：拿还是不拿

先记住付款规则（更细的价格规则见[机制详解](/strategy/mechanics)）：

- 道具一般卖 1 或 2 个红心容器。没有红心容器时，改卖 3 个魂心。忏悔起，偶尔有道具在你还有红心容器时也标魂心价。
- 忏悔起，只剩 1 个红心容器时，原价 2 容器的交易会改收 **1 个容器 + 2 个魂心**；魂心不足时仍可交易，但必须重新算付完后的存活血量，不能认为只扣那 1 个容器。
- 红心容器全付光不会死，前提是还有魂心、黑心或骨心。
- 只要在恶魔房付血（红心容器或魂心）买过一次道具，这局就不会再出天使房。
- 恶魔房只在第 1 章第二层到第 4 章（子宫）之间出现。

| 你的情况 | 怎么做 |
| --- | --- |
| 付完还剩红心容器，或者还有魂心、黑心、骨心 | 可以拿。优先品质 3–4、标价 2 心的道具 |
| 付完什么血都不剩 | 不拿，会直接死 |
| 想要天使房，或者想拿钥匙碎片1/2 | 一次都别买。通关过暗室或宝箱（The Chest）一次后，天使房里的天使雕像可以用炸弹炸醒，打赢掉钥匙碎片；两块凑齐才能开通往超级撒但的金色大门 |
| 这局已经买过一次 | 天使房已经没了，除非有痛悔短祷（Act of Contrition）；后面的恶魔房只需要考虑血够不够 |
| ???（??? / Blue Baby） | 忏悔起按 1 或 2 个魂心付，不是 3 个 |
| 店主（Keeper） | 忏悔起用硬币付：1 心的卖 15 个，2 心的卖 30 个 |
| 游魂（The Lost）、里游魂、鬼魂状态的里雅各（Tainted Jacob） | 忏悔起可以免费拿一件，其余的随之消失 |
| 已经到了子宫 | 这是最后能开出恶魔房的一章 |

::: warning 忏悔+ 的新付款方式
带 `devilsacrifice` 标签的恶魔交易道具，改为踩献祭尖刺（Sacrifice Spikes）付款，不扣红心容器。例如剃刀片（Razor Blade）、狂怒！（Berserk!）、一磅肉（A Pound of Flesh）。原文规则为第一次踩有 50% 概率给道具，第二次必给；拾取这样生成的底座仍算恶魔交易，会影响自然天使房。
:::

想反过来走天使路线：圣餐（Eucharist）让每次都开天使房；痛悔短祷（Act of Contrition）能让买过交易之后仍然出天使房。恶魔房和天使房的出现概率怎么算，见[机制详解](/strategy/mechanics)。

## 恶魔房里值得换心的道具

下表都在恶魔房道具池里，品质按忏悔+。「标价 2 心」取自 wiki 道具信息框。

| 道具 | 品质 | 效果 | 注意事项 |
| --- | --- | --- | --- |
| 硫磺火（Brimstone） | 4 | 泪弹换成蓄力血激光，穿透敌人和障碍 | 射速 ÷3；标价 2 心 |
| 妈妈的菜刀（Mom's Knife） | 4 | 泪弹换成可蓄力投掷的菜刀，拿在手里也能伤敌 | 标价 2 心；宝箱房道具池也有，忏悔起权重 0.2 |
| 淫魔（Incubus） | 4 | 跟班，发射和你一样的泪弹 | 忏悔起非莉莉丝（Lilith）角色伤害降 25%；标价 2 心 |
| 作孽双子（Twisted Pair） | 4 | 两侧各一个跟班，用你的射速、射程和泪弹效果，各造成 0.375 倍伤害 | 标价 2 心 |
| 超级喷射（Mega Blast） | 4 | 主动：发射 15 秒巨型激光，能跨房间、跨层 | 池中权重只有 0.2；激光期间不能捡道具、开箱子 |
| 亚巴顿（Abaddon） | 3 | 伤害 +1.5，移速 +0.2；红心容器全换成黑心，再给 2 黑心 | 拿完没有红心容器，之后的交易改收 3 个魂心；标价 2 心 |
| 契约（The Pact） | 3 | 伤害 +0.5，射速 +0.7，2 个黑心 | 标价 2 心 |
| 山羊头（Goat Head） | 3 | 之后每个能开门的 Boss 房都必开恶魔房或天使房 | — |
| 死神之触（Death's Touch） | 3 | 伤害 +1.5，射速 -0.3，泪弹换成大镰刀并穿透 | 标价 2 心 |
| 犹大的影子（Judas' Shadow） | 3 | 死后以犹大之影（Black Judas）带 2 黑心复活 | 等于一条命；标价 2 心 |
| 撒但圣经（Satanic Bible） | 忏悔 4 → 忏悔+ 3 | 主动：给 1 黑心；用过之后，本层 Boss 掉落变成恶魔交易 | 要在打 Boss 前用；标价 2 心 |
| 达摩克里斯之剑（Damocles） | 忏悔 2 → 忏悔+ 3 | 主动：头顶悬剑，所有底座道具翻倍 | 见下方警告；标价 2 心 |

::: warning 达摩克里斯之剑
用过之后只要受伤一次，剑就可能在任何时候落下，直接杀死你，不看剩多少血。自伤（献祭房、献血机、诅咒房等）不算受伤。
:::

## 天使房里值得拿的道具

天使房道具免费，但拿走一件，其余免费道具会消失。下表都在天使房道具池里，品质按忏悔+。

| 道具 | 品质 | 效果 | 注意事项 |
| --- | --- | --- | --- |
| 神性（Godhead） | 4 | 追踪泪弹，泪弹带伤害光环；伤害 +0.5 | 射速、弹速各 -0.3 |
| 圣心（Sacred Heart） | 4 | +1 红心容器并回满血；伤害 ×2.3 再 +1；追踪泪弹 | 射速 -0.4；忏悔+ 起算作撒拉弗变身（Seraphim）的组件 |
| 神圣屏障（Holy Mantle） | 4 | 每个房间第一次受到的伤害被挡掉 | 宝箱房道具池也有，忏悔起权重 0.2 |
| 圣饼（The Wafer） | 4 | 大多数超过半心的伤害降为半心 | — |
| 光明之冠（Crown of Light） | 4 | +2 魂心；红心容器全满（或没有红心容器）时伤害 ×2 | 受伤后本房间失效 |
| 终末天启（Revelation） | 4 | 飞行；持续射击 2.35 秒后松开，放出圣光激光 | 忏悔+ 起不再给 2 个魂心 |
| 十字圣球（Sacred Orb） | 4 | 低品质道具自动重置，见品质一节 | 池中权重 0.5 |
| 英灵剑（Spirit Sword） | 3 | 攻击换成挥剑，每下造成角色伤害的 3 倍再加 3.5；蓄力可旋转攻击 | 总血量不少于红心容器数时，挥剑会放剑气 |
| 圣餐（Eucharist） | 3 | 之后每次能开门都开天使房 | — |
| 痛悔短祷（Act of Contrition） | 3 | 射速 +0.7，1 个永恒之心；买过恶魔交易后仍会出天使房 | 也会减轻掉红心对开门概率的惩罚 |
| 天堂阶梯（The Stairway） | 3 | 每层初始房间出现梯子，通往天使商店 | 离开初始房间梯子就消失；道具卖 15 或 30 个硬币 |
| 光环（The Halo） | 忏悔 2 → 忏悔+ 3 | +1 红心容器，伤害、射速、射程、移速小幅提升 | — |

## 宝箱房里容易被低估的道具

下面这些都在宝箱房道具池里，效果要理解机制才用得好。

| 道具 | 品质 | 效果 | 怎么用 / 注意事项 |
| --- | --- | --- | --- |
| 六面骰（The D6） | 4 | 主动：把房间里所有底座道具重置成同一道具池的其他道具 | wiki 说在有多件道具的房间用最划算：商店、恶魔房、天使房、Boss Rush。以撒解锁它后开局自带 |
| 计数二十面骰（Spindown Dice） | 4 | 主动：房间里每件道具的内部编号减 1，变成那个编号的道具 | 池中权重只有 0.1；没解锁的道具会被跳过 |
| 吐根酊（Ipecac） | 4 | 泪弹换成抛物线飞行的爆炸毒弹，伤害 +40 | 射速变为 1/3；爆炸通常会伤到自己半心 |
| 发光沙漏（Glowing Hourglass） | 3 | 主动：回到上一个房间，撤销这个房间里发生的一切 | 忏悔起每层只能用 3 次，之后变成沙漏（The Hourglass）的效果。忏悔起，进了本局第一个恶魔房再用它退出来，仍能保住下一次必出天使房 |
| 合成宝袋（Bag of Crafting） | 3 | 收集最多 8 个掉落物，合成一个道具 | 放进去的掉落物决定做出的道具品质 |
| 被掰弯的硬币（Crooked Penny） | 2 | 主动：50% 把房间里的道具、掉落物、饰品、箱子全部翻倍；失败则全部消失，只给 1 硬币 | 在商店、恶魔房用，翻出来的那份免费 |

## 常见组合

下面每组都写在英文 wiki 某个道具页的「Synergies」段落里。

| 组合 | 两件道具各是什么 | 合起来变成什么 |
| --- | --- | --- |
| 硫磺火 + 妈妈的菜刀 | 蓄力血激光；可投掷的菜刀 | 菜刀优先，不吃硫磺火的射速惩罚。扔出菜刀后再射出一小串菜刀，忏悔起每把造成 2 倍伤害 |
| 硫磺火 + 内眼（The Inner Eye） | 血激光；内眼一次发 3 颗泪弹、射速降低（宝箱房道具） | 一次射 3 道激光。wiki 说内眼虽有射速惩罚，总输出提升比完美视力（20/20，2 道激光）更明显 |
| 终末天启 + 天使棱镜（Angelic Prism） | 圣光激光；天使棱镜是大半径环绕物，泪弹穿过会分裂成 4 颗 | 激光打到棱镜，分成 4 道 |
| 英灵剑 + 妈妈的菜刀 | 挥剑攻击；投掷菜刀 | 蓄力旋转攻击时把剑扔出去一小段，边飞边转 |
| 英灵剑 + 三圣颂（Trisagion） | 挥剑攻击；三圣颂把泪弹换成穿刺光波，单次 33% 伤害但每秒最多打 15 次 | 剑气换成三圣颂光波，伤害更高 |
| 光明之冠 + 神圣屏障 | 满血时伤害 ×2、受伤就熄；每房间挡一次伤害 | 屏障挡下的那一下不会让冠冕熄灭 |
| 达摩克里斯之剑 + 神圣屏障 | 道具翻倍、受伤后可能掉剑；每房间挡一次伤害 | 被屏障挡下的伤害不算受伤，不会开始掉剑的判定。剑真的落下时，屏障挡不住 |
| 嗝屁猫的爪子（Guppy's Paw）+ 嗝屁猫（Dead Cat） | 爪子是主动道具，1 个红心容器换 3 个魂心；嗝屁猫把红心容器设为 1 个，给 9 条命，每次复活带 1 个红心容器 | 每次复活后把那个容器换成 3 魂心，wiki 说相当于血量变成 3 倍。两件都算嗝屁猫变身（Guppy）的组件，都在恶魔房道具池 |

## 每层流程清单

规则和价格见入门文章，这里只列取舍。

| 环节 | 做什么 | 取舍要点 |
| --- | --- | --- |
| 开图 | 按住 <KeyCap>Tab</KeyCap> 看地图，标出宝箱房、商店和隐藏房的候选位置 | 先算这层钥匙和炸弹够不够，不够就按[心、钱、炸弹、钥匙怎么用](/guide/first-win/pickups)的优先级分 |
| 宝箱房 | 拿道具。带着重置类主动道具时，先看品质再决定重置不重置 | 看见过的道具不会从池里消失，只是在池里的权重降低；碰过的道具才会从所有道具池移除 |
| 商店 | 在道具和钥匙、炸弹之间取舍 | 店主的恶魔交易要用硬币付，别把钱花光；被掰弯的硬币在商店用最值 |
| 隐藏房 | 用炸弹炸开隐藏房和超级隐藏房 | 找法见[房间类型入门](/guide/first-win/rooms)，每层留够炸弹 |
| Boss 房 | 有撒但圣经就在打 Boss 前用；想开恶魔房、天使房就少掉红心 | 概率规则见[机制详解](/strategy/mechanics) |
| 恶魔房 / 天使房 | 按上面的决策表拿。六面骰在这两种房间用最划算 | 发光沙漏不会让本来没开的门开出来 |
| 进第 4 章前 | 资源在前三章花掉，原因见[新手前 10 局该注意什么](/guide/first-win/first-runs) | 子宫是最后能开恶魔房的一章 |

## 参考资料

- [Item Quality](https://bindingofisaacrebirth.wiki.gg/wiki/Item_Quality)
- [Item Pool](https://bindingofisaacrebirth.wiki.gg/wiki/Item_Pool)
- [Devil Room (Item Pool)](https://bindingofisaacrebirth.wiki.gg/wiki/Devil_Room_(Item_Pool))
- [Angel Room (Item Pool)](https://bindingofisaacrebirth.wiki.gg/wiki/Angel_Room_(Item_Pool))
- [Treasure Room (Item Pool)](https://bindingofisaacrebirth.wiki.gg/wiki/Treasure_Room_(Item_Pool))
- [Devil Room](https://bindingofisaacrebirth.wiki.gg/wiki/Devil_Room)
- [Angel Room](https://bindingofisaacrebirth.wiki.gg/wiki/Angel_Room)
- [Tainted Lost](https://bindingofisaacrebirth.wiki.gg/wiki/Tainted_Lost)
- 恶魔房道具：[Brimstone](https://bindingofisaacrebirth.wiki.gg/wiki/Brimstone)、[Mom's Knife](https://bindingofisaacrebirth.wiki.gg/wiki/Mom%27s_Knife)、[Incubus](https://bindingofisaacrebirth.wiki.gg/wiki/Incubus)、[Twisted Pair](https://bindingofisaacrebirth.wiki.gg/wiki/Twisted_Pair)、[Mega Blast](https://bindingofisaacrebirth.wiki.gg/wiki/Mega_Blast)、[Abaddon](https://bindingofisaacrebirth.wiki.gg/wiki/Abaddon)、[The Pact](https://bindingofisaacrebirth.wiki.gg/wiki/The_Pact)、[Goat Head](https://bindingofisaacrebirth.wiki.gg/wiki/Goat_Head)、[Death's Touch](https://bindingofisaacrebirth.wiki.gg/wiki/Death%27s_Touch)、[Judas' Shadow](https://bindingofisaacrebirth.wiki.gg/wiki/Judas%27_Shadow)、[Satanic Bible](https://bindingofisaacrebirth.wiki.gg/wiki/Satanic_Bible)、[Damocles](https://bindingofisaacrebirth.wiki.gg/wiki/Damocles)、[Abyss](https://bindingofisaacrebirth.wiki.gg/wiki/Abyss)、[Void](https://bindingofisaacrebirth.wiki.gg/wiki/Void)、[Guppy's Paw](https://bindingofisaacrebirth.wiki.gg/wiki/Guppy%27s_Paw)、[Dead Cat](https://bindingofisaacrebirth.wiki.gg/wiki/Dead_Cat)
- 天使房道具：[Godhead](https://bindingofisaacrebirth.wiki.gg/wiki/Godhead)、[Sacred Heart](https://bindingofisaacrebirth.wiki.gg/wiki/Sacred_Heart)、[Holy Mantle](https://bindingofisaacrebirth.wiki.gg/wiki/Holy_Mantle)、[The Wafer](https://bindingofisaacrebirth.wiki.gg/wiki/The_Wafer)、[Crown Of Light](https://bindingofisaacrebirth.wiki.gg/wiki/Crown_Of_Light)、[Revelation](https://bindingofisaacrebirth.wiki.gg/wiki/Revelation)、[Sacred Orb](https://bindingofisaacrebirth.wiki.gg/wiki/Sacred_Orb)、[Spirit Sword](https://bindingofisaacrebirth.wiki.gg/wiki/Spirit_Sword)、[Eucharist](https://bindingofisaacrebirth.wiki.gg/wiki/Eucharist)、[Act of Contrition](https://bindingofisaacrebirth.wiki.gg/wiki/Act_of_Contrition)、[The Stairway](https://bindingofisaacrebirth.wiki.gg/wiki/The_Stairway)、[The Halo](https://bindingofisaacrebirth.wiki.gg/wiki/The_Halo)、[Angelic Prism](https://bindingofisaacrebirth.wiki.gg/wiki/Angelic_Prism)、[Trisagion](https://bindingofisaacrebirth.wiki.gg/wiki/Trisagion)
- 宝箱房道具：[The D6](https://bindingofisaacrebirth.wiki.gg/wiki/The_D6)、[Spindown Dice](https://bindingofisaacrebirth.wiki.gg/wiki/Spindown_Dice)、[Ipecac](https://bindingofisaacrebirth.wiki.gg/wiki/Ipecac)、[Glowing Hourglass](https://bindingofisaacrebirth.wiki.gg/wiki/Glowing_Hourglass)、[Bag of Crafting](https://bindingofisaacrebirth.wiki.gg/wiki/Bag_of_Crafting)、[Crooked Penny](https://bindingofisaacrebirth.wiki.gg/wiki/Crooked_Penny)、[The Inner Eye](https://bindingofisaacrebirth.wiki.gg/wiki/The_Inner_Eye)、[The Ludovico Technique](https://bindingofisaacrebirth.wiki.gg/wiki/The_Ludovico_Technique)
- [External Item Descriptions 源码（GitHub，eid_config.lua 与中文语言文件）](https://github.com/wofsauge/External-Item-Descriptions)

<!-- 待核实：
- 嗝屁猫的爪子（Guppy's Paw）：信息框品质为 3 且没有版本标记，但正文写「忏悔+ 中合成宝袋按品质 2 计算」，是否为忏悔+ 从 2 调到 3 未确认，正文未写版本差异。
- 恶魔房道具池里的 Money = Power、Little Horn 未能读到品质字段（页面读取被拦截或字段缺失），未纳入表格。
- 合成宝袋原料总值与道具品质的对应表：WebFetch 摘要的表格前后矛盾，未写入。
- 天使房页面摘要提到念珠（Rosary Bead）饰品在忏悔+ 让天使房必定出现，与该页其他内容对不上，未采用。
- 发光沙漏「特殊房间进门代价不退还」来自摘要，未逐字核实，未写入。
- 各角色的初始红心容器数未查角色页面，决策表因此不按具体角色给阈值。
- 撒但圣经忏悔+ 新增的「如果恶魔交易是主动道具，下一件道具改在底座生成」一句含义不清，未写入。
-->
