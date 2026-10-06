<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { withBase } from 'vitepress'
import { characters, marks, taintedUnlock, taintedName, characterGuide, characterUnlockGuide } from '../data/characters'
import { emptyProgress, loadProgress, parseProgress, mergeProgress, saveProgress, summarize, totalMarks, type MarkState, type Progress } from '../progress'
import GameIcon from './GameIcon.vue'
import HeartMeter from './HeartMeter.vue'

// 进度只存在访客自己的浏览器里；隐私模式下读写失败也能正常使用（只是不保存）
const state = reactive<Progress>(emptyProgress())
const tab = ref<'chars' | 'marks'>('chars')
const showTainted = ref(false)
const saveOk = ref(true)
const loaded = ref(false)
const importMode=ref<'merge'|'replace'>('merge')

function apply(data: Progress) {
  state.chars = { ...data.chars, isaac: true }
  state.tainted = { ...data.tainted }
  state.marks = { ...data.marks }
}

onMounted(() => {
  const saved = loadProgress()
  if (saved) apply(saved)
  loaded.value = true
})

watch(
  state,
  () => {
    if (loaded.value) saveOk.value = saveProgress(state)
  },
  { deep: true },
)

const markKey = (charId: string, tainted: boolean, markId: string) => `${charId}${tainted ? '-t' : ''}:${markId}`
function cycle(key: string) {
  const next = (((state.marks[key] ?? 0) + 1) % 3) as MarkState
  if (next === 0) delete state.marks[key]
  else state.marks[key] = next
}

const stats = computed(() => summarize(state))

const rows = computed(() => {
  const base = characters.map((c) => ({ ...c, tainted: false, label: c.name }))
  if (!showTainted.value) return base
  return [...base, ...characters.map((c) => ({ ...c, tainted: true, label: taintedName(c) }))]
})

function markLabel(markId: string, state: MarkState = 0) {
  if (state === 0) return '未完成'
  if (markId === 'greed') return state === 1 ? '贪婪模式' : '极贪模式'
  return state === 1 ? '普通' : '困难'
}

function rowHard(charId: string, tainted: boolean) {
  return marks.filter((m) => state.marks[markKey(charId, tainted, m.id)] === 2).length
}

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
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return
  try {
    if(file.size>1024*1024)throw new Error('oversized')
    const data = parseProgress(JSON.parse(await file.text()))
    if (!data) throw new Error('invalid progress')
    apply(importMode.value==='merge'?mergeProgress(state,data):data)
  } catch {
    alert('导入失败：文件不是以撒路书导出的进度文件。')
  }
  input.value = ''
}

function reset() {
  if (confirm('确定清空全部进度吗？建议先导出备份。')) apply(emptyProgress())
}
</script>

<template>
  <div class="tracker">
    <!-- 状态栏 -->
    <div class="hud sketch">
      <div class="meter">
        <div class="meter-label">总进度 {{ Math.round(stats.overall * 100) }}%</div>
        <HeartMeter :value="stats.overall" :hearts="12" :size="28" />
      </div>
      <ul class="counts">
        <li>
          <GameIcon name="face" :size="30" />
          <span><b>{{ stats.unlocked }}</b>/{{ characters.length }}<small>角色</small></span>
        </li>
        <li>
          <GameIcon name="face-dark" :size="30" />
          <span><b>{{ stats.tainted }}</b>/{{ characters.length }}<small>里角色</small></span>
        </li>
        <li>
          <GameIcon name="trophy" :size="30" />
          <span><b>{{ stats.marksDone }}</b>/{{ totalMarks }}<small>完成标记</small></span>
        </li>
      </ul>
    </div>

    <!-- 标签页与操作 -->
    <div class="toolbar">
      <div class="tabs" role="tablist">
        <button role="tab" class="sketch" :aria-selected="tab === 'chars'" :class="{ on: tab === 'chars' }" @click="tab = 'chars'">
          <GameIcon name="key" :size="18" />角色解锁
        </button>
        <button role="tab" class="sketch" :aria-selected="tab === 'marks'" :class="{ on: tab === 'marks' }" @click="tab = 'marks'">
          <GameIcon name="skull" :size="18" />完成标记
        </button>
      </div>
      <div class="io">
        <label>导入方式<select v-model="importMode" aria-label="导入方式"><option value="merge">合并进度</option><option value="replace">替换全部进度</option></select></label>
        <button class="ghost" @click="exportJson">导出</button>
        <button class="ghost" @click="fileInput?.click()">导入</button>
        <button class="ghost danger" @click="reset">清空</button>
        <input ref="fileInput" type="file" accept="application/json" hidden @change="importJson" />
      </div>
    </div>
    <p v-if="!saveOk" class="warn">当前浏览器不允许保存数据，刷新后进度会丢失。可以用「导出」手动备份。</p>

    <!-- 角色解锁 -->
    <div v-show="tab === 'chars'" class="char-list">
      <div v-for="c in characters" :key="c.id" class="char sketch" :class="{ done: state.chars[c.id] }">
        <label class="char-main">
          <input v-model="state.chars[c.id]" type="checkbox" :disabled="c.id === 'isaac'" />
          <span class="box" aria-hidden="true" />
          <span class="char-body">
            <span class="char-name">{{ c.name }} <small>{{ c.en }}</small></span>
            <span class="char-cond">{{ c.unlock }}</span>
          </span>
        </label>
        <div class="char-actions">
          <a :href="withBase(characterUnlockGuide(c))" :aria-label="`${c.name}获取方式`">表获取</a>
          <a :href="withBase(characterUnlockGuide(c, true))" :aria-label="`${taintedName(c)}获取方式`">里获取</a>
          <a :href="withBase(characterGuide(c))" :aria-label="`${c.name}攻略`">表攻略</a>
          <a :href="withBase(characterGuide(c, true))" :aria-label="`${taintedName(c)}攻略`">里攻略</a>
        </div>
        <label class="t-label" :class="{ on: state.tainted[c.id] }" :title="`${taintedName(c)}已解锁`">
          <input v-model="state.tainted[c.id]" type="checkbox" :aria-label="`${taintedName(c)}已解锁`" />
          里
        </label>
      </div>
      <p class="hint"><b>「里」</b>表示对应的里角色已解锁。解锁方法：{{ taintedUnlock }}。</p>
    </div>

    <!-- 完成标记 -->
    <div v-show="tab === 'marks'">
      <div class="legend">
        <span><i class="cell s0" />未完成</span>
        <span><i class="cell s1" />普通</span>
        <span><i class="cell s2" />困难</span>
        <span class="legend-tip">点击格子切换状态；贪婪列：普通 = 贪婪，困难 = 极贪</span>
        <label class="switch"><input v-model="showTainted" type="checkbox" /> 显示里角色</label>
      </div>
      <p class="hint">合计记录已完成的格数；困难 / 极贪另列计数。里角色的组合奖励要凑齐对应一组，单独完成其中一格不代表奖励已解锁。<a :href="withBase('/strategy/completion-marks')">查看十二格与奖励规则</a>；点角色名查看本角色奖励表。</p>
      <div class="grid-wrap">
        <table class="mark-grid">
          <thead>
            <tr>
              <th class="sticky">角色</th>
              <th v-for="m in marks" :key="m.id" :title="`${m.name}（${m.en}）`">{{ m.short }}</th>
              <th>已完成</th>
              <th>困难 / 极贪</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="r in rows" :key="r.id + r.tainted" :class="{ tainted: r.tainted }">
              <th class="sticky"><a :href="withBase(characterGuide(r, r.tainted) + '#completion-rewards')">{{ r.label }}</a></th>
              <td v-for="m in marks" :key="m.id">
                <button
                  class="cell"
                  :class="`s${state.marks[markKey(r.id, r.tainted, m.id)] ?? 0}`"
                  :aria-label="`${r.label} · ${m.name} · ${markLabel(m.id, state.marks[markKey(r.id, r.tainted, m.id)])}`"
                  :title="`${r.label} · ${m.name} · ${markLabel(m.id, state.marks[markKey(r.id, r.tainted, m.id)])}`"
                  @click="cycle(markKey(r.id, r.tainted, m.id))"
                />
              </td>
              <td class="sum">{{ rowDone(r.id, r.tainted) }}/{{ marks.length }}</td>
              <td class="sum">{{ rowHard(r.id, r.tainted) }}/{{ marks.length }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<style scoped>
.tracker {
  margin-top: 8px;
}
button {
  font: inherit;
  cursor: pointer;
}
.hud {
  --sk-shadow: 0 5px 0 var(--ib-outline);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 18px 28px;
  padding: 18px 22px;
  border-radius: 12px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 5px 0 var(--ib-outline);
}
.meter-label {
  font-size: 13px;
  font-weight: 800;
  color: var(--ib-ink-2);
  margin-bottom: 4px;
}
.counts {
  list-style: none;
  display: flex;
  gap: 22px;
  margin: 0;
  padding: 0;
}
.counts li {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--ib-ink-3);
  font-size: 13px;
}
.counts b {
  font-family: var(--ib-font-display);
  font-size: 30px;
  font-weight: 400;
  color: var(--ib-ink);
}
.counts small {
  display: block;
  font-size: 12px;
  font-weight: 700;
}
.toolbar {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin: 26px 0 14px;
}
.tabs {
  display: inline-flex;
  gap: 6px;
}
.tabs button {
  --sk-bw: 2px;
  --sk-bg: var(--ib-paper-2);
  --sk-shadow: 0 3px 0 var(--ib-outline);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 10px;
  font-family: var(--ib-font-display);
  font-size: 17px;
  color: var(--ib-ink-2);
}
.tabs button.on {
  --sk-bg: var(--ib-blood-btn);
  color: var(--ib-on-dark);
}
.io {
  flex-wrap: wrap;
  align-items: center;
  display: flex;
  gap: 6px;
}
.ghost {
  border: 2px solid var(--ib-line);
  background: transparent;
  color: var(--ib-ink-2);
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 13px;
  font-weight: 700;
}
.ghost:hover {
  border-color: var(--ib-outline);
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
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.char {
  --sk-bw: 2px;
  --sk-shadow: 0 3px 0 var(--ib-outline);
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 12px;
  align-items: center;
  padding: 12px 14px;
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2px solid var(--ib-outline);
  box-shadow: 0 3px 0 var(--ib-outline);
}
.char.done {
  --sk-bg: var(--ib-paper-2);
}
.char-actions {
  grid-column: 1;
  grid-row: 2;
  display: flex;
  gap: 6px 16px;
  flex-wrap: wrap;
  padding-left: 38px;
  font-size: 13px;
}
.char-main {
  grid-column: 1;
  grid-row: 1;
  position: relative;
  display: grid;
  grid-template-columns: 26px 1fr;
  gap: 12px;
  align-items: center;
  cursor: pointer;
}
.char-main > input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.box {
  position: relative;
  width: 24px;
  height: 24px;
  border-radius: 6px;
  border: 2.5px solid var(--ib-outline);
  background: var(--ib-floor);
}
.char.done .box {
  background: #d8302a;
}
.char.done .box::after {
  content: '';
  position: absolute;
  left: 6px;
  top: 1px;
  width: 6px;
  height: 12px;
  border: solid #fff8ef;
  border-width: 0 3px 3px 0;
  transform: rotate(45deg);
}
.char-main > input:focus-visible + .box {
  outline: 3px solid var(--ib-soul);
  outline-offset: 2px;
}
.char-body {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.char-name {
  font-family: var(--ib-font-display);
  font-size: 18px;
  letter-spacing: 0.03em;
  color: var(--ib-ink);
}
.char-name small {
  font-family: var(--vp-font-family-base);
}
.char-name small {
  font-weight: 500;
  color: var(--ib-ink-3);
  margin-left: 4px;
}
.char-cond {
  font-size: 13.5px;
  color: var(--ib-ink-2);
  line-height: 1.6;
}
.char.done .char-cond {
  color: var(--ib-ink-3);
  text-decoration: line-through;
  text-decoration-color: rgba(216, 48, 42, 0.5);
}
.t-label {
  grid-column: 2;
  grid-row: 1 / 3;
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 2px dashed var(--ib-ink-3);
  font-weight: 900;
  color: var(--ib-ink-3);
  cursor: pointer;
}
.t-label input {
  position: absolute;
  opacity: 0;
  pointer-events: none;
}
.t-label.on {
  border: 2px solid var(--ib-outline);
  background: #6a5874;
  color: #f4e8d0;
}
.t-label:has(input:focus-visible) {
  outline: 3px solid var(--ib-soul);
  outline-offset: 2px;
}
.hint {
  grid-column: 1 / -1;
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
  font-weight: 700;
  color: var(--ib-ink-2);
  margin-bottom: 12px;
}
.legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.legend .cell {
  width: 18px;
  height: 18px;
  cursor: default;
}
.legend-tip {
  font-weight: 500;
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
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 4px 0 var(--ib-outline);
}
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
  font-family: var(--ib-font-display);
  font-size: 14px;
  font-weight: 400;
  color: var(--ib-on-dark);
  white-space: nowrap;
  background: var(--ib-wall);
}
.mark-grid tbody th {
  text-align: left;
  font-family: var(--ib-font-display);
  font-size: 15px;
  font-weight: 400;
  color: var(--ib-ink);
  white-space: nowrap;
  padding-left: 12px;
}
.sticky {
  position: sticky;
  left: 0;
  background: var(--ib-paper) !important;
  z-index: 1;
}
thead .sticky {
  background: var(--ib-wall) !important;
}
tr.tainted th {
  color: var(--ib-ink-2);
}
.sum {
  font-size: 12px;
  font-weight: 700;
  color: var(--ib-ink-3);
  white-space: nowrap;
  padding-right: 12px !important;
}
.cell {
  display: inline-block;
  width: 26px;
  height: 26px;
  border-radius: 6px;
  border: 2px solid var(--ib-line);
  background: var(--ib-floor);
  padding: 0;
  vertical-align: middle;
  transition: transform 0.1s;
}
button.cell:hover {
  transform: scale(1.12);
  border-color: var(--ib-outline);
}
.cell.s1 {
  border: 2.5px solid #d8302a;
  background: var(--ib-blood-soft);
}
.cell.s2 {
  border: 2.5px solid var(--ib-outline);
  background: #d8302a;
}

@media (max-width: 760px) {
  .char-list {
    grid-template-columns: 1fr;
  }
  .counts {
    gap: 14px;
  }
  .switch {
    margin-left: 0;
  }
}
</style>
