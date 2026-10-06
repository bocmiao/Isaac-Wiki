import type { IconName } from '../components/GameIcon.vue'

// 攻略库栏目。group 决定在攻略库页和侧栏里的分组；link 缺省时为 /strategy/<id>
export interface StrategyCategory {
  id: string
  name: string
  icon: IconName
  desc: string
  /** 这一篇能查到什么，攻略库页展示 */
  covers: string[]
  group: StrategyGroup
  link?: string
}

export type StrategyGroup = '规则与选择' | '角色' | 'Boss 与结局' | '特殊模式'
export const strategyGroups: StrategyGroup[] = ['规则与选择', '角色', 'Boss 与结局', '特殊模式']

export const strategyCategories: StrategyCategory[] = [
  {
    id: 'rooms',
    name: '全部房间',
    icon: 'lock',
    desc: '常见与特殊房间的入口、奖励、消耗和打法',
    covers: ['门票与生命条件', '三种隐藏房怎么找', '骰子、卧室、黑市与错误房', '路线功能房与红房间'],
    group: '规则与选择',
  },
  {
    id: 'floors',
    name: '全部楼层',
    icon: 'map',
    desc: '主线变体、母亲路线、上行与贪婪七层',
    covers: ['每章 I / II 与变体', '镜面、矿车和刀片', '照片出口与各终局层', '回家上行与贪婪楼层'],
    group: '规则与选择',
  },
  {
    id: 'mechanics',
    name: '机制详解',
    icon: 'card',
    desc: '恶魔房、天使房、献祭房、商店、诅咒、隐藏房',
    covers: ['恶魔房 / 天使房怎么出', '献祭房每次给什么', '商店、乞丐与机器', '隐藏房怎么找'],
    group: '规则与选择',
  },
  {
    id: 'items',
    name: '道具取舍',
    icon: 'crown',
    desc: '恶魔交易拿不拿、哪些道具值得换心',
    covers: ['道具强弱刻度', '恶魔交易取舍', '天使房 / 宝箱房好道具', '每层流程清单'],
    group: '规则与选择',
  },
  {
    id: 'character-roster',
    name: '角色速查',
    icon: 'key',
    desc: '34 个角色入口、开局强化、完成标记',
    covers: ['34 个角色一览', '开局强化先做哪些', '十二格标记与奖励'],
    group: '角色',
  },
  {
    id: 'characters',
    name: '表角色',
    icon: 'face',
    desc: '17 个表角色怎么玩、先练哪个',
    covers: ['17 个角色定位总表', '逐个角色打法', '新手先练谁'],
    group: '角色',
  },
  {
    id: 'tainted',
    name: '里角色',
    icon: 'face-dark',
    desc: '17 个里角色的机制和上手思路',
    covers: ['里角色总表', '逐个里角色打法', '先练哪个', '合并解锁规则'],
    group: '角色',
  },
  {
    id: 'endings',
    name: '结局与路线',
    icon: 'chest',
    desc: '22 个结局的前置条件和路线',
    covers: ['结局一览表', '教堂 / 阴间 / 虚空 / 母亲 / 家怎么去'],
    group: 'Boss 与结局',
    link: '/guide/unlocks/endings',
  },
  {
    id: 'bosses',
    name: 'Boss 打法',
    icon: 'skull',
    desc: '妈妈的心脏到祸兽，终局 Boss 逐个讲',
    covers: ['（一）心脏、撒但、以撒、???、羔羊、超级撒但', '（二）死寂、精神错乱、母亲、祸兽、究极贪婪'],
    group: 'Boss 与结局',
  },
  {
    id: 'challenges',
    name: '挑战模式',
    icon: 'trophy',
    desc: '45 个挑战总表、先做哪些、难点打法',
    covers: ['全部挑战总表', '优先做哪些', '常卡挑战打法'],
    group: '特殊模式',
  },
  {
    id: 'greed',
    name: '贪婪模式',
    icon: 'coin',
    desc: '贪婪与极贪打法、捐款机里程碑',
    covers: ['贪婪规则', '极贪打法', '捐款机累计奖励'],
    group: '特殊模式',
  },
  {
    id: 'seeds',
    name: '种子',
    icon: 'dice',
    desc: '种子怎么输、彩蛋和特殊种子',
    covers: ['输入方法', '特殊种子一览', '哪些会禁用成就'],
    group: '特殊模式',
  },
]

export const categoryLink = (c: StrategyCategory) => c.link ?? `/strategy/${c.id}`
