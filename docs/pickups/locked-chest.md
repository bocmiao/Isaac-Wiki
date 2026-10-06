---
title: "金箱子"
---
# 金箱子

<VersionBadge checked="2026-10" />

通常需要钥匙，开后可有拾取物或道具。

## 获取与使用

先留宝箱房钥匙，再比较开箱预算。

## 操作顺序

1. 先留宝箱房或路线钥匙，再决定是否开金箱；打开后继续观察内容。

## 限制与特殊角色

箱子解锁与道具解锁是两层条件，钥匙只解决这次开启。

## 道具来源池参考

固定**忏悔** XML 快照的 `goldenChest` 道具池收录 25 件；以下列出前 12 件供认道具。池内候选不等于一次开箱必出道具，也不是当前忏悔+完整奖池或掉率表。

[皮带](/items/c28)、[妈妈的内裤](/items/c29)、[铁丝衣架](/items/c32)、[25美分](/items/c74)、[宿命](/items/c179)、[魔力八号球](/items/c194)、[挤压玩具](/items/c196)、[螺丝](/items/c255)、[撕碎的照片](/items/c341)、[弹簧锁钥匙](/items/c343)、[火柴盒](/items/c344)、[琥珀爆米花](/items/c354)。

## 控制台练习

```text
spawn 5.60.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=locked-chest)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [ChestSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/ChestSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
