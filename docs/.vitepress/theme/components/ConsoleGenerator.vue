<script setup lang="ts">
import { computed, reactive, ref } from 'vue'

import { characters, taintedName } from '../data/characters'
import { buildCommand, playerIds, commandItems, findCommandItems, stageNames } from '../tools/commands'
const input=reactive({action:'give',kind:'c',item:105,player:0,stage:1,suffix:'',debug:3,version:'plus'})
const query=ref(''),queue=ref<string[]>([]),message=ref('')
const filtered=computed(()=>findCommandItems(query.value,input.kind))
const selected=computed(()=>commandItems.find(i=>i.id===input.kind+input.item))
function changeKind(){query.value='';input.item=commandItems.find(i=>i.id.startsWith(input.kind))?.gameId??0}
const itemAction=computed(()=>['give','remove','pedestal','give2'].includes(input.action))
const command=computed(()=>buildCommand(input))
const roster=characters.flatMap((c,index)=>[{id:playerIds[index],name:c.name},{id:playerIds[17+index],name:taintedName(c)}])
const text=computed(()=>queue.value.length?queue.value.join('\n'):command.value??'')
async function copy(){try{await navigator.clipboard.writeText(text.value);message.value='已复制命令。'}catch{message.value='无法自动复制，请选中下方文本手动复制。'}}
function add(){if(command.value&&queue.value.length<100){queue.value.push(command.value);message.value='已加入清单。'}else message.value='命令无效或清单已满100条。'}
</script>
<template>
 <div class="tool-panel">
  <div class="tool-grid"><label>游戏版本<select v-model="input.version" aria-label="游戏版本"><option value="plus">忏悔+</option><option value="rep">忏悔</option></select></label><label>操作<select v-model="input.action" aria-label="操作"><option value="give">直接给道具</option><option value="pedestal">生成地上道具底座</option><option value="remove">移除道具</option><option value="give2">给次角色（如以扫）</option><option value="restart">指定角色开新局</option><option value="stage">切楼层</option><option value="debug">切换 debug 开关</option><option value="time">读取时间</option><option value="listcollectibles">列出持有道具</option><option value="clear">清屏</option></select></label></div>
  <template v-if="itemAction"><label>物品类型<select v-model="input.kind" aria-label="物品类型" @change="changeKind"><option value="c">道具 c</option><option value="t">饰品 t</option><option value="k">卡牌 / 符文 / 魂石 k</option><option value="p">胶囊效果 p</option></select></label><label>搜索道具<input v-model="query" type="search" placeholder="中文、英文或ID" /></label><label>选择道具<select v-model.number="input.item" aria-label="选择道具"><option v-for="i in filtered" :key="i.id" :value="i.gameId">{{i.id}} · {{i.name}} · {{i.en}}</option></select></label><p v-if="!filtered.length">没有找到道具；搜索不会自动改动之前已选的编号。</p></template>
  <label v-if="input.action==='restart'">开局角色<select v-model.number="input.player" aria-label="开局角色"><option v-for="c in roster" :key="c.id" :value="c.id">{{c.id}} · {{c.name}}</option></select></label>
  <div v-if="input.action==='stage'" class="tool-grid"><label>楼层编号（1–13）<select v-model.number="input.stage" aria-label="楼层名称"><option v-for="(name,index) in stageNames" :key="index" :value="index+1">{{index+1}} · {{name}}</option></select></label><label>楼层变体<select v-model="input.suffix" aria-label="楼层变体"><option value="">默认</option><option value="a">a</option><option value="b">b</option><option value="c">c</option><option value="d">d</option></select></label></div>
  <label v-if="input.action==='debug'">debug编号<input v-model.number="input.debug" type="number" min="1" :max="input.version==='plus'?14:13" /></label>
  <div class="tool-result" aria-live="polite"><strong>当前命令：{{command??'参数组合无效，请查命令表'}}</strong></div>
  <p v-if="itemAction">已选道具：{{selected?.name}}（{{input.kind}}{{input.item}}）。直接给道具与生成底座不同；搜索结果变化不会替你重新选择道具。</p>
  <p v-if="itemAction">胶囊只按效果生成给予命令，不把效果编号写成地上胶囊颜色。金胶囊占位编号不生成命令。移除支持道具 / 饰品，次角色给予支持道具；其他组合提示无效。</p>
  <p v-if="input.action==='restart'">会替换当前局；不等于永久解锁角色，也不会自动补齐开局强化。</p>
  <p v-if="input.action==='debug'">编号是开关：同号再执行会关闭。批量重复不等于保持开启。</p>
  <p v-if="input.action==='stage'">楼层变体含义见命令表；普通主线与贪婪的楼层编号对应不同。</p>
  <div class="tool-actions"><button :disabled="!command" @click="add">加入命令清单</button><button :disabled="!text" @click="copy">复制命令</button><button @click="queue=[]">清空清单</button><button :disabled="!queue.length" @click="queue.pop()">移除最后一条</button></div>
  <label>可复制的命令<textarea :value="text" aria-label="可复制的命令" readonly rows="8" spellcheck="false" /></label><p role="status">{{message}}</p>
  <p>只生成文本，不执行命令、不连接游戏。清空本页清单不会撤销游戏中已执行的命令。此版本不生成永久成就批量解锁，也不替模组自定义实体猜编号。</p>
 </div>
</template>
