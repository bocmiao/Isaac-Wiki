<script setup lang="ts">
import { withBase } from 'vitepress'
import { stages } from '../data/stages'
import GameIcon from './GameIcon.vue'

// 仿游戏楼层之间的过场：一条往下走的路，五个楼层节点，小人站在当前层
const props = defineProps<{ current?: number; compact?: boolean }>()
const at = () => props.current ?? 1
</script>

<template>
  <nav class="track" :class="{ compact }" aria-label="学习路线五层">
    <ol>
      <li
        v-for="s in stages"
        :key="s.floor"
        :class="{ here: s.floor === at(), past: s.floor < at(), ready: s.status === 'ready' }"
      >
        <a :href="withBase(s.link)" class="node-link" :aria-current="s.floor === current ? 'page' : undefined">
          <span class="marker" aria-hidden="true">
            <GameIcon v-if="s.floor === at()" name="face" :size="compact ? 26 : 30" />
          </span>
          <span class="room sketch" :style="{ '--sk-bg': s.color }">
            <span class="num">{{ s.floor }}</span>
          </span>
          <span class="place">{{ s.place }}</span>
          <span class="title">{{ s.title }}</span>
          <span v-if="!compact" class="status">{{ s.status === 'ready' ? '已上线' : '写作中' }}</span>
        </a>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.track ol {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  position: relative;
}
/* 楼层之间的路 */
.track ol::before {
  content: '';
  position: absolute;
  left: 10%;
  right: 10%;
  top: 62px;
  border-top: 4px dashed var(--ib-ink-3);
  opacity: 0.6;
}
.compact ol::before {
  top: 52px;
}
li {
  position: relative;
  margin: 0 !important;
}
.node-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  text-decoration: none !important;
  color: inherit !important;
  padding: 0 4px;
}
.marker {
  height: 36px;
  display: flex;
  align-items: flex-end;
  justify-content: center;
}
.here .marker {
  animation: hop 1.6s ease-in-out infinite;
}
.room {
  position: relative;
  width: 54px;
  height: 46px;
  margin-top: 4px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s;
}
.compact .room {
  width: 44px;
  height: 38px;
}
.node-link:hover .room {
  transform: translateY(-3px);
}
/* 当前所在层：像小地图里的当前房间一样加白框 */
.here .room {
  outline: 3px solid #fbf7ef;
  outline-offset: 3px;
  border-radius: 6px;
}
.dark .here .room {
  outline-color: #e9e3d6;
}
.num {
  font-family: var(--ib-font-display);
  font-size: 24px;
  color: #f6ecd8;
  text-shadow: 0 2px 0 rgba(0, 0, 0, 0.5);
}
.place {
  margin-top: 12px;
  font-size: 12px;
  font-weight: 700;
  color: var(--ib-ink-3);
  letter-spacing: 0.1em;
}
.title {
  font-family: var(--ib-font-display);
  font-size: 18px;
  letter-spacing: 0.03em;
  color: var(--ib-ink);
  line-height: 1.4;
}
.compact .title {
  font-size: 15px;
}
.here .title {
  color: var(--ib-blood);
}
.status {
  margin-top: 6px;
  font-size: 11.5px;
  font-weight: 700;
  padding: 1px 8px;
  border-radius: 999px;
  border: 1.5px solid var(--ib-line);
  color: var(--ib-ink-3);
}
.ready .status {
  border-color: var(--ib-blood);
  color: var(--ib-blood);
}
@keyframes hop {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-4px);
  }
}

/* 窄屏：改成竖向的路 */
@media (max-width: 640px) {
  .track ol {
    grid-template-columns: 1fr;
    gap: 6px;
  }
  .track ol::before {
    left: 61px;
    right: auto;
    top: 24px;
    bottom: 24px;
    border-top: none;
    border-left: 4px dashed var(--ib-ink-3);
  }
  .node-link {
    display: grid;
    grid-template-columns: 34px 52px 1fr auto;
    grid-template-rows: auto auto;
    column-gap: 12px;
    align-items: center;
    text-align: left;
    padding: 4px 0;
  }
  .marker {
    grid-row: 1 / 3;
    height: auto;
    align-items: center;
  }
  .room,
  .compact .room {
    grid-row: 1 / 3;
    width: 46px;
    height: 40px;
    margin: 0;
  }
  .place {
    margin: 0;
    grid-column: 3;
  }
  .title {
    grid-column: 3;
  }
  .status {
    grid-column: 4;
    grid-row: 1 / 3;
    margin: 0;
  }
}
</style>
