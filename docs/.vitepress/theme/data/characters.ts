// 角色解锁条件，核对来源：bindingofisaacrebirth.wiki.gg 各角色页面（2026-10）。
// 中文译名暂用社区常用叫法，后续按游戏官方中文统一。

export interface Character {
  id: string
  name: string
  en: string
  unlock: string
}

export const characters: Character[] = [
  { id: 'isaac', name: '以撒', en: 'Isaac', unlock: '初始可用' },
  { id: 'magdalene', name: '抹大拉', en: 'Magdalene', unlock: '同时拥有 7 个或更多红心容器' },
  { id: 'cain', name: '该隐', en: 'Cain', unlock: '同时持有 55 枚硬币' },
  { id: 'judas', name: '犹大', en: 'Judas', unlock: '击败撒但' },
  { id: 'bluebaby', name: '???', en: '??? (Blue Baby)', unlock: '击败妈妈的心脏 10 次' },
  { id: 'eve', name: '夏娃', en: 'Eve', unlock: '连续 2 层不拾取任何心' },
  { id: 'samson', name: '参孙', en: 'Samson', unlock: '连续 2 层不受任何伤害' },
  { id: 'azazel', name: '阿撒泻勒', en: 'Azazel', unlock: '一局内完成 3 次恶魔交易' },
  { id: 'lazarus', name: '拉撒路', en: 'Lazarus', unlock: '同时拥有 4 个或更多魂心' },
  { id: 'eden', name: '伊甸', en: 'Eden', unlock: '通关第 4 章（子宫）' },
  {
    id: 'lost',
    name: '游魂',
    en: 'The Lost',
    unlock: '携带饰品「寻人启事」在献祭房死亡（寻人启事需先用以撒击败羔羊解锁）',
  },
  { id: 'lilith', name: '莉莉丝', en: 'Lilith', unlock: '用阿撒泻勒击败究极贪婪' },
  { id: 'keeper', name: '店主', en: 'Keeper', unlock: '向贪婪捐款机累计捐 1000 枚硬币' },
  { id: 'apollyon', name: '亚玻伦', en: 'Apollyon', unlock: '击败超级撒但' },
  {
    id: 'forgotten',
    name: '遗骸',
    en: 'The Forgotten',
    unlock: '拼出「妈妈的铲子」，在暗室坟墓房的土堆上使用',
  },
  {
    id: 'bethany',
    name: '伯大尼',
    en: 'Bethany',
    unlock: '用拉撒路在困难模式击败妈妈的心脏或它活着，全程不死',
  },
  { id: 'jacob', name: '雅各和以扫', en: 'Jacob & Esau', unlock: '用任意角色击败母亲' },
]

export const taintedUnlock = '在「家」用红钥匙、红钥匙碎片或该隐的魂石打开左侧墙上的衣柜'

export interface Mark {
  id: string
  name: string
  short: string
  en: string
}

// 角色完成标记（每个角色 12 个）
export const marks: Mark[] = [
  { id: 'heart', name: '妈妈的心脏', short: '心脏', en: "Mom's Heart / It Lives" },
  { id: 'isaac', name: '以撒', short: '以撒', en: 'Isaac' },
  { id: 'satan', name: '撒但', short: '撒但', en: 'Satan' },
  { id: 'bluebaby', name: '???', short: '???', en: '???' },
  { id: 'lamb', name: '羔羊', short: '羔羊', en: 'The Lamb' },
  { id: 'megasatan', name: '超级撒但', short: '超撒', en: 'Mega Satan' },
  { id: 'bossrush', name: 'Boss Rush', short: 'BR', en: 'Boss Rush' },
  { id: 'hush', name: '死寂', short: '死寂', en: 'Hush' },
  { id: 'greed', name: '究极贪婪', short: '贪婪', en: 'Ultra Greed' },
  { id: 'delirium', name: '精神错乱', short: '错乱', en: 'Delirium' },
  { id: 'mother', name: '母亲', short: '母亲', en: 'Mother' },
  { id: 'beast', name: '祸兽', short: '祸兽', en: 'The Beast' },
]
