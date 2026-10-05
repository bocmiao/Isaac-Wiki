<script setup lang="ts">
// 首页插图：仿游戏小地图。每个房间是一个格子，特殊房间带图标。
type Kind = 'start' | 'room' | 'treasure' | 'shop' | 'boss' | 'secret' | 'here'
const rooms: { x: number; y: number; kind: Kind }[] = [
  { x: 2, y: 2, kind: 'start' },
  { x: 1, y: 2, kind: 'room' },
  { x: 0, y: 2, kind: 'treasure' },
  { x: 3, y: 2, kind: 'room' },
  { x: 3, y: 1, kind: 'here' },
  { x: 4, y: 1, kind: 'shop' },
  { x: 2, y: 3, kind: 'room' },
  { x: 2, y: 4, kind: 'room' },
  { x: 3, y: 4, kind: 'room' },
  { x: 4, y: 4, kind: 'boss' },
  { x: 1, y: 3, kind: 'secret' },
  { x: 1, y: 1, kind: 'room' },
  { x: 1, y: 0, kind: 'room' },
]
const W = 52
const H = 44
const G = 8
const px = (x: number) => 14 + x * (W + G)
const py = (y: number) => 14 + y * (H + G)
</script>

<template>
  <svg class="map" viewBox="0 0 320 276" role="img" aria-label="仿游戏小地图的插图">
    <g v-for="(r, i) in rooms" :key="i" :class="['room', r.kind]">
      <rect :x="px(r.x)" :y="py(r.y)" :width="W" :height="H" rx="6" />
      <!-- 宝箱房：皇冠 -->
      <path
        v-if="r.kind === 'treasure'"
        :d="`M${px(r.x) + 14} ${py(r.y) + 30}l3 -14l7 8l2 -10l2 10l7 -8l3 14z`"
        class="icon"
      />
      <!-- 商店：$ -->
      <text v-if="r.kind === 'shop'" :x="px(r.x) + W / 2" :y="py(r.y) + 30" class="glyph">$</text>
      <!-- Boss 房：骷髅 -->
      <g v-if="r.kind === 'boss'" class="skull">
        <circle :cx="px(r.x) + W / 2" :cy="py(r.y) + 19" r="10" />
        <rect :x="px(r.x) + W / 2 - 6" :y="py(r.y) + 25" width="12" height="8" rx="2" />
        <circle :cx="px(r.x) + W / 2 - 4" :cy="py(r.y) + 19" r="2.6" class="eye" />
        <circle :cx="px(r.x) + W / 2 + 4" :cy="py(r.y) + 19" r="2.6" class="eye" />
      </g>
      <!-- 当前位置 -->
      <circle v-if="r.kind === 'here'" :cx="px(r.x) + W / 2" :cy="py(r.y) + H / 2" r="7" class="pulse" />
      <circle v-if="r.kind === 'here'" :cx="px(r.x) + W / 2" :cy="py(r.y) + H / 2" r="5" class="me" />
    </g>
  </svg>
</template>

<style scoped>
.map {
  width: 100%;
  max-width: 340px;
  filter: drop-shadow(0 10px 24px rgba(43, 35, 32, 0.18));
}
.room rect {
  fill: var(--ib-paper-3);
  stroke: var(--ib-ink);
  stroke-width: 2;
}
.room.start rect,
.room.here rect {
  fill: var(--vp-c-bg-elv);
}
.room.secret rect {
  fill: transparent;
  stroke-dasharray: 5 4;
  stroke: var(--ib-ink-3);
}
.room.boss rect {
  fill: var(--ib-blood-soft);
  stroke: var(--ib-blood);
}
.room.treasure rect {
  fill: var(--ib-gold-soft);
  stroke: var(--ib-gold);
}
.icon {
  fill: var(--ib-gold);
}
.glyph {
  font-size: 22px;
  font-weight: 800;
  text-anchor: middle;
  fill: var(--ib-ink);
}
.skull circle,
.skull rect {
  fill: var(--ib-blood);
}
.skull .eye {
  fill: var(--ib-paper);
}
.me {
  fill: var(--ib-blood);
}
.pulse {
  fill: none;
  stroke: var(--ib-blood);
  stroke-width: 2;
  transform-box: fill-box;
  transform-origin: center;
  animation: pulse 1.8s ease-out infinite;
}
@keyframes pulse {
  from {
    opacity: 0.8;
    transform: scale(1);
  }
  to {
    opacity: 0;
    transform: scale(2.4);
  }
}
@media (prefers-reduced-motion: reduce) {
  .pulse {
    animation: none;
  }
}
</style>
