import type { IconName } from '../components/GameIcon.vue'

// 攻略库栏目，对应计划书「教程与攻略内容矩阵」。batch = 计划上线批次
export interface StrategyCategory {
  id: string
  name: string
  icon: IconName
  desc: string
  plan: string[]
  batch: 1 | 2 | 3
  /** 已有正式内容 */
  ready?: boolean
}

export const strategyCategories: StrategyCategory[] = [
  {
    id: 'endings',
    name: '结局与路线',
    icon: 'chest',
    desc: '每个结局的前置条件和分支路线怎么走',
    plan: ['结局一览与前置条件', '各分支路线详细打法'],
    batch: 1,
    ready: true,
  },
  {
    id: 'unlocks',
    name: '解锁与白金神',
    icon: 'key',
    desc: '角色解锁顺序、完成标记、全成就规划',
    plan: ['角色解锁顺序', '完成标记说明', '全成就规划'],
    batch: 1,
    ready: true,
  },
  {
    id: 'mechanics',
    name: '机制详解',
    icon: 'card',
    desc: '恶魔房与天使房、献祭房、商店、诅咒、隐藏房',
    plan: ['恶魔房与天使房的出现规则', '献祭房', '商店、赌博机与乞丐', '诅咒', '隐藏房怎么找'],
    batch: 2,
    ready: true,
  },
  {
    id: 'items',
    name: '道具取舍与流派',
    icon: 'crown',
    desc: '恶魔交易拿不拿、强力组合、每层该做什么',
    plan: ['恶魔交易怎么取舍', '哪些道具值得换心', '常见强力组合', '每层该做什么'],
    batch: 2,
    ready: true,
  },
  {
    id: 'characters',
    name: '表角色攻略',
    icon: 'face',
    desc: '17 个表角色各自怎么玩、先练哪个',
    plan: ['新手先练哪个角色', '17 个表角色逐个上手'],
    batch: 2,
    ready: true,
  },
  {
    id: 'bosses',
    name: 'Boss 打法',
    icon: 'skull',
    desc: '终局 Boss 优先，之后补普通 Boss',
    plan: ['妈妈与妈妈的心脏', '以撒与撒但', '羔羊与超级撒但', '死寂、精神错乱、母亲、祸兽', '普通 Boss'],
    batch: 2,
    ready: true,
  },
  {
    id: 'tainted',
    name: '里角色攻略',
    icon: 'face-dark',
    desc: '17 个里角色的解锁、机制和上手思路',
    plan: ['里角色怎么解锁', '17 个里角色逐个上手'],
    batch: 3,
  },
  {
    id: 'challenges',
    name: '挑战模式',
    icon: 'trophy',
    desc: '全部挑战逐个讲解，先做解锁重要道具的',
    plan: ['挑战优先级', '全部挑战逐个讲解'],
    batch: 3,
  },
  {
    id: 'greed',
    name: '贪婪模式',
    icon: 'coin',
    desc: '贪婪与极贪打法、捐款机与相关解锁',
    plan: ['贪婪模式入门', '极贪模式', '捐款机与相关解锁'],
    batch: 3,
  },
  {
    id: 'seeds',
    name: '种子',
    icon: 'dice',
    desc: '彩蛋种子、特殊种子、种子怎么输',
    plan: ['种子怎么输入', '彩蛋种子与特殊种子'],
    batch: 3,
  },
]

export const batchLabel = { 1: '首批', 2: '第二批', 3: '第三批' } as const
