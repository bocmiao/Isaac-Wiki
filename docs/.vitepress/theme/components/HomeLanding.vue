<script setup lang="ts">
import { withBase } from 'vitepress'
import { marks } from '../data/characters'
import FloorTrack from './FloorTrack.vue'
import GameIcon, { type IconName } from './GameIcon.vue'
import HeartMeter from './HeartMeter.vue'
import RoomHero from './RoomHero.vue'
import StrategyGrid from './StrategyGrid.vue'
import StreakTitle from './StreakTitle.vue'

// 「选择角色」：按玩家现在的状态给入口，对应计划书里的三类目标用户
const personas: { icon: IconName; name: string; state: string; go: string; link: string }[] = [
  { icon: 'face', name: '刚入坑', state: '还没打败过妈妈', go: '从第 1 层开始', link: '/guide/start/' },
  { icon: 'chest', name: '通关过几次', state: '想解锁更多角色和结局', go: '去第 3 层：解锁主线', link: '/guide/unlocks/' },
  { icon: 'trophy', name: '冲白金神', state: '里角色、挑战、全成就', go: '打开解锁清单', link: '/tools/tracker' },
  { icon: 'gamepad', name: '主机 / 联机', state: '11 月 19 日主机版上线', go: '看联机专题', link: '/topics/coop' },
]

const topics: { icon: IconName; title: string; desc: string; link: string; tag?: string }[] = [
  {
    icon: 'coop',
    title: '联机专题',
    desc: '在线联机怎么开、四人联机的角色搭配、联机时的解锁规则。',
    link: '/topics/coop',
    tag: '11 月 19 日',
  },
  { icon: 'gamepad', title: '主机专题', desc: '手柄操作、没有模组时怎么认道具、主机和 PC 版的区别。', link: '/topics/console' },
  { icon: 'wrench', title: '配置与模组', desc: '中文、道具说明模组、什么时候能装模组。', link: '/topics/mods' },
]

// 常见问题：只放已经对照 wiki 或官方信息核实过的答案
const faqs = [
  {
    q: '里角色怎么解锁？',
    a: '到达「家」这一层，用红钥匙、破碎的钥匙或该隐之魂打开左侧墙上的衣柜。第一次到「家」时，打开妈妈卧室里的箱子必定能拿到红钥匙。',
    link: '/strategy/tainted',
  },
  {
    q: '游魂（The Lost）怎么解锁？',
    a: '携带饰品「寻人启事」在献祭房死亡。寻人启事要先用以撒击败羔羊才会解锁。',
    link: '/strategy/unlocks',
  },
  {
    q: '忏悔+（Repentance+）有中文吗？',
    a: '没有。官方简体中文只在忏悔里能选，Repentance+ 移除了语言选项，界面是英文。想要中文就关掉 Repentance+ 玩忏悔；想在线联机就只能用英文版，或者自行决定是否装玩家做的中文补丁。',
    link: '/guide/start/chinese',
  },
  {
    q: '在线联机能解锁成就吗？',
    a: '可以。Repentance+ 的在线联机支持全部模式，包括挑战和每日挑战。但中途加入别人的局，那一局不能解锁。',
    link: '/topics/coop',
  },
  {
    q: '主机版什么时候出？',
    a: '《Repentance+ Online》2026 年 11 月 19 日登陆 PS5、Xbox Series X|S 和 Switch 2，包含全部 DLC 和最多四人在线联机。',
    link: '/topics/console',
  },
  {
    q: '伊甸和雅各与以扫怎么解锁？',
    a: '伊甸：通关第 4 章（子宫）。雅各和以扫：用任意角色击败母亲。',
    link: '/strategy/unlocks',
  },
]

// 清单预览：示例数据
const previewRows = ['以撒', '抹大拉', '该隐', '犹大']
const previewDone = [
  [2, 2, 1, 1, 2, 0, 1, 0, 0, 0, 0, 0],
  [2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
</script>

<template>
  <div class="landing">
    <RoomHero />

    <a class="notice sketch" :href="withBase('/topics/coop')">
      <GameIcon name="gamepad" :size="26" />
      <span><b>主机版《Repentance+ Online》11 月 19 日发售</b>，支持四人在线联机。先看联机专题 →</span>
    </a>

    <!-- 选择角色 -->
    <section class="section">
      <header class="section-head">
        <StreakTitle title="选择你的角色" />
        <p>按你现在的情况，从最合适的地方开始。</p>
      </header>
      <div class="personas">
        <a v-for="(p, i) in personas" :key="p.name" class="persona sketch" :href="withBase(p.link)" :style="{ '--tilt': `${i % 2 ? 1.2 : -1.2}deg` }">
          <span class="portrait"><GameIcon :name="p.icon" :size="56" /></span>
          <span class="p-name">{{ p.name }}</span>
          <span class="p-state">{{ p.state }}</span>
          <span class="p-go">{{ p.go }} →</span>
        </a>
      </div>
    </section>

    <!-- 新手路线 -->
    <section class="section">
      <header class="section-head">
        <StreakTitle title="新手路线：往下走五层" />
        <p>用游戏的楼层做比喻，每一层只讲你当下用得上的东西。</p>
      </header>
      <div class="panel sketch">
        <FloorTrack />
      </div>
    </section>

    <!-- 攻略库 -->
    <section class="section">
      <header class="section-head row">
        <div>
          <StreakTitle title="攻略库" />
          <p>结局路线、Boss、角色、挑战……按计划分三批上线。</p>
        </div>
        <a class="ib-btn paper" :href="withBase('/strategy/')">全部攻略 →</a>
      </header>
      <StrategyGrid />
    </section>

    <!-- 专题 -->
    <section class="section">
      <header class="section-head">
        <StreakTitle title="专题" />
        <p>不在路线上、但新人最常问的问题。</p>
      </header>
      <div class="topics">
        <a v-for="t in topics" :key="t.title" class="topic sketch" :href="withBase(t.link)">
          <GameIcon :name="t.icon" :size="40" />
          <span class="t-body">
            <span class="t-title">{{ t.title }} <em v-if="t.tag">{{ t.tag }}</em></span>
            <span class="t-desc">{{ t.desc }}</span>
          </span>
        </a>
      </div>
    </section>

    <!-- 解锁清单 + 常见问题 -->
    <section class="section split">
      <div>
        <header class="section-head">
          <StreakTitle title="解锁清单" />
          <p>17 个角色的解锁条件，34 个角色的完成标记。点一下就记下，进度存在你自己的浏览器里。</p>
        </header>
        <a class="tracker-card sketch" :href="withBase('/tools/tracker')">
          <span class="tc-top">
            <HeartMeter :value="0.21" :hearts="8" :size="22" />
            <span class="tc-cta">开始记录 →</span>
          </span>
          <span class="mini-grid" aria-hidden="true">
            <span class="mini-row head">
              <span class="name"></span>
              <span v-for="m in marks" :key="m.id" class="cell-head">{{ m.short }}</span>
            </span>
            <span v-for="(row, r) in previewRows" :key="row" class="mini-row">
              <span class="name">{{ row }}</span>
              <span v-for="(d, c) in previewDone[r]" :key="c" class="cell" :class="`s${d}`" />
            </span>
          </span>
        </a>
      </div>
      <div>
        <header class="section-head">
          <StreakTitle title="常见问题" />
          <p>新人问得最多的几件事。</p>
        </header>
        <div class="faq">
          <details v-for="(f, i) in faqs" :key="f.q" class="sketch" :open="i === 0">
            <summary><GameIcon name="pill" :size="20" />{{ f.q }}</summary>
            <p>{{ f.a }} <a :href="withBase(f.link)">详细 →</a></p>
          </details>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing {
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 24px 72px;
}
.notice {
  --sk-bw: 2px;
  --sk-shadow: 0 3px 0 var(--ib-outline);
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 26px auto 0;
  max-width: 760px;
  padding: 10px 18px;
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2px solid var(--ib-outline);
  box-shadow: 0 3px 0 var(--ib-outline);
  font-size: 14.5px;
  color: var(--ib-ink-2);
  text-decoration: none;
  transition: transform 0.15s;
}
.notice:hover {
  transform: translateY(-2px);
}
.notice b {
  color: var(--ib-ink);
}

.section {
  margin-top: 64px;
}
.section-head {
  margin-bottom: 22px;
}
.section-head.row {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}
.section-head p {
  margin: 12px 0 0 6px;
  color: var(--ib-ink-2);
  font-size: 15px;
}
.panel {
  --sk-shadow: 0 5px 0 var(--ib-outline);
  padding: 22px 16px 26px;
  border-radius: 12px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 5px 0 var(--ib-outline);
}

/* 选择角色：像角色选择界面里画在纸上的卡片 */
.personas {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}
.persona {
  --sk-shadow: 0 5px 0 var(--ib-outline);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 20px 14px 16px;
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 5px 0 var(--ib-outline);
  text-decoration: none !important;
  color: inherit !important;
  transform: rotate(var(--tilt));
  transition: transform 0.15s;
}
.persona:hover {
  transform: rotate(0) translateY(-4px) scale(1.02);
}
.portrait {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 84px;
  height: 84px;
  border-radius: 50%;
  background: var(--ib-paper-2);
  border: 2px dashed var(--ib-line);
}
.persona:hover .portrait {
  border-color: var(--ib-blood);
}
.p-name {
  margin-top: 12px;
  font-family: var(--ib-font-display);
  font-size: 24px;
  letter-spacing: 0.06em;
  color: var(--ib-ink);
}
.p-state {
  margin-top: 4px;
  font-size: 13.5px;
  color: var(--ib-ink-2);
}
.p-go {
  margin-top: 14px;
  padding-top: 10px;
  width: 100%;
  border-top: 2px dashed var(--ib-line);
  font-family: var(--ib-font-display);
  font-size: 16px;
  letter-spacing: 0.03em;
  color: var(--ib-blood);
}

/* 专题 */
.topics {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.topic {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  padding: 18px;
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 4px 0 var(--ib-outline);
  text-decoration: none !important;
  color: inherit !important;
  transition: transform 0.15s;
}
.topic:hover {
  transform: translateY(-3px);
}
.t-body {
  display: flex;
  flex-direction: column;
}
.t-title {
  font-family: var(--ib-font-display);
  font-size: 21px;
  letter-spacing: 0.04em;
  color: var(--ib-ink);
}
.t-title em {
  font-style: normal;
  font-size: 11.5px;
  font-weight: 800;
  color: var(--ib-on-dark);
  background: var(--ib-blood-btn);
  padding: 1px 7px;
  border-radius: 6px;
  margin-left: 6px;
  vertical-align: 2px;
}
.t-desc {
  margin-top: 4px;
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--ib-ink-2);
}

/* 解锁清单 + 常见问题 */
.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}
.tracker-card {
  --sk-shadow: 0 5px 0 var(--ib-outline);
  display: block;
  padding: 18px;
  border-radius: 12px;
  background: var(--ib-paper);
  border: 2.5px solid var(--ib-outline);
  box-shadow: 0 5px 0 var(--ib-outline);
  text-decoration: none !important;
  transition: transform 0.15s;
}
.tracker-card:hover {
  transform: translateY(-3px);
}
.tc-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.tc-cta {
  font-family: var(--ib-font-display);
  font-size: 18px;
  color: var(--ib-blood);
}
.mini-grid {
  display: block;
}
.mini-row {
  display: grid;
  grid-template-columns: 52px repeat(12, 1fr);
  gap: 4px;
  margin-bottom: 4px;
  align-items: center;
}
.name {
  font-size: 13px;
  font-weight: 700;
  color: var(--ib-ink-2);
}
.cell-head {
  font-size: 10.5px;
  text-align: center;
  color: var(--ib-ink-3);
  white-space: nowrap;
  overflow: hidden;
}
.cell {
  aspect-ratio: 1;
  border-radius: 4px;
  border: 1.5px solid var(--ib-line);
  background: var(--ib-paper-2);
}
.cell.s1 {
  border: 2px solid var(--ib-blood);
  background: var(--ib-blood-soft);
}
.cell.s2 {
  border: 2px solid var(--ib-outline);
  background: #d8302a;
}
.faq {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
details {
  --sk-bw: 2px;
  --sk-shadow: 0 3px 0 var(--ib-outline);
  border-radius: 10px;
  background: var(--ib-paper);
  border: 2px solid var(--ib-outline);
  box-shadow: 0 3px 0 var(--ib-outline);
}
summary {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 14px;
  font-family: var(--ib-font-display);
  font-size: 17px;
  letter-spacing: 0.03em;
  color: var(--ib-ink);
  cursor: pointer;
  list-style: none;
}
summary::-webkit-details-marker {
  display: none;
}
summary::after {
  content: '+';
  margin-left: auto;
  font-size: 20px;
  font-weight: 900;
  color: var(--ib-ink-3);
}
details[open] summary::after {
  content: '−';
}
details p {
  margin: 0;
  padding: 0 16px 14px 44px;
  font-size: 14px;
  line-height: 1.75;
  color: var(--ib-ink-2);
}
details a {
  font-weight: 800;
  color: var(--ib-blood);
  white-space: nowrap;
}

@media (max-width: 960px) {
  .personas {
    grid-template-columns: repeat(2, 1fr);
  }
  .topics {
    grid-template-columns: 1fr;
  }
  .split {
    grid-template-columns: 1fr;
    gap: 0;
  }
  .split > div + div {
    margin-top: 64px;
  }
}
@media (max-width: 520px) {
  .landing {
    padding: 16px 16px 56px;
  }
  .personas {
    gap: 12px;
  }
  .persona {
    padding: 16px 8px 12px;
  }
  .portrait {
    width: 64px;
    height: 64px;
  }
  .portrait :deep(svg) {
    width: 42px;
    height: 42px;
  }
  .p-name {
    font-size: 16px;
  }
  .section {
    margin-top: 48px;
  }
  .mini-row {
    grid-template-columns: 44px repeat(12, 1fr);
    gap: 3px;
  }
  .cell-head {
    font-size: 9px;
  }
}
</style>
