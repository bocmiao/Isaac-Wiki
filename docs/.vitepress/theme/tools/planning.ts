import routes from '../data/routes.json'
import synergies from '../data/synergies.json'
import { record, int } from './storage'
export const gates = [
  {id:'heart10',text:'心脏累计打败 10 次（蓝子宫）'},
  {id:'heart11',text:'心脏累计打败 11 次（它活着）'},
  {id:'isaac5',text:'以撒累计打败 5 次（全家福）'},
  {id:'satan5',text:'撒但累计打败 5 次（底片）'},
  {id:'chapter6',text:'通关过宝箱或暗室（超级撒但金门）'},
  {id:'hush1',text:'打败过死寂（虚空）'},
  {id:'hush3',text:'死寂累计打败 3 次（秘密出口）'},
  {id:'mother1',text:'打败过母亲（奇怪的门）'},
  {id:'greed500',text:'贪婪捐款累计 500 枚（极贪）'},
]
export interface RouteProgress {v:1;target:string;unlocks:string[];completed:Record<string,string[]>}
export const emptyRoutes=():RouteProgress=>({v:1,target:'blue',unlocks:[],completed:{}})
export function parseRoutes(x:unknown):RouteProgress|null {
  if(!record(x)||x.v!==1||typeof x.target!=='string'||!routes.some(r=>r.id===x.target)||!Array.isArray(x.unlocks)||!x.unlocks.every(k=>typeof k==='string'&&gates.some(g=>g.id===k))||!record(x.completed))return null
  const completed:Record<string,string[]>={}
  for(const [key,value] of Object.entries(x.completed)) {
    const route=routes.find(r=>r.id===key)
    if(!route||!Array.isArray(value)||!value.every(s=>typeof s==='string'&&route.steps.some(t=>t.id===s)))return null
    completed[key]=[...new Set(value)]
  }
  return {v:1,target:x.target,unlocks:[...new Set(x.unlocks)],completed}
}
export function effectiveUnlocks(unlocks:string[]) {
  const set=new Set(unlocks)
  if(set.has('heart11'))set.add('heart10')
  if(set.has('hush3'))set.add('hush1')
  return set
}
export function missingGates(target:string,unlocks:string[],branch='blue') {
  const route=routes.find(r=>r.id===target);if(!route)return []
  const requirements=[...route.requirements]
  if(target==='mega')requirements.push('heart11',branch==='lamb'?'satan5':'isaac5')
  const known=effectiveUnlocks(unlocks)
  return gates.filter(g=>requirements.includes(g.id)&&!known.has(g.id))
}
export interface ComboProgress {v:1;owned:number[]}
const supported=new Set(synergies.flatMap(s=>s.items))
export function parseCombos(x:unknown):ComboProgress|null {
  if(!record(x)||x.v!==1||!Array.isArray(x.owned)||!x.owned.every(n=>int(n,1000)&&supported.has(n)))return null
  return {v:1,owned:[...new Set(x.owned)].sort((a,b)=>a-b)}
}
export const synergyState=(items:number[],owned:number[])=>items.every(n=>owned.includes(n))?'ready':items.some(n=>owned.includes(n))?'partial':'none'
