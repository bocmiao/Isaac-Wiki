import lookup from './data.json'
import type { SaveProgress } from './save-reader'
import { flag } from './save-reader'
export function achievementExport(save:SaveProgress){return {v:1,done:lookup.achievements.filter(a=>flag(save.achievements,a.id)===true).map(a=>a.id)}}
export function challengeExport(save:SaveProgress){return {v:1,completed:lookup.challenges.filter(c=>flag(save.challenges,c.id)===true).map(c=>c.id)}}
export function characterExport(save:SaveProgress){
 const chars:Record<string,boolean>={isaac:true},tainted:Record<string,boolean>={},marks:Record<string,number>={}
 for(const character of lookup.characters){
  const isTainted=character.id.startsWith('tainted-'),id=character.id.replace(/^tainted-/,'')
  const unlocked=character.achievement?flag(save.achievements,character.achievement):true
  if(unlocked!==null)(isTainted?tainted:chars)[id]=unlocked
  for(const mark of character.marks){const value=save.counters[mark.counter];if(value===1||value===2)marks[`${id}${isTainted?'-t':''}:${mark.id}`]=value}
 }
 return {v:1,chars,tainted,marks}
}
export function donationExport(save:SaveProgress){
 const greed=save.counters[lookup.donations.greed],normal=save.counters[lookup.donations.normal]
 if(greed>1000||normal>999)throw Error('捐款计数超出已核对范围，未生成导入文件。')
 const characters:Record<string,number>={}
 for(const character of lookup.characters){const value=save.counters[character.donationCounter];if(value<=1000000)characters[character.id.replace(/^tainted-(.*)$/,'$1-t')]=value}
 const ids=[134,151,135,152,136,153,137,154,59,138]
 return {v:1,greed,normal,characters,normalUnlocked:ids.filter(id=>flag(save.achievements,id)===true)}
}
