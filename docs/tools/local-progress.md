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

挑战条目也包含 45 个挑战的前期、中期、终点打法与易错点，离线可以直接展开阅读；“打开教程”对应各挑战的独立页面。

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
| 成就与角色 | 读取当前存档的解锁位，不用 Steam 账号成就替代 |
| 道具 | 分开判断永久解锁与道具收藏记录；按类型和 ID 区分同名道具 |
| 饰品、卡牌、胶囊 | 可关联永久解锁前置；不能用道具收藏数组判断它们是否曾拿过 |
| 完成标记 | 读取各角色对应事件计数器，区分普通与困难 / 极贪；里角色合并成就不会被倒推成全部单独标记 |
| 挑战 | 读取 45 个挑战的完成记录，附规则、前置与奖励 |
| 捐款 | 普通机当前计数、贪婪机累计和各角色贪婪捐款计数；余额与永久里程碑解锁分别看 |

支持已核对的 `ISAACNGSAVE09R` 区段格式，覆盖公开资料中的忏悔与忏悔+布局。新格式、校验失败或记录不足会提示不支持 / 无法判断。尚未在你的实际存档上验证，首次读取请与游戏 Stats / Secrets / Items 核对。

「导出当前筛选 CSV」可保存待办清单；「导出成就清单 JSON」可导入[全成就打勾](/achievements/#catalog)。不会自动覆盖网站里已有的手动勾选。

## 数据来源

- 解析布局：[IsaacPorter，提交 608ce76](https://github.com/frto027/IsaacPorter/blob/608ce768e2bcbf9dbcf965f517c19a1f57f4d0d7/IsaacSave.h)；校验规则与字节数组另对照 [isaac-save-edit-script，提交 516fe1c](https://github.com/jamesthejellyfish/isaac-save-edit-script/blob/516fe1c8d3245677313c159bd1debde37f80fbd0/script.py)。本工具自行实现只读解析，没有存档写入功能。
- 事件和角色解锁编号：[IsaacScript / REPENTOGON 枚举，提交 428232c](https://github.com/IsaacScript/isaacscript/tree/428232c3d2cae4c422bb4c360b96b15fde37b79c/packages/isaac-typescript-definitions-repentogon/src/enums)。只引用编号事实，不要求安装 REPENTOGON。
- 效果、来源和教程：[图鉴来源说明](/about#entry-sources)及[全成就索引](/achievements/)；wiki.gg 条件与教程按 CC BY-SA 4.0 保留出处和授权。

<iframe :src="toolUrl" title="本地存档进度对照工具" style="width:100%;height:1100px;border:2px solid var(--ib-outline);border-radius:12px" loading="lazy"></iframe>
