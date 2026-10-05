// Syntax from topics/debug-console-commands.md. IDs are validated against the reviewed tables.
import items from '../data/item-links.json'
const ids=new Set(items.map(i=>i.id))
export const playerIds=[0,1,2,3,4,5,6,7,8,9,10,13,14,15,16,18,19,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
export interface CommandInput {action:string;item:number;player:number;stage:number;suffix:string;debug:number;version:string}
export function buildCommand(i:CommandInput):string|null {
 if(['give','remove','pedestal','give2'].includes(i.action)){
  if(!ids.has(i.item))return null
  return i.action==='give'?`g c${i.item}`:i.action==='remove'?`r c${i.item}`:i.action==='give2'?`g2 c${i.item}`:`spawn 5.100.${i.item}`
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
