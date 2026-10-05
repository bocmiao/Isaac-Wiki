import { defineConfig } from 'vitepress'
import { strategyCategories } from './theme/data/strategy'

// 学习路线的五个阶段，侧栏和首页共用同一套命名
const guideSidebar = [
  {
    text: '第 1 层 · 地下室：开局准备',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/start/' },
      { text: '基础操作', link: '/guide/start/controls' },
      { text: '版本与 DLC 怎么买', link: '/guide/start/versions' },
      { text: '中文设置与常见问题', link: '/guide/start/chinese' },
    ],
  },
  {
    text: '第 2 层 · 洞穴：第一次通关',
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
    text: '第 3 层 · 深处：解锁主线',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/unlocks/' },
      { text: '角色解锁顺序', link: '/guide/unlocks/order' },
      { text: '结局一览与前置条件', link: '/guide/unlocks/endings' },
    ],
  },
  {
    text: '第 4 层 · 子宫：进阶思路',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/advanced/' },
      { text: '机制详解', link: '/strategy/mechanics' },
      { text: '道具取舍与流派', link: '/strategy/items' },
      { text: '角色速查与练习路线', link: '/strategy/character-roster' },
      { text: '表角色攻略', link: '/strategy/characters' },
      { text: 'Boss 打法（一）', link: '/strategy/bosses' },
      { text: 'Boss 打法（二）', link: '/strategy/bosses-2' },
    ],
  },
  {
    text: '第 5 层 · 暗室：里角色与白金神',
    collapsed: false,
    items: [
      { text: '阶段总览', link: '/guide/platinum/' },
      { text: '全部成就与详细解锁', link: '/guide/achievements/' },
      { text: '特殊成就详细教程', link: '/guide/achievements/special' },
      { text: '里角色攻略', link: '/strategy/tainted' },
      { text: '挑战模式', link: '/strategy/challenges' },
      { text: '贪婪模式', link: '/strategy/greed' },
      { text: '种子', link: '/strategy/seeds' },
    ],
  },
]

guideSidebar.push({
  text: '全成就 · 编号教程',
  collapsed: true,
  items: [
    { text: '搜索全部 641 项', link: '/guide/achievements/' },
    { text: '特殊成就与查漏', link: '/guide/achievements/special' },
    ...[1, 101, 201, 301, 401, 501, 601].map((start) => {
      const end = Math.min(start + 99, 641)
      return { text: `#${start}–${end} 详细解锁`, link: `/guide/achievements/ids-${String(start).padStart(3, '0')}-${end}` }
    }),
  ],
})

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
      { text: '新手路线', link: '/guide/', activeMatch: '/guide/' },
      { text: '攻略库', link: '/strategy/', activeMatch: '/strategy/' },
      {
        text: '专题',
        items: [
          { text: '联机专题', link: '/topics/coop' },
          { text: '主机专题', link: '/topics/console' },
          { text: '配置与实用模组', link: '/topics/mods' },
          { text: '调试控制台：开启与关闭', link: '/topics/debug-console' },
        ],
      },
      { text: '全成就', link: '/guide/achievements/', activeMatch: '/guide/achievements/' },
      { text: '工具', link: '/tools/', activeMatch: '/tools/' },
      { text: '关于', link: '/about' },
    ],
    sidebar: {
      '/guide/': guideSidebar,
      '/tools/': [{ text: '实用工具', items: [
        { text: '工具首页', link: '/tools/' },
        { text: '角色解锁清单', link: '/tools/tracker' },
        { text: '恶魔 / 天使房概率', link: '/tools/deal-chance' },
        { text: '献祭房奖励查询', link: '/tools/sacrifice' },
        { text: '挑战进度清单', link: '/tools/challenges' },
        { text: '捐款机进度', link: '/tools/donations' },
        { text: '道具组合查询', link: '/tools/synergies' },
        { text: '主线路线规划', link: '/tools/routes' },
        { text: '控制台命令生成器', link: '/tools/console-generator' },
      ] }],
      '/strategy/': [
        {
          text: '攻略库',
          items: [
            { text: '全部攻略', link: '/strategy/' },
            { text: '全部成就与详细解锁', link: '/guide/achievements/' },
            { text: '角色速查与练习路线', link: '/strategy/character-roster' },
            ...strategyCategories.flatMap((c) =>
              c.id === 'bosses'
                ? [
                    { text: 'Boss 打法（一）：主线终局', link: '/strategy/bosses' },
                    { text: 'Boss 打法（二）：死寂到祸兽', link: '/strategy/bosses-2' },
                  ]
                : [{ text: c.name, link: `/strategy/${c.id}` }],
            ),
            { text: '中英译名对照', link: '/strategy/glossary' },
          ],
        },
      ],
      '/topics/': [
        {
          text: '专题',
          items: [
            { text: '联机专题', link: '/topics/coop' },
            { text: '主机专题', link: '/topics/console' },
            { text: '配置与实用模组', link: '/topics/mods' },
            { text: '调试控制台：开启与关闭', link: '/topics/debug-console' },
            { text: '调试控制台：命令大全', link: '/topics/debug-console-commands' },
            { text: '调试控制台：练习与排错', link: '/topics/debug-console-practice' },
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
