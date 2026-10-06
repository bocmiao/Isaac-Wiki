import assert from 'node:assert/strict'
import { crc32 } from 'node:zlib'
import { flag, itemState, readSave, saveChecksum } from '../local-tools/progress/save-reader'
import lookup from '../local-tools/progress/data.json'

function u32(value:number) { const result=Buffer.alloc(4);result.writeUInt32LE(value);return result }
function block(type:number,body:Buffer,count=body.length) { return Buffer.concat([u32(type),u32(body.length),u32(count),body]) }
function fixture(achievementCount=642) {
  const achievements=Buffer.alloc(achievementCount);achievements[1]=1;achievements[29]=1;achievements[82]=1;achievements[641]=achievementCount>641?1:0
  const collectibles=Buffer.alloc(733);collectibles[105]=1
  const counters=Buffer.alloc(512*4)
  for(const [id,value] of [[20,100],[115,879],[27,1],[173,2],[203,2],[216,1],[440,2],[471,2]])counters.writeUInt32LE(value,id*4)
  const challenges=Buffer.alloc(46);challenges[1]=1
  const bestiary=Buffer.concat([1,2,3,4].map(id=>Buffer.concat([u32(id),u32(0)])))
  const bytes=Buffer.concat([Buffer.from('ISAACNGSAVE09R  '),u32(0),
    block(1,achievements),block(2,counters,512),block(3,Buffer.alloc(0),0),block(4,collectibles),
    block(5,Buffer.alloc(0)),block(6,Buffer.alloc(0)),block(7,challenges),block(8,Buffer.alloc(0)),
    block(9,Buffer.alloc(4),1),block(10,Buffer.alloc(0)),block(11,bestiary,4),Buffer.alloc(8)])
  bytes.writeUInt32LE(crc32(bytes.subarray(16,-4),0xfedcba76),bytes.length-4)
  return bytes
}
function buffer(bytes:Buffer) { return Uint8Array.from(bytes).buffer }
const sample=fixture()
assert.equal(saveChecksum(sample),sample.readUInt32LE(sample.length-4)) // independent built-in CRC
const save=readSave(buffer(sample),'rep+persistentgamedata2.dat')
assert.equal(save.version,'plus')
assert.equal(flag(save.achievements,1),true)
assert.equal(flag(save.achievements,2),false)
assert.equal(flag(save.achievements,641),true)
assert.equal(flag(save.achievements,642),null)
assert.equal(flag(save.collectibles,105),true)
assert.equal(save.counters[115],879)
assert.equal(save.challenges[1],1)
assert.equal(itemState(save,lookup.items.find(item=>item.key==='c105')!),'collected')
assert.equal(itemState(save,lookup.items.find(item=>item.key==='c118')!),'uncollected')
assert.equal(itemState(save,lookup.items.find(item=>item.key==='c59')!),'special')
assert.equal(itemState(save,{kind:'t',id:105,unlocks:[],collection:false}),'unlocked')
assert.equal(itemState(save,{kind:'c',id:105,unlocks:[2],collection:true}),'locked')
assert.equal(itemState(save,{kind:'c',id:105,unlocks:[9999],collection:true}),'unknown')
const rep=readSave(buffer(fixture(638)),'rep_persistentgamedata1.dat')
assert.equal(rep.version,'rep')
assert.equal(flag(rep.achievements,641),null)
assert.throws(()=>readSave(new ArrayBuffer(10)),/太短/)
assert.throws(()=>readSave(new ArrayBuffer(28)),/不支持/)
const corrupt=Buffer.from(sample);corrupt[40]^=1
assert.throws(()=>readSave(buffer(corrupt)),/校验/)
assert.throws(()=>readSave(buffer(sample.subarray(0,-4))),/校验/)
const unknown=Buffer.from(sample);unknown.writeUInt32LE(12,20)
unknown.writeUInt32LE(crc32(unknown.subarray(16,-4),0xfedcba76),unknown.length-4)
assert.throws(()=>readSave(buffer(unknown)),/未知/)
const oversized=Buffer.from(sample);oversized.writeUInt32LE(0xffffffff,24)
oversized.writeUInt32LE(crc32(oversized.subarray(16,-4),0xfedcba76),oversized.length-4)
assert.throws(()=>readSave(buffer(oversized)),/越界/)
const invalid=Buffer.from(sample);invalid[33]=3
invalid.writeUInt32LE(crc32(invalid.subarray(16,-4),0xfedcba76),invalid.length-4)
assert.throws(()=>readSave(buffer(invalid)),/布尔/)
assert.deepEqual(lookup.donations,{normal:20,greed:115})
assert.equal(lookup.characters.find(row=>row.id==='forgotten')!.marks.find(mark=>mark.id==='heart')!.counter,203)
assert.equal(lookup.characters.find(row=>row.id==='tainted-isaac')!.marks.find(mark=>mark.id==='heart')!.counter,216)
assert.equal(lookup.characters.find(row=>row.id==='forgotten')!.marks.find(mark=>mark.id==='beast')!.counter,471)
assert.equal(new Set(lookup.characters.flatMap(row=>row.marks.map(mark=>mark.counter))).size,408)
assert.equal(lookup.characters.find(row=>row.id==='tainted-lost')!.achievement,484)
assert(lookup.achievements.every(row=>row.tutorial.includes(row.conditionZh)))
console.log('PASS read-only 09R arrays, independent CRC, truncated/corrupt/new formats, collection-vs-unlock and exact character counters')
