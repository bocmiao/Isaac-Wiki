---
title: "人物图鉴"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/characters.json"
const entries = allEntries as CatalogEntry[]
</script>

# 人物图鉴

<VersionBadge checked="2026-10" />

按名称找角色，点卡片看解锁步骤、选道具和打法。每页还列出这个角色的完成标记奖励。

## 按名称与类型查找 {#catalog}

<EntryCatalog :entries="entries" label="人物图鉴" />

## 解锁与练习

- [角色解锁步骤](/guide/unlocks/order) · [全部里角色获取方式](/guide/unlocks/order#tainted-list)
- [开局强化](/strategy/character-roster#upgrades) · [完成标记与全角色奖励](/strategy/completion-marks)
- [新手练习建议](/strategy/characters#新手先练哪个) · [角色解锁清单](/tools/tracker)

<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
