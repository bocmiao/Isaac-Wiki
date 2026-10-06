import lookup from './data.json'
import { achievementExport, challengeExport, characterExport, donationExport } from './exports'
import modeRewards from '../../docs/.vitepress/theme/data/mode-rewards.json'
import { flag, itemState, MAX_SAVE_BYTES, readSave, type SaveProgress } from './save-reader'
import { completionRewardDetail, completionRewardLink } from './completion-rewards'

const SITE = 'https://bocmiao.github.io/Isaac-Wiki'
type Row = { id: string; name: string; group: string; state: string; detail: string; link: string; search?: string }
const labels: Record<string,string> = { locked:'未解锁',uncollected:'已解锁 · 未收集',collected:'已收集',unlocked:'已解锁',special:'隐藏形态 · 按机制获取',unknown:'记录不足 / 无法判断',todo:'未完成',done:'已完成',normal:'普通完成 · 待补困难 / 极贪',hard:'困难 / 极贪完成' }
const missing = new Set(['locked','uncollected','todo','normal'])
const $ = <T extends HTMLElement = HTMLElement>(id: string) => document.getElementById(id) as T
const input = $('file') as HTMLInputElement
const query = $('query') as HTMLInputElement
const group = $('group') as HTMLSelectElement
const state = $('state') as HTMLSelectElement
let progress: SaveProgress | null = null
let rows: Row[] = []
let tab = 'items'
let page = 1
let generation = 0
let loadedAt = ''
let sourceReader: (() => Promise<File>) | null = null
const pageSize = 40

function escape(text: string) { return text.replace(/[&<>"']/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]!)) }
function achievementLink(id: number) {
  const achievement = lookup.achievements.find(row => row.id === id)
  return achievement ? `/achievements/${achievement.page}#achievement-${id}` : '/achievements/'
}
function greedRewardDetail(id: string) {
  const reward=modeRewards.find(row=>row.id===id)
  if (!reward) return ''
  const regular=reward.greed?`${reward.greed.items.map(item=>item.name).join('、')}（成就 #${reward.greed.id}）`:'没有独立的普通贪婪通关奖励；可记标记、捐款。'
  const hard=`${reward.greedier.items.map(item=>item.name).join('、')}（成就 #${reward.greedier.id}）`
  return `\n普通贪婪奖励：${regular}\n极贪奖励：${hard}\n极贪先捐款累计 500 枚开放，需要完成金色二阶段；红标记与捐款里程碑分开计。`
}
function rebuild(keepFilters = false) {
  if (!progress) return
  const previousGroup=group.value,previousQuery=query.value,previousState=state.value,previousPage=page
  const save = progress
  if (tab === 'items') rows = lookup.items.map(item => ({id:item.key,name:item.name,group:item.group,
    state:itemState(save,item),detail:`${item.en}\n${item.effects}\n\n${item.acquisition}`,
    link:`/items/${item.key}`}))
  if (tab === 'achievements') rows = lookup.achievements.filter(row => save.version === 'plus' || row.id <= 637).map(row => {
    const value = flag(save.achievements,row.id)
    return {id:String(row.id),name:row.name,group:row.group,state:value===null?'unknown':value?'done':'todo',
      detail:row.tutorial,link:achievementLink(row.id)}
  })
  if (tab === 'characters') rows = lookup.characters.map(row => {
    const value = row.achievement ? flag(save.achievements,row.achievement) : true
    const condition = lookup.achievements.find(achievement=>achievement.id===row.achievement)
    return {id:row.id,name:row.name,group:row.group,state:value===null?'unknown':value?'unlocked':'locked',
      detail:condition?.tutorial??'以撒初始可用。',link:`/characters/${row.id}`}
  })
  if (tab === 'marks') rows = lookup.characters.flatMap(character => character.marks.map(mark => {
    const value = save.counters[mark.counter]
    return {id:`${character.id}/${mark.id}`,name:`${character.name} · ${mark.name}`,group:character.name,
      state:value===0?'todo':value===1?'normal':value===2?'hard':'unknown',
      detail:(mark.id==='greed'?'普通贪婪与极贪共用这一格；完成极贪后显示为困难状态。'+greedRewardDetail(character.id)+'\n\n':
        '这里显示本角色的实际完成标记；里角色合并奖励是否解锁，会另列说明。\n\n')+completionRewardDetail(save,character,mark.id),
      link:mark.id==='greed'?`/modes/greed-rewards#reward-${character.id}`:completionRewardLink(character.id,mark.id),search:`${character.en} ${mark.name}`}
  }))
  if (tab === 'challenges') rows = lookup.challenges.map(row => {
    const value=flag(save.challenges,row.id)
    return {id:String(row.id),name:row.name,group:row.character,state:value===null?'unknown':value?'done':'todo',
      detail:`${row.description}\n目标：${row.target}\n规则：${row.rules}\n开放前置：${row.unlock}\n奖励：${row.reward}\n\n${row.tutorial}`,
      link:`/challenges/${row.id}`}
  })
  if (tab === 'donations') rows = [
    {id:'normal',name:'普通捐款机',group:'机器总计',state:'unlocked',detail:`当前计数：${save.counters[lookup.donations.normal]} 枚。炸机器可能减少当前余额；已获得的里程碑解锁应另看成就。`,link:'/tools/donations'},
    {id:'greed',name:'贪婪捐款机',group:'机器总计',state:'unlocked',detail:`累计计数：${save.counters[lookup.donations.greed]} 枚。500 枚解锁极贪，879 枚为游魂开局神圣屏障，1000 枚解锁店主。`,link:'/tools/donations'},
    ...lookup.characters.map(character=>({id:character.id,name:character.name+' · 贪婪捐款',group:character.group,state:'unlocked',
      detail:`该角色累计：${save.counters[character.donationCounter]} 枚。卡住概率见网站捐款工具，资料未列出的档位显示为未知。`,link:'/tools/donations'})),
  ]
  group.innerHTML='<option value="">全部分类 / 角色</option>'+[...new Set(rows.map(row=>row.group))].map(name=>`<option>${escape(name)}</option>`).join('')
  if(keepFilters&&rows.some(row=>row.group===previousGroup))group.value=previousGroup
  query.value=keepFilters?previousQuery:'';page=keepFilters?previousPage:1
  state.value=keepFilters?previousState:tab==='donations'?'all':'missing'
  for (const button of document.querySelectorAll<HTMLButtonElement>('[data-tab]')) button.setAttribute('aria-pressed',String(button.dataset.tab===tab))
  render()
}
function matching() {
  const q=query.value.trim().toLowerCase().replace(/^#/,'')
  const idQuery=/^(?:[ctkp])?\d+$/.test(q)
  return rows.filter(row=>(!group.value||row.group===group.value)&&
    (state.value==='all'||(state.value==='missing'?missing.has(row.state):state.value==='complete'?['done','hard','collected','unlocked'].includes(row.state):row.state===state.value))&&
    (!q||(idQuery ? row.id===q || (!/^[ctkp]/.test(q)&&row.id.replace(/^[ctkp]/,'')===q)
      : `${row.id} ${row.name} ${row.detail} ${row.search??''}`.toLowerCase().includes(q))))
}
function render() {
  const selected=matching(),pages=Math.max(1,Math.ceil(selected.length/pageSize))
  page=Math.min(page,pages)
  const unknown=rows.filter(row=>row.state==='unknown').length
  $('count').textContent=`${selected.length} 项 · 第 ${page} / ${pages} 页${unknown?` · 另有 ${unknown} 项无法判断，请切换状态核对`:''}`
  $('results').innerHTML=selected.length?selected.slice((page-1)*pageSize,page*pageSize).map(row=>
    `<article class="result"><div class="top"><span class="badge ${row.state==='unknown'?'unknown':missing.has(row.state)?'todo':'done'}">${labels[row.state]}</span><small>${escape(row.group)}</small><code>${escape(row.id)}</code></div><h3>${escape(row.name)}</h3><details><summary>查看条件、效果与获取步骤</summary><p class="detail">${escape(row.detail)}</p></details><a href="${SITE+row.link}" target="_blank" rel="noreferrer">打开完整教程 ↗</a></article>`).join(''):'<p class="empty">没有匹配条目。可以切换到「全部状态」或清除筛选。</p>'
  $('previous').toggleAttribute('disabled',page===1)
  $('next').toggleAttribute('disabled',page===pages)
  $('pager').textContent=`${page} / ${pages}`
}
async function load(reader: () => Promise<File>, keepFilters = false) {
  const request=++generation
  $('message').textContent='正在读取与核对存档…'
  $('message').className='message'
  try {
    const file=await reader()
    if (file.size>MAX_SAVE_BYTES) throw new Error('文件超过 8 MB，请选择永久进度存档。')
    const result=readSave(await file.arrayBuffer(),file.name)
    if (request!==generation)return
    progress=result;sourceReader=reader;loadedAt=new Date().toLocaleString()
    const done=lookup.achievements.filter(row=>flag(result.achievements,row.id)===true).length
    const collected=lookup.items.filter(item=>item.collection&&flag(result.collectibles,item.id)===true).length
    const slot=/persistentgamedata([123])/.exec(file.name)?.[1]??'未从文件名识别'
    $('message').textContent=`${file.name} · 存档栏 ${slot} · ${result.version==='plus'?'忏悔+':'忏悔'} · 已读取 ${loadedAt}`
    $('stats').textContent=`已解锁成就 ${done} 项 · 当前索引内已收集道具 ${collected} 项 · 45 个挑战 · 34 个角色的真实完成标记`
    $('loaded').hidden=false
    $('refresh').hidden=false
    rebuild(keepFilters)
  } catch(error) {
    if (request!==generation)return
    progress=null;sourceReader=null;rows=[]
    $('loaded').hidden=true;$('refresh').hidden=true
    $('message').textContent=error instanceof Error?error.message:'读取失败。'
    $('message').className='message error'
  }
}
$('choose').addEventListener('click',async()=>{
  const picker=(window as Window & {showOpenFilePicker?: (options:unknown)=>Promise<{getFile:()=>Promise<File>}[]>}).showOpenFilePicker
  if (!picker){input.click();return}
  try {
    const [handle]=await picker.call(window,{multiple:false,types:[{description:'以撒永久进度存档',accept:{'application/octet-stream':['.dat']}}]})
    $('refresh').textContent='重新读取';delete $('refresh').dataset.fallback
    await load(()=>handle.getFile())
  } catch(error) {
    if ((error as DOMException).name==='AbortError')return
    // Browser restrictions may prevent native handles; the ordinary file picker still works offline.
    input.click()
  }
})
input.addEventListener('change',()=>{
  const file=input.files?.[0]
  if(file){void load(async()=>file);$('refresh').textContent='重新选择存档';$('refresh').dataset.fallback='true'}
  input.value=''
})
$('refresh').addEventListener('click',()=>{
  if($('refresh').dataset.fallback==='true') input.click()
  else if(sourceReader)void load(sourceReader,true)
})
for(const button of document.querySelectorAll<HTMLButtonElement>('[data-tab]'))button.addEventListener('click',()=>{tab=button.dataset.tab!;rebuild()})
for(const element of [query,group,state])element.addEventListener('input',()=>{page=1;render()})
$('reset').addEventListener('click',()=>{query.value='';group.value='';state.value='all';page=1;render()})
$('previous').addEventListener('click',()=>{page--;render();$('filters').scrollIntoView({block:'start'})})
$('next').addEventListener('click',()=>{page++;render();$('filters').scrollIntoView({block:'start'})})
function download(contents: string,name: string,type: string) {
  const url=URL.createObjectURL(new Blob([contents],{type}))
  const anchor=document.createElement('a');anchor.href=url;anchor.download=name;anchor.click()
  setTimeout(()=>URL.revokeObjectURL(url),1000)
}
$('export-achievements').addEventListener('click',()=>{
  if(!progress)return
  download(JSON.stringify(achievementExport(progress),null,2),'isaac-achievements.json','application/json')
})
for(const [id,name,make] of [['export-characters','isaac-characters.json',characterExport],['export-challenges','isaac-challenges.json',challengeExport],['export-donations','isaac-donations.json',donationExport]] as const){
 $(id).addEventListener('click',()=>{if(!progress)return;try{download(JSON.stringify(make(progress),null,2),name,'application/json')}catch(error){$('message').textContent=(error as Error).message}})
}
$('export-csv').addEventListener('click',()=>{
  if(!progress)return
  const quote=(value:string)=>'"'+(/^[=+@-]/.test(value)?"'":'')+value.replace(/"/g,'""')+'"'
  const table=[['编号','名称','分类','状态','条件与步骤','教程地址'],...matching().map(row=>[row.id,row.name,row.group,labels[row.state],row.detail,SITE+row.link])]
  download('\uFEFF'+table.map(row=>row.map(quote).join(',')).join('\r\n'),'isaac-'+tab+'-progress.csv','text/csv;charset=utf-8')
})
const drop=$('drop')
drop.addEventListener('dragover',event=>{event.preventDefault();drop.classList.add('dragging')})
drop.addEventListener('dragleave',()=>drop.classList.remove('dragging'))
drop.addEventListener('drop',event=>{
  event.preventDefault();drop.classList.remove('dragging')
  const file=(event as DragEvent).dataTransfer?.files[0]
  if(file){void load(async()=>file);$('refresh').textContent='重新选择存档';$('refresh').dataset.fallback='true'}
})
