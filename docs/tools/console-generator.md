---
title: 控制台命令生成器
---

# 控制台命令生成器

<VersionBadge checked="2026-10" />

先看[开启控制台](/topics/debug-console)。这里按[命令大全](/topics/debug-console-commands)生成单条或多行命令，支持收藏道具、34个角色、普通主线楼层、debug开关及读取命令。它不执行命令，也不连接你的游戏。

<ConsoleGenerator />

## 编号来源与使用范围

`item-links.json`在本仓库原先不存在，本次补建：道具编号对照 [IsaacDocs CollectibleType](https://wofsauge.github.io/IsaacDocs/rep/enums/CollectibleType.html)，中英文名称对照[EID作者资料](https://github.com/wofsauge/External-Item-Descriptions)，取两边均能核对的720项。名称不是手动拼出编号；代码使用 `c105` 等明确编号，不靠模糊名称匹配。

此处面向 PC 忏悔 / 忏悔+，不包含模组新增道具或任意实体生成，也不把饰品、卡牌、胶囊的编号当收藏道具。`g`直接给道具，`spawn 5.100.ID`生成地上底座，主动道具可能替换原有槽位。切角色会替换当前局，debug同号重复是切换而非强制开启；复制多行前先看清执行顺序。

道具编号数据对照2026-10-05已有源快照：EID提交 `ee7f463a00c11263272ee737a52961fb562d26b8` 与 IsaacDocs提交 `e05b1fd90e33608a7a7a8dcb70a89cef908cc41a` 的枚举。生成脚本是 `scripts/generate-tool-data.py`，需明确传入本地来源仓库路径，不联网抓取或自动猜补缺失编号。
