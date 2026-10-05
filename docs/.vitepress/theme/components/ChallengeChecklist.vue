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
  <article v-for="c in rows" :key="c.id" class="tool-card">
   <label><input type="checkbox" :checked="data.completed.includes(c.id)" @change="toggle(c.id)" />#{{c.id}} {{c.name}} 已完成</label>
   <p>{{c.description}} · {{c.character}} → {{c.target}}</p><p><strong>开放条件：</strong>{{c.unlock}}</p><p><strong>规则：</strong>{{c.rules}}</p><p><strong>奖励：</strong>{{c.reward}}</p>
   <a :href="withBase('/strategy/challenges#全部挑战总表')">查看挑战攻略</a>
  </article>
  <p v-if="!rows.length">没有符合条件的挑战。</p>
 </div>
</template>
