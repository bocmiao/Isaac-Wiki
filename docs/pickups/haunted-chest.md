---
title: "鬼箱子"
---
# 鬼箱子

<VersionBadge checked="2026-10" />

靠近时可能遭遇幽灵敌人的攻击。

## 获取与使用

辨认后保持移动，先处理敌人，再考虑内容。

## 操作顺序

1. 先观察靠近时出现的敌人并留移动路线，再处理箱子内容。

## 限制与特殊角色

名称像宝箱不等于可以安全站桩；不要在低血时忽略幽灵攻击。

## 永久解锁

先满足[成就 #611](/achievements/ids-601-641#achievement-611)；解锁后才可能在对应来源生成，不保证这一局掉落。

## 控制台练习

```text
spawn 5.58.1
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=haunted-chest)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [ChestSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/ChestSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
