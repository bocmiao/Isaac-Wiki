// IDs come from the full reviewed catalog. Pill effect IDs never become pickup color IDs.
import catalog from '../data/catalog/items.json'
import { filterCatalog } from '../data/catalog'
export const commandItems = catalog.filter(item => item.id !== 'p9999' && item.id !== 'c59')
const ids = new Set(commandItems.map(i => i.id))
export const playerIds=[0,1,2,3,4,5,6,7,8,9,10,13,14,15,16,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
export const stageNames=['地下室 I','地下室 II','洞穴 I','洞穴 II','深处 I','深处 II','子宫 I','子宫 II','蓝子宫','阴间','暗室','虚空','家']
export interface CommandInput {action:string;item:number;kind?:string;player:number;stage:number;suffix:string;debug:number;version:string}
export function findCommandItems(query:string,kind='c') {
 return filterCatalog(commandItems.filter(item=>item.id.startsWith(kind)),query)
}
export function buildCommand(i:CommandInput):string|null {
 if(['give','remove','pedestal','give2'].includes(i.action)){
  const kind=i.kind??'c', key=kind+i.item
  if(!ids.has(key))return null
  // Remove / secondary-player syntax is verified for collectibles and trinkets only.
  if(i.action==='remove'&&!['c','t'].includes(kind))return null
  if(i.action==='give2'&&kind!=='c')return null
  if(i.action==='pedestal')return kind==='c'?`spawn 5.100.${i.item}`:kind==='t'?`spawn 5.350.${i.item}`:kind==='k'?`spawn 5.300.${i.item}`:null
  return i.action==='give'?`g ${key}`:i.action==='remove'?`r ${key}`:`g2 ${key}`
 }
 if(i.action==='restart')return playerIds.includes(i.player)?`restart ${i.player}`:null
 if(i.action==='debug')return Number.isInteger(i.debug)&&i.debug>=1&&i.debug<=(i.version==='plus'?14:13)?`debug ${i.debug}`:null
 if(i.action==='stage'){
  if(!Number.isInteger(i.stage)||i.stage<1||i.stage>13)return null
  const allowed=i.stage<=6?['','a','b','c','d']:i.stage<=8?['','a','b','c']:i.stage===10||i.stage===11?['','a']:['']
  return allowed.includes(i.suffix)?`stage ${i.stage}${i.suffix}`:null
 }
 return ['time','listcollectibles','clear'].includes(i.action)?i.action:null
}
