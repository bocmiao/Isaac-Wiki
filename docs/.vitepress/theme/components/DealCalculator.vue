<script setup lang="ts">
import { computed, reactive } from 'vue'
import { calculateDeal, defaultDeal, type DealInput } from '../tools/rules'
const input=reactive(defaultDeal())
const result=computed(()=>calculateDeal(input))
const valid=computed(()=>[input.wisps,input.confessions].every(Number.isInteger)&&input.wisps>=0&&input.wisps<=8&&input.confessions>=0&&input.confessions<=10)
const percent=(n:number)=>(n*100).toFixed(2)+'%'
const doorFlags:[keyof DealInput,string][]=[['contrition','痛悔短祷'],['beggarKilled','炸死乞丐 / 腐烂乞丐 / 电池乞丐'],['devilKilled','本层炸死恶魔乞丐'],['keyKilled','本层炸死钥匙大师'],['shopkeeperKilled','本层炸死店主'],['revelations','持有启示录'],['blackCandle','黑蜡烛'],['belial','持有彼列之书'],['sausage','腊肠'],['goat','山羊头'],['eucharist','圣餐']]
const angelFlags:[keyof DealInput,string][]=[['paid','本局做过恶魔交易'],['virtues','美德之书'],['donated','本层普通捐款机已捐满10枚'],['key1','钥匙碎片1'],['key2','钥匙碎片2'],['beggarPayout','本层乞丐给出道具'],['rosary','念珠段'],['devilPayout','本层恶魔乞丐给出道具']]
</script>
<template>
 <div class="tool-panel">
  <label>版本<select v-model="input.plus" aria-label="版本"><option :value="true">忏悔+</option><option :value="false">忏悔</option></select></label>
  <label><input v-model="input.eligible" type="checkbox" />当前楼层允许主线交易门</label>
  <h2>开门条件</h2>
  <label><input v-model="input.floorClean" type="checkbox" />整层没受红心伤害</label>
  <label><input v-model="input.bossClean" type="checkbox" :disabled="input.floorClean" />Boss 战没受红心伤害（整层无伤时自动满足）</label>
  <div class="tool-grid"><label v-for="[key,label] in doorFlags" :key="key"><input v-model="input[key]" type="checkbox" />{{ label }}</label></div>
  <div class="tool-grid">
   <label>五芒星数量<select v-model.number="input.pentagrams" aria-label="五芒星数量"><option :value="0">0</option><option :value="1">1</option><option :value="2">2或更多</option></select></label>
   <label>撒但圣经魂火（0–8）<input v-model.number="input.wisps" type="number" min="0" max="8" /></label>
   <label>最近一次交易门<select v-model="input.history" aria-label="最近一次交易门"><option value="none">三层以上 / 未出现</option><option value="last">上一层出现（×0.25）</option><option value="two">两层前出现（×0.5）</option></select></label>
  </div>
  <h2>天使判定条件</h2>
  <label>首次恶魔门经历<select v-model="input.previousDoor" aria-label="首次恶魔门经历"><option value="never">还没见过交易门</option><option value="entered">之前见过且进入过</option><option value="skipped">首扇恶魔门完全没进，保底未用</option></select></label>
  <div class="tool-grid"><label v-for="[key,label] in angelFlags" :key="key"><input v-model="input[key]" type="checkbox" />{{ label }}</label></div>
  <div class="tool-grid">
   <label>本层献祭祝福<select v-model.number="input.sacrifice" aria-label="本层献祭祝福"><option :value="0">没有</option><option :value="3">第3次祝福（15%）</option><option :value="5">第5次祝福（50%）</option><option :value="8">两次都有（65%）</option></select></label>
   <label>本层忏悔室祝福次数<input v-model.number="input.confessions" type="number" min="0" max="10" /></label>
  </div>
  <p v-if="!valid" role="alert">魂火请输入0–8整数，忏悔室祝福请输入0–10整数。</p>
  <div v-else class="tool-result deal-result" aria-live="polite">
   <div class="deal-nums">
    <span><small>出现交易门</small><b>{{ percent(result.door) }}</b></span>
    <template v-if="!result.uncertain">
     <span><small>最终是天使房</small><b>{{ percent(result.angelTotal) }}</b></span>
     <span><small>最终是恶魔房</small><b>{{ percent(result.devilTotal) }}</b></span>
    </template>
   </div>
   <p v-if="!result.uncertain">开门后是天使房的比例 {{ percent(result.angel) }}：{{ result.reason }}</p>
   <p v-else>同时满足天使保底和恶魔乞丐的反向判定，资料没写哪个优先，这种组合不给最终房型概率。</p>
   <p class="deal-note">开门加成合计 {{ result.raw.toFixed(2) }}% × 惩罚 {{ result.penalty }}，超过 100% 按 100% 算；山羊头 / 圣餐直接必开。</p>
  </div>
  <details v-if="valid"><summary>查看加成与独立判定明细</summary><ul><li v-for="[name,value] in result.terms" :key="name">{{name}}：+{{value}}%</li></ul><p>天使普通判定为 1 − 所有失败概率的乘积。</p><ul><li v-for="[name,value] in result.checks" :key="name">{{name}}：{{percent(value)}}</li></ul></details>
  <button type="button" @click="Object.assign(input,defaultDeal())">重置条件</button>
 </div>
</template>

<style scoped>
/* 结果贴在屏幕底部：往上勾选条件时随时能看到数字变化 */
.deal-result { position: sticky; bottom: 12px; z-index: 5; box-shadow: 0 4px 0 var(--ib-outline); background: var(--ib-paper); }
.deal-nums { display: flex; flex-wrap: wrap; gap: 8px 24px; }
.deal-nums span { display: flex; flex-direction: column; }
.deal-nums small { font-size: 12px; color: var(--ib-ink-3); }
.deal-nums b { font-family: var(--ib-font-display); font-size: 26px; font-weight: 400; line-height: 1.2; color: var(--ib-blood); }
.deal-note { font-size: 12.5px; color: var(--ib-ink-3); }
</style>
