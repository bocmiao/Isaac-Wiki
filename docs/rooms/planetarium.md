---
title: "星象房"
description: "星象房的进入条件、奖励、风险、打法和路线出口。"
prev: {"text": "黑市", "link": "/rooms/black-market"}
next: {"text": "Boss Rush", "link": "/rooms/boss-rush"}
---
# 星象房 {#planetarium}

<EntryHeader en="Planetarium" category="特殊奖励" icon="eye" />

<VersionBadge checked="2026-10" />

## 解锁

一局取得 3 件带 `stars` 标签的道具，例如星座道具、魔力八号球、水晶球，解锁[成就 406](/achievements/ids-401-500#achievement-406)。解锁后才会正常参与生成，不代表之后每层都有。

## 进入与收益

星月标记，通常 1 钥匙，提供星象房池道具。正常生成范围和道具修改有关；望远镜片等可扩展范围，魔力八号球、水晶球等能提高机会。

## 发育思路

完全跳过宝箱房可以提高之后生成机会。普通主线没有必要为了赌星象房连续放弃眼前的稳定提升；祸兽路线可以计划上行时再拿跳过的宝箱房。进门看完道具再走不算跳过。要查某件星象房道具效果，用[道具速查](/tools/items)。

## 生成规则与概率参考

基础机会为 1%；第一次进入星象房之前，跳过宝箱房通常为后续机会增加 20 个百分点。进宝箱房看了再走不算跳过，已经拿走道具也不能撤回“进入过”的记录。进入一次星象房后，跳房累积加成不再按首次规则保留；不能把先前显示的高概率一直带到后续楼层。

| 因素 | 概率变化 | 范围与例外 |
| --- | --- | --- |
| 魔力八号球 | +15 个百分点 | 各阶段适用看首次进入规则，不把持有复制品自动相加 |
| 水晶球 | +15 个百分点；满足跳过宝箱房的条件时可达到 100% | 有机会不等于当前楼层具备生成资格 |
| 腊肠 | +6.9 个百分点 | 交易房加成和星象房加成分别计算 |
| 望远镜片 | 基础 +9；首次进入前额外 +15 | 通常可扩展至子宫 / 尸宫；金色和妈妈的盒子差异见[饰品页](/items/t152) |
| 楼层与模式 | 普通范围主要是前三章；贪婪不按这套生成 | 替代路线内部层号、特殊挑战和模组可改变判断 |

例如首次星象房前，基础 1% 加一次有效跳房通常是 21%，再有魔力八号球通常为 36%；仍须本层允许生成。资料交叉核对 [REPENTOGON 的忏悔实现参考](https://github.com/TeamREPENTOGON/REPENTOGON/blob/bc881d424ba31183cd9cb3def3446af0fc5733c2/repentogon/Patches/CustomDevilPlanetariumChance.cpp)与 EID。这份实现参考属于忏悔；忏悔+ 的特殊路线与模组例外仍需另行核实。

## 同类条目

[干净卧室](/rooms/clean-bedroom) · [肮脏卧室](/rooms/dirty-bedroom) · [夹层](/rooms/crawlspace) · [黑市](/rooms/black-market)

[返回房间图鉴](/rooms/) · [路线与结局](/guide/unlocks/endings) · [机制详解](/strategy/mechanics)

## 资料来源

::: details 查看出处
房间与楼层规则见路线、机制和角色解锁教程；分类参考 [IsaacDocs](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums)。具体数值见[机制详解](/strategy/mechanics)及[成就条件](/achievements/)。
:::
