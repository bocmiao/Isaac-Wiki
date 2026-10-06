---
title: "木箱子"
---
# 木箱子

<VersionBadge checked="2026-10" />

独立箱子类型，开放后可在正常掉落中出现。

## 获取与使用

先清场再开，具体内容以实际生成结果为准。

## 操作顺序

1. 先核对永久解锁，清场后再接近；按实际出现内容选择。

## 限制与特殊角色

正常生成机会不等于每局必出现，也不能据箱子名称保证掉某一件道具。

## 永久解锁

先满足[成就 #609](/achievements/ids-601-641#achievement-609)；解锁后才可能在对应来源生成，不保证这一局掉落。

## 道具来源池参考

固定**忏悔** XML 快照的 `woodenChest` 道具池收录 11 件；以下列出前 11 件供认道具。池内候选不等于一次开箱必出道具，也不是当前忏悔+完整奖池或掉率表。

[殉道者之血](/items/c7)、[木头勺子](/items/c27)、[梯子](/items/c60)、[圣痕](/items/c138)、[牙签](/items/c183)、[木制镍币](/items/c349)、[小箱子](/items/c362)、[妈妈的盒子](/items/c439)、[节拍器](/items/c488)、[自我先生！](/items/c527)、[店主的盒子](/items/c719)。

## 控制台练习

```text
spawn 5.56.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=wooden-chest)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [ChestSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/ChestSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
