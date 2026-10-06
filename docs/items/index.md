---
title: "道具图鉴"
aside: false
---

<script setup lang="ts">
import type { CatalogEntry } from "../.vitepress/theme/data/catalog"
import allEntries from "../.vitepress/theme/data/catalog/items.json"
const entries = allEntries as CatalogEntry[]
</script>

# 道具图鉴

<VersionBadge checked="2026-10" />

按中文名、英文名、游戏内 ID 或效果关键词搜索。每个道具、饰品、卡牌 / 符文和胶囊都有独立页，包含效果、数值、版本差异、来源及已关联的解锁教程。

## 按名称与类型查找 {#catalog}

<EntryCatalog :entries="entries" label="道具图鉴" />

<span id="参考资料"></span>

## 数据依据 {#sources}

[条目来源与更新方式](/about#entry-sources)。各详情页附原始资料链接；道具名称按类型与 ID 区分，同名的特殊形态不会相互覆盖。
