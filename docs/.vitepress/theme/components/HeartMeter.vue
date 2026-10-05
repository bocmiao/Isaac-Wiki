<script setup lang="ts">
import { computed } from 'vue'

// 用游戏里的红心表示进度：每颗心 = 1/total，支持半颗心
const props = withDefaults(defineProps<{ value: number; hearts?: number; label?: string }>(), {
  hearts: 12,
})

const halves = computed(() => Math.round(Math.max(0, Math.min(1, props.value)) * props.hearts * 2))
const states = computed(() =>
  Array.from({ length: props.hearts }, (_, i) => {
    const left = halves.value - i * 2
    return left >= 2 ? 'full' : left === 1 ? 'half' : 'empty'
  }),
)
const path = 'M12 20.5s-7.2-4.5-9.4-9A5.2 5.2 0 0 1 12 6.2a5.2 5.2 0 0 1 9.4 5.3c-2.2 4.5-9.4 9-9.4 9z'
</script>

<template>
  <div class="hearts" role="img" :aria-label="label ?? `进度 ${Math.round(value * 100)}%`">
    <svg v-for="(s, i) in states" :key="i" viewBox="0 0 24 24" class="heart" :class="s">
      <defs>
        <clipPath :id="`half-${i}`"><rect x="0" y="0" width="12" height="24" /></clipPath>
      </defs>
      <path :d="path" class="shell" />
      <path v-if="s === 'full'" :d="path" class="fill" />
      <path v-if="s === 'half'" :d="path" class="fill" :clip-path="`url(#half-${i})`" />
    </svg>
  </div>
</template>

<style scoped>
.hearts {
  display: flex;
  flex-wrap: wrap;
  gap: 2px;
}
.heart {
  width: 22px;
  height: 22px;
}
.shell {
  fill: var(--ib-paper-3);
  stroke: var(--ib-ink);
  stroke-width: 1.6;
  stroke-linejoin: round;
}
.fill {
  fill: var(--ib-blood);
}
</style>
