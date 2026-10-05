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
      { text: '表角色攻略', link: '/strategy/characters' },
      { text: 'Boss 打法（一）', link: '/strategy/bosses' },
      { text: 'Boss 打法（二）', link: '/strategy/bosses-2' },
    ],
  },
  {
    text: '第 5 层 · 暗室：里角色与白金神',
    collapsed: true,
    items: [{ text: '阶段总览', link: '/guide/platinum/' }],
  },
]

export default defineConfig({
  lang: 'zh-CN',
  title: '以撒路书',
  description: '从第一局到白金神的中文以撒学习路线，对齐忏悔 / 忏悔+ 版本',
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
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
          { text: '配置与模组', link: '/topics/mods' },
        ],
      },
      { text: '解锁清单', link: '/tools/tracker' },
      { text: '关于', link: '/about' },
    ],
    sidebar: {
      '/guide/': guideSidebar,
      '/strategy/': [
        {
          text: '攻略库',
          items: [
            { text: '全部攻略', link: '/strategy/' },
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
            { text: '配置与模组', link: '/topics/mods' },
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
      copyright: '内容以 CC BY-NC-SA 4.0 发布',
    },
  },
})
