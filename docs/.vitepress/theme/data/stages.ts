// 学习路线五个阶段。用以撒的楼层做比喻：越往下越深入。
export interface Stage {
  floor: number
  place: string
  /** 该层在原版里的主色调，用于楼层节点 */
  color: string
  title: string
  summary: string
  link: string
  topics: string[]
  status: 'ready' | 'soon'
}

export const stages: Stage[] = [
  {
    floor: 1,
    place: '地下室',
    color: '#8a6038',
    title: '开局准备',
    summary: '买哪个版本、中文怎么调、按键和模组，开第一局前花 10 分钟看完。',
    link: '/guide/start/',
    topics: ['基础操作', '版本与 DLC', '中文设置'],
    status: 'ready',
  },
  {
    floor: 2,
    place: '洞穴',
    color: '#7a7064',
    title: '第一次通关',
    summary: '认识房间、管好心和资源，打到妈妈并击败她。',
    link: '/guide/first-win/',
    topics: ['房间类型', '心与资源', '第一次打妈妈'],
    status: 'soon',
  },
  {
    floor: 3,
    place: '深处',
    color: '#4b4e58',
    title: '解锁主线',
    summary: '按推荐顺序解锁角色和结局，知道每个结局要先做什么。',
    link: '/guide/unlocks/',
    topics: ['角色解锁顺序', '结局一览', '真结局路线'],
    status: 'soon',
  },
  {
    floor: 4,
    place: '子宫',
    color: '#a23a32',
    title: '进阶思路',
    summary: '恶魔房还是天使房、哪些道具值得换心、每层该做什么。',
    link: '/guide/advanced/',
    topics: ['恶魔与天使', '道具取舍', 'Boss 打法'],
    status: 'soon',
  },
  {
    floor: 5,
    place: '暗室',
    color: '#241e1e',
    title: '里角色与白金神',
    summary: '里角色逐个上手，规划全成就，走完最后一段路。',
    link: '/guide/platinum/',
    topics: ['里角色', '挑战模式', '全成就规划'],
    status: 'soon',
  },
]
