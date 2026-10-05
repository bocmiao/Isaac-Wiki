<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { characters, taintedName } from '../data/characters'
import normalMilestones from '../data/normal-donations.json'
import { greedMilestones, jamChance, shopLevels } from '../tools/rules'
import { int, parseDonations, useToolStorage, type DonationProgress } from '../tools/storage'
const roster=characters.flatMap(c=>[{id:c.id,name:c.name},{id:c.id+'-t',name:taintedName(c)}])
const {data,message,storageError,exportFile,importFile}=useToolStorage<DonationProgress>('isaac-roadbook-donations-v1',()=>({v:1,greed:0,normal:0,characters:{}}),x=>parseDonations(x,roster.map(c=>c.id)))
const who=ref('isaac'),greedier=ref(false),amount=ref(1)
const greedDraft=ref<number|string>(0),normalDraft=ref<number|string>(0),charDraft=ref<number|string>(0)
watch(data,()=>{greedDraft.value=data.value.greed;normalDraft.value=data.value.normal;charDraft.value=data.value.characters[who.value]??0},{deep:true})
watch(who,()=>charDraft.value=data.value.characters[who.value]??0)
const personal=computed(()=>data.value.characters[who.value]??0)
const known=computed(()=>Object.hasOwn(data.value.characters,who.value))
const jam=computed(()=>known.value?jamChance(personal.value,greedier.value):null)
const next=computed(()=>greedMilestones.find(([n])=>n>data.value.greed))
const level=computed(()=>shopLevels.reduce((level,n,index)=>data.value.normal>=n?index:level,0))
function setTotals(){
 if(!int(greedDraft.value,1000)||!int(normalDraft.value,999)||!int(charDraft.value,1000000)){message.value='累计数必须为范围内整数，原进度未改变。';return}
 data.value={v:1,greed:greedDraft.value as number,normal:normalDraft.value as number,characters:{...data.value.characters,[who.value]:charDraft.value as number}}
 message.value='已按游戏实际累计数校正。'
}
function donate(){
 if(!known.value){message.value='先校正此角色的历史累计；全新角色可填写0并保存。';return}
 if(!int(amount.value,1000)||amount.value<1){message.value='本次实际捐款请输入1–1000之间的整数。';return}
 if(data.value.greed+amount.value>1000||personal.value+amount.value>1000000){message.value='超过累计上限，未改变进度；请核对本次实际投进去的金额。';return}
 data.value={...data.value,greed:data.value.greed+amount.value,characters:{...data.value.characters,[who.value]:personal.value+amount.value}}
 message.value='已记录实际捐款；总累计与该角色累计都已增加。'
}
</script>
<template>
 <div class="tool-panel">
  <p class="tool-result">贪婪累计 {{data.greed}} / 1000 · 普通累计 {{data.normal}} / 999</p>
  <div class="tool-grid"><label>捐款角色<select v-model="who" aria-label="捐款角色"><option v-for="c in roster" :key="c.id" :value="c.id">{{c.name}}</option></select></label><label><input v-model="greedier" type="checkbox" />极贪模式</label><label>本次实际捐入枚数<input v-model.number="amount" type="number" min="1" max="1000" /></label></div>
  <button @click="donate">记录本次贪婪捐款</button>
  <p>此角色累计 {{known?personal:'未填写'}} 枚；当前卡住概率：<strong>{{jam===null?(known?'资料未列出此档，不估算':'尚未填写角色历史，不估算'):jam+'%'}}</strong>。这不是整批捐完的保证。</p>
  <p v-if="next">下个目标：{{next[0]}} 枚 · {{next[1]}}，还差 {{next[0]-data.greed}} 枚。</p><p v-else>1000 枚目标已记录；请以游戏内解锁店主为准。</p>
  <h2>校正已有存档</h2>
  <p>总累计和角色历史累计独立填写；不知道角色历史时不要从总累计推算。普通机可能因炸机变化，按游戏当前显示校正。</p>
  <div class="tool-grid"><label>贪婪机总累计（0–1000）<input v-model.number="greedDraft" type="number" min="0" max="1000" /></label><label>普通机当前累计（0–999）<input v-model.number="normalDraft" type="number" min="0" max="999" /></label><label>此角色历史累计<input v-model.number="charDraft" type="number" min="0" max="1000000" /></label></div>
  <button @click="setTotals">保存校正数值</button>
  <h2>贪婪里程碑</h2><table class="ms"><thead><tr><th></th><th>累计</th><th>解锁</th><th>还差</th></tr></thead><tbody><tr v-for="[n,name] in greedMilestones" :key="n" :class="{ got: data.greed>=n }"><td>{{data.greed>=n?'✓':''}}</td><td>{{n}}</td><td>{{name}}</td><td>{{data.greed>=n?'—':`${n-data.greed} 枚`}}</td></tr></tbody></table>
  <h2>普通捐款机</h2><p>当前数字对应的商店等级：{{level}}。炸机降低数字不会撤销已解锁等级，实际最高等级以游戏存档为准；困难模式仍会随机。</p>
  <table class="ms"><thead><tr><th></th><th>累计</th><th>成就</th><th>还差</th></tr></thead><tbody><tr v-for="m in normalMilestones" :key="m.id" :class="{ got: data.normal>=m.coins }"><td>{{data.normal>=m.coins?'✓':''}}</td><td>{{m.coins}}</td><td>{{m.name}}（#{{m.id}}）</td><td>{{data.normal>=m.coins?'—':`${m.coins-data.normal} 枚`}}</td></tr></tbody></table>
  <div class="tool-actions"><button @click="exportFile">导出捐款进度</button><label class="tool-import">导入并替换捐款进度<input type="file" accept="application/json,.json" @change="importFile" /></label></div><p role="status">{{message}}</p><p v-if="storageError" role="alert">{{storageError}}</p>
 </div>
</template>

<style scoped>
.ms td:last-child, .ms td:nth-child(2) { white-space: nowrap; }
.ms td:first-child, .ms th:first-child { width: 2em; min-width: 0; padding-left: 6px; padding-right: 0; text-align: center; color: var(--ib-blood); font-weight: 800; }
.ms tr.got { opacity: .6; }
</style>
