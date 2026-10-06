import assert from 'node:assert/strict'
import { parseAchievementIds } from '../docs/.vitepress/theme/tools/achievements'
import { calibrateDonations, confirmedShopLevel } from '../docs/.vitepress/theme/tools/donations'
import { parseChallenges, parseDonations } from '../docs/.vitepress/theme/tools/storage'
import { emptyProgress, parseProgress, mergeProgress } from '../docs/.vitepress/theme/progress'
import { buildCommand, findCommandItems } from '../docs/.vitepress/theme/tools/commands'
import { characterExport, challengeExport, donationExport } from '../local-tools/progress/exports'
import type { SaveProgress } from '../local-tools/progress/save-reader'
import lookup from '../local-tools/progress/data.json'
for(const value of [{v:1,done:['1']},{v:1,done:[1,642]},{v:2,done:[1]}, {done:[1]},[1,null],null])assert.equal(parseAchievementIds(value),null)
assert.deepEqual(parseAchievementIds({v:1,done:[29,1,29]}),[1,29]);assert.deepEqual(parseAchievementIds({v:1,done:[]}),[])
const old={v:1 as const,greed:0,normal:600,characters:{},normalUnlocked:[154]}
const calibrated=calibrateDonations(old,'isaac',500,20,'')!
assert.deepEqual(calibrated.characters,{});assert.equal(confirmedShopLevel(calibrated),4);assert.equal(old.normal,600)
assert.deepEqual(calibrateDonations(calibrated,'isaac',500,20,0)!.characters,{isaac:0})
assert.equal(calibrateDonations(old,'isaac',1001,20,''),null)
const cmd={action:'give',item:1,player:0,stage:1,suffix:'',debug:3,version:'plus'}
assert.equal(buildCommand({...cmd,kind:'t'}),'g t1');assert.equal(buildCommand({...cmd,kind:'k'}),'g k1')
assert.equal(buildCommand({...cmd,item:0,kind:'p'}),'g p0');assert.equal(buildCommand({...cmd,item:9999,kind:'p'}),null)
assert.equal(buildCommand({...cmd,kind:'p',action:'pedestal'}),null)
assert.equal(buildCommand({...cmd,kind:'k',action:'remove'}),null)
assert.deepEqual(findCommandItems('1','t').map(x=>x.id),['t1'])
assert.deepEqual(findCommandItems('p9999','p'),[])
const save:SaveProgress={format:'09R',version:'plus',filename:'fixture.dat',achievements:Array(642).fill(0),collectibles:Array(733).fill(0),challenges:Array(46).fill(0),counters:Array(512).fill(0)}
save.achievements[154]=1;save.challenges[45]=1;save.counters[20]=20;save.counters[115]=500
const tainted=lookup.characters.find(c=>c.id==='tainted-isaac')!
save.achievements[tainted.achievement]=1;save.counters[tainted.marks[0].counter]=2
const exported=characterExport(save);assert.equal(exported.tainted.isaac,true);assert.equal(exported.marks['isaac-t:heart'],2)
assert(parseProgress(exported));assert.deepEqual(parseChallenges(challengeExport(save)),{v:1,completed:[45]})
assert.deepEqual(donationExport(save).normalUnlocked,[154])
assert(parseDonations(donationExport(save),lookup.characters.map(c=>c.id.replace(/^tainted-(.*)$/,'$1-t'))))
const current=emptyProgress();current.marks['isaac:heart']=2;current.chars.cain=true
const merged=mergeProgress(current,exported);assert.equal(merged.marks['isaac:heart'],2);assert.equal(merged.chars.cain,true)
assert.equal(current.tainted.isaac,undefined)
console.log('PASS strict imports, unknown donation history, permanent milestones, typed commands and local-to-site exports')
