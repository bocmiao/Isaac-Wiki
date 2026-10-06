---
title: "金硬币"
---
# 金硬币

<VersionBadge checked="2026-10" />

拾取后可重新出现在附近，直到这一枚的连续奖励结束。

## 获取与使用

先清场再追硬币，可能出现在地形危险处；不承诺可无限捡。

## 操作顺序

1. 清掉敌人后再连续追捡，注意新的出现位置是否靠近尖刺或坑。

## 限制与特殊角色

会继续出现不等于无限硬币；生命危险时先停止追钱。

## 永久解锁

先满足[成就 #613](/achievements/ids-601-641#achievement-613)；解锁后才可能在对应来源生成，不保证这一局掉落。

## 控制台练习

```text
spawn 5.20.7
```

只生成地上实体，不会证明自然获取、永久解锁或收藏条件已经满足。 [打开命令生成器](/tools/console-generator?pickup=golden-penny)，开启控制台见[控制台教程](/topics/debug-console)。

编号对照 [PickupVariant](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/PickupVariant.md) 与 [CoinSubType](https://github.com/wofsauge/IsaacDocs/blob/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/docs/enums/CoinSubType.md)；枚举不证明开启成本与掉率。

## 相关机制与来源

[资源与生命](/guide/first-win/pickups) · [机器与乞丐](/strategy/machines) · [拾取物总览](/pickups/) · [成就索引](/achievements/)。

解锁条件关联本站固定成就快照，生命与资源行为沿用对应指南。池表来自固定 [IsaacDocs XML](https://github.com/wofsauge/IsaacDocs/tree/e05b1fd90e33608a7a7a8dcb70a89cef908cc41a/scripts/data)，不把忏悔池表声明为当前忏悔+实测。使用取舍属于本站建议；不补未核实的完整奖池、掉率或伤害例外。
