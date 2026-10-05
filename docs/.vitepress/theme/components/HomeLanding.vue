<script setup lang="ts">
import { withBase } from 'vitepress'
import { stages } from '../data/stages'
import { marks } from '../data/characters'
import DungeonMap from './DungeonMap.vue'
import HeartMeter from './HeartMeter.vue'

const topics = [
  {
    tag: '11 月 19 日主机版发售',
    title: '联机专题',
    desc: '在线联机怎么开、中途加入为什么不能解锁成就、四人联机的角色搭配。',
    link: '/topics/coop',
  },
  {
    tag: 'Switch 2 / PS5 / Xbox',
    title: '主机专题',
    desc: '手柄操作、没有模组时怎么认道具、主机和 PC 版有什么不同。',
    link: '/topics/console',
  },
  {
    tag: 'PC',
    title: '配置与模组',
    desc: '中文、道具说明模组、什么时候能装模组，以及成就不解锁怎么办。',
    link: '/topics/mods',
  },
]

// 清单预览用的示例数据：前 4 个角色，部分标记已完成
const previewRows = ['以撒', '抹大拉', '该隐', '犹大']
const previewDone = [
  [1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0],
  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
</script>

<template>
  <div class="landing">
    <!-- 首屏 -->
    <section class="hero">
      <div class="hero-text">
        <p class="eyebrow">适用版本 Repentance+ · 2026 年 10 月更新</p>
        <h1>从第一局<br />到<span class="red">白金神</span></h1>
        <p class="lead">中文以撒学习路线。每一层只讲你现在用得上的东西，道具数据直接链到 wiki，不让你在几百个道具里迷路。</p>
        <div class="actions">
          <a class="btn brand" :href="withBase('/guide/start/')">我是新手，从第 1 层开始</a>
          <a class="btn alt" :href="withBase('/tools/tracker')">打开解锁清单</a>
        </div>
        <a class="notice" :href="withBase('/topics/coop')">
          <span class="pill">新</span>
          主机版《Repentance+ Online》11 月 19 日发售，先看联机专题 →
        </a>
      </div>
      <div class="hero-art">
        <DungeonMap />
        <p class="caption">你在这里。下面是往下走的五层。</p>
      </div>
    </section>

    <!-- 五层路线 -->
    <section class="section">
      <div class="section-head">
        <h2>学习路线：往下走五层</h2>
        <p>按顺序读，也可以直接跳到你卡住的那一层。</p>
      </div>
      <ol class="path">
        <li v-for="s in stages" :key="s.floor" class="stage" :class="s.status">
          <div class="floor-tag">
            <span class="num">{{ s.floor }}</span>
            <span class="place">{{ s.place }}</span>
          </div>
          <a class="stage-card" :href="withBase(s.link)">
            <div class="stage-top">
              <h3>{{ s.title }}</h3>
              <span class="status">{{ s.status === 'ready' ? '已上线' : '写作中' }}</span>
            </div>
            <p>{{ s.summary }}</p>
            <div class="chips">
              <span v-for="t in s.topics" :key="t" class="chip">{{ t }}</span>
            </div>
          </a>
        </li>
      </ol>
    </section>

    <!-- 专题 -->
    <section class="section">
      <div class="section-head">
        <h2>专题</h2>
        <p>不在路线上、但新人最常问的问题。</p>
      </div>
      <div class="topic-grid">
        <a v-for="t in topics" :key="t.title" class="topic" :href="withBase(t.link)">
          <span class="topic-tag">{{ t.tag }}</span>
          <h3>{{ t.title }}</h3>
          <p>{{ t.desc }}</p>
          <span class="more">阅读 →</span>
        </a>
      </div>
    </section>

    <!-- 解锁清单预告 -->
    <section class="section tracker-promo">
      <div class="promo-text">
        <h2>解锁清单：用红心记录进度</h2>
        <p>17 个角色的解锁条件、34 个角色的完成标记，点一下就记下。进度保存在你自己的浏览器里，不用注册，也可以导出备份。</p>
        <a class="btn brand" :href="withBase('/tools/tracker')">开始记录</a>
      </div>
      <div class="promo-card" aria-hidden="true">
        <div class="promo-meter">
          <span>总进度</span>
          <HeartMeter :value="0.21" :hearts="8" />
        </div>
        <div class="mini-grid">
          <div class="mini-row head">
            <span class="name"></span>
            <span v-for="m in marks" :key="m.id" class="cell-head" :title="m.name">{{ m.short }}</span>
          </div>
          <div v-for="(row, r) in previewRows" :key="row" class="mini-row">
            <span class="name">{{ row }}</span>
            <span v-for="(d, c) in previewDone[r]" :key="c" class="cell" :class="{ done: d }" />
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.landing {
  max-width: 1120px;
  margin: 0 auto;
  padding: 32px 24px 64px;
}
.hero {
  display: grid;
  grid-template-columns: 1.25fr 1fr;
  gap: 48px;
  align-items: center;
  padding: 32px 0 48px;
}
.eyebrow {
  display: inline-block;
  font-size: 13px;
  font-weight: 600;
  color: var(--ib-blood);
  background: var(--ib-blood-soft);
  border: 1px solid var(--ib-blood);
  padding: 4px 12px;
  border-radius: 999px;
  margin: 0 0 20px;
}
h1 {
  font-size: clamp(40px, 6vw, 64px);
  line-height: 1.12;
  font-weight: 800;
  letter-spacing: 0.02em;
  color: var(--ib-ink);
  margin: 0 0 20px;
}
.red {
  color: var(--ib-blood);
}
.lead {
  font-size: 18px;
  line-height: 1.8;
  color: var(--ib-ink-2);
  max-width: 34em;
  margin: 0 0 28px;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 24px;
}
.btn {
  display: inline-block;
  padding: 11px 22px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  transition: transform 0.15s, background 0.15s;
  border: 2px solid var(--ib-ink);
  box-shadow: 0 3px 0 var(--ib-ink);
}
.btn:hover {
  transform: translateY(-1px);
}
.btn:active {
  transform: translateY(2px);
  box-shadow: 0 1px 0 var(--ib-ink);
}
.btn.brand {
  background: var(--ib-blood);
  color: #fff8ef;
}
.dark .btn.brand {
  color: #17120f;
}
.btn.alt {
  background: var(--vp-c-bg-elv);
  color: var(--ib-ink);
}
.notice {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: var(--ib-ink-2);
  text-decoration: none;
}
.notice:hover {
  color: var(--ib-blood);
}
.pill {
  font-size: 12px;
  font-weight: 700;
  color: #fff8ef;
  background: var(--ib-soul);
  padding: 2px 8px;
  border-radius: 6px;
}
.hero-art {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.caption {
  margin-top: 12px;
  font-size: 13px;
  color: var(--ib-ink-3);
}

.section {
  padding: 40px 0;
  border-top: 1px dashed var(--ib-line);
}
.section-head h2 {
  font-size: 26px;
  font-weight: 800;
  margin: 0 0 6px;
  color: var(--ib-ink);
}
.section-head p {
  margin: 0 0 24px;
  color: var(--ib-ink-2);
}

/* 五层路线：左侧楼层标签 + 竖线串起来 */
.path {
  list-style: none;
  padding: 0;
  margin: 0;
  position: relative;
}
.path::before {
  content: '';
  position: absolute;
  left: 35px;
  top: 30px;
  bottom: 30px;
  border-left: 3px dashed var(--ib-line);
}
.stage {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 20px;
  align-items: center;
  margin-bottom: 14px;
  position: relative;
}
.floor-tag {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 14px;
  border: 2px solid var(--ib-ink);
  background: var(--vp-c-bg-elv);
  z-index: 1;
}
.stage.ready .floor-tag {
  background: var(--ib-blood);
  border-color: var(--ib-blood);
  color: #fff8ef;
}
.dark .stage.ready .floor-tag {
  color: #17120f;
}
.num {
  font-size: 26px;
  font-weight: 800;
  line-height: 1;
}
.place {
  font-size: 12px;
  margin-top: 4px;
  opacity: 0.85;
}
.stage-card {
  display: block;
  padding: 16px 20px;
  border-radius: 14px;
  border: 1px solid var(--ib-line);
  background: var(--vp-c-bg-elv);
  box-shadow: var(--ib-shadow);
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, transform 0.15s;
}
.stage-card:hover {
  border-color: var(--ib-blood);
  transform: translateX(3px);
}
.stage-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}
.stage-card h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: var(--ib-ink);
}
.status {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 6px;
  color: var(--ib-ink-3);
  border: 1px solid var(--ib-line);
  white-space: nowrap;
}
.stage.ready .status {
  color: var(--ib-blood);
  border-color: var(--ib-blood);
}
.stage-card p {
  margin: 6px 0 10px;
  color: var(--ib-ink-2);
  font-size: 15px;
}
.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.chip {
  font-size: 12.5px;
  padding: 2px 10px;
  border-radius: 999px;
  background: var(--ib-paper-3);
  color: var(--ib-ink-2);
}

/* 专题卡片 */
.topic-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}
.topic {
  display: flex;
  flex-direction: column;
  padding: 20px;
  border-radius: 14px;
  border: 1px solid var(--ib-line);
  background: var(--vp-c-bg-elv);
  box-shadow: var(--ib-shadow);
  text-decoration: none;
  color: inherit;
  transition: border-color 0.15s, transform 0.15s;
}
.topic:hover {
  border-color: var(--ib-blood);
  transform: translateY(-2px);
}
.topic-tag {
  align-self: flex-start;
  font-size: 12px;
  color: var(--ib-soul);
  background: var(--ib-soul-soft);
  padding: 2px 8px;
  border-radius: 6px;
}
.topic h3 {
  margin: 12px 0 6px;
  font-size: 18px;
  font-weight: 700;
  color: var(--ib-ink);
}
.topic p {
  flex: 1;
  margin: 0 0 12px;
  font-size: 14.5px;
  color: var(--ib-ink-2);
  line-height: 1.7;
}
.more {
  font-size: 14px;
  font-weight: 600;
  color: var(--ib-blood);
}

/* 解锁清单预告 */
.tracker-promo {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
}
.promo-text h2 {
  font-size: 26px;
  font-weight: 800;
  margin: 0 0 10px;
  color: var(--ib-ink);
}
.promo-text p {
  color: var(--ib-ink-2);
  margin: 0 0 20px;
  line-height: 1.8;
}
.promo-card {
  padding: 20px;
  border-radius: 14px;
  border: 2px solid var(--ib-ink);
  background: var(--vp-c-bg-elv);
  box-shadow: 0 4px 0 var(--ib-ink);
}
.promo-meter {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 13px;
  font-weight: 700;
  color: var(--ib-ink-2);
}
.mini-row {
  display: grid;
  grid-template-columns: 56px repeat(12, 1fr);
  gap: 4px;
  margin-bottom: 4px;
  align-items: center;
}
.name {
  font-size: 13px;
  color: var(--ib-ink-2);
}
.cell-head {
  font-size: 11px;
  text-align: center;
  color: var(--ib-ink-3);
}
.cell {
  aspect-ratio: 1;
  border-radius: 4px;
  background: var(--ib-paper-3);
}
.cell.done {
  background: var(--ib-blood);
}

@media (max-width: 860px) {
  .hero {
    grid-template-columns: 1fr;
    gap: 24px;
    padding-top: 8px;
  }
  .hero-art {
    order: -1;
  }
  .hero-art :deep(.map) {
    max-width: 220px;
  }
  .topic-grid {
    grid-template-columns: 1fr;
  }
  .tracker-promo {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 520px) {
  .landing {
    padding: 16px 16px 48px;
  }
  .stage {
    grid-template-columns: 56px 1fr;
    gap: 12px;
  }
  .floor-tag {
    width: 56px;
    height: 56px;
  }
  .path::before {
    left: 27px;
  }
  .num {
    font-size: 22px;
  }
}
</style>
