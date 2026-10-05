<script setup lang="ts">
import { withBase } from 'vitepress'
import { categoryLink, strategyCategories, strategyGroups } from '../data/strategy'
import GameIcon from './GameIcon.vue'

// 攻略库栏目：每个栏目像一件摆在道具台上的道具
defineProps<{ detailed?: boolean }>()
</script>

<template>
  <!-- 攻略库页：按分组排 -->
  <template v-if="detailed">
    <section v-for="g in strategyGroups" :key="g" class="group">
      <h2 class="group-title">{{ g }}</h2>
      <div class="grid detailed">
        <a v-for="c in strategyCategories.filter((x) => x.group === g)" :key="c.id" class="cat sketch" :href="withBase(categoryLink(c))">
          <span class="icon-wrap"><GameIcon :name="c.icon" :size="40" /></span>
          <span class="name">{{ c.name }}</span>
          <span class="desc">{{ c.desc }}</span>
          <ul class="plan">
            <li v-for="p in c.covers" :key="p">{{ p }}</li>
          </ul>
        </a>
      </div>
    </section>
  </template>
  <div v-else class="grid">
    <a v-for="c in strategyCategories" :key="c.id" class="cat sketch" :href="withBase(categoryLink(c))">
      <span class="icon-wrap"><GameIcon :name="c.icon" :size="detailed ? 40 : 36" /></span>
      <span class="name">{{ c.name }}</span>
      <span class="desc">{{ c.desc }}</span>
    </a>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 14px;
}
.grid.detailed {
  grid-template-columns: repeat(2, 1fr);
}
.cat {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 18px 12px 14px;
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 4px 0 var(--ib-outline);
  text-decoration: none !important;
  color: inherit !important;
  transition: transform 0.15s, box-shadow 0.15s;
}
.cat:hover {
  transform: translateY(-3px);
  --sk-shadow: 0 7px 0 var(--ib-outline);
}
.icon-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 62px;
  height: 52px;
  /* 小石台 */
  background: radial-gradient(ellipse 70% 22% at 50% 92%, rgba(0, 0, 0, 0.22), transparent 70%);
}
.cat:hover .icon-wrap :deep(svg) {
  animation: bob 1s ease-in-out infinite;
}
.name {
  margin-top: 8px;
  font-family: var(--ib-font-display);
  font-size: 19px;
  letter-spacing: 0.04em;
  color: var(--ib-ink);
}
.desc {
  margin-top: 4px;
  font-size: 12.5px;
  line-height: 1.55;
  color: var(--ib-ink-2);
}
.batch {
  margin-top: 10px;
  font-size: 11px;
  font-weight: 800;
  padding: 1px 8px;
  border-radius: 999px;
  border: 1.5px solid currentColor;
}
.ready {
  color: var(--ib-on-dark);
  background: var(--ib-blood-btn);
  border-color: var(--ib-outline) !important;
}
.b1 {
  color: var(--ib-blood);
}
.b2 {
  color: var(--ib-gold);
}
.b3 {
  color: var(--ib-ink-3);
}

.group + .group {
  margin-top: 28px;
}
.group-title {
  margin: 0 0 12px !important;
  padding: 0 !important;
  border: 0 !important;
  font-size: 22px !important;
}
.group-title::before,
.group-title::after {
  display: none !important;
}
/* 攻略库页：横向卡片，列出计划内容 */
.detailed .cat {
  display: grid;
  grid-template-columns: 64px 1fr;
  grid-template-areas:
    'icon name'
    'icon desc'
    'icon plan';
  text-align: left;
  align-items: start;
  column-gap: 14px;
  padding: 18px;
}
.detailed .icon-wrap {
  grid-area: icon;
}
.detailed .name {
  grid-area: name;
  margin: 0;
  font-size: 21px;
}
.detailed .desc {
  grid-area: desc;
  font-size: 13.5px;
}
.plan {
  grid-area: plan;
  margin: 8px 0 0 !important;
  padding-left: 18px !important;
  font-size: 13px;
  color: var(--ib-ink-2);
  line-height: 1.7;
}
.plan li {
  margin: 0 !important;
}
@keyframes bob {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}
@media (max-width: 1000px) {
  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 720px) {
  .grid,
  .grid.detailed {
    grid-template-columns: repeat(2, 1fr);
  }
  .detailed .cat {
    grid-template-columns: 1fr;
    grid-template-areas: 'icon' 'name' 'desc' 'plan';
  }
}
@media (max-width: 420px) {
  .grid.detailed {
    grid-template-columns: 1fr;
  }
}
</style>
