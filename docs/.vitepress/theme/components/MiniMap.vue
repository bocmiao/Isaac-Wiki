<script setup lang="ts">
import { withBase } from 'vitepress'
import GameIcon, { type IconName } from './GameIcon.vue'

// 仿游戏右上角的小地图：每个房间对应站内的一个区域，点房间就能过去。
// 白色 = 当前房间（首页），灰色 = 去过的普通房间，深色虚线 = 隐藏房。
type Room = { x: number; y: number; label: string; link?: string; icon?: IconName; kind: 'here' | 'room' | 'special' | 'secret' }
const rooms: Room[] = [
  { x: 1, y: 1, label: '首页（你在这里）', kind: 'here' },
  { x: 1, y: 0, label: '新手路线', link: '/guide/', kind: 'room' },
  { x: 0, y: 1, label: '攻略库', link: '/strategy/', icon: 'crown', kind: 'special' },
  { x: 2, y: 1, label: '解锁清单', link: '/tools/tracker', icon: 'key', kind: 'special' },
  { x: 1, y: 2, label: '联机专题', link: '/topics/coop', icon: 'skull', kind: 'special' },
  { x: 2, y: 0, label: '配置与模组', link: '/topics/mods', kind: 'room' },
  { x: 3, y: 1, label: '主机专题', link: '/topics/console', kind: 'room' },
  { x: 0, y: 2, label: '关于（隐藏房）', link: '/about', kind: 'secret' },
]
const W = 30
const H = 24
const G = 4
</script>

<template>
  <nav class="minimap" aria-label="小地图：站内导航">
    <div class="grid" :style="{ width: `${4 * W + 3 * G}px`, height: `${3 * H + 2 * G}px` }">
      <component
        :is="r.link ? 'a' : 'span'"
        v-for="r in rooms"
        :key="r.label"
        class="room"
        :class="r.kind"
        :href="r.link ? withBase(r.link) : undefined"
        :title="r.label"
        :aria-label="r.label"
        :style="{ left: `${r.x * (W + G)}px`, top: `${r.y * (H + G)}px`, width: `${W}px`, height: `${H}px` }"
      >
        <GameIcon v-if="r.icon" :name="r.icon" :size="16" />
        <span v-if="r.kind === 'secret'" class="q">?</span>
      </component>
    </div>
  </nav>
</template>

<style scoped>
.minimap {
  padding: 8px;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.32);
}
.grid {
  position: relative;
}
.room {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 3px;
  background: #8f8a84;
  border: 2px solid #1a1512;
  transition: transform 0.12s, background 0.12s;
}
a.room:hover,
a.room:focus-visible {
  transform: scale(1.15);
  background: #e8e2d8;
  z-index: 1;
}
.room.here {
  background: #fbf7ef;
}
.room.special {
  background: #a9a39b;
}
.room.secret {
  background: rgba(0, 0, 0, 0.25);
  border-style: dashed;
  border-color: #8f8a84;
}
.q {
  font-family: var(--ib-font-display);
  font-size: 14px;
  color: #d9d3ca;
  line-height: 1;
}
</style>
