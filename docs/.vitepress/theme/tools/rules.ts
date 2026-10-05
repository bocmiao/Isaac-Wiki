// Rules transcribed from strategy/mechanics.md and strategy/greed.md, reviewed 2026-10-05.
export interface DealInput {
  plus: boolean; eligible: boolean; floorClean: boolean; bossClean: boolean
  contrition: boolean; beggarKilled: boolean; devilKilled: boolean; keyKilled: boolean; shopkeeperKilled: boolean
  revelations: boolean; blackCandle: boolean; belial: boolean; pentagrams: number; wisps: number; sausage: boolean
  goat: boolean; eucharist: boolean; history: 'none' | 'last' | 'two'
  previousDoor: 'never' | 'entered' | 'skipped'; paid: boolean; virtues: boolean
  donated: boolean; key1: boolean; key2: boolean; beggarPayout: boolean; devilPayout: boolean
  sacrifice: 0 | 3 | 5 | 8; confessions: number; rosary: boolean
}
export const defaultDeal = (): DealInput => ({
  plus: true, eligible: true, floorClean: true, bossClean: true, contrition: false,
  beggarKilled: false, devilKilled: false, keyKilled: false, shopkeeperKilled: false,
  revelations: false, blackCandle: false, belial: false, pentagrams: 0, wisps: 0, sausage: false,
  goat: false, eucharist: false, history: 'none', previousDoor: 'never', paid: false, virtues: false,
  donated: false, key1: false, key2: false, beggarPayout: false, devilPayout: false,
  sacrifice: 0, confessions: 0, rosary: false,
})
const clamp = (n: number, max: number) => Math.max(0, Math.min(max, Number.isFinite(n) ? n : 0))
export function calculateDeal(i: DealInput) {
  const terms: [string, number][] = [['基础', 1], ['整层红心保护', i.floorClean ? 99 : i.contrition ? 40 : 0], ['Boss 红心保护', i.floorClean || i.bossClean ? 35 : i.contrition ? 15 : 0]]
  if (i.beggarKilled || (i.plus && (i.devilKilled || i.keyKilled))) terms.push(['炸乞丐',35])
  if (i.shopkeeperKilled) terms.push(['炸店主',10])
  if (i.revelations) terms.push(['持有启示录',17.5])
  if (i.blackCandle) terms.push(['黑蜡烛',15])
  if (i.belial) terms.push(['持有彼列之书',12.5])
  if (i.pentagrams > 0) terms.push(['五芒星',10 + (i.pentagrams >= 2 ? 5 : 0)])
  if (i.wisps > 0) terms.push(['撒但圣经魂火',clamp(Math.floor(i.wisps),8)*10])
  if (i.sausage) terms.push(['腊肠',6.9])
  const raw = terms.reduce((n,[,v])=>n+v,0)
  const penalty = i.history==='last' ? 0.25 : i.history==='two' ? 0.5 : 1
  const door = !i.eligible ? 0 : i.goat || i.eucharist ? 1 : clamp(raw*penalty/100,1)
  const checks: [string,number][] = [['基础',0.5]]
  if (i.donated) checks.push(['本层捐款10枚',0.5])
  if (i.key1) checks.push(['钥匙碎片1',0.25])
  if (i.key2) checks.push(['钥匙碎片2',0.25])
  if (i.beggarPayout) checks.push(['乞丐给道具',0.1])
  if (!i.plus && i.devilKilled) checks.push(['炸恶魔乞丐',0.25])
  if (i.sacrifice) checks.push(['献祭祝福',i.sacrifice===3 ? 0.15 : i.sacrifice===5 ? 0.5 : 0.65])
  if (i.confessions>0) checks.push(['忏悔室祝福',clamp(Math.floor(i.confessions)*0.1,1)])
  if (i.rosary) checks.push(['念珠段',i.plus ? 1 : 0.5])
  if (i.virtues) checks.push(['美德之书',0.125])
  let angel = 0, reason = '天使前置未满足'
  const eligibleAngel = !i.paid || i.contrition || i.virtues
  const guaranteed = i.eucharist || (eligibleAngel && i.previousDoor!=='never' && i.plus && i.rosary) || (eligibleAngel && (i.previousDoor==='skipped' || (i.previousDoor==='never' && (i.virtues || i.sacrifice>0 || i.confessions>0))))
  if (guaranteed) { angel=1; reason='满足天使保底 / 圣餐' }
  else if (eligibleAngel && i.previousDoor!=='never') { angel=1-checks.reduce((p,[,v])=>p*(1-v),1); reason='独立判定：1 − ∏(1 − p)' }
  // The source does not specify the precedence of a forced Angel override versus reverse Devil roll.
  const uncertain = guaranteed && i.devilPayout
  if (i.devilPayout && !guaranteed) { angel*=0.9; reason+='；恶魔乞丐反向判定 ×0.9' }
  return { terms, raw, penalty, door, checks, angel, angelTotal:door*angel, devilTotal:door*(1-angel), reason, uncertain }
}
export const sacrificeRewards = [
  '50% 无；50% 1 硬币','50% 无；50% 1 硬币','33% 无；67% 祝福','50% 无；50% 1 个箱子',
  '33% 3 硬币；67% 更强的祝福','33% 传送到天使房（做过交易也行；本层已见恶魔房则回恶魔房）；67% 1 个箱子',
  '33% 天使房道具；67% 魂心。做过交易时，魂心有50%换成赎罪（需解锁）',
  '7 个即爆炸弹（忏悔 / 忏悔+）','乌列','50% 7 魂心；50% 30 硬币','加百列','50% 无；50% 传送到暗室',
]
export function sacrificeReward(count:number) { return sacrificeRewards[Math.min(12,Math.max(1,Math.floor(count)))-1] }
export const greedMilestones = [
  [2,'幸运币'],[14,'特殊吊死店主'],[33,'木制镍币'],[68,'该隐开局回形针'],[111,'Everything is Terrible 2!!!'],
  [234,'特殊店主'],[439,'夏娃开局剃刀片'],[500,'极贪模式'],[666,'商店钥匙'],[879,'游魂开局神圣屏障'],[999,'Generosity'],[1000,'店主；机器爆炸'],
] as const
export function jamChance(coins:number,greedier:boolean):number|null {
  if (!Number.isInteger(coins) || coins<0) return null
  if (coins<=54) return 0
  if (greedier) return 1
  if (coins<=93) return 1
  if (coins<=113) return 2
  if (coins<=126) return 3
  if (coins>=169 && coins<=173) return 10
  if (coins>=200) return 20
  return null // 127–168 and 174–199 are omitted in the source. Never interpolate.
}
export const shopLevels = [0,20,100,200,600]
