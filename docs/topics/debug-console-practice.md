---
title: 调试控制台：练习示例与排错
description: 道具组合、D6重掷、Boss走位、角色练习与资源生成的控制台示例，含命令恢复和常见错误。
---

# 调试控制台：练习示例与排错

<VersionBadge checked="2026-10" />

::: tip 速览
- **`g` 直接装备道具，地上底座要用 `spawn 5.100.道具编号`**（[常见错误](#errors)）
- **`debug N` 是开关**，同一编号再输一次就是关闭（[常见错误](#errors)）
- **练 Boss 先开 `debug 3` 看招，再关掉练真实走位**（[Boss](#bosses)）
- **练完把 `EnableDebugConsole` 改回 `0` 并重启**（[收尾](#finish)）
- 本页是练习清单；先按[开启与关闭](/topics/debug-console)确认能打开，命令用途和编号查[命令大全与编号](/topics/debug-console-commands)
:::

以下清单针对 PC 忏悔 / 忏悔+，会替换或修改当前局，先保存需要保留的进度并安排专门练习；示例已对照文档与编号表，未在本云环境执行游戏命令。

## 第一次输入：看时间与持有物 {#first}

```text
time
listcollectibles
```

前者输出本局时间，后者列出收藏道具。二者适合确认入口与读取状态。`clear` 清除显示，空输入 Enter 或 Esc 收起窗口。

## 比较道具组合 {#combo}

开新局以撒，再给悲伤洋葱与硫磺火：

```text
restart 0
g c1
g c118
listcollectibles
```

`restart 0` 会替换旧局。`g` 直接装备，`c1` 是悲伤洋葱，`c118` 是硫磺火。

- 先射击观察，再用 `r c118` 移除硫磺火比较变化；移除不保证撤销所有历史效果。
- 想严格比较两套开局，分别重新开局并记录角色、模式与完整道具组合，避免混入之前的 debug 开关。
- 不要一开始就开启高伤害或高幸运，否则看到的不是正常强度。

组合取舍见[道具攻略](/strategy/items)。

## D6：练习重掷地上道具 {#d6}

```text
restart 0
g c105
spawn 5.100.1
debug 8
```

`c105` 是 D6；`spawn 5.100.1` 在地上生成悲伤洋葱底座。关闭控制台后使用主动，观察重掷；`debug 8` 让主动保持满充能，适合连续测试。练完再次输入 `debug 8` 关闭。

直接 `g c1` 给的是**已经装备的道具**，不会给 D6 一个地上底座。底座重掷结果还受房间道具池、解锁、种子与版本影响，不保证每次出现同一道具。相关表角色思路见[以撒攻略](/strategy/characters#isaac)。

## 补资源与观察血量机制 {#pickups}

以下每条在地上生成一个拾取物，仍需角色走过去拾取：

```text
spawn 5.10.1
spawn 5.10.3
spawn 5.20.1
spawn 5.30.1
spawn 5.40.1
```

依次是整颗红心、魂心、1 分硬币、普通钥匙、普通炸弹。心类型见 [HeartSubType](https://wofsauge.github.io/IsaacDocs/rep/enums/HeartSubType.html)。红心不会无条件增加上限；游魂、店主、伯大尼等按自己的机制处理拾取物，不能用普通角色规则解释，见[角色速查](/strategy/character-roster)。

若要生成四枚硬币，先 `spawn 5.20.1`，再 `repeat 3`；后者是**额外三次**，不是总计三次。练习数量保持少量即可。

## Boss：先看招式，再练真实走位 {#bosses}

### 练妈妈

```text
restart 0
stage 6
g k5
```

`stage 6` 到深牢 II，`k5` 是皇帝卡；收起控制台并使用卡牌到 Boss 房。想先观察攻击，可输入一次 `debug 3` 开无限生命；它可能仍触发受伤反馈，不代表所有特殊死亡都被禁止。

观察完，结束这一轮并新开同样练习，保持 `debug 3` 关闭、不要开 `debug 4` 或 `debug 10`，再测真实伤害与走位。`macro mom` 会给圣经与高伤害等配置，适合快速测试，不能直接衡量普通开局难度。

### 练死寂

```text
restart 0
g c1
stage 9
g k5
```

进入死寂所在的蓝子宫层，再使用皇帝卡。这里通过控制台跳过限时与路线前置；正常局仍按[Boss 攻略](/strategy/bosses)满足入口条件。伤害配置可自行调整，但记录清楚比较时用了什么。

### 练祸兽

```text
restart 0
stage 13
goto x.itemdungeon.666
```

这是公开 `macro beast` 中的跳层与战斗房命令。这里去掉其随机道具组合，方便自己安排装备；不会替你演练上行、拿爸爸的便条或 Dogma 的完整路线。需要快速测试整套预设可用 `macro beast`，但随机装备不适合比较角色强度。

## 练角色与双人机制 {#characters}

- `restart 10`：以游魂开新局。
- `restart 31`：以里游魂开新局。
- `restart 19`：以雅各与以扫开新局；`g c1` 给主角色，`g2 c1` 给次角色。

这些入口不替代正常角色解锁，也不保证你的存档已经具有 D6、神圣斗篷等永久初始强化。先核对[角色速查](/strategy/character-roster)里的强化前置，再解释开局差异。游魂与里游魂不是同一机制，隐藏角色正常获取见[角色解锁](/guide/unlocks/order)。

想练贪婪 / 极贪模式，先在菜单选正确模式再进入对局；`macro ug` 的旧开发布局并不是切换模式的等价方法。模式与标记见[贪婪攻略](/strategy/greed)。

## 模组排错：先读取，再修改 {#mods}

```text
lua print("Hello World!")
luamem
```

第一条只输出文字，第二条读取 Lua 内存。查模组资源时可按情况用 `clearcache`、`reloadshaders`；重跑代码的 `luamod 文件夹名` 可能重复注册回调，完整重启游戏通常更适合普通玩家确认加载状态。

不要把工坊标题直接当作文件夹名。模组安装、配置菜单与冲突排查见[配置与实用模组](/topics/mods)。

## 常见错误与恢复 {#errors}

| 问题 | 原因 / 处理 |
| --- | --- |
| 想要卡牌却得到道具 | `c` 是收藏道具，卡牌 / 符文用 `k`；胶囊效果用 `p` |
| 发道具后地上没有底座 | `g` 直接装备；用 `spawn 5.100.道具编号` 生成底座 |
| `repeat` 数量超出预期 | 参数是额外执行次数，算上第一次 |
| Boss 不受正常伤害或很快死亡 | 检查 `debug 4` / `debug 10`；同一编号再次输入是关闭，不是重设 |
| 无限生命突然消失 | 可能重复输入 `debug 3` 或运行含同一开关的宏，导致切回关闭 |
| 换层仍有之前装备 | `stage` 不等于新开局；需要从头用 `restart` |
| 房间不存在或传送失败 | 布局随层、版本和模组不同；核对特殊房类型、布局、维度，不用随机大编号 |
| 减去道具仍不回到原样 | `remove` 不是撤销历史；重新建立练习局，不用反复移除猜测 |
| 用 `clear` 后能力还在 | 只清屏。debug 同号切换，其他效果视情况移除或新开局 |
| 练习后角色 / 标记多了 | 满足前置的普通局可能正常写入解锁；结束局不会回退永久进度。恢复只能依赖预先备份，不用 `rewind` 代替存档恢复 |

## 练完怎么收尾 {#finish}

记下用过的 debug 编号并逐项关闭，结束练习局。准备恢复普通游玩或每日挑战时，完全退出游戏，把 `EnableDebugConsole` 改回 `0` 后重启；每日挑战还要关闭模组。隐藏窗口和清屏都不能代替这些步骤。

完整用途、编号与版本差异见[命令大全](/topics/debug-console-commands)。本页例子对应 [Debug Console](https://bindingofisaacrebirth.wiki.gg/wiki/Debug_Console)、[IsaacDocs](https://wofsauge.github.io/IsaacDocs/rep/tutorials/DebugConsole.html)及其枚举资料，核对日期 2026-10-05。
