---
title: "表角色攻略"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/characters.json"
const entries = (allEntries as CatalogEntry[]).filter(entry => entry.group === "表角色")
</script>

# 表角色攻略

<VersionBadge checked="2026-10" />

每个角色都有独立页，包含开局、获取方式、核心机制、分阶段发育、清房与 Boss 操作、路线与标记建议。表角色与对应里角色互相链接。

## 按名称与类型查找 {#catalog}

<EntryCatalog :entries="entries" label="人物图鉴" legacy />

## 解锁与练习

- [角色解锁步骤](/guide/unlocks/order) · [全部里角色获取方式](/guide/unlocks/order#tainted-list)
- [开局强化](/strategy/character-roster#upgrades) · [完成标记与全角色奖励](/strategy/completion-marks)
- [新手练习建议](/strategy/characters#新手先练哪个) · [角色解锁清单](/tools/tracker)

## 总表

原来的角色总表已整理为上方卡片；点击名字进入完整独立攻略。

## 逐个角色

各角色的发育、打法与路线段落完整保留在独立页中。

## 新手先练哪个

按客观条件排：

1. **[以撒](/characters/isaac#isaac)**：唯一初始可用，3 个红心容器，没有特殊规则。
2. **[抹大拉](/characters/magdalene#magdalene)**：4 个红心容器，美味的心能自己回血；注意移速慢。
3. **[参孙](/characters/samson#samson)**、**[拉撒路](/characters/lazarus#lazarus)**：3 个红心容器、正常射击。拉撒路每层多一条命。
4. **[该隐](/characters/cain#cain)**、**[夏娃](/characters/eve#eve)**、**[亚玻伦](/characters/apollyon#apollyon)**（2 个红心容器）、**[犹大](/characters/judas#judas)**（1 个）：血少，能稳定躲弹幕后再用。
5. **[阿撒泻勒](/characters/azazel#azazel)**、**[???](/characters/bluebaby#bluebaby)**、**[伯大尼](/characters/bethany#bethany)**：攻击方式或血量规则不同。
6. **[游魂](/characters/lost#lost)**（一碰就死）、**[店主](/characters/keeper#keeper)**（刚解锁时最弱）、**[莉莉丝](/characters/lilith#lilith)**（不能自己射）、**[遗骸](/characters/forgotten#forgotten)**、**[雅各和以扫](/characters/jacob#jacob)**（一方死亡整局结束）、**[伊甸](/characters/eden#eden)**（随机且耗币）。

::: tip 先给以撒拿六面骰
解锁 ??? 以后，用他打一次以撒（Boss），以撒就会开局自带六面骰。
:::

::: warning 店主和游魂先做开局解锁
店主先打以撒（Boss）拿木制镍币，再打死寂拿第 3 个硬币心。游魂先往贪婪捐款机捐满 879 枚硬币拿神圣屏障，否则任何一次伤害都会结束这一局。
:::


<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
