---
title: 配置与实用模组
description: Steam 创意工坊实用模组推荐：中文道具说明、配置菜单、Boss 血条、小地图与星象房概率，含安装、兼容和冲突排查。
---

# 配置与实用模组

<VersionBadge />

::: tip 速览
- **先在不开模组、不开控制台的正常局里打败一次妈妈（Mom，第 3 章的 Boss）**，再装（[成就](#achievements)）
- **最小组合：EID 中文道具说明 + Mod Config Menu - Impure**（[逐步加装](#最小组合与逐步加装)）
- **其余按需加**：Boss 血条、小地图或星象房概率，不必订阅整套合集（[按用途选](#recommended)）
- **官方在线联机前关闭全部模组并重启**，详见[联机专题](/topics/coop)（[故障排查](#troubleshooting)）
- 本页讲 Steam 创意工坊模组，调试控制台见[调试控制台系列](/topics/debug-console)
:::

## 按用途选模组 {#recommended}

点名称打开对应 Steam 创意工坊页面。「支持版本」只写作者明确说明的版本：能订阅不代表已兼容。

| 模组 | 用途 | 何时装 | 支持版本 |
| --- | --- | --- | --- |
| [External Item Descriptions（EID）](https://steamcommunity.com/sharedfiles/filedetails/?id=836319872) | 显示道具、饰品、卡牌、符文、胶囊等说明，支持中文 | 打败妈妈后优先装 | 胎衣+、忏悔、忏悔+ |
| [Mod Config Menu - Impure](https://steamcommunity.com/sharedfiles/filedetails/?id=3701683951) | 给支持它的模组提供游戏内设置菜单 | 和 EID 一起装，方便改语言与显示 | 胎衣+、忏悔、忏悔+ |
| [Enhanced Boss Bars](https://steamcommunity.com/sharedfiles/filedetails/?id=2635267643) | 每个 Boss、每段分别显示血条和图标，多目标战斗看得清 | 常打多 Boss 房、想看清剩余血量 | 忏悔、忏悔+ |
| [MinimapAPI](https://steamcommunity.com/sharedfiles/filedetails/?id=1978904635) | 小地图缩放、掉落物与乞丐图标、显示自定义 | 常回头拿资源，嫌原版地图不清楚 | 胎衣+、忏悔、忏悔+ |
| [Planetarium Chance](https://steamcommunity.com/sharedfiles/filedetails/?id=2489006943) | 在 HUD 显示本层生成[星象房](/guide/first-win/rooms)的概率 | 已解锁星象房，想规划跳宝箱房路线 | 忏悔+ |

装之前注意：

- **EID**：基础说明不需要 REPENTOGON（另一个扩展模组），部分扩展功能才需要它。
- **Impure**：不要同时启用 Pure、旧版或其他独立的配置菜单版本。
- **Enhanced Boss Bars**：作者明确说它和其他修改 Boss 血条设计的模组冲突。
- **MinimapAPI**：既是地图工具，也是其他模组的前置。它本身不能快捷传送。
- **Planetarium Chance**：不会替你解锁星象房，也不会强制生成星象房。概率什么时候更新、续局时显示准不准，见[下文](#planetarium)。

### 最小组合与逐步加装

1. **第一次打败妈妈前**：先不开模组。需要认道具时，用[网页图鉴](/items/)。
2. **开始刷角色和完成标记**（完成标记：用各角色打败各个终点 Boss 留下的记录）：装 EID + Impure 配置菜单。先确认中文说明、设置入口和本局可解锁状态正常。
3. **想看清战斗**：再加 Enhanced Boss Bars，只保留一套修改 Boss 血条的模组。
4. **想看清走图资源**：再加 MinimapAPI；有了它不代表可以传送。
5. **已经解锁星象房**：按需装 Planetarium Chance。还没解锁时，先满足游戏里的解锁条件，这个模组不会帮你开放星象房。

每次只加一个新模组，重启后开一局检查。这样出问题时，能找到是哪一个模组引起的。

## EID：中文道具说明 {#eid}

EID 用来解释道具和机制，尤其适合这些场合：学新角色、决定拿不拿恶魔交易、看里该隐合成道具要用的材料、决定里以撒（被动道具最多 8 格）该丢哪个。

按设置不同，EID 还能显示更多构筑信息。它的说明来自模组自带的资料，游戏更新后要留意作者有没有跟着更新。

- 按 <KeyCap>F2</KeyCap> 显示 / 隐藏说明。
- 在支持 EID 的配置菜单里，把 Language 改成简体中文。作者配置文件中的语言代码是 `zh_cn`。
- 默认语言代码为 `auto`，在忏悔中会尝试跟随游戏语言。游戏本身没有中文选项时，`auto` 切不到中文，要手动选。
- EID 不等于完整汉化：它的中文说明不会把所有菜单、剧情和其他模组一并翻成中文。
- REPENTOGON 是另外的扩展，订阅 EID 不会自动装上它。只有 EID 的部分扩展功能需要它，新手只看基础中文说明，不用装。

不想装配置菜单时，也可以直接改 `eid_config.lua` 文件。普通玩家优先用菜单：手改文件容易改错，还可能被模组更新覆盖。

::: info 忏悔+ 自带说明能否代替 EID
忏悔+ 已有游戏内道具说明功能，但显示条件、语言和内容范围与 EID 不同。只想玩原版或在线联机，先看游戏设置中的 Item Descriptions。需要中文或扩展说明，再考虑 EID。具体规则见[中文设置与常见问题](/guide/start/chinese)。
:::

## Impure：配置菜单怎么打开 {#config-menu}

Impure 本身不增加道具，也不会自动修改其他模组。只有接入了这个菜单的模组，才会在菜单里出现设置项。

1. 进入一局游戏，清空当前房间，确认没有战斗危险。
2. 默认按 <KeyCap>L</KeyCap> 打开。作者 README 还列出固定备用键 <KeyCap>F10</KeyCap>；手柄默认按下右摇杆。
3. 选 EID 等对应模组，改语言、字号或显示位置；退出菜单再看效果。

**在主菜单里打不开**，要进入对局后再按。

- 按键只响蜂鸣、不出菜单：可能是 Impure 检测到危险，先清房再试。
- 完全找不到入口：确认 Mods 菜单里启用了 Impure、没有同时开 Pure 或旧版，然后重启游戏。
- 旧教程推荐的是 Pure：不要因此把 Pure 和 Impure 都打开。

## Enhanced Boss Bars：看清多目标血条 {#boss-bars}

主要功能：每个 Boss 单独的图标、多种血条样式，以及按 Boss、按分段分别显示血量。血条能帮你判断先打哪个目标，但不会改变 Boss 的攻击套路，也代替不了[Boss 打法](/strategy/bosses)。

如果同时看到原版和模组的两套血条，先关掉其他 Boss 血条模组并重启。第一次安装或切换游戏语言时，也可能出现重复显示。旧资料里的 Better Boss Bar、Paper Healthbars 等是别的血条模组，不必和 Enhanced Boss Bars 叠装。

## MinimapAPI：记资源，不等于传送 {#minimap}

MinimapAPI 能调小地图的大小和显示方式，并用图标标出掉落物、机器与乞丐，适合清完一层后回头捡红心、硬币和钥匙。它还给其他地图模组提供接口，所以常作为别的模组的“必需物品”列在工坊页面上。

- 先调到能看清的大小，避免挡住角色血量或 EID 说明。
- 它不会把没探索过的房间都显示出来，图标只标出已知的东西。
- 出现两张小地图时先重启。重启后还是两张，再排查其他替换小地图的模组。
- 传送通常来自另一个模组，不是安装 MinimapAPI 后默认获得的能力。

## Planetarium Chance：显示的是当前层概率 {#planetarium}

Planetarium Chance 显示本层生成星象房的概率，适合判断不进宝箱房值不值。星象房要先在游戏里解锁，这个数字才有用；没解锁时，装了模组也不会出星象房。

有两处容易误读：

- **本层的布局已经生成好了**。拿到影响星象房概率的道具后，要到下一层，概率才会变；本层不会重新生成。
- **退出后续局**时，本层显示的概率可能不准，到下一层会恢复。显示的只是概率，不能说明本层一定有星象房。

在忏悔+ 上，这个模组有已知的着色器显示问题，作者给了临时处理办法。装好后留意图标显示是否正常。图标显示异常，不代表存档里星象房的解锁条件被重置了。

## 快捷回程：按需查阅，不混入信息模组组合 {#fast-travel}

[Goodtrip MLX's Tweak](https://steamcommunity.com/sharedfiles/filedetails/?id=3749565569)属于 GoodTrip 快捷走图系列，会改变走图方式，需要时再额外安装。

| 项目 | 说明 |
| --- | --- |
| 前置 | 必需 **MinimapAPI**，配置菜单为可选；使用前停用原 Goodtrip |
| 默认操作 | 按住 Tab 显示地图光标，用射击方向键选择房间，松开 Tab 传送 |
| 默认设置 | 支持镜像地图。默认不能传送到诅咒房，光标速度默认 2。都能在配置菜单或配置文件里改 |
| 支持版本 | 工坊页没写清，用前自己在当前版本试一下 |

这类模组减少往返，**会改变走图玩法**：

- 不同分支的处理并不完全相同，比如：没探索过的房间能不能传、战斗中能不能传、门锁、诅咒房扣血、限时奖励入口。订阅前看清作者说明和依赖。
- 不要同时启用原版、Fixed、MLX 等多个传送分支。
- 正在练习原版限时路线或献祭、诅咒房的资源取舍时，先按正常走图规则练。

MinimapAPI、Planetarium Chance、EID 与快捷传送模组的用途各不相同。加新内容的大型模组会改变道具池、角色和房间，建议熟悉原版后，再按它们自己的说明安装。

## Steam 订阅、启用与卸载 {#install}

这套步骤用于 PC 的 Steam 版，还要有模组页要求的 DLC。重生本体或胎衣时代的旧式资源替换，不按这里的 Lua 模组流程安装。主机玩家看[主机专题](/topics/console)。

1. 在上面的工坊入口确认模组名称、作者、支持的 DLC，以及“必需物品 / Required Items”。别按相似名称装成转载版。
2. 点“订阅”，等 Steam 下载完成。前置模组要逐个确认已订阅，它们不一定会跟着一起下载。
3. 启动游戏，在 Mods 菜单确认目标模组已启用。
4. 完全退出并重启游戏，再进入正常局检查实际效果。不要只看到已订阅，就认为加载成功。
5. 想暂时停用，在 Mods 菜单关掉；想卸载，在工坊取消订阅。订阅状态和游戏内启用状态是两回事。

### 什么时候能解锁成就 {#achievements}

- **第一次打败妈妈之前，启用模组会让成就无法解锁**。先关掉模组和调试控制台，在不用种子的正常局里打败妈妈，再开模组。
- **打败妈妈之后**，启用模组本身不再一律禁止解锁。但种子局、每日挑战、普通挑战和胜利圈（打完羔羊后选择继续下一轮）等仍有各自的规则。
- 每局开始时看一眼钥匙数量下方：有划掉的奖杯图标，这局就解锁不了东西。
- 换存档栏、切忏悔 / 忏悔+ 或更换 DLC 后，重新确认当前进度和可解锁状态；不要仅凭另一版本已经打过妈妈来判断。
- 每日挑战前关闭模组与控制台；官方在线联机前关闭全部模组并重启游戏。

该解锁的角色或标记没出现，先按[成就排查表](/guide/start/chinese#成就为什么不解锁)检查游戏条件。只装了显示信息的模组，也不代表任何模式都能解锁。

## 常见故障按这个顺序查 {#troubleshooting}

| 现象 | 先查什么 | 下一步 |
| --- | --- | --- |
| 订阅了但没效果 | Steam 下载是否完成、Mods 中是否启用、DLC 是否匹配 | 完全退出重启，只启用目标模组与必需前置 |
| EID 还是英文 | Language 是否为 `auto`，游戏本身有没有中文选项 | 手动选择中文 / `zh_cn`，不要再订阅第二个相同 EID |
| EID 说明消失 | 是否按过 F2、是否启用了其他 HUD 模组 | F2 切换一次，调整说明位置，再逐个排查 |
| 配置菜单打不开 | 是否在对局中、房间是否安全、是否同时启用 Pure / 旧版 | 清房后按 L 或 F10，保留一个菜单版本并重启 |
| 重复 Boss 血条 | 是否同时装了其他 Boss 血条替换 | 只保留一套并重启 |
| 两张小地图 | 首次安装未重启、多个地图模组重复渲染 | 重启，再停用重叠功能的模组 |
| 星象房概率看起来没变 | 是否仍在当前楼层、是否刚续局、房间是否已解锁 | 到下一层再检查，概率不是必出保证 |
| 更新后闪退或显示异常 | 游戏与模组是否同步更新，前置是否符合作者要求 | 先关闭最近新增的模组；逐个恢复，记录游戏版本再向作者反馈 |
| 官方在线联机不可用 | 是否还有模组启用或修改游戏文件的补丁 | 关闭模组并重启；文件修改类补丁按其作者说明处理 |

要用控制台排查模组或练习道具，见[调试控制台系列](/topics/debug-console)；开启控制台不等于订阅模组。

有些中文补丁是运行外部程序直接改游戏文件的，和工坊模组不是一回事。关掉 Mods 菜单里的模组、取消订阅，都还原不了这类补丁，处理方法见[中文设置](/guide/start/chinese)。

## 资料与核对范围

本次（2026-10-05）已读取上面六个模组的工坊原页面，并对照下面的作者仓库 README、配置与工坊元数据。这里不包含实际游戏中的模组安装测试，也不将无法复核的当前工坊版本标作已兼容。

- [EID 作者 README](https://github.com/wofsauge/External-Item-Descriptions)与[安装指南](https://github.com/wofsauge/External-Item-Descriptions/wiki/How-to-install-the-mod)、[语言配置](https://github.com/wofsauge/External-Item-Descriptions/blob/ee7f463a00c11263272ee737a52961fb562d26b8/eid_config.lua)。
- [Mod Config Menu - Impure 作者 README](https://github.com/piber20/Mod-Config-Menu-Impure)。
- [Enhanced Boss Bars 作者 README 与元数据](https://github.com/wofsauge/Enhanced-Boss-Bars)。
- [MinimapAPI 作者项目与文档](https://github.com/TazTxUK/MinimapAPI)。本次对照维护仓库 2026-03-31 的提交，未将早期镜像作为当前发布依据。
- [Planetarium Chance 作者 README 与元数据](https://github.com/Sectimus/isaac-planetarium-chance)。
- [GoodTripPlus 作者 README](https://github.com/Jamlet-T/GoodTripPlus)：仅用于核对其引用的 MLX 工坊入口与分支差异，没有把这个未确认工坊发布的派生项目当成一键订阅推荐。
- [REPENTANCE+ Is Here（Steam 官方新闻）](https://store.steampowered.com/news/app/250900/view/1783238125358311)：在线联机前关闭模组的规则。
- [Modding（英文 wiki）](https://bindingofisaacrebirth.wiki.gg/wiki/Modding_(Afterbirth_%E2%80%A0))、[Achievements](https://bindingofisaacrebirth.wiki.gg/wiki/Achievements)、[Daily Challenges](https://bindingofisaacrebirth.wiki.gg/wiki/Daily_Challenges)：模组和特殊模式的成就规则。

<!-- 待核实：未进行游戏内加载测试；Goodtrip mlxtweak 页面未明确列出完整版本范围，评论中的热更新兼容问题未作为可靠结论。 -->
<!-- 待核实：首次击败妈妈解除模组解锁限制的精确存档作用域；既有 wiki 资料存在矛盾，正文推荐在目标存档确认可解锁状态，不推断全局或逐存档规则。 -->
