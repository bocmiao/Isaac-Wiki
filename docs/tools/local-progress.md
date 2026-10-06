---
title: 本地存档进度对照
aside: false
---

<script setup lang="ts">
import { withBase } from 'vitepress'
const toolUrl = withBase('/downloads/isaac-progress.html')
</script>

# 本地存档进度对照

<VersionBadge checked="2026-10" />

选择你自己的永久进度存档，列出未解锁成就、已解锁但未收集的道具、未开放角色、未完成挑战以及普通 / 困难完成标记，再对照条件与获取教程。

<p><a :href="toolUrl" download="isaac-progress.html">下载本地工具 HTML</a> · <a :href="toolUrl" target="_blank" rel="noreferrer">在新窗口使用</a></p>

## 本地怎么用

1. 下载 `isaac-progress.html`，用 Edge / Chrome 双击打开。工具本体、清单、条件和步骤都在文件里，无需 Python、模组或控制台。
2. 正常退出游戏，让进度保存完成。点「选择存档 .dat」，或把文件拖进工具。
3. 核对顶部的文件名和存档栏，选择「道具与收集」「成就」「角色」「完成标记」「挑战」或「捐款」。默认筛出待完成事项。
4. 在道具页选择「已解锁未收集」，即可找已经开放、但这个存档还没有收藏记录的道具。展开条目查看效果、条件和获取说明，完整站内教程可以点击打开。
5. 玩完后重新读取文件。支持文件关联的 Edge / Chrome 可用「重新读取」；使用拖拽或普通文件选择时，按钮会要求重新选择最新文件。

读取和筛选在你的设备上完成，文件不上传服务器，不写回游戏存档。下载版可断网使用；打开完整站内教程需要联网。

## 读完存档后先看哪里

- **想补收藏**：选“道具与收集 → 已解锁未收集”，看缺哪些道具、可能在哪拿到。
- **想补角色标记**：选“完成标记”，查该角色还缺哪个 Boss、是否只打过普通。里角色合并奖励会列出同组缺项。
- **想做挑战**：选“挑战”，展开规则和打法。45 个挑战的前期、中期和终点建议都可离线阅读。
- **想补捐款**：选“捐款”，分别看普通机余额、贪婪机总累计和各角色捐款。

奖励已解锁与角色标记齐全可能不同。例如左手还有击败超级傲慢的获取方式，因此不能只凭它已解锁就认定犹大打过 ???。详细区别见[完成标记与奖励](/strategy/completion-marks)。

## Windows Steam《忏悔+》存档位置

通常先找 Steam 安装目录，然后检查：

```text
Steam\userdata\<账号数字目录>\250900\remote\rep+persistentgamedata1.dat
Steam\userdata\<账号数字目录>\250900\remote\rep+persistentgamedata2.dat
Steam\userdata\<账号数字目录>\250900\remote\rep+persistentgamedata3.dat
```

`1 / 2 / 3` 是三个独立存档栏，Steam 可能装在其他盘。其他存档位置可在「文档\My Games\Binding of Isaac Repentance+」检查；带日期的文件通常是备份。不要选择本局的 `gamestate`、`options.ini` 或日志。

## 哪些记录能对照

| 分类 | 实际读取与限制 |
| --- | --- |
| 成就与角色 | 显示当前存档已解锁的内容；与 Steam 账号成就分开 |
| 道具 | 分开判断永久解锁与道具收藏记录；按类型和 ID 区分同名道具 |
| 饰品、卡牌、胶囊 | 可关联永久解锁前置；无法判断每件是否曾拿过 |
| 完成标记 | 显示各角色的实际标记，区分普通与困难 / 极贪；合并奖励另列缺项 |
| 挑战 | 读取 45 个挑战的完成记录，附规则、前置与奖励 |
| 捐款 | 普通机当前计数、贪婪机累计和各角色贪婪捐款计数；余额与永久里程碑解锁分别看 |

支持忏悔 / 忏悔+ 的已知永久进度格式。新格式、校验失败或记录不足会提示无法读取或无法判断。首次读取时，请与游戏的 Stats → Secrets / Items 核对。

## 导出清单，带回网站记录

| 导出按钮 | 导入到哪里 |
| --- | --- |
| 当前筛选 CSV | 用表格软件打开，作为待办清单 |
| 角色与标记 JSON | [角色解锁清单](/tools/tracker) |
| 挑战 JSON | [挑战进度清单](/tools/challenges) |
| 捐款 JSON | [捐款进度](/tools/donations) |
| 成就清单 JSON | [全成就打勾](/achievements/#catalog) |

在对应工具选择“导入”。角色、标记、成就和挑战默认合并，保留已有的解锁和困难记录，也可选择替换。捐款按当前存档数值替换，永久里程碑按存档的成就状态显示。不同类型的 JSON 请导入对应工具。

## 数据来源

- 解析布局：[IsaacPorter，提交 608ce76](https://github.com/frto027/IsaacPorter/blob/608ce768e2bcbf9dbcf965f517c19a1f57f4d0d7/IsaacSave.h)；校验规则与字节数组另对照 [isaac-save-edit-script，提交 516fe1c](https://github.com/jamesthejellyfish/isaac-save-edit-script/blob/516fe1c8d3245677313c159bd1debde37f80fbd0/script.py)。本工具自行实现只读解析，没有存档写入功能。
- 事件和角色解锁编号：[IsaacScript / REPENTOGON 枚举，提交 428232c](https://github.com/IsaacScript/isaacscript/tree/428232c3d2cae4c422bb4c360b96b15fde37b79c/packages/isaac-typescript-definitions-repentogon/src/enums)。只引用编号事实，不要求安装 REPENTOGON。
- 效果、来源和教程：[图鉴来源说明](/about#entry-sources)及[全成就索引](/achievements/)；wiki.gg 条件与教程按 CC BY-SA 4.0 保留出处和授权。

<iframe :src="toolUrl" title="本地存档进度对照工具" style="width:100%;height:1100px;border:2px solid var(--ib-outline);border-radius:12px" loading="lazy"></iframe>
