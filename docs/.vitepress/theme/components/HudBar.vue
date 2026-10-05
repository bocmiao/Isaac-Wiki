<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { withBase } from 'vitepress'
import { characters } from '../data/characters'
import { strategyCategories } from '../data/strategy'
import { stages } from '../data/stages'
import { loadProgress, summarize } from '../progress'
import GameIcon from './GameIcon.vue'
import HeartMeter from './HeartMeter.vue'

// 仿游戏左上角的状态栏：红心 = 访客自己的解锁进度，下面三行是站点内容的规模
const progress = ref<number | null>(null)
onMounted(() => {
  const p = loadProgress()
  progress.value = p ? summarize(p).overall : null
})
const pad = (n: number) => String(n).padStart(2, '0')
</script>

<template>
  <div class="hud">
    <a class="hud-hearts" :href="withBase('/tools/tracker')" :title="progress === null ? '还没开始记录进度' : '你的解锁进度'">
      <HeartMeter :value="progress ?? 0" :hearts="6" :size="26" />
      <span class="hud-note">{{ progress === null ? '还没开始记录 →' : `你的进度 ${Math.round(progress * 100)}%` }}</span>
    </a>
    <ul class="hud-counts">
      <li><GameIcon name="coin" :size="20" /><b>×{{ pad(strategyCategories.length) }}</b><span>类攻略</span></li>
      <li><GameIcon name="bomb" :size="20" /><b>×{{ pad(stages.length) }}</b><span>层路线</span></li>
      <li><GameIcon name="key" :size="20" /><b>×{{ pad(characters.length) }}</b><span>个角色</span></li>
    </ul>
  </div>
</template>

<style scoped>
.hud {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.hud-hearts {
  display: flex;
  flex-direction: column;
  gap: 2px;
  text-decoration: none;
}
.hud-note {
  font-size: 12px;
  font-weight: 700;
  color: var(--ib-ink-3);
}
.hud-hearts:hover .hud-note {
  color: var(--ib-blood);
}
.hud-counts {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}
.hud-counts li {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: var(--ib-ink-2);
}
.hud-counts b {
  font-family: var(--vp-font-family-mono);
  font-size: 16px;
  font-weight: 900;
  color: var(--ib-ink);
  min-width: 34px;
}
</style>
