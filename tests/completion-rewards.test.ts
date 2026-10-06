import assert from 'node:assert/strict'
import { completionRewardDetail, completionRewardLink, rewardsForMark } from '../local-tools/progress/completion-rewards'
import { type SaveProgress } from '../local-tools/progress/save-reader'
import lookup from '../local-tools/progress/data.json'

const save: SaveProgress = {format:'09R',filename:'rep+persistentgamedata1.dat',version:'plus',achievements:Array(642).fill(0),collectibles:Array(733).fill(0),counters:Array(512).fill(0),challenges:Array(46).fill(0)}
const character=lookup.characters.find(c=>c.id==='tainted-isaac')!
const counter=(id:string)=>character.marks.find(m=>m.id===id)!.counter
save.counters[counter('isaac')]=1
save.counters[counter('bluebaby')]=2
save.counters[counter('satan')]=2
let detail=completionRewardDetail(save,character,'isaac')
assert(detail.includes('成就 #548'))
assert(detail.includes('本角色此标记途径还缺：羔羊（未完成）'))
assert(!detail.includes('以撒（未完成）'))
save.achievements[548]=1
detail=completionRewardDetail(save,character,'isaac')
assert(detail.includes('奖励解锁状态：已解锁'))
assert(detail.includes('羔羊（未完成）')) // Reward flags must never set missing marks.
assert.equal(save.counters[counter('lamb')],0)
save.counters[counter('lamb')]=1
assert(completionRewardDetail(save,character,'isaac').includes('所列标记条件已满足'))
save.counters[counter('bossrush')]=2
assert(completionRewardDetail(save,character,'bossrush').includes('死寂（未完成）'))
save.counters[counter('greed')]=1
assert(completionRewardDetail(save,character,'greed').includes('仅普通贪婪，需极贪'))
assert(completionRewardDetail(save,character,'heart').includes('没有独立的里角色奖励'))
assert.equal(completionRewardLink(character.id,'isaac'),'/characters/tainted-isaac#reward-main-four')
assert.equal(completionRewardLink(character.id,'hush'),'/characters/tainted-isaac#reward-timed-pair')
assert.equal(completionRewardLink(character.id,'heart'),'/characters/tainted-isaac#completion-rewards')
const judas=lookup.characters.find(c=>c.id==='judas')!
save.achievements[77]=1
assert(completionRewardDetail(save,judas,'bluebaby').includes('超级傲慢'))
assert(completionRewardDetail(save,judas,'bluebaby').includes('???（未完成）'))
const lost=lookup.characters.find(c=>c.id==='lost')!
for(const mark of lost.marks)save.counters[mark.counter]=2
save.counters[lost.marks.find(m=>m.id==='heart')!.counter]=1
assert(completionRewardDetail(save,lost,'isaac').includes('仅普通，需困难'))
save.counters[lost.marks.find(m=>m.id==='heart')!.counter]=99
assert(completionRewardDetail(save,lost,'isaac').includes('记录不足 / 无法判断'))
const short={...save,achievements:Array(548).fill(0)}
assert(completionRewardDetail(short,character,'isaac').includes('奖励解锁状态：记录不足 / 无法判断'))
assert.equal(rewardsForMark('isaac','heart').find(r=>r.kind==='heart')!.minimum,2)
console.log('PASS current-character composite prerequisites, difficulty gaps, independent achievement flags, alternate unlocks and unknown records')
