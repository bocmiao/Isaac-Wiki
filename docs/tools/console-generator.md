---
title: 控制台命令生成器
---

# 控制台命令生成器

<VersionBadge checked="2026-10" />

选好要做的事，生成可以直接粘贴进游戏控制台的命令，可以攒成多行一起复制。只生成文字，不会连接或操作你的游戏。

还没开控制台先看[开启与关闭](/topics/debug-console)；每条命令什么意思见[命令大全](/topics/debug-console-commands)。

<ConsoleGenerator />

## 注意 {#编号来源与使用范围}

- 「直接给道具」（`g c编号`）是直接进身上；「生成地上道具底座」（`spawn 5.100.编号`）是在房间里放一个可以捡的。给主动道具会顶掉你原来那一格。
- 「指定角色开新局」会直接替换当前这一局，也不会永久解锁这个角色。
- `debug 编号` 是开关：同一个编号再执行一次就关掉。
- 支持原版道具 `c`、饰品 `t`、卡牌 / 符文 `k`、胶囊效果 `p`，以及已核对的 29 类资源 / 宝箱实体，不为模组自定义编号生成命令。
- 移除只提供道具、饰品；给次角色只提供收藏道具。胶囊效果 ID 不等于地上胶囊颜色 ID，金胶囊占位 `p9999` 不输出。
- 「生成资源 / 宝箱」是放置地上实体，不是增加库存或完成永久解锁；即爆炸弹会爆炸，金电池有伤害风险。
- 用了控制台的存档要先在正常局打败过妈妈才能继续拿成就，详见[开启与关闭](/topics/debug-console)。

道具与拾取物编号来自 [IsaacDocs](https://wofsauge.github.io/IsaacDocs/rep/enums/CollectibleType.html)，中英文名来自 [EID](https://github.com/wofsauge/External-Item-Descriptions)。资源子类型另固定核对 `PickupVariant`、心 / 硬币 / 钥匙 / 炸弹 / 电池子类型表；从[拾取物页面](/pickups/)可直接打开对应生成器。
