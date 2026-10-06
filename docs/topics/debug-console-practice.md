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

以下清单针对 PC 忏悔 / 忏悔+。这些命令会替换或修改当前这一局，练习前先保存需要保留的进度，专门开练习局来用。

## 第一次输入：看时间与持有物 {#first}

```text
time
listcollectibles
```

`time` 显示本局时间，`listcollectibles` 列出身上的道具。这两条不改游戏，适合确认控制台能用、查看当前状态。`clear` 清屏；输入框为空时按 Enter，或按 Esc，收起窗口。

## 比较道具组合 {#combo}

用以撒开一局新游戏，再给他悲伤洋葱（The Sad Onion）和硫磺火（Brimstone）：

```text
restart 0
g c1
g c118
listcollectibles
```

`restart 0` 会替换旧局。`g` 直接装备，`c1` 是悲伤洋葱，`c118` 是硫磺火。

- 先射击观察，再用 `r c118` 移除硫磺火，比较前后变化。注意移除道具不一定能撤销它已经造成的所有效果。
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

- `c105` 是 D6。
- `spawn 5.100.1` 在地上生成一个放着悲伤洋葱的底座。
- `debug 8` 让主动道具一直满充能，可以连续测试。

收起控制台后用 D6，观察底座上的道具怎么变。练完再输一次 `debug 8` 关掉。

直接 `g c1` 给的是**已经装备的道具**，地上不会有底座给 D6 重掷。重掷出什么，受房间道具池、解锁情况、种子与版本影响，不会每次都一样。相关角色思路见[以撒攻略](/characters/isaac#isaac)。

## 补资源与观察血量机制 {#pickups}

下面每条命令在地上生成一个拾取物，角色要自己走过去捡：

```text
spawn 5.10.1
spawn 5.10.3
spawn 5.20.1
spawn 5.30.1
spawn 5.40.1
```

依次是整颗红心、魂心（蓝色的心，见[拾取物](/guide/first-win/pickups)）、1 分硬币、普通钥匙、普通炸弹。其他心的编号见 [HeartSubType](https://wofsauge.github.io/IsaacDocs/rep/enums/HeartSubType.html)。

- 捡红心不会无条件增加红心上限。
- 游魂、店主、伯大尼等角色对拾取物有自己的规则，不能按普通角色理解，见[角色速查](/strategy/character-roster)。

要生成 4 枚硬币：先 `spawn 5.20.1`，再 `repeat 3`。`repeat 3` 是**再额外执行 3 次**，不是总共 3 次。练习时少生成一点就够了。

## Boss：先看招式，再练真实走位 {#bosses}

### 练妈妈

```text
restart 0
stage 6
g k5
```

`stage 6` 跳到深处 II，`k5` 是卡牌 IV-皇帝（IV - The Emperor）。收起控制台后用这张卡，直接去 Boss 房。

想先观察妈妈的攻击，可以输一次 `debug 3` 开无限生命。开了以后被打中仍可能有受伤反馈，某些特殊的死亡方式也不一定能挡住。

看完招式，结束这一局，按同样步骤重开。这次不开 `debug 3`，也不开 `debug 4` 或 `debug 10`，练真实的伤害和走位。

`macro mom` 会给圣经（The Bible）、高伤害等配置，适合快速测试，但用它打不出普通开局的真实难度。

### 练死寂

```text
restart 0
g c1
stage 9
g k5
```

`stage 9` 进入死寂所在的蓝子宫层，再用皇帝卡去 Boss 房。用控制台可以跳过正常局里的时间限制和路线要求；正常局要先满足入口条件，见[Boss 攻略](/strategy/bosses)。伤害配置可以自己调整，但要记清楚比较时用了哪些道具。

### 练祸兽

```text
restart 0
stage 13
goto x.itemdungeon.666
```

这两条取自 `macro beast` 宏里的跳层和进战斗房命令，去掉了宏里随机给的道具，方便自己安排装备。它直接进祸兽战，不会带你走完整路线（上行、拿爸爸的便条、打 Dogma）。

想快速测试整套预设，可以直接用 `macro beast`。但它给的装备是随机的，不适合拿来比较角色强度。

## 练角色与双人机制 {#characters}

- `restart 10`：以游魂开新局。
- `restart 31`：以里游魂开新局。
- `restart 19`：以雅各与以扫开新局；`g c1` 给主角色，`g2 c1` 给次角色。

用 `restart` 换角色，不等于在存档里解锁了这个角色。D6、神圣屏障（Holy Mantle）这类永久初始强化，存档里没解锁的话，这样开局也不会有。开局装备和别人不一样时，先查[角色速查](/strategy/character-roster)里这些强化的解锁条件。

游魂和里游魂的机制不一样。隐藏角色的正常解锁方法见[角色解锁](/guide/unlocks/order)。

想练贪婪 / 极贪模式，要先在菜单里选好模式再进对局。`macro ug` 只是旧的开发用布局，不能代替切换模式。模式与标记见[贪婪攻略](/strategy/greed)。

## 模组排错：先读取，再修改 {#mods}

```text
lua print("Hello World!")
luamem
```

第一条只输出一行文字，第二条读取 Lua 内存。

- 查模组资源问题时，可以按情况用 `clearcache`、`reloadshaders`。
- `luamod 文件夹名` 会重跑模组代码，但可能重复注册回调（同一段代码被触发两次）。普通玩家想确认模组有没有加载好，完整重启游戏更稳。

不要把工坊标题直接当作文件夹名。模组安装、配置菜单与冲突排查见[配置与实用模组](/topics/mods)。

## 常见错误与恢复 {#errors}

| 问题 | 原因 / 处理 |
| --- | --- |
| 想要卡牌却得到道具 | `c` 是收藏道具，卡牌 / 符文用 `k`；胶囊效果用 `p` |
| 发道具后地上没有底座 | `g` 直接装备；用 `spawn 5.100.道具编号` 生成底座 |
| `repeat` 数量超出预期 | 参数是额外执行的次数，总数要再加上第一次 |
| Boss 不受正常伤害或很快死亡 | 检查 `debug 4` / `debug 10`；同一编号再次输入是关闭，不是重设 |
| 无限生命突然消失 | 可能重复输入 `debug 3` 或运行含同一开关的宏，导致切回关闭 |
| 换层仍有之前装备 | `stage` 不等于新开局；需要从头用 `restart` |
| 房间不存在或传送失败 | 布局随层、版本和模组不同；核对特殊房类型、布局、维度，不用随机大编号 |
| 减去道具仍不回到原样 | `remove` 不是撤销历史；重新建立练习局，不用反复移除猜测 |
| 用 `clear` 后能力还在 | `clear` 只清屏。debug 开关要再输一次同号关掉；其他效果用 `r` 移除或新开局 |
| 练习后角色 / 标记多了 | 打败过妈妈的存档，练习局也可能正常写入解锁，结束这局不会撤回。只能用事先的备份恢复，`rewind` 代替不了 |

## 练完怎么收尾 {#finish}

1. 记下用过的 debug 编号，逐个关掉，结束练习局。
2. 要回到普通游玩或打每日挑战：完全退出游戏，把 `EnableDebugConsole` 改回 `0`，再重启。
3. 打每日挑战还要关掉模组。

隐藏窗口和清屏都代替不了这些步骤。

完整用途、编号与版本差异见[命令大全](/topics/debug-console-commands)。本页例子对应 [Debug Console](https://bindingofisaacrebirth.wiki.gg/wiki/Debug_Console)、[IsaacDocs](https://wofsauge.github.io/IsaacDocs/rep/tutorials/DebugConsole.html)及其枚举资料，核对日期 2026-10-05。示例只对照了文档与编号表，没有在游戏里实际执行。
