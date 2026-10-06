---
title: "旧箱子"
---
# 旧箱子

<VersionBadge checked="2026-10" />

特殊箱子，有自己的奖励来源。

## 获取与使用

与普通金箱子奖池分开看；不把某一件道具当成必出。

## 操作顺序

1. 先清场并观察实际开启状态；如果产生道具，按其效果决定是否拿。

## 限制与特殊角色

这是旧箱子的独立来源池，不能把妈妈箱子、金箱子和旧箱子视为同一个奖池。

## 道具来源池参考

固定**忏悔** XML 快照的 `oldChest` 道具池收录 25 件；以下列出前 12 件供认道具。池内候选不等于一次开箱必出道具，也不是当前忏悔+完整奖池或掉率表。

[妈妈的内裤](/items/c29)、[妈妈的高跟鞋](/items/c30)、[妈妈的口红](/items/c31)、[妈妈的胸罩](/items/c39)、[妈妈的卫生巾](/items/c41)、[妈妈的眼睛](/items/c55)、[妈妈的药瓶](/items/c102)、[妈妈的美瞳](/items/c110)、[妈妈的菜刀](/items/c114)、[妈妈的钱包](/items/c139)、[爸爸的钥匙](/items/c175)、[妈妈的零钱包](/items/c195)。

## 控制台练习

```text
spawn 5.55.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=old-chest)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [ChestSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/ChestSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
