<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import achievements from '../data/achievements.json'
const query = ref('')
const version = ref('plus')
const category = ref('all')
const groups = [...new Set(achievements.map(a => a.group))].sort()
const results = computed(() => {
  const terms = query.value.trim().toLocaleLowerCase().replace(/^#/, '').split(/\s+/).filter(Boolean)
  return achievements.filter(a =>
    (version.value === 'plus' || a.id <= 637) &&
    (category.value === 'all' || a.group === category.value) &&
    terms.every(t => `${a.id} ${a.name} ${a.conditionZh} ${a.group}`.toLocaleLowerCase().includes(t)),
  )
})
</script>

<template>
  <section class="achievement-catalog" aria-label="全成就查询">
    <div class="filters">
      <label>查找成就<input v-model="query" type="search" placeholder="编号、英文名称、角色或中文条件" /></label>
      <label>版本<select v-model="version" aria-label="版本"><option value="plus">忏悔+ · 641 项</option><option value="rep">忏悔 · 637 项</option></select></label>
      <label>分类<select v-model="category" aria-label="分类"><option value="all">全部分类</option><option v-for="g in groups" :key="g" :value="g">{{ g }}</option></select></label>
    </div>
    <p role="status" aria-live="polite">找到 {{ results.length }} / {{ version === 'plus' ? 641 : 637 }} 项。点名称查看解锁步骤。</p>
    <p v-if="!results.length">没有匹配的成就。试试编号、英文名，或清空分类条件。</p>
    <div v-else class="results">
      <article v-for="a in results" :key="a.id" class="achievement">
        <a :href="withBase(`/guide/achievements/${a.page}#achievement-${a.id}`)"><strong>#{{ a.id }} · {{ a.name }}</strong></a>
        <p>{{ a.conditionZh }}</p>
        <small>{{ a.group }} · {{ a.minimum }}加入</small>
      </article>
    </div>
  </section>
</template>

<style scoped>
.filters { display: flex; flex-wrap: wrap; gap: 12px; }
label { display: flex; flex-direction: column; gap: 6px; flex: 1 1 150px; font-size: 14px; }
input, select { border: 1px solid var(--vp-c-divider); border-radius: 6px; padding: 8px; background: var(--vp-c-bg); color: var(--vp-c-text-1); width: 100%; min-width: 0; }
input:focus-visible, select:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 2px; }
.results { display: grid; gap: 12px; }
.achievement { border: 1px solid var(--vp-c-divider); border-radius: 8px; padding: 12px 16px; overflow-wrap: anywhere; }
.achievement p { margin: 6px 0; }
.achievement small { color: var(--vp-c-text-2); }
</style>
