---
title: "小电池与其他电池"
---
# 小电池与其他电池

<VersionBadge checked="2026-10" />

给主动道具补充充能，不等于得到电池类收藏道具。

## 获取与使用

先确认主动的充能方式和是否已满；额外储存、过充由道具决定。

## 操作顺序

1. 先看主动是否需要充能，以及能否储存额外充能；有收益再捡。

## 限制与特殊角色

拾取电池与获得蓄电池、9 伏特等收藏道具不同，不会自动获得它们的被动效果。

## 控制台练习

```text
spawn 5.90.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=battery)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [BatterySubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/BatterySubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
