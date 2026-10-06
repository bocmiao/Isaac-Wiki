---
title: "金钥匙"
---
# 金钥匙

<VersionBadge checked="2026-10" />

当层普通用钥匙时不扣库存，换层不保留该层效果。

## 获取与使用

当层优先开需要的锁，特殊机器的互动另看其规则。

## 操作顺序

1. 当层把原本就需要的锁打开，换层前完成重要开门事项。

## 限制与特殊角色

效果按层消失；乞丐或特殊互动另有规则，不能一概按无限投喂计算。

## 控制台练习

```text
spawn 5.30.2
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=golden-key)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [KeySubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/KeySubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
