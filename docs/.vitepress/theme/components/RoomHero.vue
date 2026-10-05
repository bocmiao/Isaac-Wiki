<script setup lang="ts">
import { withBase } from 'vitepress'
import GameIcon from './GameIcon.vue'
import HudBar from './HudBar.vue'
import ItemPedestal from './ItemPedestal.vue'
import StreakTitle from './StreakTitle.vue'

// 首页首屏：俯视的一个房间。四面墙上各有一扇门通往网站的四个区域，
// 地面中间的道具台放着最重要的入口。深色模式下地面会出现妈妈脚掌的影子。
const doors = [
  { side: 'top', label: '新手路线', icon: 'map', link: '/guide/', kind: 'normal' },
  { side: 'left', label: '攻略库', icon: 'crown', link: '/strategy/', kind: 'treasure' },
  { side: 'right', label: '解锁清单', icon: 'key', link: '/tools/tracker', kind: 'locked' },
  { side: 'bottom', label: '联机 · 主机专题', short: '联机专题', icon: 'gamepad', link: '/topics/coop', kind: 'boss' },
] as const
</script>

<template>
  <section class="room-hero" aria-label="以撒路书首页">
    <div class="wall">
      <a
        v-for="d in doors"
        :key="d.side"
        class="door-link"
        :class="d.side"
        :href="withBase(d.link)"
      >
        <span class="door" :class="d.kind" aria-hidden="true"><span class="hole" /></span>
        <span class="door-label"><GameIcon :name="d.icon" :size="20" />{{ d.label }}</span>
      </a>

      <div class="floor">
        <HudBar class="hud" />

        <div class="deco" aria-hidden="true">
          <GameIcon name="rock" :size="52" class="rock-a" />
          <GameIcon name="rock" :size="34" class="rock-b" />
          <GameIcon name="poop" :size="40" class="poop" />
          <span class="mom-shadow" />
        </div>

        <div class="center">
          <p class="version">适用版本 Repentance+ · 2026 年 10 月</p>
          <h1 class="game-title">以撒路书</h1>
          <p class="tagline">从第一局到白金神的中文以撒学习路线</p>

          <a class="pickup" :href="withBase('/guide/start/')">
            <ItemPedestal icon="map" :size="50" glow />
            <StreakTitle tag="div" size="sm" title="新手路线" sub="从第 1 层开始 · 开局前 10 分钟看完" />
          </a>

          <!-- 窄屏没有地方放门，改成按钮 -->
          <div class="door-menu">
            <a v-for="d in doors" :key="d.side" class="ib-btn paper" :href="withBase(d.link)">
              <GameIcon :name="d.icon" :size="20" />{{ 'short' in d ? d.short : d.label }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.room-hero {
  --wall-w: 44px;
}
.wall {
  position: relative;
  padding: var(--wall-w);
  border-radius: 22px;
  border: 3px solid var(--ib-outline);
  background-color: var(--ib-wall);
  /* 石砖缝 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='22'%3E%3Cpath d='M0 .5h44M0 11.5h44M11 0v11M33 11v11' stroke='%23000' stroke-opacity='.35' fill='none'/%3E%3C/svg%3E");
  box-shadow: 0 10px 0 rgba(0, 0, 0, 0.25);
}
.dark .wall {
  /* 妈腿层的墙几乎是黑的，砖缝改用浅色才看得见 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='44' height='22'%3E%3Cpath d='M0 .5h44M0 11.5h44M11 0v11M33 11v11' stroke='%23fff' stroke-opacity='.08' fill='none'/%3E%3C/svg%3E");
}
.dark .floor {
  /* 妈腿层：冷灰色的大石板 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.4 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='140'%3E%3Cpath d='M0 46h76V0M76 46h104M118 46v94M0 100h118M44 100v40M118 82h62' stroke='%23fff' stroke-opacity='.07' stroke-width='2' fill='none'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 30% 22% at 50% 50%, rgba(120, 130, 150, 0.08), transparent 70%);
}
.floor {
  position: relative;
  min-height: 540px;
  border-radius: 6px;
  background-color: var(--ib-room-floor);
  /* 地下室：泥土噪点 + 几块深色污渍 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.22 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 18% 14% at 22% 30%, rgba(90, 55, 25, 0.16), transparent 70%),
    radial-gradient(ellipse 14% 10% at 78% 72%, rgba(90, 55, 25, 0.14), transparent 70%),
    radial-gradient(ellipse 10% 8% at 60% 18%, rgba(90, 55, 25, 0.1), transparent 70%);
  box-shadow: inset 0 0 0 3px var(--ib-outline), inset 0 22px 30px -6px rgba(0, 0, 0, 0.45),
    inset 18px 0 26px -10px rgba(0, 0, 0, 0.3), inset -18px 0 26px -10px rgba(0, 0, 0, 0.3),
    inset 0 -12px 22px -10px rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 56px 120px;
  overflow: hidden;
}

/* ---------- 门 ---------- */
.door-link {
  position: absolute;
  z-index: 2;
  text-decoration: none !important;
}
.door {
  position: absolute;
  display: block;
  background: #7d5a3e;
  border: 3px solid var(--ib-outline);
  transition: filter 0.15s;
}
.dark .door {
  background: #3d4049;
}
.door.treasure {
  background: #e0a630;
}
.door.locked {
  background: #b9bec7;
}
.door.boss {
  background: #a5271f;
}
.hole {
  position: absolute;
  inset: 7px;
  background: var(--ib-hole);
  transition: background 0.2s;
}
.door-link:hover .hole,
.door-link:focus-visible .hole {
  background: radial-gradient(circle at 50% 50%, #ffe6a8, #c98a2a 60%, var(--ib-hole));
}
.door-label {
  position: absolute;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  font-size: 14px;
  font-weight: 800;
  color: var(--ib-ink);
  background: var(--ib-paper);
  border: 2px solid var(--ib-outline);
  border-radius: 999px;
  padding: 4px 12px 4px 8px;
  box-shadow: 0 3px 0 var(--ib-outline);
  transition: transform 0.15s;
}
.door-link:hover .door-label,
.door-link:focus-visible .door-label {
  transform: scale(1.06);
  background: var(--ib-blood-btn);
  color: var(--ib-on-dark);
}

/* 上下门：横向开口；左右门：竖向开口。拱形朝墙外 */
.top,
.bottom {
  left: 50%;
}
.top .door,
.bottom .door {
  width: 92px;
  height: calc(var(--wall-w) + 6px);
  left: -46px;
}
.top .door {
  top: -6px;
  border-radius: 46px 46px 6px 6px;
}
.top .hole {
  border-radius: 40px 40px 0 0;
  bottom: -3px;
}
.top .door-label {
  top: calc(var(--wall-w) + 14px);
  transform-origin: top center;
  translate: -50% 0;
}
.bottom .door {
  bottom: -6px;
  border-radius: 6px 6px 46px 46px;
}
.bottom .hole {
  border-radius: 0 0 40px 40px;
  top: -3px;
}
.top {
  top: 0;
}
.bottom {
  bottom: 0;
}
.bottom .door-label {
  bottom: calc(var(--wall-w) + 14px);
  translate: -50% 0;
}
.left,
.right {
  top: 50%;
}
.left {
  left: 0;
}
.right {
  right: 0;
}
.left .door,
.right .door {
  height: 92px;
  width: calc(var(--wall-w) + 6px);
  top: -46px;
}
.left .door {
  left: -6px;
  border-radius: 46px 6px 6px 46px;
}
.left .hole {
  border-radius: 40px 0 0 40px;
  right: -3px;
}
.right .door {
  right: -6px;
  border-radius: 6px 46px 46px 6px;
}
.right .hole {
  border-radius: 0 40px 40px 0;
  left: -3px;
}
.left .door-label {
  left: calc(var(--wall-w) + 14px);
  translate: 0 -50%;
}
.right .door-label {
  right: calc(var(--wall-w) + 14px);
  translate: 0 -50%;
}

/* ---------- 地面上的东西 ---------- */
.hud {
  position: absolute;
  top: 18px;
  left: 22px;
  z-index: 1;
}
.deco > * {
  position: absolute;
}
.rock-a {
  top: 16%;
  right: 12%;
}
.rock-b {
  top: 24%;
  right: 8%;
}
.poop {
  bottom: 14%;
  left: 13%;
}
.mom-shadow {
  display: none;
}
.dark .mom-shadow {
  display: block;
  right: 14%;
  bottom: 16%;
  width: 200px;
  height: 70px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(0, 0, 0, 0.75), rgba(0, 0, 0, 0.25) 60%, transparent 72%);
  animation: stomp 5s ease-in infinite;
}
@keyframes stomp {
  0% {
    transform: scale(0.3);
    opacity: 0;
  }
  70% {
    transform: scale(1);
    opacity: 1;
  }
  78% {
    transform: scale(1.05);
    opacity: 1;
  }
  100% {
    transform: scale(1.05);
    opacity: 0;
  }
}

.center {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.version {
  margin: 0 0 6px;
  font-size: 13px;
  font-weight: 800;
  color: var(--ib-blood);
  letter-spacing: 0.06em;
}
.game-title {
  margin: 0;
  font-size: clamp(52px, 8vw, 92px);
  line-height: 1.1;
  font-weight: 900;
  letter-spacing: 0.08em;
  color: var(--ib-on-dark);
  -webkit-text-stroke: 9px var(--ib-outline);
  paint-order: stroke fill;
  text-shadow: 0 7px 0 var(--ib-outline);
  transform: rotate(-2deg);
}
.tagline {
  margin: 14px 0 26px;
  font-size: 17px;
  font-weight: 700;
  color: var(--ib-ink-2);
}
.pickup {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none !important;
  transition: transform 0.15s;
}
.pickup:hover {
  transform: scale(1.04);
}
.pickup :deep(.streak) {
  margin-top: 10px;
}
.door-menu {
  display: none;
}

/* ---------- 窄屏 ---------- */
@media (max-width: 860px) {
  .floor {
    padding: 56px 40px;
  }
  .left .door-label,
  .right .door-label {
    display: none;
  }
}
@media (max-width: 720px) {
  .room-hero {
    --wall-w: 16px;
  }
  .wall {
    border-radius: 14px;
  }
  .door-link {
    display: none;
  }
  .floor {
    min-height: 0;
    flex-direction: column;
    align-items: stretch;
    padding: 16px 16px 24px;
  }
  .hud {
    position: relative;
    top: auto;
    left: auto;
    margin-bottom: 22px;
  }
  .hud :deep(.hud-counts) {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 4px 14px;
  }
  .hud :deep(.hud-counts b) {
    min-width: 0;
  }
  .rock-a {
    top: 18px;
    right: 14px;
  }
  .rock-a,
  .rock-b,
  .poop {
    display: none;
  }
  .dark .mom-shadow {
    right: 4%;
    bottom: 26%;
    width: 140px;
  }
  .door-menu {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    width: 100%;
    margin-top: 24px;
  }
  .tagline {
    font-size: 15px;
  }
  .door-menu .ib-btn {
    justify-content: center;
    padding: 10px 8px;
    font-size: 14px;
  }
}
</style>
