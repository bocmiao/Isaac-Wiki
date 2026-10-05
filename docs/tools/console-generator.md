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
- 只支持 PC 忏悔 / 忏悔+ 的原版道具（720 件），不含模组道具、饰品、卡牌和胶囊。
- 用了控制台的存档要先在正常局打败过妈妈才能继续拿成就，详见[开启与关闭](/topics/debug-console)。

道具编号来自 [IsaacDocs](https://wofsauge.github.io/IsaacDocs/rep/enums/CollectibleType.html)，中英文名来自 [EID](https://github.com/wofsauge/External-Item-Descriptions)，只收两边都能对上的道具。
