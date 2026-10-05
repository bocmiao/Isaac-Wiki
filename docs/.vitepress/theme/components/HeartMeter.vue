<script setup lang="ts">
import { computed, useId } from 'vue'

// 用游戏里的红心容器表示进度：每颗心 = 1/hearts，支持半颗心
const props = withDefaults(defineProps<{ value: number; hearts?: number; size?: number; label?: string }>(), {
  hearts: 12,
  size: 24,
})

const halves = computed(() => Math.round(Math.max(0, Math.min(1, props.value)) * props.hearts * 2))
const states = computed(() =>
  Array.from({ length: props.hearts }, (_, i) => {
    const left = halves.value - i * 2
    return left >= 2 ? 'full' : left === 1 ? 'half' : 'empty'
  }),
)
const uid = useId()
const path =
  'M16 27.5S5.5 21 3.6 14.6C2.3 10.2 5 5.8 9.4 5.6c2.9-.1 5 1.6 6.6 4 1.6-2.4 3.7-4.1 6.6-4 4.4.2 7.1 4.6 5.8 9C26.5 21 16 27.5 16 27.5z'
</script>

<template>
  <div class="hearts" role="img" :aria-label="label ?? `进度 ${Math.round(value * 100)}%`">
    <svg v-for="(s, i) in states" :key="i" viewBox="0 0 32 32" :width="size" :height="size" class="heart">
      <defs>
        <clipPath :id="`hm-${uid}-${i}`"><rect x="0" y="0" width="16" height="32" /></clipPath>
      </defs>
      <path :d="path" class="empty" />
      <path v-if="s !== 'empty'" :d="path" class="fill" :clip-path="s === 'half' ? `url(#hm-${uid}-${i})` : undefined" />
      <path :d="path" class="outline" />
      <ellipse v-if="s !== 'empty'" cx="9.6" cy="11.2" rx="1.8" ry="2.8" class="shine" transform="rotate(-30 9.6 11.2)" />
    </svg>
  </div>
</template>

<style scoped>
.hearts {
  display: flex;
  flex-wrap: wrap;
  gap: 1px;
}
.empty {
  fill: var(--ib-heart-empty);
}
.fill {
  fill: #d8302a;
}
.outline {
  fill: none;
  stroke: var(--ib-heart-stroke);
  stroke-width: 2.4;
  stroke-linejoin: round;
}
.shine {
  fill: #fff;
  opacity: 0.75;
}
</style>
