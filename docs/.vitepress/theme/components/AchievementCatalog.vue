<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { withBase } from 'vitepress'
import achievements from '../data/achievements.json'
import { parseAchievementIds as parseIds } from '../tools/achievements'

// 全成就搜索 + 打勾。已完成的编号只存在访客自己的浏览器里，和解锁清单分开存。
const STORAGE_KEY = 'isaac-roadbook-achievements-v1'
const PAGE = 20

const query = ref('')
const version = ref('plus')
const category = ref('all')
const status = ref<'all' | 'todo' | 'done'>('all')
const shown = ref(PAGE)
const done = ref<Set<number>>(new Set())
const ready = ref(false)
const message = ref('')
const storageError = ref('')
const importMode = ref<'merge'|'replace'>('merge')
const fileInput = ref<HTMLInputElement>()

const groups = [...new Set(achievements.map((a) => a.group))].sort()
const total = computed(() => (version.value === 'plus' ? 641 : 637))
const doneCount = computed(() => [...done.value].filter((id) => id <= total.value).length)

const results = computed(() => {
  const terms = query.value.trim().toLocaleLowerCase().replace(/^#/, '').split(/\s+/).filter(Boolean)
  return achievements.filter(
    (a) =>
      (version.value === 'plus' || a.id <= 637) &&
      (category.value === 'all' || a.group === category.value) &&
      (status.value === 'all' || (status.value === 'done') === done.value.has(a.id)) &&
      terms.every((t) => `${a.id} ${a.name} ${a.conditionZh} ${a.group}`.toLocaleLowerCase().includes(t)),
  )
})
watch([query, version, category, status], () => {
  shown.value = PAGE
})
watch(query, () => {
  if (!ready.value) return
  const url = new URL(window.location.href)
  if (query.value) url.searchParams.set('q', query.value)
  else url.searchParams.delete('q')
  window.history.replaceState(window.history.state, '', url)
})

onMounted(() => {
  query.value = new URLSearchParams(window.location.search).get('q') ?? ''
  try {
    const ids = parseIds(JSON.parse(localStorage.getItem(STORAGE_KEY) ?? '[]'))
    if (ids) done.value = new Set(ids)
    else storageError.value = '保存的进度格式异常，未读取旧勾选；可以导入有效备份。'
  } catch {
    storageError.value = '无法读取本地进度；可以继续勾选并导出备份。'
  }
  ready.value = true
})

function save() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...done.value].sort((a, b) => a - b)))
    storageError.value = ''
  } catch {
    storageError.value = '浏览器不允许保存，刷新后本页新进度会丢失，请先导出备份。'
  }
}

function toggle(id: number) {
  const next = new Set(done.value)
  next.has(id) ? next.delete(id) : next.add(id)
  done.value = next
  save()
}

function exportJson() {
  const blob = new Blob([JSON.stringify({ v: 1, done: [...done.value].sort((a, b) => a - b) })], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = 'isaac-achievements.json'
  a.click()
  URL.revokeObjectURL(a.href)
}

async function importJson(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  try {
    if (file.size > 1024 * 1024) throw new Error()
    const ids = parseIds(JSON.parse(await file.text()))
    if (!ids) throw new Error()
    done.value = new Set(importMode.value==='merge'?[...done.value,...ids]:ids)
    save()
    message.value = `已核对 ${ids.length} 项，${importMode.value==='merge'?'合并':'替换'}后共 ${done.value.size} 项。`
  } catch {
    message.value = '文件格式不对，进度没有改动。'
  }
  ;(e.target as HTMLInputElement).value = ''
}
</script>

<template>
  <section class="achievement-catalog" aria-label="全成就查询">
    <div class="progress">
      <div class="bar" role="progressbar" :aria-valuenow="doneCount" aria-valuemin="0" :aria-valuemax="total">
        <span :style="{ width: `${(doneCount / total) * 100}%` }" />
      </div>
      <p>
        <b>已打勾 {{ ready ? doneCount : '–' }} / {{ total }}</b>
        <span class="hint">勾选只记在本浏览器，不会读取游戏存档。</span>
        <span class="io">
          <button type="button" class="link" @click="exportJson">导出</button>
          <label>导入方式<select v-model="importMode" aria-label="导入方式"><option value="merge">合并勾选</option><option value="replace">替换全部勾选</option></select></label>
          <button type="button" class="link" @click="fileInput?.click()">导入</button>
          <input ref="fileInput" type="file" accept="application/json" hidden @change="importJson" />
        </span>
      </p>
      <p v-if="message" class="msg" role="status">{{ message }}</p>
      <p v-if="storageError" class="msg" role="alert">{{ storageError }}</p>
    </div>

    <div class="filters">
      <label class="wide">查找成就<input v-model="query" type="search" :disabled="!ready" placeholder="编号、英文名称、角色或中文条件" /></label>
      <label>版本<select v-model="version" :disabled="!ready"><option value="plus">忏悔+ · 641 项</option><option value="rep">忏悔 · 637 项</option></select></label>
      <label>分类<select v-model="category" :disabled="!ready"><option value="all">全部分类</option><option v-for="g in groups" :key="g" :value="g">{{ g }}</option></select></label>
      <label>状态<select v-model="status" :disabled="!ready"><option value="all">全部</option><option value="todo">只看未完成</option><option value="done">只看已完成</option></select></label>
    </div>
    <p role="status" aria-live="polite" class="count">
      找到 {{ results.length }} 项<template v-if="results.length > shown">，先显示前 {{ shown }} 项</template>。点名称看做法，点左边方框打勾。
    </p>
    <p v-if="!results.length">没有匹配的成就。试试编号、英文名，或清空筛选条件。</p>
    <div v-else class="results">
      <article v-for="a in results.slice(0, shown)" :key="a.id" class="achievement" :class="{ done: done.has(a.id) }">
        <button type="button" class="check" :aria-pressed="done.has(a.id)" :aria-label="`#${a.id} ${done.has(a.id) ? '取消完成' : '标记完成'}`" @click="toggle(a.id)">
          <svg v-if="done.has(a.id)" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5l3.2 3L13 4.5" /></svg>
        </button>
        <div>
          <a :href="withBase(`/achievements/${a.page}#achievement-${a.id}`)"><strong>#{{ a.id }} · {{ a.name }}</strong></a>
          <p>{{ a.conditionZh }}</p>
          <small>{{ a.group }} · {{ a.minimum }}加入</small>
        </div>
      </article>
      <button v-if="results.length > shown" type="button" class="more ib-btn" @click="shown += 40">
        再显示 {{ Math.min(40, results.length - shown) }} 项（还有 {{ results.length - shown }} 项）
      </button>
    </div>
  </section>
</template>

<style scoped>
.progress {
  margin-bottom: 16px;
}
.bar {
  height: 14px;
  border: 2px solid var(--ib-outline);
  border-radius: 999px;
  background: var(--ib-paper-2, var(--ib-paper));
  overflow: hidden;
}
.bar span {
  display: block;
  height: 100%;
  background: var(--ib-blood);
  transition: width 0.2s;
}
.progress p {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 4px 12px;
  margin: 8px 0 0;
  font-size: 14px;
}
.hint {
  color: var(--ib-ink-3);
  font-size: 13px;
}
.io {
  flex-wrap: wrap;
  align-items: center;
  margin-left: auto;
  display: flex;
  gap: 12px;
}
.link {
  color: var(--vp-c-brand-1);
  font-weight: 700;
  text-decoration: underline;
}
.msg {
  color: var(--ib-blood);
}
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1 1 120px;
  font-size: 14px;
}
label.wide {
  flex: 3 1 240px;
}
input,
select {
  border: 2px solid var(--ib-outline);
  border-radius: 6px;
  padding: 8px;
  background: var(--ib-paper);
  color: var(--vp-c-text-1);
  width: 100%;
  min-width: 0;
}
input:focus-visible,
select:focus-visible,
.check:focus-visible {
  outline: 2px solid var(--vp-c-brand-1);
  outline-offset: 2px;
}
.count {
  font-size: 14px;
  color: var(--ib-ink-3);
}
.results {
  display: grid;
  gap: 10px;
}
.achievement {
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: 12px;
  align-items: start;
  border: 2px solid var(--ib-outline);
  border-radius: 8px;
  padding: 12px 16px;
  background: var(--ib-paper);
  overflow-wrap: anywhere;
}
.achievement.done {
  opacity: 0.62;
}
.achievement.done strong {
  text-decoration: line-through;
}
.achievement a {
  text-decoration: none;
}
.achievement p {
  margin: 4px 0;
}
.achievement small {
  color: var(--vp-c-text-2);
}
.check {
  width: 26px;
  height: 26px;
  margin-top: 1px;
  border: 2px solid var(--ib-outline);
  border-radius: 5px;
  background: var(--vp-c-bg);
  display: grid;
  place-items: center;
}
.done .check {
  background: var(--ib-blood);
}
.check svg {
  width: 18px;
  height: 18px;
  fill: none;
  stroke: var(--ib-on-dark);
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}
.more {
  justify-self: center;
}
</style>
