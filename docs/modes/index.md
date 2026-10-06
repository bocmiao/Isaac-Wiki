---
title: 全部模式与玩法
description: 普通、困难、贪婪、极贪、编号挑战、每日挑战、种子局、胜利圈、重跑和合作玩法的入口、规则与奖励。
aside: false
---
<script setup>
import entries from '../.vitepress/theme/data/catalog/modes.json'
</script>

# 全部模式与玩法

<VersionBadge checked="2026-10" />

选角色时的基础难度有 **Normal、Hard、Greed、Greedier** 四种。编号挑战、每日挑战与种子局是特殊开局，胜利圈与重跑是通关后的延续玩法；本地合作、在线合作则是在相应模式上多人游玩。下面分别讲清进入方式、前置、规则、奖励和打法。

## 先选要做的事

| 目标 | 推荐入口 | 进度限制 |
| --- | --- | --- |
| 第一次打妈妈、学清房 | [普通模式](/modes/normal) | 可以推进正常解锁；一般不补困难红标记 |
| 全角色困难标记、冲白金神 | [困难模式](/modes/hard) | 困难完成覆盖同目标的普通完成 |
| 解锁店主、极贪、游魂神圣屏障 | [贪婪](/modes/greed) / [极贪](/modes/greedier) | 看贪婪捐款机，与普通捐款机分开 |
| 解锁挑战奖励 | [编号挑战](/modes/challenges) · [45 篇攻略](/challenges/) | 只能解锁所选挑战的完成奖励 |
| 每日参与、胜利和连胜成就 | [每日挑战](/modes/daily) | 正式每日计数，练习局不计 |
| 重复练一张图、试道具 | [种子局](/modes/seeded) · [练习与控制台](/modes/practice) | 手动指定普通种子不解锁普通成就 |
| 保留道具搭配再跑一圈 | [胜利圈](/modes/victory-lap) / [RERUN](/modes/rerun) | 离线不能用于普通成就、角色标记 |
| 和朋友一起玩 | [本地合作](/modes/local-coop) / [在线合作](/modes/online-coop) | 要区分完整角色、宝宝及中途加入 |
| 玩创意工坊的特殊规则 | [自定义挑战与模组局](/modes/custom-challenges) | 模组挑战不等于官方 45 项奖励 |

“可以解锁”还要求当前局没有种子、特殊模式等禁成就限制。每日、胜利圈和编号挑战各自的专属奖励不能互相替代。进度以游戏的成就、标记与奖杯结果为准。

## 按玩法查看

<EntryCatalog :entries="entries" label="模式与玩法" />

## 怎么对照自己还缺什么

先查[各模式能解锁什么与失败排查](/modes/unlock-rules)，确定应在哪种局完成；贪婪相关具体奖励见[34 个角色奖励对照](/modes/greed-rewards)。

[本地存档进度对照](/tools/local-progress) 可读取 Windows Steam 忏悔+ 的成就、角色标记、挑战完成与捐款记录。网页手动清单见[全成就打勾](/achievements/#catalog)、[挑战清单](/tools/challenges)和[捐款机进度](/tools/donations)。

## 资料来源

基础难度分类对照 [IsaacDocs Difficulty 枚举](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/Difficulty.md)。其余规则沿用本站[挑战攻略](/strategy/challenges)、[贪婪机制](/strategy/greed)、[种子](/strategy/seeds)、[特殊成就教程](/achievements/special)和[联机专题](/topics/coop)。各独立页注明相应来源与版本范围。
