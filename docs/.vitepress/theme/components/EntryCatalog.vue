<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter, withBase } from 'vitepress'
import GameIcon from './GameIcon.vue'
import { filterCatalog, type CatalogEntry } from '../data/catalog'
import legacyLinks from '../data/catalog/legacy-links.json'

const props = defineProps<{ entries: CatalogEntry[]; label: string; legacy?: boolean }>()
const route = useRoute()
const router = useRouter()
const query = ref('')
const group = ref('')
const page = ref(1)
const ready = ref(false)
const size = 36
const hasGameIds = computed(() => props.entries.some(entry => entry.gameId !== undefined))
const groups = computed(() => [...new Set(props.entries.map(entry => entry.group))])
const matches = computed(() => filterCatalog(props.entries, query.value, group.value))
const pages = computed(() => Math.max(1, Math.ceil(matches.value.length / size)))
const visible = computed(() => matches.value.slice((page.value - 1) * size, page.value * size))
watch([query, group, () => props.entries], () => { page.value = 1 })

function goPage(value: number) {
  page.value = value
  document.querySelector('.catalog-controls')?.scrollIntoView({ block: 'center', behavior: 'smooth' })
}

// Existing shared-article bookmarks remain valid, including character build/combat subheadings.
function followLegacyAnchor() {
  if (!props.legacy || !window.location.hash) return
  let anchor: string
  try { anchor = decodeURIComponent(window.location.hash.slice(1)) } catch { return }
  const base = withBase('/')
  const path = route.path.startsWith(base) ? '/' + route.path.slice(base.length) : route.path
  const target = (legacyLinks as Record<string, string>)[path.replace(/\.html$/, '') + '#' + anchor]
  if (target) {
    void router.go(withBase(target))
    return true
  }
}
onMounted(async () => {
  if (followLegacyAnchor()) return
  const params = new URLSearchParams(window.location.search)
  query.value = params.get('q') ?? ''
  const initialGroup = params.get('group') ?? ''
  if (groups.value.includes(initialGroup)) group.value = initialGroup
  await nextTick()
  const initialPage = Number(params.get('page'))
  if (Number.isInteger(initialPage) && initialPage > 0) page.value = Math.min(initialPage, pages.value)
  ready.value = true
})
// Filters remain shareable and survive returning from a detail page.
watch([query, group, page], () => {
  const url = new URL(window.location.href)
  for (const [key, value] of [['q', query.value], ['group', group.value], ['page', page.value > 1 ? String(page.value) : '']]) {
    if (value) url.searchParams.set(key, value)
    else url.searchParams.delete(key)
  }
  window.history.replaceState(window.history.state, '', url)
})
</script>

<template>
  <section class="entry-catalog" :aria-label="label" :aria-busy="!ready">
    <div class="catalog-controls">
      <label class="catalog-search">
        {{ hasGameIds ? '搜索名称、ID 或效果' : '搜索名称或关键词' }}
        <input v-model="query" type="search" :disabled="!ready" :placeholder="hasGameIds ? '例如：硫磺火、Brimstone、c118、飞行' : '中文名、英文名或关键词'" autocomplete="off" />
      </label>
      <label>
        类型
        <select v-model="group" :disabled="!ready">
          <option value="">全部类型</option>
          <option v-for="name in groups" :key="name" :value="name">{{ name }}</option>
        </select>
      </label>
      <button v-if="query || group" class="ib-btn reset" type="button" :disabled="!ready" @click="query = ''; group = ''">清除筛选</button>
    </div>
    <p class="catalog-count" role="status" aria-live="polite">
      {{ matches.length }} 个条目<template v-if="pages > 1"> · 第 {{ page }} / {{ pages }} 页</template>
    </p>
    <ul v-if="visible.length" class="catalog-grid">
      <li v-for="entry in visible" :key="entry.id" class="catalog-card">
        <span v-for="alias in legacy ? entry.aliases : []" :id="alias" :key="alias" class="legacy-anchor" />
        <a :href="withBase(entry.link)" :aria-label="`${entry.name} · ${entry.group}`">
          <div class="card-top">
            <span class="card-icon"><GameIcon :name="entry.icon" :size="30" /></span>
            <span class="card-type">{{ entry.group }}</span>
            <code v-if="entry.gameId !== undefined">{{ entry.id }}</code>
          </div>
          <strong class="card-name">{{ entry.name }}</strong>
          <span v-if="entry.en" class="card-english">{{ entry.en }}</span>
          <span class="card-summary">{{ entry.summary }}</span>
          <span class="card-open">查看详情 <span aria-hidden="true">→</span></span>
        </a>
      </li>
    </ul>
    <div v-else class="empty-state">
      没有找到匹配条目。试试英文名、短关键词，或清除类型筛选。
    </div>
    <nav v-if="pages > 1" class="catalog-pagination" aria-label="条目分页">
      <button class="ib-btn" type="button" :disabled="!ready || page === 1" @click="goPage(page - 1)">上一页</button>
      <span>{{ page }} / {{ pages }}</span>
      <button class="ib-btn" type="button" :disabled="!ready || page === pages" @click="goPage(page + 1)">下一页</button>
    </nav>
  </section>
</template>

<style scoped>
.entry-catalog { margin: 18px 0 32px; }
.catalog-controls { display: flex; flex-wrap: wrap; align-items: end; gap: 12px; padding: 16px; border: 2px solid var(--ib-outline); border-radius: 10px; background: var(--ib-paper); }
.catalog-controls label { display: flex; flex-direction: column; gap: 6px; flex: 1 1 140px; font-size: 13px; font-weight: 700; }
.catalog-controls .catalog-search { flex: 3 1 250px; }
input, select { width: 100%; min-width: 0; padding: 10px 12px; border: 2px solid var(--ib-outline); border-radius: 7px; color: var(--vp-c-text-1); background: var(--ib-paper); font-size: 15px; }
input:focus-visible, select:focus-visible, .catalog-card a:focus-visible { outline: 3px solid var(--vp-c-brand-1); outline-offset: 3px; }
.reset { min-height: 44px; }
.catalog-count { font-size: 14px; color: var(--ib-ink-3); }
.catalog-grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; list-style: none; margin: 0 !important; padding: 0 !important; }
.catalog-card { min-width: 0; margin: 0 !important; border: 2px solid var(--ib-outline); border-radius: 12px; background: var(--ib-paper); box-shadow: 0 3px 0 var(--ib-outline); transition: transform .15s; }
.catalog-card:hover { transform: translateY(-2px); }
.catalog-card a { display: flex; flex-direction: column; gap: 6px; height: 100%; padding: 16px; text-decoration: none !important; color: inherit !important; border-radius: inherit; overflow-wrap: anywhere; }
.card-top { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; font-size: 12px; }
.card-icon { display: grid; place-items: center; width: 40px; height: 40px; flex-shrink: 0; background: var(--ib-gold-soft); border-radius: 9px; }
.card-type { color: var(--ib-ink-3); }
.card-top code { margin-left: auto; white-space: nowrap; }
.card-name { font-family: var(--ib-font-display); font-size: 23px; line-height: 1.4; color: var(--ib-ink); }
.card-english { font-size: 12px; line-height: 1.5; color: var(--ib-ink-3); }
.card-summary { display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; margin-top: 4px; font-size: 14px; line-height: 1.65; }
.card-open { margin-top: auto; padding-top: 12px; color: var(--vp-c-brand-1); font-size: 13px; font-weight: 700; }
.legacy-anchor { display: block; height: 0; scroll-margin-top: 90px; }
.catalog-pagination { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 16px; margin-top: 24px; font-size: 14px; }
button:disabled { cursor: default; opacity: .5; }
.empty-state { border: 2px dashed var(--ib-line); border-radius: 10px; padding: 24px; }
@media (max-width: 640px) {
  .catalog-grid { grid-template-columns: minmax(0, 1fr); }
  .catalog-controls { padding: 12px; }
  .catalog-card a { padding: 14px; }
}
@media (prefers-reduced-motion: reduce) { .catalog-card { transition: none; } }
</style>
