<script setup lang="ts">
import { ref } from 'vue'
import { withBase } from 'vitepress'
import GameIcon from './GameIcon.vue'
import HudBar from './HudBar.vue'
import ItemPedestal from './ItemPedestal.vue'
import MiniMap from './MiniMap.vue'
import StreakTitle from './StreakTitle.vue'

// 首页首屏：俯视视角的一个房间，布局照着原版画面来。
// 左上状态栏、右上小地图、右下口袋卡牌；四面墙上的门通往四个区域：
// 普通木门 = 新手路线，金色宝箱门 = 攻略库，上锁的门 = 解锁清单，红色 Boss 门 = 联机专题。
// 深色模式（妈腿层）下，妈妈的眼睛会从门洞里往外看，地上会出现她脚掌的影子。
const doors = [
  { side: 'top', label: '新手路线', icon: 'map', link: '/guide/', kind: 'wood' },
  { side: 'left', label: '攻略库', icon: 'crown', link: '/strategy/', kind: 'treasure' },
  { side: 'right', label: '解锁清单', icon: 'key', link: '/tools/tracker', kind: 'locked' },
  { side: 'bottom', label: '联机 · 主机专题', short: '联机专题', icon: 'gamepad', link: '/topics/coop', kind: 'boss' },
] as const

// 口袋卡牌：点一下换一条小贴士（内容都已核实）
const tips = [
  '射击方向和移动方向是分开的，可以一边后退一边射击。',
  '按住 Tab 可以查看整层地图。',
  '按住 R 可以快速重开这一局。',
  '第一次到「家」时，妈妈卧室的箱子里必定有红钥匙。',
  '用阿撒泻勒击败究极贪婪，可以解锁莉莉丝。',
]
const tipIndex = ref(0)
const nextTip = () => (tipIndex.value = (tipIndex.value + 1) % tips.length)
</script>

<template>
  <section class="room-hero" aria-label="以撒路书首页">
    <div class="wall">
      <a v-for="d in doors" :key="d.side" class="door-link" :class="d.side" :href="withBase(d.link)">
        <span class="door" :class="d.kind" aria-hidden="true">
          <span class="hole">
            <GameIcon name="eye" :size="42" class="mom-eye" />
          </span>
          <GameIcon v-if="d.kind === 'locked'" name="lock" :size="24" class="door-badge" />
          <GameIcon v-if="d.kind === 'boss'" name="skull" :size="22" class="door-badge" />
        </span>
        <span class="door-label sketch"><GameIcon :name="d.icon" :size="20" />{{ d.label }}</span>
      </a>

      <div class="floor">
        <HudBar class="hud" />
        <MiniMap class="minimap" />

        <div class="deco" aria-hidden="true">
          <GameIcon name="rock" :size="50" class="rock-a" />
          <GameIcon name="rock" :size="32" class="rock-b" />
          <GameIcon name="poop" :size="40" class="poop" />
          <span class="mom-shadow" />
        </div>

        <div class="center">
          <p class="version">适用版本 忏悔 / 忏悔+ · 2026 年 10 月</p>
          <h1 class="game-title">以撒路书</h1>
          <p class="tagline">从第一局到白金神的中文以撒学习路线</p>

          <a class="pickup" :href="withBase('/guide/start/')">
            <ItemPedestal icon="map" :size="52" glow />
            <StreakTitle tag="div" size="sm" title="新手路线" sub="从第 1 层开始 · 开局前 10 分钟看完" />
          </a>

          <!-- 窄屏没有地方放门，改成按钮 -->
          <div class="door-menu">
            <a v-for="d in doors" :key="d.side" class="ib-btn paper" :href="withBase(d.link)">
              <GameIcon :name="d.icon" :size="20" />{{ 'short' in d ? d.short : d.label }}
            </a>
          </div>
        </div>

        <button class="pocket" type="button" :title="'换一条小贴士'" @click="nextTip">
          <span class="pocket-card"><GameIcon name="card" :size="34" /><span class="key-q">Q</span></span>
          <span class="pocket-text">
            <b>小贴士 {{ tipIndex + 1 }}/{{ tips.length }}</b>
            <span>{{ tips[tipIndex] }}</span>
          </span>
        </button>
      </div>
    </div>
  </section>
</template>

<style scoped>
.room-hero {
  --wall-w: 48px;
}
.wall {
  position: relative;
  padding: var(--wall-w);
  border-radius: 24px;
  border: 3px solid var(--ib-outline);
  background-color: var(--ib-wall);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='48'%3E%3Cg fill='%235d412c' stroke='%2325170e' stroke-width='1.8'%3E%3Crect x='3' y='3' width='26' height='19' rx='8'/%3E%3Crect x='33' y='2' width='28' height='20' rx='7'/%3E%3Crect x='-13' y='26' width='26' height='19' rx='8'/%3E%3Crect x='51' y='26' width='26' height='19' rx='8'/%3E%3Crect x='17' y='27' width='30' height='18' rx='7'/%3E%3C/g%3E%3Cpath d='M9 7h12M39 6h14M23 31h14M-7 30h12M57 30h12' fill='none' stroke='%237c583a' stroke-width='1.6' stroke-linecap='round'/%3E%3C/svg%3E");
  box-shadow: 0 10px 0 rgba(0, 0, 0, 0.28);
}
.dark .wall {
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='48'%3E%3Cg fill='%231c1d22' stroke='%23000000' stroke-width='1.8'%3E%3Crect x='3' y='3' width='26' height='19' rx='8'/%3E%3Crect x='33' y='2' width='28' height='20' rx='7'/%3E%3Crect x='-13' y='26' width='26' height='19' rx='8'/%3E%3Crect x='51' y='26' width='26' height='19' rx='8'/%3E%3Crect x='17' y='27' width='30' height='18' rx='7'/%3E%3C/g%3E%3Cpath d='M9 7h12M39 6h14M23 31h14M-7 30h12M57 30h12' fill='none' stroke='%232d2f37' stroke-width='1.6' stroke-linecap='round'/%3E%3C/svg%3E");
}
/* 墙面透视：上墙受光、下墙最暗、左右居中，四个角有斜向接缝 */
.wall::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  background:
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10' preserveAspectRatio='none'%3E%3Cpath d='M0 0L10 10' stroke='black' stroke-opacity='.55' stroke-width='.35' vector-effect='non-scaling-stroke' fill='none'/%3E%3C/svg%3E") top left / var(--wall-w) var(--wall-w) no-repeat,
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10' preserveAspectRatio='none'%3E%3Cpath d='M10 0L0 10' stroke='black' stroke-opacity='.55' stroke-width='.35' vector-effect='non-scaling-stroke' fill='none'/%3E%3C/svg%3E") top right / var(--wall-w) var(--wall-w) no-repeat,
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10' preserveAspectRatio='none'%3E%3Cpath d='M0 10L10 0' stroke='black' stroke-opacity='.55' stroke-width='.35' vector-effect='non-scaling-stroke' fill='none'/%3E%3C/svg%3E") bottom left / var(--wall-w) var(--wall-w) no-repeat,
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10' preserveAspectRatio='none'%3E%3Cpath d='M10 10L0 0' stroke='black' stroke-opacity='.55' stroke-width='.35' vector-effect='non-scaling-stroke' fill='none'/%3E%3C/svg%3E") bottom right / var(--wall-w) var(--wall-w) no-repeat,
    linear-gradient(rgba(255, 235, 200, 0.07), rgba(255, 235, 200, 0.07)) top / 100% var(--wall-w) no-repeat,
    linear-gradient(rgba(0, 0, 0, 0.32), rgba(0, 0, 0, 0.32)) bottom / 100% var(--wall-w) no-repeat,
    linear-gradient(rgba(0, 0, 0, 0.16), rgba(0, 0, 0, 0.16)) left / var(--wall-w) 100% no-repeat,
    linear-gradient(rgba(0, 0, 0, 0.16), rgba(0, 0, 0, 0.16)) right / var(--wall-w) 100% no-repeat;
}

.floor {
  position: relative;
  z-index: 1;
  min-height: 580px;
  border-radius: 4px;
  background-color: var(--ib-room-floor);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.2 0 0 0 0 0.12 0 0 0 0 0.05 0 0 0 0.3 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url%28%23n%29'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 18% 14% at 22% 30%, rgba(90, 55, 25, 0.18), transparent 70%),
    radial-gradient(ellipse 14% 10% at 78% 72%, rgba(90, 55, 25, 0.16), transparent 70%),
    radial-gradient(ellipse 10% 8% at 60% 18%, rgba(90, 55, 25, 0.12), transparent 70%);
  /* 墙投在地上的阴影 + 四角暗角 */
  box-shadow: inset 0 0 0 3px var(--ib-outline), inset 0 26px 30px -8px rgba(0, 0, 0, 0.5),
    inset 22px 0 28px -12px rgba(0, 0, 0, 0.35), inset -22px 0 28px -12px rgba(0, 0, 0, 0.35),
    inset 0 -14px 24px -10px rgba(0, 0, 0, 0.35), inset 0 0 120px rgba(40, 20, 5, 0.28);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 64px 170px;
  overflow: hidden;
}
.dark .floor {
  /* 妈腿层：冷灰色的大石板 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.6' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.45 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url%28%23n%29'/%3E%3C/svg%3E"), url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='180' height='140'%3E%3Cpath d='M0 46h76V0M76 46h104M118 46v94M0 100h118M44 100v40M118 82h62' stroke='%23fff' stroke-opacity='.07' stroke-width='2' fill='none'/%3E%3C/svg%3E"),
    radial-gradient(ellipse 30% 22% at 50% 50%, rgba(120, 130, 150, 0.08), transparent 70%);
  box-shadow: inset 0 0 0 3px var(--ib-outline), inset 0 26px 30px -8px rgba(0, 0, 0, 0.7),
    inset 22px 0 28px -12px rgba(0, 0, 0, 0.5), inset -22px 0 28px -12px rgba(0, 0, 0, 0.5),
    inset 0 -14px 24px -10px rgba(0, 0, 0, 0.5), inset 0 0 140px rgba(0, 0, 0, 0.55);
}

/* ---------- 门 ---------- */
.door-link {
  position: absolute;
  z-index: 3;
  text-decoration: none !important;
}
.door {
  position: absolute;
  display: block;
  border: 3px solid var(--ib-outline);
}
.door.wood {
  background: #8a5a33 repeating-linear-gradient(90deg, transparent 0 12px, rgba(0, 0, 0, 0.28) 12px 14px);
}
.door.treasure {
  background: #e0a630;
  box-shadow: inset 0 0 0 3px #f7d77a;
}
.door.locked {
  background: #9aa0a8 repeating-linear-gradient(90deg, transparent 0 12px, rgba(0, 0, 0, 0.18) 12px 14px);
}
.door.boss {
  background: #9e2a22;
  box-shadow: inset 0 0 0 3px #c9473c;
}
.dark .door.wood {
  background-color: #4a4d56;
}
.hole {
  position: absolute;
  inset: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: var(--ib-hole);
  transition: background 0.2s;
}
/* 上锁的门：门洞是关着的门板 */
.door.locked .hole {
  background: #5c5f66 repeating-linear-gradient(90deg, transparent 0 9px, rgba(0, 0, 0, 0.3) 9px 11px);
}
.door-link:hover .hole,
.door-link:focus-visible .hole {
  background: radial-gradient(circle at 50% 50%, #ffe6a8, #c98a2a 60%, var(--ib-hole));
}
.door-badge {
  position: absolute;
  left: 50%;
  top: 50%;
  translate: -50% -50%;
  z-index: 1;
}
.door-link:hover .door.locked .door-badge {
  animation: unlock 0.4s ease-out forwards;
}
@keyframes unlock {
  to {
    opacity: 0;
    transform: translateY(-10px) rotate(-20deg);
  }
}
.mom-eye {
  opacity: 0;
  transform: scale(0.4);
  transition: opacity 0.2s, transform 0.25s;
}
/* 妈腿层：门洞里是妈妈的眼睛 */
.dark .door-link:hover .hole,
.dark .door-link:focus-visible .hole {
  background: radial-gradient(circle, #3a0d0a, #000 70%);
}
.dark .door-link:hover .mom-eye,
.dark .door-link:focus-visible .mom-eye {
  opacity: 1;
  transform: scale(1);
}
.dark .door.boss .mom-eye {
  animation: peek 7s ease-in-out infinite;
}
@keyframes peek {
  0%,
  62%,
  100% {
    opacity: 0;
    transform: scale(0.4);
  }
  68%,
  88% {
    opacity: 1;
    transform: scale(1);
  }
  78% {
    opacity: 1;
    transform: scale(1, 0.1);
  }
}
.door-label {
  --sk-bw: 2px;
  --sk-shadow: 0 3px 0 var(--ib-outline);
  position: absolute;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
  font-family: var(--ib-font-display);
  font-size: 16px;
  letter-spacing: 0.04em;
  color: var(--ib-ink);
  border-radius: 999px;
  padding: 3px 12px 3px 8px;
  transition: transform 0.15s;
}
.door-link:hover .door-label,
.door-link:focus-visible .door-label {
  --sk-bg: var(--ib-blood-btn);
  color: var(--ib-on-dark);
  transform: scale(1.06);
}

/* 上下门横向开口，左右门竖向开口，拱形朝墙外 */
.top,
.bottom {
  left: 50%;
}
.top {
  top: 0;
}
.bottom {
  bottom: 0;
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
.top .door,
.bottom .door {
  width: 100px;
  height: calc(var(--wall-w) + 8px);
  left: -50px;
}
.top .door {
  top: -6px;
  border-radius: 50px 50px 4px 4px;
}
.top .hole {
  border-radius: 42px 42px 0 0;
  bottom: -3px;
}
.bottom .door {
  bottom: -6px;
  border-radius: 4px 4px 50px 50px;
}
.bottom .hole {
  border-radius: 0 0 42px 42px;
  top: -3px;
}
.left .door,
.right .door {
  height: 100px;
  width: calc(var(--wall-w) + 8px);
  top: -50px;
}
.left .door {
  left: -6px;
  border-radius: 50px 4px 4px 50px;
}
.left .hole {
  border-radius: 42px 0 0 42px;
  right: -3px;
}
.right .door {
  right: -6px;
  border-radius: 4px 50px 50px 4px;
}
.right .hole {
  border-radius: 0 42px 42px 0;
  left: -3px;
}
.top .door-label {
  top: calc(var(--wall-w) + 14px);
  translate: -50% 0;
}
.bottom .door-label {
  bottom: calc(var(--wall-w) + 14px);
  translate: -50% 0;
}
.left .door-label {
  left: calc(var(--wall-w) + 14px);
  translate: 0 -50%;
}
.right .door-label {
  right: calc(var(--wall-w) + 14px);
  translate: 0 -50%;
}

/* ---------- 地上的东西 ---------- */
.hud {
  position: absolute;
  top: 18px;
  left: 22px;
  z-index: 2;
}
.minimap {
  position: absolute;
  top: 18px;
  right: 22px;
  z-index: 2;
}
.deco > * {
  position: absolute;
}
.rock-a {
  bottom: 22%;
  left: 7%;
}
.rock-b {
  bottom: 17%;
  left: 12%;
}
.poop {
  top: 64%;
  right: 9%;
}
.mom-shadow {
  display: none;
}
.dark .mom-shadow {
  display: block;
  left: 22%;
  bottom: 12%;
  width: 210px;
  height: 72px;
  border-radius: 50%;
  background: radial-gradient(ellipse, rgba(0, 0, 0, 0.8), rgba(0, 0, 0, 0.3) 60%, transparent 72%);
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
  margin: 0 0 4px;
  font-size: 13px;
  font-weight: 800;
  color: var(--ib-blood);
  letter-spacing: 0.06em;
}
.game-title {
  margin: 0;
  font-family: var(--ib-font-display);
  font-size: clamp(56px, 8.5vw, 104px);
  line-height: 1.15;
  font-weight: 400;
  letter-spacing: 0.08em;
  color: #f4ead8;
  -webkit-text-stroke: 10px var(--ib-outline);
  paint-order: stroke fill;
  text-shadow: 0 8px 0 var(--ib-outline);
  transform: rotate(-2deg);
}
.dark .game-title {
  color: #e9e3d6;
}
.tagline {
  margin: 12px 0 24px;
  font-family: var(--ib-font-display);
  font-size: 20px;
  letter-spacing: 0.04em;
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

/* 口袋卡牌（右下角） */
.pocket {
  position: absolute;
  right: 20px;
  bottom: 18px;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 10px;
  max-width: 290px;
  padding: 6px 12px 6px 6px;
  border: none;
  border-radius: 8px;
  background: rgba(30, 18, 8, 0.62);
  color: var(--ib-on-dark);
  text-align: left;
  font: inherit;
  cursor: pointer;
  transition: background 0.15s;
}
.pocket:hover {
  background: rgba(30, 18, 8, 0.78);
}
.dark .pocket {
  background: rgba(0, 0, 0, 0.45);
}
.pocket-card {
  position: relative;
  flex: none;
}
.key-q {
  position: absolute;
  right: -8px;
  bottom: -6px;
  min-width: 18px;
  padding: 2px 3px 1px;
  font-family: var(--ib-font-display);
  font-size: 13px;
  line-height: 1;
  text-align: center;
  border-radius: 4px;
  border: 1.5px solid #f6ecd8;
  background: #1f150e;
  color: #f6ecd8;
}
.pocket-text {
  display: flex;
  flex-direction: column;
  font-size: 12.5px;
  line-height: 1.5;
}
.pocket-text b {
  font-family: var(--ib-font-display);
  font-weight: 400;
  font-size: 14px;
  color: #f2c53d;
}

/* ---------- 窄屏 ---------- */
@media (max-width: 1100px) {
  .floor {
    padding: 150px 60px 110px;
  }
  .left .door-label,
  .right .door-label {
    display: none;
  }
}
@media (max-width: 720px) {
  .room-hero {
    --wall-w: 18px;
  }
  .wall {
    border-radius: 14px;
  }
  .door-link,
  .minimap,
  .deco > :not(.mom-shadow) {
    display: none;
  }
  .floor {
    min-height: 0;
    flex-direction: column;
    align-items: stretch;
    padding: 16px 14px 18px;
  }
  .hud {
    position: relative;
    top: auto;
    left: auto;
    margin-bottom: 18px;
  }
  .hud :deep(.counts) {
    flex-direction: row;
    flex-wrap: wrap;
    gap: 2px 14px;
  }
  .hud :deep(.counts b) {
    min-width: 0;
  }
  .dark .mom-shadow {
    left: 4%;
    bottom: 30%;
    width: 140px;
  }
  .tagline {
    font-size: 17px;
  }
  .door-menu {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px 10px;
    width: 100%;
    margin-top: 24px;
  }
  .door-menu .ib-btn {
    justify-content: center;
    padding: 9px 8px;
    font-size: 16px;
  }
  .pocket {
    position: relative;
    right: auto;
    bottom: auto;
    max-width: none;
    margin-top: 18px;
  }
}
</style>
