<script setup lang="ts">
import { computed } from 'vue'
import { stages } from '../data/stages'

// 阶段页顶部：显示当前在第几层，以及上下层的位置
const props = defineProps<{ floor: number }>()
const stage = computed(() => stages.find((s) => s.floor === props.floor)!)
</script>

<template>
  <div class="stage-header">
    <div class="floors" aria-hidden="true">
      <span v-for="s in stages" :key="s.floor" class="dot" :class="{ on: s.floor === floor, past: s.floor < floor }" />
    </div>
    <div class="eyebrow">第 {{ stage.floor }} 层 · {{ stage.place }}</div>
    <p class="summary">{{ stage.summary }}</p>
  </div>
</template>

<style scoped>
.stage-header {
  margin: 8px 0 24px;
  padding: 16px 18px;
  border: 1px solid var(--ib-line);
  border-radius: 12px;
  background: var(--vp-c-bg-elv);
  box-shadow: var(--ib-shadow);
}
.floors {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
}
.dot {
  width: 28px;
  height: 6px;
  border-radius: 3px;
  background: var(--ib-paper-3);
}
.dot.past {
  background: var(--ib-ink-3);
}
.dot.on {
  background: var(--ib-blood);
}
.eyebrow {
  font-size: 13px;
  font-weight: 700;
  color: var(--ib-blood);
  letter-spacing: 0.06em;
}
.summary {
  margin: 4px 0 0 !important;
  color: var(--ib-ink-2);
}
</style>
