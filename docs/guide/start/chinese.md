---
title: 中文设置与常见问题
---

# 中文设置与常见问题

<VersionBadge checked="2026-10" />

::: tip 速览
- **官方中文只在忏悔里有**：关掉 Repentance+，回主菜单切 Language（[步骤](#在忏悔里切换中文)）
- **忏悔和 Repentance+ 是两套存档**，进度互不同步（[看提醒](#在忏悔里切换中文)）
- **Repentance+ 里看中文只能装第三方补丁**，装不装自己决定（[补丁](#为什么有人还装中文补丁)）
- **成就不解锁**，先看钥匙数下面有没有划掉的奖杯（[排查](#成就为什么不解锁)）
- **三个存档栏位进度独立**，Steam 成就可按 Alt+F2 补回（[存档](#三个存档栏位是独立的)）
:::

游戏有官方简体中文，但只在忏悔（Repentance）里能选；开着 Repentance+ 时设置里没有语言选项，界面是英文。所以想玩官方中文就关掉 Repentance+，想在线联机就开着它玩英文版，或者自己决定要不要装玩家做的中文补丁。

## 官方中文是哪来的

- 2021 年 11 月，忏悔的 1.7.5 更新加入了简体中文，同时加入的还有日语、韩语、西班牙语、德语和俄语。
- 官方当时说这些翻译还不完整，之后好几次更新都在补本地化文件。
- Steam 商店的语言表只写了英语，简体中文那一栏显示「不支持」。别被吓到，在忏悔里确实能切到中文。

## 在忏悔里切换中文

1. 如果装了 Repentance+，先在 Steam 的 DLC 管理里把 Repentance+ 取消勾选。
2. 启动游戏，选一个存档，进入主菜单里的 Options（选项）。
3. 找到 Language，切换成中文。

暂停菜单里的选项没有 Language 这一项，要回主菜单改。

::: warning 忏悔和 Repentance+ 是两套存档
第一次打开 Repentance+ 时，游戏会复制一份忏悔的存档来用。之后两边的进度互不同步：在忏悔里解锁的东西，回到 Repentance+ 不会出现，反过来也一样。来回切换之前，先想好主要在哪边打进度。
:::

## 为什么有人还装中文补丁

英文 wiki 把 Language 选项标成「Repentance+ 中已移除」。想在 Repentance+ 里联机、又想看中文的玩家，就会去装创意工坊上的玩家补丁「[Rep+] 忏悔+的官中补丁」。按它自己的说明，它会把官方中文重新启用并补全。

::: warning 这是第三方补丁
它不是官方出的。安装时要运行一个外部程序改游戏文件，官方每次更新后都会失效，需要重装。想移除时，在 Steam 里验证游戏文件完整性即可。本站不保证它的安全和效果，装不装你自己决定。
:::

如果只是想看懂道具，也可以用支持中文的道具说明模组，见[配置与模组](/topics/mods)。

## 成就为什么不解锁

先看界面上钥匙数量的下面。如果有一个被划掉的奖杯图标，说明这一局解锁不了成就。常见原因如下：

| 情况 | 说明 |
| --- | --- |
| 开着模组但尚未满足前置 | 初始阶段会阻止解锁。先关闭模组与控制台，在正常局击败一次妈妈；满足前置后，启用模组本身不再一概禁止正常解锁 |
| 开了调试控制台但尚未满足前置 | 首先在不开模组、不开控制台的正常局击败一次妈妈；每日挑战等还需另外关闭，不能只按普通局规则判断 |
| 自己输入了种子（Seed） | 手动输入普通种子的局不能解锁。特殊种子（彩蛋种子）里有一部分会禁用成就，一部分不影响，见[种子](/strategy/seeds) |
| 在挑战（Challenges）里 | 只能解锁「完成这个挑战」本身的成就 |
| 在每日挑战（Daily Run）里 | 只能解锁每日挑战相关的成就 |
| 在胜利圈（Victory Lap）里 | 离线玩时不能解锁（胜利圈自己的成就除外）；在线联机的胜利圈不受影响 |
| 在线联机中途加入 | 中途加入的那一局不能解锁，要从头开始玩的局才行 |

::: tip 新手最稳的做法
第一次打败妈妈之前，什么模组都别开，也别输种子。
:::

控制台的配置路径、开关、命令与练习方法见[调试控制台系列](/topics/debug-console)。仅收起控制台窗口不会关闭它。

## 三个存档栏位是独立的

游戏有 3 个存档栏位。每个栏位的解锁进度单独保存，换一个新栏位就要重新解锁。Repentance+ 的游戏内道具说明也是按存档算的，每个存档都要先打败一次妈妈。

Steam 成就则跟着账号走。如果 Steam 上已经有某个成就，但当前存档里没解锁，可以进 Stats（统计）菜单，打开 Secrets 页面，按 <KeyCap>Alt</KeyCap>+<KeyCap>F2</KeyCap>，让游戏按 Steam 成就补上解锁。

## 下一步

设置好就可以开始第一局了，接着看第 2 层：[第一次通关](/guide/first-win/)。

## 参考资料

- [Options（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Options)
- [V1.7.5（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/V1.7.5)
- [V1.7.8（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/V1.7.8)
- [Update v1.7.5 (LOCALIZATIONS AND MORE)（Steam 官方新闻，2021-11-10）](https://store.steampowered.com/news/app/250900/view/4971405952698827291)
- [《以撒的结合：忏悔》1.7.5 版本更新推出官方简体中文（IT之家）](https://www.ithome.com/0/586/093.htm)
- [The Binding of Isaac: Repentance（Steam 商店，简体中文页面）](https://store.steampowered.com/app/1426300/?l=schinese)
- [The Binding of Isaac: Repentance+（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/The_Binding_of_Isaac:_Repentance%2B)
- [Progress between Repentance and Repentance+ Question（Steam 社区讨论）](https://steamcommunity.com/app/250900/discussions/0/4631484492942429050/)
- [Does anyone know what happens if I uninstall repantance plus?（Steam 社区讨论）](https://steamcommunity.com/app/250900/discussions/0/601895828709188323/)
- [[Rep+] 忏悔+的官中补丁v2.0+（Steam 创意工坊）](https://steamcommunity.com/sharedfiles/filedetails/?id=3568677664)
- [Achievements（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Achievements)
- [Modding (Afterbirth †)（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Modding_(Afterbirth_%E2%80%A0))
- [Seeds（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Seeds)
- [Challenges（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Challenges)
- [Victory Lap（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Victory_Lap)
- [Online (open beta)（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Online_(open_beta))
- [REPENTANCE+ Is Here（Steam 官方新闻，2024-11-18）](https://store.steampowered.com/news/app/250900/view/1783238125358311)
- [Save File Completion（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Save_File_Completion)
- [Achievement Tips（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Achievement_Tips)
- [V1.9.7.13（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/V1.9.7.13)

<!-- 待核实：「忏悔和 Repentance+ 是两套存档、互不同步」来自 Steam 社区多名玩家的说明，与英文 wiki「游戏会保留装 Repentance+ 之前的存档备份」一致，但没有找到官方原文。 -->
<!-- 待核实：「先打败一次妈妈」才能开模组解锁，这个条件是按存档算还是全局算，来源矛盾：英文 wiki 模组页说不需要每个存档都打一次；Options 页（EnableMods / EnableDebugConsole）说会阻止「在新存档上」解锁。正文没写按存档还是全局。 -->
<!-- 待核实：游戏内 Language 列表里中文选项的确切写法、切换后是否需要重启，未查到。 -->
<!-- 待核实：重生 / 胎衣 / 胎衣+（不开忏悔）时有没有中文，未查到可靠来源，正文只写忏悔。 -->
<!-- 待核实：Steam 客户端里关闭 DLC 的具体点击路径，未在官方帮助页面打开确认。 -->
<!-- 待核实：按 Alt+F2 同步后，通关标记（completion marks）是否也会显示，只见于 Steam 社区玩家说法（说不会），正文未写。 -->
