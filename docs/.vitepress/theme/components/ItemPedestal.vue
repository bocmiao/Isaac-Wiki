<script setup lang="ts">
import GameIcon, { type IconName } from './GameIcon.vue'

// 道具台：道具悬浮在石台上方，轻微上下浮动
withDefaults(defineProps<{ icon: IconName; size?: number; glow?: boolean }>(), { size: 44, glow: false })
</script>

<template>
  <div class="pedestal" :style="{ '--s': `${size}px` }">
    <div class="item" :class="{ glow }">
      <GameIcon :name="icon" :size="size" />
    </div>
    <div class="shadow" />
    <svg class="stand" viewBox="0 0 64 34" aria-hidden="true">
      <path d="M6 10h52v18a4 4 0 0 1-4 4H10a4 4 0 0 1-4-4z" fill="var(--ib-stone)" stroke="var(--ib-outline)" stroke-width="2.4" />
      <ellipse cx="32" cy="10" rx="26" ry="7" fill="#c9c3ba" stroke="var(--ib-outline)" stroke-width="2.4" />
      <path d="M14 18v8M50 18v8" stroke="var(--ib-outline)" stroke-width="1.6" opacity=".35" />
    </svg>
  </div>
</template>

<style scoped>
.pedestal {
  position: relative;
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  width: calc(var(--s) * 1.6);
}
.item {
  position: relative;
  z-index: 1;
  animation: bob 2.4s ease-in-out infinite;
}
.item.glow::before {
  content: '';
  position: absolute;
  inset: -40%;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 230, 160, 0.65), transparent 65%);
  z-index: -1;
}
.shadow {
  width: calc(var(--s) * 0.7);
  height: calc(var(--s) * 0.14);
  margin-top: calc(var(--s) * 0.08);
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.3);
  animation: shrink 2.4s ease-in-out infinite;
}
.stand {
  width: 100%;
  margin-top: calc(var(--s) * -0.06);
}
@keyframes bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-6px);
  }
}
@keyframes shrink {
  0%,
  100% {
    transform: scaleX(1);
  }
  50% {
    transform: scaleX(0.8);
    opacity: 0.7;
  }
}
</style>
