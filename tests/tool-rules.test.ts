import assert from 'node:assert/strict'
import { calculateDeal, defaultDeal, jamChance, sacrificeReward, greedMilestones, shopLevels } from '../docs/.vitepress/theme/tools/rules'
import { buildCommand } from '../docs/.vitepress/theme/tools/commands'
import { parseChallenges, parseDonations } from '../docs/.vitepress/theme/tools/storage'
import challenges from '../docs/.vitepress/theme/data/challenges.json'
import normal from '../docs/.vitepress/theme/data/normal-donations.json'
const close=(a:number,b:number)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`)
let d={...defaultDeal(),history:'last' as const,previousDoor:'entered' as const,key1:true}
let r=calculateDeal(d);close(r.door,.3375);close(r.angel,.625);close(r.angelTotal,.2109375);close(r.angelTotal+r.devilTotal,r.door)
close(calculateDeal({...d,history:'two'}).door,.675)
close(calculateDeal({...d,paid:true}).angel,0)
close(calculateDeal({...d,paid:true,contrition:true}).angel,.625)
close(calculateDeal({...d,previousDoor:'skipped'}).angel,1)
close(calculateDeal({...d,previousDoor:'never',sacrifice:3}).angel,1)
close(calculateDeal({...d,sacrifice:8}).angel,1-(.5*.75*.35))
close(calculateDeal({...d,devilPayout:true}).angel,.625*.9)
assert.equal(calculateDeal({...d,eucharist:true,devilPayout:true}).uncertain,true)
close(calculateDeal({...d,eligible:false,goat:true}).door,0)
const noDoor=calculateDeal({...d,eligible:false,eucharist:true,devilPayout:true})
assert.equal(noDoor.uncertain,false)
close(noDoor.angelTotal,0);close(noDoor.devilTotal,0)
let base={...defaultDeal(),floorClean:false,bossClean:false,previousDoor:'entered' as const}
close(calculateDeal({...base,plus:false,devilKilled:true}).door,.01)
close(calculateDeal({...base,plus:true,devilKilled:true}).door,.36)
close(calculateDeal({...base,plus:false,devilKilled:true}).angel,.625)
close(calculateDeal({...base,contrition:true}).door,.56)
assert.deepEqual([54,55,93,94,113,114,126,127,168,169,173,174,199,200].map(n=>jamChance(n,false)),[0,1,1,2,2,3,3,null,null,10,10,null,null,20])
assert.deepEqual([54,55,127,200].map(n=>jamChance(n,true)),[0,1,1,1])
assert.equal(sacrificeReward(12),sacrificeReward(100));assert.match(sacrificeReward(8),/7 个即爆炸弹/)
assert.deepEqual(challenges.map(c=>c.id),Array.from({length:45},(_,i)=>i+1));assert.equal(challenges[44].name,'DELETE THIS')
assert.deepEqual(shopLevels,[0,20,100,200,600]);assert.equal(greedMilestones.at(-1)?.[0],1000)
assert.deepEqual(normal.map(x=>x.coins),[10,20,50,100,150,200,400,600,900,999])
assert.deepEqual(parseChallenges({v:1,completed:[45,1,1]}),{v:1,completed:[1,45]})
for(const x of [{v:1,completed:[0]},{v:1,completed:[46]},{v:1,completed:['1']},{v:2,completed:[]},{v:1,completed:null}])assert.equal(parseChallenges(x),null)
assert.equal(parseDonations({v:1,greed:1001,normal:0,characters:{}},['isaac']),null)
assert.equal(parseDonations({v:1,greed:0,normal:0,characters:{unknown:10}},['isaac']),null)
assert.equal(parseDonations({v:1,greed:0,normal:0,characters:{isaac:-1}},['isaac']),null)
assert.deepEqual(parseDonations({v:1,greed:500,normal:900,characters:{isaac:127}},['isaac']),{v:1,greed:500,normal:900,characters:{isaac:127}})
const command={action:'give',item:105,player:0,stage:1,suffix:'',debug:8,version:'plus'}
assert.equal(buildCommand(command),'g c105');assert.equal(buildCommand({...command,action:'pedestal',item:118}),'spawn 5.100.118')
assert.equal(buildCommand({...command,item:999999}),null);assert.equal(buildCommand({...command,action:'restart',player:37}),'restart 37')
assert.equal(buildCommand({...command,action:'restart',player:20}),null)
assert.equal(buildCommand({...command,action:'stage',stage:8,suffix:'c'}),'stage 8c')
assert.equal(buildCommand({...command,action:'stage',stage:13,suffix:'a'}),null)
assert.equal(buildCommand({...command,action:'debug',debug:14,version:'rep'}),null)
assert.equal(buildCommand({...command,action:'debug',debug:14}),'debug 14')
console.log('PASS probability ordering/overrides, omitted jam bands, source milestones, import validation and console syntax')
