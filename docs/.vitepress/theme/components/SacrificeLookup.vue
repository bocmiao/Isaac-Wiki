<script setup lang="ts">
import { computed, ref } from 'vue'
import { sacrificeReward, sacrificeRewards } from '../tools/rules'
const count=ref(1)
const valid=computed(()=>Number.isInteger(count.value)&&count.value>=1&&count.value<=999)
const reward=computed(()=>valid.value?sacrificeReward(count.value):'请输入1–999之间的整数')
</script>
<template>
 <div class="tool-panel">
  <label>本层第几次有效献祭<input v-model.number="count" type="number" min="1" max="999" /></label>
  <div class="tool-actions"><button @click="count=Math.max(1,(Number(count)||1)-1)">上一次</button><button @click="count=Math.min(999,(Number(count)||1)+1)">下一次</button><button @click="count=1">换层，重置为第1次</button></div>
  <div class="tool-result" aria-live="polite"><strong>{{valid?`第${count}次`:'次数无效'}}</strong><p>{{reward}}</p></div>
  <p>这里只查询本层有效扣血次数；护盾挡掉伤害不计次，换层清零。12次及以后每次仍按同一档，不是第12次必进暗室。</p>
  <table><thead><tr><th>次数</th><th>结果（忏悔 / 忏悔+）</th></tr></thead><tbody><tr v-for="(text,index) in sacrificeRewards" :key="index"><td>{{index===11?'12起':index+1}}</td><td>{{text}}</td></tr></tbody></table>
 </div>
</template>
