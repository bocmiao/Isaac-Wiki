---
title: "充能钥匙"
---
# 充能钥匙

<VersionBadge checked="2026-10" />

提供钥匙资源，也能给主动道具充能。

## 获取与使用

主动已经满充时，先考虑使用后再拾取，避免充能收益浪费。

## 操作顺序

1. 主动已满时，若本来就要使用可先用再捡，让钥匙和充能都产生收益。

## 限制与特殊角色

没有合适主动或已经满充时，不把充能收益重复算一次。

## 永久解锁

先满足[成就 #333](/achievements/ids-301-400#achievement-333)；解锁后才可能在对应来源生成，不保证这一局掉落。

## 控制台练习

```text
spawn 5.30.4
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=charged-key)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [KeySubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/KeySubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
