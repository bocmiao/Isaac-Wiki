---
title: 调试控制台：开启与关闭
description: 忏悔与忏悔+调试控制台开启方法、配置文件路径、按键、成就与每日挑战限制及常见问题。
---

# 调试控制台：开启与关闭

<VersionBadge checked="2026-10" />

::: tip 速览
- **忏悔 / 忏悔+ 在 `options.ini` 设 `EnableDebugConsole=1`**，不用装模组（[版本](#versions)）
- **先进入一局，美式键盘按 Esc 下方的反引号键打开**，输入法先切英文（[基本操作](#controls)）
- **前置未满足时开控制台会阻止解锁**，先在正常局击败妈妈（[成就](#achievements)）
- **关闭要改回 `0` 并重启**，收起窗口或 `clear` 都不算（[关闭](#disable)）
- 本系列分三页，本页讲开启与关闭；命令和编号见[命令大全与编号](/topics/debug-console-commands)，练习清单见[练习示例与排错](/topics/debug-console-practice)，工坊模组见[配置与实用模组](/topics/mods)
:::

这里说的是 PC 游戏内的 Debug Console（Switch、PlayStation、Xbox 等见[主机专题](/topics/console)），能发道具、生成敌人、切楼层、换角色，也能检查房间和运行模组代码，适合练 Boss、比较道具组合和排查模组。它会直接改变游戏状态，练习前先结束想保留的正常局，重要存档先备份。

## 哪个版本能用 {#versions}

| 版本 | 开启方法 |
| --- | --- |
| 重生 / 胎衣 | 没有胎衣+之后开放给玩家的调试控制台，不能照搬下方方法 |
| 胎衣+（Afterbirth+） | 启用至少一个模组；不需要专门安装“开启控制台”模组 |
| 忏悔（Repentance） / 忏悔+（Repentance+） | 在对应版本的 `options.ini` 设置 `EnableDebugConsole=1`；开启本身不要求装模组 |
| 主机版 | 不提供这里的调试控制台 |

命令表以忏悔 / 忏悔+ 为主，旧版、失效和未列出的命令另有标注。REPENTOGON 或其他模组可能扩展命令，本系列不把扩展功能当作原版功能。

## Windows 开启步骤 {#enable}

1. 先启动目标版本一次，再完全退出游戏，避免游戏退出时覆盖手工修改。
2. 按 <KeyCap>Win</KeyCap> + <KeyCap>R</KeyCap>，输入 `%USERPROFILE%\Documents\My Games` 打开目录。如果“文档”迁移到 OneDrive 等位置，请到实际文档目录下找 `My Games`。
3. 忏悔进入 `Binding of Isaac Repentance`；忏悔+进入 `Binding of Isaac Repentance+`，打开其中的 `options.ini`。不要修改游戏安装目录里同名但不生效的文件。
4. 用文本编辑器搜索 `EnableDebugConsole`，将这一行改为下方内容并保存：

```ini
EnableDebugConsole=1
```

5. 启动游戏、选择存档、**进入一局**。在英文美式键盘布局下，按 Esc 下方的反引号 / 波浪号键打开控制台。输入 `time` 后按 Enter；能看到本局时间就说明入口正常。

忏悔与忏悔+各有配置与存档目录，改其中一份不会自动开启另一份。找不到文件时，先核对实际启动的 DLC 与版本，而不是到处复制配置。

### Linux、Steam Deck 与 macOS {#paths}

| 运行方式 | 去哪里找 |
| --- | --- |
| Linux 原生胎衣+ | `~/.local/share/binding of isaac afterbirth+/options.ini`；原生版仍按胎衣+的模组开启规则 |
| Linux / Steam Deck 经 Proton 运行 | 对应 Steam 库的 `steamapps/compatdata/250900/pfx/drive_c/users/steamuser/Documents/My Games/`，再进入目标版本目录 |
| macOS 原生版 | 公开文档列出 `~/Library/Application Support/Binding of Isaac Rebirth`；原生版本支持范围与 Windows 不同，不因存在此目录就认定能运行忏悔 / 忏悔+ |

Proton 路径随 Steam 库、安装盘而变；Steam Deck 若没有方便的输入方式，可接键盘。不要把 Windows 的固定盘符套用到这些环境。

## 基本操作 {#controls}

- 命令输入后按 Enter 执行；上方向键回到上一条命令，下方向键清空输入行。
- 输入框留空时按 Enter，或按 Esc，收起控制台。
- 中文输入法先切到英文。开启键取决于**键盘布局**：美式是反引号，英式常为 `'` / `@`，德式为 `ö`，法式为 `ù`。不是所有键盘都认同一个物理键。
- 可粘贴多行命令，但会依次执行。先逐条理解效果，再复制练习清单；不要把文字说明和注释也一起粘进去。
- `clear` 只清屏；收起窗口只隐藏界面。二者都不会关闭控制台、撤销命令或恢复正常局。

## 如何关闭与恢复正常游玩 {#disable}

忏悔 / 忏悔+：完全退出游戏，在同一份 `options.ini` 改为 `EnableDebugConsole=0`，保存后重启。胎衣+：关闭启用的模组并重启。要参加每日挑战，也要关闭模组。

调试状态中 `debug N` 的编号是**开关**，同一局再次输入相同编号可关闭；不知道开过哪些时，结束练习并开新局更容易确认。新局不会撤销已经写入存档的永久解锁；也不会自动恢复被 `restart`、`seed` 或 `challenge` 替换的旧局。

## 成就、解锁与存档 {#achievements}

- 新存档尚未满足前置时，开启控制台会阻止正常解锁。先在**不开模组、不开控制台、非手动种子**的正常局击败妈妈，再开始练习。首次击败妈妈前置的精确跨栏位作用域在公开资料中有不同表述，换栏位或版本时应确认目标进度。
- 满足前置后，普通局中启用控制台并不一概禁用成就。**练习也可能留下完成标记或解锁**，不是自动隔离的沙盒；想保留正常进度路线，应先备份或使用专门练习档，并确认其前置与本局状态。
- 每日挑战要求关闭控制台和模组；仅收起窗口没有用。手动普通种子、挑战、胜利圈等另有规则，见[成就排查](/guide/start/chinese#成就为什么不解锁)。
- 钥匙数量下方划掉的奖杯是本局无法正常解锁的重要提示。没有该图标也不替你满足具体成就条件。
- `achievement` 是胎衣+旧命令，忏悔已不提供这个旧入口。不要把旧教程的“一键全成就”当成正常角色获取方法；角色实际条件见[角色解锁顺序](/guide/unlocks/order)。

## 开不了时逐项查 {#troubleshooting}

| 现象 | 排查方法 |
| --- | --- |
| 改了文件仍打不开 | 游戏是否关闭后再编辑？是否保存成功？是否改了正在运行版本的目录？ |
| 配置没有生成 | 先启动目标版本一次再退出；确认文档实际位置、Proton 前缀与 Steam 库 |
| 主菜单按键无效 | 先进入一局，控制台不是主菜单功能 |
| 打出了中文或符号但不打开 | 切英文输入法与美式键盘布局，再试 Esc 下方键 |
| 关窗口后每日挑战仍不可用 | 改为 `0`，同时关闭模组并重启 |
| 命令没效果或提示不存在 | 查下一页的版本标注、拼写与参数；确认是否来自某个模组扩展 |
| 游戏异常或闪退 | 停止重复无效编号，重新开练习局；自定义实体、房间和角色按对应模组文档检查 |

## 资料与核对范围

2026-10-05 对照公开 [Debug Console](https://bindingofisaacrebirth.wiki.gg/wiki/Debug_Console)、[Options](https://bindingofisaacrebirth.wiki.gg/wiki/Options) 与 [IsaacDocs 控制台教程](https://wofsauge.github.io/IsaacDocs/rep/tutorials/DebugConsole.html)整理。此处核对的是文档、站内链接与页面显示；云环境没有游戏程序，未在游戏中逐条执行命令。
