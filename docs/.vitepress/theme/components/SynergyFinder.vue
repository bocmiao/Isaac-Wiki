<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import combos from '../data/synergies.json'
import itemLinks from '../data/item-links.json'
import { useToolStorage } from '../tools/storage'
import { parseCombos, synergyState, type ComboProgress } from '../tools/planning'
const {data,message,storageError,exportFile,importFile}=useToolStorage<ComboProgress>('isaac-roadbook-combos-v1',()=>({v:1,owned:[]}),parseCombos)
const query=ref(''), filter=ref('all')
const items=computed(()=>itemLinks.filter(i=>combos.some(c=>c.items.includes(i.id))))
const name=(id:number)=>itemLinks.find(i=>i.id===id)?.name??String(id)
const state=(ids:number[])=>synergyState(ids,data.value.owned)
const labels={ready:'已有两件',partial:'还差一件',none:'尚未持有'}
const visible=computed(()=>combos.filter(c=>{
  const q=query.value.trim().toLowerCase()
  const text=[c.title,c.effect,c.individual,...c.items.map(id=>{const i=itemLinks.find(i=>i.id===id);return `${id} ${i?.en} ${i?.name}`})].join(' ').toLowerCase()
  return (!q||text.includes(q))&&(filter.value==='all'||state(c.items)===filter.value)
}))
</script>
<template>
<section class="tool-panel" aria-label="道具组合查询">
  <div class="tool-grid">
    <label>搜索组合<input v-model="query" type="search" placeholder="中文、英文、道具 ID 或效果关键词"></label>
    <label>持有状态<select v-model="filter" aria-label="持有状态"><option value="all">全部组合</option><option value="ready">已有两件</option><option value="partial">还差一件</option><option value="none">尚未持有</option></select></label>
  </div>
  <details><summary>勾选本局已有道具（{{ data.owned.length }} 件）</summary>
    <div class="tool-grid"><label v-for="item in items" :key="item.id"><input v-model="data.owned" type="checkbox" :value="item.id">{{ item.name }} · {{ item.en }} · #{{ item.id }}</label></div>
  </details>
  <div class="tool-actions"><button @click="data.owned=[]">新的一局：清空持有</button><button @click="exportFile">导出持有清单</button><label>导入持有清单<input type="file" accept="application/json,.json" @change="importFile"></label></div>
  <p v-if="storageError" role="alert">{{ storageError }}</p><p v-if="message" role="status">{{ message }}</p>
  <p aria-live="polite">显示 {{ visible.length }} / {{ combos.length }} 组。这里只查询已收录组合；没有结果不能说明两件道具没有联动。</p>
  <article v-for="combo in visible" :key="combo.id" class="tool-card">
    <h3>{{ combo.title }}</h3><p><strong>{{ labels[state(combo.items)] }}</strong><span v-if="state(combo.items)==='partial'"> · 缺少 {{ combo.items.filter(n=>!data.owned.includes(n)).map(name).join('、') }}</span></p>
    <p>{{ combo.effect }}</p><details><summary>单件效果与编号</summary><p>{{ combo.individual }}</p><p>{{ combo.items.map(n=>`${name(n)} #${n}`).join(' + ') }}</p></details>
    <a :href="withBase(combo.source)">查看组合攻略与参考来源</a>
  </article>
  <p v-if="!visible.length">没有匹配的已收录组合，请更换关键词或持有状态。</p>
</section>
</template>
