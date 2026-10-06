import { onMounted, ref, watch, type Ref } from 'vue'
export function useToolStorage<T>(key:string, empty:()=>T, parse:(x:unknown)=>T|null, merge?: (current:T,next:T)=>T) {
  const data=ref(empty()) as Ref<T>
  const message=ref('')
  const storageError=ref('')
  const importMode=ref<'merge'|'replace'>(merge?'merge':'replace')
  let ready=false
  onMounted(()=>{
    try { const raw=localStorage.getItem(key); if(raw) { const next=parse(JSON.parse(raw)); if(next) data.value=next; else message.value='保存的数据格式异常，已使用空白进度。' } }
    catch { storageError.value='无法读取本地进度，可继续使用并导出备份。' }
    ready=true
  })
  watch(data,()=>{ if(!ready)return; try{localStorage.setItem(key,JSON.stringify(data.value));storageError.value=''}catch{storageError.value='本地保存失败，请导出备份；本页仍可继续使用。'} },{deep:true,flush:'sync'})
  function exportFile(){
    try { const url=URL.createObjectURL(new Blob([JSON.stringify(data.value,null,2)],{type:'application/json'})); const a=document.createElement('a');a.href=url;a.download=key+'.json';a.click();URL.revokeObjectURL(url);message.value='已导出当前进度。' }
    catch {message.value='导出失败，请检查浏览器下载设置。'}
  }
  async function importFile(event:Event){
    const input=event.target as HTMLInputElement;const file=input.files?.[0];if(!file)return
    try { if(file.size>1024*1024)throw Error();const next=parse(JSON.parse(await file.text()));if(!next)throw Error();data.value=merge&&importMode.value==='merge'?merge(data.value,next):next;message.value=importMode.value==='merge'?'已核对格式并合并此工具的进度。':'已核对格式并替换此工具的进度。' }
    catch {message.value='导入失败：格式或数值不正确，原进度未改变。'}
    finally{input.value=''}
  }
  return {data,message,storageError,exportFile,importFile,importMode}
}
export const record=(x:unknown):x is Record<string,unknown>=>x!==null && typeof x==='object' && !Array.isArray(x)
export const int=(x:unknown,max:number)=>typeof x==='number' && Number.isInteger(x) && x>=0 && x<=max
export interface ChallengeProgress {v:1; completed:number[]}
export function parseChallenges(x:unknown):ChallengeProgress|null {
  if(!record(x)||x.v!==1||!Array.isArray(x.completed)||!x.completed.every(n=>int(n,45)&&n>=1))return null
  return {v:1,completed:[...new Set(x.completed)].sort((a,b)=>a-b)}
}
export interface DonationProgress {v:1;greed:number;normal:number;characters:Record<string,number>;normalUnlocked?:number[]}
export function parseDonations(x:unknown,ids:string[]):DonationProgress|null {
  if(!record(x)||x.v!==1||!int(x.greed,1000)||!int(x.normal,999)||!record(x.characters))return null
  const chars:Record<string,number>={}
  for(const [key,value]of Object.entries(x.characters)) {
    if(!ids.includes(key)||!int(value,1000000))return null
    chars[key]=value as number
  }
  const milestones = new Set([134,151,135,152,136,153,137,154,59,138])
  if(x.normalUnlocked!==undefined&&(!Array.isArray(x.normalUnlocked)||!x.normalUnlocked.every(n=>milestones.has(n))))return null
  return {v:1,greed:x.greed as number,normal:x.normal as number,characters:chars,
    ...(x.normalUnlocked===undefined?{}:{normalUnlocked:[...new Set(x.normalUnlocked as number[])]})}
}
