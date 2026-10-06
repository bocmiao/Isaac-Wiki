import { defineConfig } from 'vitepress'
import { itemLinks } from './item-links'
import { tableLabels } from './table-labels'
import characterEntries from './theme/data/catalog/characters.json'
import roomEntries from './theme/data/catalog/rooms.json'
import floorEntries from './theme/data/catalog/floors.json'

const catalogLinks = [
  { text: '人物图鉴', link: '/characters/' },
  { text: '房间图鉴', link: '/rooms/' },
  { text: '楼层图鉴', link: '/floors/' },
  { text: '道具图鉴', link: '/items/' },
]
function entrySidebar(label: string, path: string, entries: { group: string; name: string; link: string }[]) {
  return [
    { text: label, link: path },
    ...[...new Set(entries.map(entry => entry.group))].map(group => ({
      text: group,
      collapsed: true,
      items: entries.filter(entry => entry.group === group).map(entry => ({ text: entry.name, link: entry.link })),
    })),
    { text: '其他图鉴', items: catalogLinks.filter(entry => entry.link !== path) },
  ]
}

// 新手路线只放自己的文章；第 4、5 层的正文在攻略库，这里只留总览页，避免点进去侧栏整个跳走
const guideSidebar = [
  { text: '新手路线总览', link: '/guide/' },
  {
    text: '第 1 层 · 开局准备',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/start/' },
      { text: '基础操作', link: '/guide/start/controls' },
      { text: '版本与 DLC 怎么买', link: '/guide/start/versions' },
      { text: '中文设置与常见问题', link: '/guide/start/chinese' },
    ],
  },
  {
    text: '第 2 层 · 第一次通关',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/first-win/' },
      { text: '新手前 10 局', link: '/guide/first-win/first-runs' },
      { text: '房间类型入门', link: '/guide/first-win/rooms' },
      { text: '心、钱、炸弹、钥匙', link: '/guide/first-win/pickups' },
      { text: '第一次打妈妈', link: '/guide/first-win/mom' },
    ],
  },
  {
    text: '第 3 层 · 解锁主线',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/unlocks/' },
      { text: '角色解锁步骤', link: '/guide/unlocks/order' },
      { text: '结局与路线', link: '/guide/unlocks/endings' },
    ],
  },
  {
    text: '第 4–5 层 · 进阶与白金神',
    collapsed: false,
    items: [
      { text: '第 4 层 · 进阶思路', link: '/guide/advanced/' },
      { text: '第 5 层 · 里角色与白金神', link: '/guide/platinum/' },
    ],
  },
]

// 攻略库按四类分组，和攻略库首页一致
const strategySidebar = [
  { text: '攻略库首页 · 按问题找', link: '/strategy/' },
  {
    text: '规则与选择',
    items: [
      { text: '房间图鉴', link: '/rooms/' },
      { text: '楼层图鉴', link: '/floors/' },
      { text: '道具图鉴', link: '/items/' },
      { text: '机制详解', link: '/strategy/mechanics' },
      { text: '道具取舍与流派', link: '/strategy/items' },
    ],
  },
  {
    text: '角色',
    items: [
      { text: '人物图鉴', link: '/characters/' },
      { text: '角色速查与开局强化', link: '/strategy/character-roster' },
      { text: '表角色攻略', link: '/strategy/characters' },
      { text: '里角色攻略', link: '/strategy/tainted' },
    ],
  },
  {
    text: 'Boss 与结局',
    items: [
      { text: 'Boss（一）：主线终局', link: '/strategy/bosses' },
      { text: 'Boss（二）：死寂到祸兽', link: '/strategy/bosses-2' },
      { text: '结局与路线 ↗', link: '/guide/unlocks/endings' },
    ],
  },
  {
    text: '特殊模式',
    items: [
      { text: '挑战模式', link: '/strategy/challenges' },
      { text: '贪婪模式', link: '/strategy/greed' },
      { text: '种子', link: '/strategy/seeds' },
    ],
  },
  {
    text: '查询',
    items: [
      { text: '中英译名对照', link: '/strategy/glossary' },
      { text: '全成就索引 ↗', link: '/achievements/' },
    ],
  },
]

const achievementSidebar = [
  {
    text: '全成就',
    items: [
      { text: '搜索全部 641 项', link: '/achievements/' },
      { text: '推荐推进顺序', link: '/achievements/#roadmap' },
      { text: '特殊成就教程', link: '/achievements/special' },
    ],
  },
  {
    text: '按编号查看',
    collapsed: true,
    items: [1, 101, 201, 301, 401, 501, 601].map((start) => {
      const end = Math.min(start + 99, 641)
      return { text: `#${start}–${end}`, link: `/achievements/ids-${String(start).padStart(3, '0')}-${end}` }
    }),
  },
  {
    text: '配套',
    items: [
      { text: '角色解锁清单', link: '/tools/tracker' },
      { text: '道具速查', link: '/tools/items' },
      { text: '角色标记与奖励', link: '/strategy/character-roster#marks' },
    ],
  },
]

const topicsSidebar = [
  {
    text: '平台与联机',
    items: [
      { text: '联机专题', link: '/topics/coop' },
      { text: '主机专题', link: '/topics/console' },
    ],
  },
  {
    text: '模组与控制台',
    items: [
      { text: '配置与实用模组', link: '/topics/mods' },
      { text: '调试控制台：开启与关闭', link: '/topics/debug-console' },
      { text: '控制台练习用法', link: '/topics/debug-console-practice' },
      { text: '控制台常用指令', link: '/topics/debug-console-commands' },
    ],
  },
]

// GitHub Pages 部署在 /Isaac-Wiki/ 子路径下，由 CI 通过 BASE 环境变量传入；本地开发默认根路径
const base = process.env.BASE ?? '/'

export default defineConfig({
  base,
  lang: 'zh-CN',
  title: '以撒路书',
  description: '从第一局到白金神的中文以撒学习路线，对齐忏悔 / 忏悔+ 版本',
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: `${base}favicon.svg` }],
    ['meta', { name: 'theme-color', content: '#b3261e' }],
  ],
  markdown: {
    config: (md) => {
      md.use(itemLinks, { base })
      md.use(tableLabels)
    },
    container: {
      tipLabel: '提示',
      warningLabel: '注意',
      dangerLabel: '危险',
      infoLabel: '说明',
      detailsLabel: '详情',
    },
  },
  themeConfig: {
    logo: '/favicon.svg',
    nav: [
      { text: '新手路线', link: '/guide/', activeMatch: '^/guide/' },
      { text: '攻略库', link: '/strategy/', activeMatch: '^/strategy/' },
      { text: '图鉴', activeMatch: '^/(characters|rooms|floors|items)/', items: catalogLinks },
      { text: '全成就', link: '/achievements/', activeMatch: '^/achievements/' },
      {
        text: '专题',
        activeMatch: '^/topics/',
        items: [
          { text: '联机专题', link: '/topics/coop' },
          { text: '主机专题', link: '/topics/console' },
          { text: '配置与实用模组', link: '/topics/mods' },
          { text: '调试控制台', link: '/topics/debug-console' },
        ],
      },
      {
        text: '工具',
        activeMatch: '^/tools/',
        items: [
          { text: '工具总览', link: '/tools/' },
          { text: '角色解锁清单', link: '/tools/tracker' },
          { text: '全成就打勾', link: '/achievements/#catalog' },
          { text: '道具速查', link: '/tools/items' },
          { text: '恶魔 / 天使房概率', link: '/tools/deal-chance' },
          { text: '献祭房奖励查询', link: '/tools/sacrifice' },
          { text: '挑战进度清单', link: '/tools/challenges' },
          { text: '捐款机进度', link: '/tools/donations' },
          { text: '控制台命令生成器', link: '/tools/console-generator' },
          { text: '道具组合查询', link: '/tools/synergies' },
          { text: '主线路线规划', link: '/tools/routes' },
        ],
      },
      { text: '关于', link: '/about' },
    ],
    sidebar: {
      '/guide/': guideSidebar,
      '/strategy/': strategySidebar,
      '/characters/': entrySidebar('人物图鉴', '/characters/', characterEntries),
      '/rooms/': entrySidebar('房间图鉴', '/rooms/', roomEntries),
      '/floors/': entrySidebar('楼层图鉴', '/floors/', floorEntries),
      '/items/': [
        { text: '道具图鉴 · 搜索全部条目', link: '/items/' },
        { text: '取舍与工具', items: [
          { text: '道具取舍与流派', link: '/strategy/items' },
          { text: '道具组合查询', link: '/tools/synergies' },
          { text: '控制台命令生成器', link: '/tools/console-generator' },
          { text: '全成就与解锁', link: '/achievements/' },
        ] },
        { text: '其他图鉴', items: catalogLinks.filter(entry => entry.link !== '/items/') },
      ],
      '/achievements/': achievementSidebar,
      '/topics/': topicsSidebar,
      '/tools/': [
        {
          text: '工具',
          items: [
            { text: '工具总览', link: '/tools/' },
            { text: '角色解锁清单', link: '/tools/tracker' },
            { text: '全成就打勾', link: '/achievements/#catalog' },
            { text: '道具速查', link: '/tools/items' },
            { text: '恶魔 / 天使房概率', link: '/tools/deal-chance' },
            { text: '献祭房奖励查询', link: '/tools/sacrifice' },
            { text: '挑战进度清单', link: '/tools/challenges' },
            { text: '捐款机进度', link: '/tools/donations' },
            { text: '控制台命令生成器', link: '/tools/console-generator' },
            { text: '道具组合查询', link: '/tools/synergies' },
            { text: '主线路线规划', link: '/tools/routes' },
          ],
        },
      ],
    },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新', formatOptions: { dateStyle: 'medium' } },
    darkModeSwitchLabel: '场景',
    lightModeSwitchTitle: '切换到地下室（浅色）',
    darkModeSwitchTitle: '切换到妈腿层（深色）',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部',
    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索教程', buttonAriaLabel: '搜索教程' },
          modal: {
            noResultsText: '没有找到相关内容',
            resetButtonTitle: '清除',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
    footer: {
      message: '非官方粉丝站。《以撒的结合》相关素材版权归 Edmund McMillen 与 Nicalis 所有。',
      copyright: '内容以 CC BY-NC-SA 4.0 发布；另有授权注明的成就系列除外',
    },
  },
})
