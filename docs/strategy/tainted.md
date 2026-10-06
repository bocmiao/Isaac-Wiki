---
title: "里角色攻略"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/characters.json"
const entries = (allEntries as CatalogEntry[]).filter(entry => entry.group === "里角色")
</script>

# 里角色攻略

<VersionBadge checked="2026-10" />

按名称找角色，点卡片看解锁步骤、选道具和打法。每页还列出这个角色的完成标记奖励。

## 按名称与类型查找 {#catalog}

<EntryCatalog :entries="entries" label="人物图鉴" legacy />

## 解锁与练习

- [角色解锁步骤](/guide/unlocks/order) · [全部里角色获取方式](/guide/unlocks/order#tainted-list)
- [开局强化](/strategy/character-roster#upgrades) · [完成标记与全角色奖励](/strategy/completion-marks)
- [新手练习建议](/strategy/characters#新手先练哪个) · [角色解锁清单](/tools/tracker)

## 总表

点击上方角色卡片查看开局、解锁方法和打法。

## 逐个里角色

角色页内可直接跳到选道具、清房与 Boss 打法、路线建议。

## 解锁和切换

里角色在游戏内中文叫「堕化」角色，例如堕化以撒。本站沿用社区说法「里角色」。

- **不是独立模式**：里角色是另一组选人列表，可以再选普通 / 困难或贪婪 / 极贪。解锁一个不会同时开放其他 16 个。
- **获取总表**：[全部 17 个里角色的对应表](/guide/unlocks/order#tainted-list)，以及[隐藏表角色的前置任务](/guide/unlocks/order#hidden)。
- **解锁**：用对应的表角色本人到「家」，在妈妈卧室前的走廊，用红钥匙（Red Key）、红钥匙碎片（Cracked Key）或该隐的魂石（Soul of Cain）打开左侧墙上的衣柜。完整步骤见[角色解锁顺序](/guide/unlocks/order)。
- **切换**：在角色选择界面，键盘按 <KeyCap>E</KeyCap>，手柄按 <KeyCap>RB</KeyCap>，切到里角色。

## 先练哪个里角色

按开局条件和规则改动的多少来排，不打分：

1. **规则改动集中在一处**：[里以撒](/characters/tainted-isaac#isaac)（3 红心容器，泪弹照常，只多了 8 格被动上限）、[里参孙](/characters/tainted-samson#samson)（3 红心容器，平时射泪弹，狂暴时才强制近战）、[里抹大拉](/characters/tainted-magdalene#magdalene)（4 个红心容器，其中 2 个是空的，近身杀敌就能回血）。
2. **有现成的保命手段**：[里犹大](/characters/tainted-judas#judas)的暗仪刺刀用后短时间无敌，能直接穿过弹幕；代价是只有黑心，不能获得红心。
3. **攻击方式完全不同**：[里莉莉丝](/characters/tainted-lilith#lilith)、[里遗骸](/characters/tainted-forgotten#forgotten)不能自己发射泪弹；[里夏娃](/characters/tainted-eve#eve)要按住射击才能生成血团；[里阿撒泻勒](/characters/tainted-azazel#azazel)要先喷嚏再放硫磺火。
4. **需要解锁储备**：[里该隐](/characters/tainted-cain#cain)只能合成道具，最好先解锁大部分掉落物。
5. **要另外练资源系统**：[里???](/characters/tainted-bluebaby#bluebaby) 要用大便补输出并留爆炸手段；[里拉撒路](/characters/tainted-lazarus#lazarus)要同时维持两套道具搭配；[里亚玻伦](/characters/tainted-apollyon#apollyon)先比较拿道具和换蝗虫；[里伯大尼](/characters/tainted-bethany#bethany)要分开管理魂心（生命）和红心变成的血充能。
6. **一次失误代价大**：[里游魂](/characters/tainted-lost#lost)没有血量；[里雅各](/characters/tainted-jacob#jacob)被里以扫撞一次，本层就变成一碰就死的灵魂；[里店主](/characters/tainted-keeper#keeper)硬币心上限固定 2 个；[里伊甸](/characters/tainted-eden#eden)每次受伤都重置道具。

::: tip 解锁顺序也有限制
每个里角色只能由对应的表角色去解锁。想练的里角色，先确认表角色已经解锁，再参考[角色解锁顺序](/guide/unlocks/order)。
:::

## 完成标记

里角色也有一套完成标记，但每人只对应 7 项专属解锁；仍有十二格要补。[死亡证明](/items/c628)要求全部 34 个表 / 里角色都完成全部困难标记，贪婪格要打极贪，共 408 格。[逐格奖励与缺项判断](/strategy/completion-marks)。

七项专属解锁的分组如下：

- 以撒、???、撒但、羔羊四个标记合起来解锁一样东西。
- Boss Rush（游戏内：头目车轮战，连打多波 Boss 的房间）和死寂合起来解锁一样东西。
- 超级撒但、极贪模式、精神错乱、母亲、祸兽各解锁一样。
- 妈妈的心脏 / 它活着、贪婪模式（究极贪婪）这两格没有解锁。

以里以撒为例：

| 标记 | 解锁 |
| --- | --- |
| 以撒 + ??? + 撒但 + 羔羊 | 妈妈的发髻（Mom's Lock） |
| Boss Rush + 死寂 | 以撒的魂石（Soul of Isaac） |
| 超级撒但 | 大箱子（Mega Chest） |
| 极贪模式 | XVII-星星？（XVII - The Stars?） |
| 精神错乱 | 计数二十面骰（Spindown Dice） |
| 母亲 | 骰子袋（Dice Bag） |
| 祸兽 | 错误王冠（Glitched Crown） |

::: tip 里该隐可以用 R键串联主线分支
R键能帮助在同一局中补多个主线目标，但贪婪 / 极贪模式仍需另开。见[里该隐](/characters/tainted-cain#cain)的资源管理和路线说明。
:::

在[解锁清单](/tools/tracker)里打开「显示里角色」，可以和表角色一样逐格记录。

<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
