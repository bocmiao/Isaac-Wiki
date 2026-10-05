<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import { characters } from '../data/characters'
import { strategyCategories } from '../data/strategy'
import { stages } from '../data/stages'
import { loadProgress, summarize } from '../progress'
import GameIcon from './GameIcon.vue'

// 仿原版左上角状态栏：主动道具 + 充能条 | 红心 | 金币、炸弹、钥匙计数。
// 主动道具是「路书」，充能条 = 访客自己在解锁清单里的进度；点它进入清单。
const progress = ref(0)
const hasProgress = ref(false)
onMounted(() => {
  const p = loadProgress()
  if (p) {
    progress.value = summarize(p).overall
    hasProgress.value = true
  }
})
const SEGMENTS = 6
const pad = (n: number) => String(n).padStart(2, '0')
</script>

<template>
  <div class="hud">
    <div class="top-row">
      <a
        class="active"
        :href="withBase('/tools/tracker')"
        :title="hasProgress ? `你的解锁进度 ${Math.round(progress * 100)}%` : '还没开始记录进度，点这里开始'"
      >
        <GameIcon name="map" :size="38" />
        <span class="charge" aria-hidden="true">
          <span class="charge-fill" :style="{ height: `${Math.max(progress, hasProgress ? 0.04 : 0) * 100}%` }" />
          <span v-for="i in SEGMENTS - 1" :key="i" class="tick" :style="{ bottom: `${(i / SEGMENTS) * 100}%` }" />
        </span>
      </a>
      <div class="hearts" aria-hidden="true">
        <GameIcon v-for="i in 3" :key="i" name="heart" :size="26" />
        <GameIcon name="soul" :size="26" />
      </div>
    </div>
    <p class="active-note">
      {{ hasProgress ? `路书充能 ${Math.round(progress * 100)}%` : '路书未充能 · 去记录进度 →' }}
    </p>
    <ul class="counts">
      <li><GameIcon name="coin" :size="20" /><b>{{ pad(strategyCategories.length) }}</b><span>类攻略</span></li>
      <li><GameIcon name="bomb" :size="20" /><b>{{ pad(stages.length) }}</b><span>层路线</span></li>
      <li><GameIcon name="key" :size="20" /><b>{{ pad(characters.length) }}</b><span>个角色</span></li>
    </ul>
  </div>
</template>

<style scoped>
.hud {
  display: flex;
  flex-direction: column;
}
.top-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}
.active {
  display: flex;
  align-items: stretch;
  gap: 4px;
  text-decoration: none;
  transition: transform 0.12s;
}
.active:hover {
  transform: scale(1.06);
}
.charge {
  position: relative;
  width: 9px;
  border: 2px solid var(--ib-outline);
  border-radius: 2px;
  background: rgba(0, 0, 0, 0.35);
  overflow: hidden;
}
.dark .charge {
  border-color: #767a85;
}
.charge-fill {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: #f2c53d;
}
.tick {
  position: absolute;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--ib-outline);
}
.dark .tick {
  background: #767a85;
}
.hearts {
  display: flex;
  gap: 1px;
  padding-top: 2px;
}
.active-note {
  margin: 4px 0 6px;
  font-size: 12px;
  font-weight: 700;
  color: var(--ib-ink-3);
}
.counts {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.counts li {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
  color: var(--ib-ink-3);
}
.counts b {
  font-family: var(--ib-font-display);
  font-weight: 400;
  font-size: 20px;
  line-height: 1.15;
  color: var(--ib-ink);
  min-width: 26px;
  letter-spacing: 0.04em;
}
</style>
