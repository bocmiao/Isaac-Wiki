<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import items from '../data/item-links.json'

// 道具速查：按中文名、英文名或 ID 搜道具 / 饰品 / 卡牌 / 胶囊，跳到 wiki.gg 中文站或 IsaacGuru。
// 名称来自 EID 中文名称表（scripts/gen-item-links.py 生成），和站内文章用的译名一致。
type Kind = 'c' | 't' | 'k' | 'p'
type Entry = [string, Kind, number, string]

const KIND_LABEL: Record<Kind, string> = { c: '道具', t: '饰品', k: '卡牌 / 符文', p: '胶囊' }
const all = Object.values(items as Record<string, Entry>).map(([zh, kind, id, en]) => ({ zh, kind, id, en }))
const PAGE = 30

const query = ref('')
const kind = ref<'all' | Kind>('all')
const shown = ref(PAGE)
watch([query, kind], () => {
  shown.value = PAGE
})

const results = computed(() => {
  const q = query.value.trim().toLowerCase()
  const list = all.filter((x) => kind.value === 'all' || x.kind === kind.value)
  if (!q) return list
  const num = /^\d+$/.test(q) ? Number(q) : null
  const scored = list
    .map((x) => {
      const zh = x.zh.toLowerCase()
      const en = x.en.toLowerCase()
      let score = -1
      if (num !== null && x.id === num) score = 0
      else if (zh === q || en === q) score = 1
      else if (zh.startsWith(q) || en.startsWith(q)) score = 2
      else if (zh.includes(q) || en.includes(q)) score = 3
      return { x, score }
    })
    .filter((r) => r.score >= 0)
  scored.sort((a, b) => a.score - b.score || a.x.id - b.x.id)
  return scored.map((r) => r.x)
})

const wiki = (zh: string) => `https://bindingofisaacrebirth.wiki.gg/zh/index.php?search=${encodeURIComponent(zh)}&go=Go`
const guru = (k: Kind, id: number) => `https://isaacguru.com/wiki/isaac/${k}${id}`
</script>

<template>
  <section class="finder" aria-label="道具速查">
    <div class="filters">
      <label class="wide">
        名称或 ID
        <input v-model="query" type="search" placeholder="例如：硫磺火、brimstone、118" autocomplete="off" />
      </label>
      <label>
        类型
        <select v-model="kind">
          <option value="all">全部 · {{ all.length }}</option>
          <option v-for="(label, k) in KIND_LABEL" :key="k" :value="k">{{ label }}</option>
        </select>
      </label>
    </div>
    <p class="count" role="status" aria-live="polite">
      找到 {{ results.length }} 个<template v-if="results.length > shown">，先显示前 {{ shown }} 个</template>。
    </p>
    <ul v-if="results.length" class="list">
      <li v-for="r in results.slice(0, shown)" :key="r.kind + r.id">
        <span class="kind" :class="r.kind">{{ KIND_LABEL[r.kind] }}</span>
        <span class="names">
          <b>{{ r.zh }}</b>
          <span class="en">{{ r.en }} · ID {{ r.id }}</span>
        </span>
        <span class="links">
          <a :href="wiki(r.zh)" target="_blank" rel="noreferrer">wiki.gg 中文</a>
          <a :href="guru(r.kind, r.id)" target="_blank" rel="noreferrer">IsaacGuru</a>
        </span>
      </li>
    </ul>
    <p v-else>没找到。试试英文名，或者换个关键字（比如只输入名字里的两个字）。</p>
    <button v-if="results.length > shown" type="button" class="more ib-btn" @click="shown += 60">再显示一些</button>
  </section>
</template>

<style scoped>
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1 1 140px;
  font-size: 14px;
}
label.wide {
  flex: 3 1 260px;
}
input,
select {
  border: 2px solid var(--ib-outline);
  border-radius: 6px;
  padding: 9px 10px;
  background: var(--ib-paper);
  color: var(--vp-c-text-1);
  width: 100%;
  min-width: 0;
  font-size: 15px;
}
input:focus-visible,
select:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}
.count {
  font-size: 14px;
  color: var(--ib-ink-3);
}
.list {
  list-style: none;
  padding: 0 !important;
  margin: 0;
  border: 2px solid var(--ib-outline);
  border-radius: 8px;
  overflow: hidden;
  background: var(--ib-paper);
}
.list li {
  display: grid;
  grid-template-columns: 84px 1fr auto;
  gap: 12px;
  align-items: center;
  margin: 0 !important;
  padding: 10px 14px;
  border-top: 1px dashed var(--ib-ink-3);
}
.list li:first-child {
  border-top: 0;
}
.kind {
  justify-self: start;
  font-size: 12px;
  font-weight: 800;
  padding: 1px 8px;
  border-radius: 999px;
  border: 1.5px solid var(--ib-outline);
}
.kind.c {
  background: var(--ib-gold-soft);
}
.kind.t {
  background: var(--ib-soul-soft);
}
.kind.k {
  background: var(--vp-custom-block-danger-bg);
}
.names {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.en {
  font-size: 13px;
  color: var(--ib-ink-3);
}
.links {
  display: flex;
  gap: 12px;
  font-size: 14px;
  white-space: nowrap;
}
.more {
  display: block;
  margin: 14px auto 0;
}
@media (max-width: 560px) {
  .list li {
    grid-template-columns: 1fr;
    gap: 4px;
  }
}
</style>
