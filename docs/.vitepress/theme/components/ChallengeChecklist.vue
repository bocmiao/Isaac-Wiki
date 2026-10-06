<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import challenges from '../data/challenges.json'
import { parseChallenges, useToolStorage, type ChallengeProgress } from '../tools/storage'
const {data,message,storageError,exportFile,importFile}=useToolStorage<ChallengeProgress>('isaac-roadbook-challenges-v1',()=>({v:1,completed:[]}),parseChallenges)
const query=ref(''),filter=ref('all')
const rows=computed(()=>challenges.filter(c=>`${c.id} ${c.name} ${c.description} ${c.reward} ${c.character}`.toLowerCase().includes(query.value.trim().toLowerCase())&&(filter.value==='all'||data.value.completed.includes(c.id)===(filter.value==='done'))))
function toggle(id:number){data.value.completed=data.value.completed.includes(id)?data.value.completed.filter(n=>n!==id):[...data.value.completed,id].sort((a,b)=>a-b)}
</script>
<template>
 <div class="tool-panel">
  <div class="tool-grid"><label>搜索挑战<input v-model="query" type="search" placeholder="编号、名称、角色或奖励" /></label><label>显示<select v-model="filter" aria-label="显示"><option value="all">全部</option><option value="todo">未完成</option><option value="done">已完成</option></select></label></div>
  <p class="tool-result" aria-live="polite">完成 {{data.completed.length}} / 45 · 当前显示 {{rows.length}} 项</p>
  <div class="tool-actions"><button @click="exportFile">导出挑战进度</button><label class="tool-import">导入并替换挑战进度<input type="file" accept="application/json,.json" @change="importFile" /></label></div>
  <p role="status">{{message}}</p><p v-if="storageError" role="alert">{{storageError}}</p>
  <article v-for="c in rows" :key="c.id" class="tool-card ch" :class="{ done: data.completed.includes(c.id) }">
   <label class="ch-head"><input type="checkbox" :checked="data.completed.includes(c.id)" :aria-label="`#${c.id} ${c.name} 已完成`" @change="toggle(c.id)" /><b>#{{c.id}} {{c.name}}</b><span class="ch-sub">{{c.description.replace(c.name,'').trim()}}</span></label>
   <dl>
    <dt>角色</dt><dd>{{c.character}} → {{c.target}}</dd>
    <dt>开放</dt><dd>{{c.unlock}}</dd>
    <dt>规则</dt><dd>{{c.rules}}</dd>
    <dt>奖励</dt><dd>{{c.reward}}</dd>
   </dl>
   <a :href="withBase(`/challenges/${c.id}`)">查看 #{{c.id}} 的发育与终点打法 →</a>
  </article>
  <p><a :href="withBase('/challenges/')">搜索全部 45 个挑战攻略</a> · <a :href="withBase('/strategy/challenges#先做哪些')">先做哪些 → 推荐顺序</a></p>
  <p v-if="!rows.length">没有符合条件的挑战。</p>
 </div>
</template>

<style scoped>
.ch-head { display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap; margin: 0 0 6px !important; }
.ch-head b { font-size: 16px; }
.ch-sub { font-size: 13px; color: var(--ib-ink-3); }
.ch dl { display: grid; grid-template-columns: 3em 1fr; gap: 2px 10px; margin: 0; font-size: 14px; line-height: 1.6; }
.ch dt { color: var(--ib-ink-3); font-weight: 700; }
.ch dd { margin: 0; }
.ch.done { opacity: .6; }
.ch.done b { text-decoration: line-through; }
</style>
