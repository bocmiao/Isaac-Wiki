<script setup lang="ts">
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import routes from '../data/routes.json'
import { useToolStorage } from '../tools/storage'
import { emptyRoutes, parseRoutes, gates, missingGates } from '../tools/planning'
const {data,message,storageError,exportFile,importFile}=useToolStorage('isaac-roadbook-routes-v1',emptyRoutes,parseRoutes)
const branch=ref('blue')
const route=computed(()=>routes.find(r=>r.id===data.value.target)!)
const missing=computed(()=>missingGates(data.value.target,data.value.unlocks,branch.value))
const completed=computed(()=>data.value.completed[data.value.target]??[])
function toggle(id:string,event:Event){
  const checked=(event.target as HTMLInputElement).checked
  data.value.completed[data.value.target]=checked?[...new Set([...completed.value,id])]:completed.value.filter(s=>s!==id)
}
function reset(){data.value.completed[data.value.target]=[];message.value='已清空当前路线的本局步骤，永久解锁记录保留。'}
</script>
<template>
<section class="tool-panel" aria-label="主线路线规划">
  <div class="tool-grid"><label>本局目标<select v-model="data.target" aria-label="本局目标"><option v-for="r in routes" :key="r.id" :value="r.id">{{ r.title }}</option></select></label>
    <label v-if="data.target==='mega'">超级撒但分支<select v-model="branch" aria-label="超级撒但分支"><option value="blue">全家福 → 宝箱</option><option value="lamb">底片 → 暗室</option></select></label>
  </div>
  <details open><summary>永久解锁条件（按实际存档勾选）</summary>
    <div class="tool-grid"><label v-for="gate in gates" :key="gate.id"><input v-model="data.unlocks" type="checkbox" :value="gate.id">{{ gate.text }}</label></div>
    <p>11 次心脏自动满足 10 次；3 次死寂自动满足 1 次。未勾选表示尚未确认，不会读取游戏存档。</p>
  </details>
  <div class="tool-result" aria-live="polite"><p v-if="missing.length"><strong>还需确认前置条件：</strong>{{ missing.map(g=>g.text).join('；') }}</p><p v-else><strong>已确认这条路线列出的永久前置。</strong>还需按下方步骤准备本局资源与入口。</p></div>
  <h3>{{ route.title }} · 本局步骤 {{ completed.length }} / {{ route.steps.length }}</h3>
  <ol><li v-for="step in route.steps" :key="step.id"><label><input type="checkbox" :checked="completed.includes(step.id)" @change="toggle(step.id,$event)">{{ step.text }}</label></li></ol>
  <p v-if="route.note">{{ route.note }}</p>
  <p>步骤勾选仅作为手动提醒，不会增加永久击败次数。各路线的步骤分别保存；换局请清空对应路线。</p>
  <div class="tool-actions"><button @click="reset">新的一局：清空当前路线步骤</button><button @click="exportFile">导出路线记录</button><label>导入路线记录<input type="file" accept="application/json,.json" @change="importFile"></label></div>
  <p v-if="storageError" role="alert">{{ storageError }}</p><p v-if="message" role="status">{{ message }}</p>
  <p><a :href="withBase(route.source)">查看详细路线、版本说明和参考来源</a> · <a :href="withBase('/tools/tracker')">角色完成标记</a> · <a :href="withBase('/tools/donations')">捐款进度</a></p>
</section>
</template>
