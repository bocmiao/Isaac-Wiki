---
title: "普通硬币与高面额硬币"
---
# 普通硬币与高面额硬币

<VersionBadge checked="2026-10" />

普通硬币 1 枚，镍币 5 枚，铸币 10 枚。

## 获取与使用

先留开门、钥匙或治疗的钱；道具可修改硬币上限。

## 操作顺序

1. 先留商店、钥匙、治疗和路线门票；高面额硬币按其面值计入库存。

## 限制与特殊角色

基础上限 99；深口袋可把硬币上限提高到 999。店主还可能需要硬币治疗。

## 控制台练习

```text
spawn 5.20.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=coin)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [CoinSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/CoinSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
