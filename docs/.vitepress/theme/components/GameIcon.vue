<script setup lang="ts">
// 游戏风图标：粗黑描边 + 平涂色块 + 一点高光。全部手写 SVG，不使用游戏原图素材。
export type IconName =
  | 'heart'
  | 'soul'
  | 'coin'
  | 'bomb'
  | 'key'
  | 'skull'
  | 'crown'
  | 'chest'
  | 'dice'
  | 'pill'
  | 'card'
  | 'tear'
  | 'trophy'
  | 'face'
  | 'face-dark'
  | 'gamepad'
  | 'wrench'
  | 'coop'
  | 'map'
  | 'rock'
  | 'poop'
  | 'lock'
  | 'eye'

withDefaults(defineProps<{ name: IconName; size?: number | string }>(), { size: 32 })
</script>

<template>
  <svg
    class="game-icon"
    viewBox="0 0 32 32"
    :width="size"
    :height="size"
    aria-hidden="true"
    stroke="var(--ib-outline)"
    stroke-width="2.2"
    stroke-linejoin="round"
    stroke-linecap="round"
  >
    <template v-if="name === 'heart' || name === 'soul'">
      <path
        d="M16 27.5S5.5 21 3.6 14.6C2.3 10.2 5 5.8 9.4 5.6c2.9-.1 5 1.6 6.6 4 1.6-2.4 3.7-4.1 6.6-4 4.4.2 7.1 4.6 5.8 9C26.5 21 16 27.5 16 27.5z"
        :fill="name === 'heart' ? '#d8302a' : '#7fa0e6'"
      />
      <ellipse cx="9.6" cy="11.2" rx="1.8" ry="2.8" fill="#fff" opacity=".75" stroke="none" transform="rotate(-30 9.6 11.2)" />
    </template>

    <template v-else-if="name === 'coin'">
      <circle cx="16" cy="16" r="11.5" fill="#e8b23a" />
      <circle cx="16" cy="16" r="7" fill="none" stroke="#9a6a0c" stroke-width="2" />
      <path d="M10.5 11.5a7 7 0 0 1 4-3" fill="none" stroke="#fff6d8" stroke-width="2" />
    </template>

    <template v-else-if="name === 'bomb'">
      <rect x="17.5" y="6.5" width="7" height="5" rx="1" fill="#6b6b74" transform="rotate(35 21 9)" />
      <circle cx="14.5" cy="19" r="10" fill="#45454d" />
      <path d="M23 6.5c1.5-3 4-3.5 6-2.5" fill="none" />
      <circle cx="29.2" cy="3.6" r="2" fill="#e8b23a" stroke="none" />
      <ellipse cx="10.5" cy="15" rx="2.2" ry="3.4" fill="#fff" opacity=".35" stroke="none" transform="rotate(30 10.5 15)" />
    </template>

    <template v-else-if="name === 'key'">
      <path d="M15.5 13.8h13a1 1 0 0 1 1 1v2.4a1 1 0 0 1-1 1H27v4h-3v-4h-1.5v3h-3v-3h-4z" fill="#d9dde3" />
      <circle cx="10" cy="16" r="6.8" fill="#d9dde3" />
      <circle cx="10" cy="16" r="2.4" fill="var(--ib-outline)" stroke="none" />
    </template>

    <template v-else-if="name === 'skull'">
      <rect x="10" y="18.5" width="12" height="9" rx="2.5" fill="#f1ead9" />
      <circle cx="16" cy="14" r="10.5" fill="#f1ead9" />
      <rect x="10.5" y="19" width="11" height="3" fill="#f1ead9" stroke="none" />
      <circle cx="11.8" cy="14.5" r="3.1" fill="var(--ib-outline)" stroke="none" />
      <circle cx="20.2" cy="14.5" r="3.1" fill="var(--ib-outline)" stroke="none" />
      <path d="M16 18.2l-1.4 2.4h2.8z" fill="var(--ib-outline)" stroke="none" />
      <path d="M14 24.5v3M18 24.5v3" fill="none" stroke-width="1.6" />
    </template>

    <template v-else-if="name === 'crown'">
      <path d="M5 23.5 6.8 9.5l5.8 6.3L16 6.5l3.4 9.3 5.8-6.3L27 23.5z" fill="#e8b23a" />
      <rect x="5" y="22" width="22" height="5" rx="1.2" fill="#c98e16" />
      <circle cx="16" cy="24.5" r="1.5" fill="#d8302a" stroke="none" />
      <circle cx="10" cy="24.5" r="1.2" fill="#7fa0e6" stroke="none" />
      <circle cx="22" cy="24.5" r="1.2" fill="#7fa0e6" stroke="none" />
    </template>

    <template v-else-if="name === 'chest'">
      <path d="M4 14c0-5 4-8 12-8s12 3 12 8z" fill="#c48a3c" />
      <rect x="4" y="14" width="24" height="13" rx="2" fill="#a8722e" />
      <path d="M4 14h24" fill="none" />
      <rect x="13.5" y="12" width="5" height="7" rx="1" fill="#e8b23a" />
      <path d="M9 8.5v18.5M23 8.5v18.5" fill="none" stroke="#7a4f1d" stroke-width="1.6" />
    </template>

    <template v-else-if="name === 'dice'">
      <rect x="5" y="5" width="22" height="22" rx="5" fill="#f6f1e6" />
      <g fill="var(--ib-outline)" stroke="none">
        <circle cx="11" cy="11" r="2.1" />
        <circle cx="21" cy="11" r="2.1" />
        <circle cx="11" cy="16" r="2.1" />
        <circle cx="21" cy="16" r="2.1" />
        <circle cx="11" cy="21" r="2.1" />
        <circle cx="21" cy="21" r="2.1" />
      </g>
    </template>

    <template v-else-if="name === 'pill'">
      <g transform="rotate(-35 16 16)">
        <path d="M16 11h-6a5 5 0 0 0 0 10h6z" fill="#e35d6a" />
        <path d="M16 11h6a5 5 0 0 1 0 10h-6z" fill="#f3efe6" />
        <path d="M8.5 14.5a2.5 2.5 0 0 1 2-1.5" fill="none" stroke="#fff" stroke-width="1.6" />
      </g>
    </template>

    <template v-else-if="name === 'card'">
      <rect x="7.5" y="3.5" width="17" height="25" rx="2.2" fill="#f4e8d0" />
      <rect x="10.5" y="6.5" width="11" height="19" rx="1" fill="none" stroke="#3f64b4" stroke-width="1.5" />
      <path d="M16 10.5l3 5.5-3 5.5-3-5.5z" fill="#d8302a" stroke-width="1.6" />
    </template>

    <template v-else-if="name === 'tear'">
      <path d="M16 3.5S7 14.5 7 20.5a9 9 0 0 0 18 0c0-6-9-17-9-17z" fill="#8cc0ee" />
      <ellipse cx="12.3" cy="20" rx="1.8" ry="3" fill="#fff" opacity=".7" stroke="none" />
    </template>

    <template v-else-if="name === 'trophy'">
      <path d="M10 8.5C6 8.5 5 10 5.5 12.5S9 16 11 15.5M22 8.5c4 0 5 1.5 4.5 4S23 16 21 15.5" fill="none" />
      <path d="M9.5 5.5h13v6a6.5 6.5 0 0 1-13 0z" fill="#e8b23a" />
      <rect x="14.2" y="17.5" width="3.6" height="4.5" fill="#c98e16" />
      <rect x="9.5" y="22" width="13" height="5" rx="1.2" fill="#7a4f1d" />
      <path d="M12.5 8v3.5" fill="none" stroke="#fff6d8" stroke-width="1.8" />
    </template>

    <template v-else-if="name === 'face' || name === 'face-dark'">
      <circle cx="16" cy="16" r="12" :fill="name === 'face' ? 'var(--ib-skin)' : '#6a5874'" />
      <ellipse cx="11.6" cy="14.5" rx="2.4" ry="3" :fill="name === 'face' ? 'var(--ib-outline)' : '#f4e8d0'" stroke="none" />
      <ellipse cx="20.4" cy="14.5" rx="2.4" ry="3" :fill="name === 'face' ? 'var(--ib-outline)' : '#f4e8d0'" stroke="none" />
      <path d="M11.6 18.5c-.4 3-1 5.5-1.6 8M20.4 18.5c.4 3 1 5.5 1.6 8" fill="none" stroke="#8cc0ee" stroke-width="2.4" />
      <path d="M13.5 22.5c1.6-1 3.4-1 5 0" fill="none" stroke-width="1.8" />
    </template>

    <template v-else-if="name === 'gamepad'">
      <path
        d="M8.5 10.5h15A6 6 0 0 1 29.4 16l.9 5.2a3.6 3.6 0 0 1-6.3 3L22 22H10l-2 2.2a3.6 3.6 0 0 1-6.3-3l.9-5.2a6 6 0 0 1 5.9-5.5z"
        fill="#5a5f6b"
      />
      <path d="M8.8 14.5v5M6.3 17h5" fill="none" stroke="#f4e8d0" stroke-width="2" />
      <circle cx="21" cy="18.5" r="1.7" fill="#7fa0e6" stroke="none" />
      <circle cx="24.2" cy="15.6" r="1.7" fill="#d8302a" stroke="none" />
    </template>

    <template v-else-if="name === 'wrench'">
      <path
        d="M21 3.5a7 7 0 0 0-6.4 9.6L4.6 23.1a2.8 2.8 0 0 0 4 4l10-10a7 7 0 0 0 9.6-6.4l-3.9 3.9-3.8-.9-.9-3.8z"
        fill="#d9dde3"
      />
    </template>

    <template v-else-if="name === 'coop'">
      <circle cx="11" cy="18" r="8.5" fill="var(--ib-skin)" />
      <circle cx="21.5" cy="14" r="8.5" fill="#f3c9a3" />
      <circle cx="8.3" cy="17.5" r="1.6" fill="var(--ib-outline)" stroke="none" />
      <circle cx="13.3" cy="17.5" r="1.6" fill="var(--ib-outline)" stroke="none" />
      <circle cx="19" cy="13.5" r="1.6" fill="var(--ib-outline)" stroke="none" />
      <circle cx="24" cy="13.5" r="1.6" fill="var(--ib-outline)" stroke="none" />
    </template>

    <template v-else-if="name === 'map'">
      <path d="M4 7.5l7-2.5 10 3 7-2.5v19l-7 2.5-10-3-7 2.5z" fill="#f4e8d0" />
      <path d="M11 5v19M21 8v19" fill="none" stroke-width="1.4" opacity=".5" />
      <path d="M7 20c3-1 4-5 8-5s4 3 7 1" fill="none" stroke="#b3241c" stroke-width="1.8" stroke-dasharray="2.5 2.5" />
      <path d="M22.5 11.5l3 3M25.5 11.5l-3 3" fill="none" stroke="#b3241c" stroke-width="2.2" />
    </template>

    <template v-else-if="name === 'rock'">
      <path d="M4.5 24C3 18 7 11.5 12.5 10.5 16 6.5 24.5 7.5 27 13.5c2.6 5.5 0 11-4.8 12H9c-2.3 0-3.6-.5-4.5-1.5z" fill="var(--ib-stone)" />
      <path d="M13 15.5l2.5 3M20 12.5l-1 3.5 2 2" fill="none" stroke-width="1.5" opacity=".55" />
    </template>

    <template v-else-if="name === 'poop'">
      <path
        d="M6 27c-3.4 0-3.6-5.4.6-6-2.2-3.3.8-6.6 4-5.6-.9-4 3-7 6.3-5.8.2-3 3.4-4.2 4.6-2.1-.9 2 .9 3 1 4.6 3 .3 4.6 3.6 2.6 6 3.8.4 4.6 7.6.6 8.9z"
        fill="#7a4f2c"
      />
      <path d="M9 21.5c3 1 9 1 14-1M11.5 16c2.5.7 6 .5 9-.8" fill="none" stroke-width="1.5" opacity=".5" />
    </template>

    <template v-else-if="name === 'lock'">
      <path d="M10.5 14v-3.5a5.5 5.5 0 0 1 11 0V14" fill="none" stroke-width="3" />
      <path d="M10.5 14v-3.5a5.5 5.5 0 0 1 11 0V14" fill="none" stroke="#c9ccd2" stroke-width="1.2" />
      <rect x="7" y="13.5" width="18" height="14" rx="3" fill="#e8b23a" />
      <circle cx="16" cy="19.5" r="2" fill="var(--ib-outline)" stroke="none" />
      <path d="M16 20.5v3.5" stroke-width="2" />
    </template>

    <template v-else-if="name === 'eye'">
      <path d="M2.5 16C6 9.5 11 7 16 7s10 2.5 13.5 9C26 22.5 21 25 16 25S6 22.5 2.5 16z" fill="#f2e6d8" />
      <path d="M6 13.5l4 1.5M26 13.5l-4 1.5M8 19.5l3-1" fill="none" stroke="#c0392b" stroke-width="1" />
      <circle cx="16" cy="16" r="6.2" fill="#b3241c" />
      <circle cx="16" cy="16" r="2.8" fill="var(--ib-outline)" stroke="none" />
      <circle cx="14" cy="13.8" r="1.3" fill="#fff" stroke="none" />
    </template>
  </svg>
</template>

<style scoped>
.game-icon {
  display: inline-block;
  flex: none;
  overflow: visible;
}
</style>
