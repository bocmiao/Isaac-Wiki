<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { characters, marks, taintedUnlock } from '../data/characters'
import HeartMeter from './HeartMeter.vue'

// 进度只存在访客自己的浏览器里；读写都包 try/catch，隐私模式下也能正常使用（只是不保存）
const STORAGE_KEY = 'isaac-roadbook-progress-v1'

type MarkState = 0 | 1 | 2 // 0 未完成 · 1 普通 · 2 困难
interface Progress {
  v: 1
  chars: Record<string, boolean>
  tainted: Record<string, boolean>
  marks: Record<string, MarkState>
}

const empty = (): Progress => ({ v: 1, chars: { isaac: true }, tainted: {}, marks: {} })
const state = reactive<Progress>(empty())
const tab = ref<'chars' | 'marks'>('chars')
const showTainted = ref(false)
const saveOk = ref(true)
const loaded = ref(false)

function apply(data: Partial<Progress>) {
  state.chars = { isaac: true, ...(data.chars ?? {}) }
  state.tainted = { ...(data.tainted ?? {}) }
  state.marks = { ...(data.marks ?? {}) }
}

onMounted(() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) apply(JSON.parse(raw))
  } catch {
    saveOk.value = false
  }
  loaded.value = true
})

watch(
  state,
  () => {
    if (!loaded.value) return
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state))
      saveOk.value = true
    } catch {
      saveOk.value = false
    }
  },
  { deep: true },
)

const markKey = (charId: string, tainted: boolean, markId: string) => `${charId}${tainted ? '-t' : ''}:${markId}`
function cycle(key: string) {
  const next = (((state.marks[key] ?? 0) + 1) % 3) as MarkState
  if (next === 0) delete state.marks[key]
  else state.marks[key] = next
}

const unlockedCount = computed(() => characters.filter((c) => state.chars[c.id]).length)
const taintedCount = computed(() => characters.filter((c) => state.tainted[c.id]).length)
const marksDone = computed(() => Object.values(state.marks).filter((v) => v > 0).length)
const totalMarks = characters.length * 2 * marks.length
const overall = computed(
  () => (unlockedCount.value + taintedCount.value + marksDone.value) / (characters.length * 2 + totalMarks),
)

const rows = computed(() => {
  const base = characters.map((c) => ({ ...c, tainted: false, label: c.name }))
  if (!showTainted.value) return base
  return [...base, ...characters.map((c) => ({ ...c, tainted: true, label: `里${c.name}` }))]
})

function rowDone(charId: string, tainted: boolean) {
  return marks.filter((m) => (state.marks[markKey(charId, tainted, m.id)] ?? 0) > 0).length
}

function exportJson() {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: 'application/json' })
  const a = document.createElement('a')
  a.href = URL.createObjectURL(blob)
  a.download = `以撒路书进度-${new Date().toISOString().slice(0, 10)}.json`
  a.click()
  URL.revokeObjectURL(a.href)
}

const fileInput = ref<HTMLInputElement>()
async function importJson(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  try {
    const data = JSON.parse(await file.text())
    if (data?.v !== 1) throw new Error('version')
    apply(data)
  } catch {
    alert('导入失败：文件不是以撒路书导出的进度文件。')
  }
  ;(e.target as HTMLInputElement).value = ''
}

function reset() {
  if (confirm('确定清空全部进度吗？建议先导出备份。')) apply(empty())
}
</script>

<template>
  <div class="tracker">
    <!-- 总进度 -->
    <div class="summary">
      <div class="meter">
        <div class="meter-label">总进度 {{ Math.round(overall * 100) }}%</div>
        <HeartMeter :value="overall" :hearts="12" />
      </div>
      <dl class="stats">
        <div>
          <dt>角色</dt>
          <dd>{{ unlockedCount }}<small>/{{ characters.length }}</small></dd>
        </div>
        <div>
          <dt>里角色</dt>
          <dd>{{ taintedCount }}<small>/{{ characters.length }}</small></dd>
        </div>
        <div>
          <dt>完成标记</dt>
          <dd>{{ marksDone }}<small>/{{ totalMarks }}</small></dd>
        </div>
      </dl>
    </div>

    <!-- 标签页 -->
    <div class="toolbar">
      <div class="tabs" role="tablist">
        <button role="tab" :aria-selected="tab === 'chars'" :class="{ on: tab === 'chars' }" @click="tab = 'chars'">
          角色解锁
        </button>
        <button role="tab" :aria-selected="tab === 'marks'" :class="{ on: tab === 'marks' }" @click="tab = 'marks'">
          完成标记
        </button>
      </div>
      <div class="io">
        <button class="ghost" @click="exportJson">导出</button>
        <button class="ghost" @click="fileInput?.click()">导入</button>
        <button class="ghost danger" @click="reset">清空</button>
        <input ref="fileInput" type="file" accept="application/json" hidden @change="importJson" />
      </div>
    </div>
    <p v-if="!saveOk" class="warn">当前浏览器不允许保存数据，刷新后进度会丢失。可以用「导出」手动备份。</p>

    <!-- 角色解锁 -->
    <div v-show="tab === 'chars'" class="char-list">
      <div v-for="c in characters" :key="c.id" class="char" :class="{ done: state.chars[c.id] }">
        <label class="char-main">
          <input v-model="state.chars[c.id]" type="checkbox" :disabled="c.id === 'isaac'" />
          <span class="box" aria-hidden="true" />
          <span class="char-body">
            <span class="char-name">{{ c.name }} <small>{{ c.en }}</small></span>
            <span class="char-cond">{{ c.unlock }}</span>
          </span>
        </label>
        <label class="t-label" :class="{ on: state.tainted[c.id] }" :title="`里${c.name}已解锁`">
          <input v-model="state.tainted[c.id]" type="checkbox" :aria-label="`里${c.name}已解锁`" />
          里
        </label>
      </div>
      <p class="hint">「里」= 对应的里角色是否已解锁。解锁方法：{{ taintedUnlock }}。</p>
    </div>

    <!-- 完成标记 -->
    <div v-show="tab === 'marks'">
      <div class="legend">
        <span><i class="cell s0" />未完成</span>
        <span><i class="cell s1" />普通</span>
        <span><i class="cell s2" />困难</span>
        <span class="legend-tip">点击格子切换状态</span>
        <label class="switch"><input v-model="showTainted" type="checkbox" /> 显示里角色</label>
      </div>
      <div class="grid-wrap">
        <table class="mark-grid">
          <thead>
            <tr>
              <th class="sticky">角色</th>
              <th v-for="m in marks" :key="m.id" :title="`${m.name}（${m.en}）`">{{ m.short }}</th>
              <th>合计</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id + r.tainted" :class="{ tainted: r.tainted }">
              <th class="sticky">{{ r.label }}</th>
              <td v-for="m in marks" :key="m.id">
                <button
                  class="cell"
                  :class="`s${state.marks[markKey(r.id, r.tainted, m.id)] ?? 0}`"
                  :aria-label="`${r.label} · ${m.name}`"
                  @click="cycle(markKey(r.id, r.tainted, m.id))"
                />
              </td>
              <td class="sum">{{ rowDone(r.id, r.tainted) }}/{{ marks.length }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tracker {
  margin-top: 16px;
}
button {
  font: inherit;
  cursor: pointer;
}
.summary {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 16px 24px;
  padding: 18px 20px;
  border: 2px solid var(--ib-ink);
  border-radius: 14px;
  background: var(--vp-c-bg-elv);
  box-shadow: 0 4px 0 var(--ib-ink);
}
.meter-label {
  font-size: 13px;
  font-weight: 700;
  color: var(--ib-ink-2);
  margin-bottom: 6px;
}
.stats {
  display: flex;
  gap: 24px;
  margin: 0;
}
.stats dt {
  font-size: 12px;
  color: var(--ib-ink-3);
}
.stats dd {
  margin: 0;
  font-size: 24px;
  font-weight: 800;
  color: var(--ib-ink);
  line-height: 1.2;
}
.stats small {
  font-size: 13px;
  font-weight: 500;
  color: var(--ib-ink-3);
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin: 24px 0 12px;
}
.tabs {
  display: inline-flex;
  padding: 4px;
  border-radius: 10px;
  background: var(--ib-paper-3);
}
.tabs button {
  border: none;
  background: transparent;
  padding: 6px 16px;
  border-radius: 8px;
  font-weight: 600;
  color: var(--ib-ink-2);
}
.tabs button.on {
  background: var(--vp-c-bg-elv);
  color: var(--ib-blood);
  box-shadow: var(--ib-shadow);
}
.io {
  display: flex;
  gap: 6px;
}
.ghost {
  border: 1px solid var(--ib-line);
  background: transparent;
  color: var(--ib-ink-2);
  padding: 5px 12px;
  border-radius: 8px;
  font-size: 13px;
}
.ghost:hover {
  border-color: var(--ib-ink-2);
  color: var(--ib-ink);
}
.ghost.danger:hover {
  border-color: var(--ib-blood);
  color: var(--ib-blood);
}
.warn {
  font-size: 13px;
  color: var(--ib-gold);
}

/* 角色列表 */
.char-list {
  display: grid;
  gap: 8px;
}
.char {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 12px 14px;
  border: 1px solid var(--ib-line);
  border-radius: 12px;
  background: var(--vp-c-bg-elv);
  transition: border-color 0.15s;
}
.char-main {
  display: grid;
  grid-template-columns: 24px 1fr;
  gap: 12px;
  align-items: center;
  cursor: pointer;
  position: relative;
}
.char:hover {
  border-color: var(--ib-ink-3);
}
.char-main > input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.box {
  width: 22px;
  height: 22px;
  border-radius: 6px;
  border: 2px solid var(--ib-ink);
  background: var(--ib-paper);
  position: relative;
}
.char.done .box {
  background: var(--ib-blood);
  border-color: var(--ib-blood);
}
.char.done .box::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 2px;
  width: 6px;
  height: 11px;
  border: solid #fff8ef;
  border-width: 0 2.5px 2.5px 0;
  transform: rotate(45deg);
}
.char-main > input:focus-visible + .box {
  outline: 2px solid var(--ib-soul);
  outline-offset: 2px;
}
.char-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.char-name {
  font-weight: 700;
  color: var(--ib-ink);
}
.char-name small {
  font-weight: 400;
  color: var(--ib-ink-3);
  margin-left: 4px;
}
.char-cond {
  font-size: 14px;
  color: var(--ib-ink-2);
  line-height: 1.6;
}
.char.done .char-cond {
  color: var(--ib-ink-3);
}
.t-label {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: 1.5px dashed var(--ib-ink-3);
  font-weight: 800;
  color: var(--ib-ink-3);
  cursor: pointer;
}
.t-label input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.t-label.on {
  border-style: solid;
  border-color: var(--ib-ink);
  background: var(--ib-ink);
  color: var(--ib-paper);
}
.t-label:has(input:focus-visible) {
  outline: 2px solid var(--ib-soul);
  outline-offset: 2px;
}
.hint {
  font-size: 13px;
  color: var(--ib-ink-3);
}

/* 完成标记表 */
.legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 16px;
  font-size: 13px;
  color: var(--ib-ink-2);
  margin-bottom: 12px;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.legend .cell {
  width: 16px;
  height: 16px;
  cursor: default;
}
.legend-tip {
  color: var(--ib-ink-3);
}
.switch {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
}
.grid-wrap {
  overflow-x: auto;
  border: 1px solid var(--ib-line);
  border-radius: 12px;
  background: var(--vp-c-bg-elv);
}
.vp-doc .mark-grid,
.mark-grid {
  display: table;
  width: 100%;
  margin: 0;
  border-collapse: collapse;
  font-size: 13px;
}
.mark-grid tr {
  background: transparent !important;
}
.mark-grid th,
.mark-grid td {
  border: none;
  border-bottom: 1px solid var(--ib-line);
  padding: 6px 4px;
  text-align: center;
  background: transparent;
}
.mark-grid thead th {
  font-size: 12px;
  font-weight: 600;
  color: var(--ib-ink-3);
  white-space: nowrap;
  background: var(--ib-paper-3);
}
.mark-grid tbody th {
  text-align: left;
  font-weight: 600;
  color: var(--ib-ink);
  white-space: nowrap;
  padding-left: 12px;
}
.sticky {
  position: sticky;
  left: 0;
  background: var(--vp-c-bg-elv) !important;
  z-index: 1;
}
thead .sticky {
  background: var(--ib-paper-3) !important;
}
tr.tainted th {
  color: var(--ib-ink-2);
}
.sum {
  font-size: 12px;
  color: var(--ib-ink-3);
  white-space: nowrap;
  padding-right: 12px !important;
}
.cell {
  display: inline-block;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 1.5px solid var(--ib-line);
  background: var(--ib-paper);
  padding: 0;
  vertical-align: middle;
  transition: transform 0.1s;
}
button.cell:hover {
  transform: scale(1.12);
  border-color: var(--ib-ink-3);
}
.cell.s1 {
  border: 2px solid var(--ib-blood);
  background: var(--ib-blood-soft);
}
.cell.s2 {
  border: 2px solid var(--ib-blood);
  background: var(--ib-blood);
}

@media (max-width: 640px) {
  .stats {
    gap: 16px;
  }
  .switch {
    margin-left: 0;
  }
}
</style>
