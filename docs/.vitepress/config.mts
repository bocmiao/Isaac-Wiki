import { defineConfig } from 'vitepress'

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
    items: [{ text: '阶段总览', link: '/guide/first-win/' }],
  },
  {
    text: '第 3 层 · 深处：解锁主线',
    collapsed: true,
    items: [{ text: '阶段总览', link: '/guide/unlocks/' }],
  },
  {
    text: '第 4 层 · 子宫：进阶思路',
    collapsed: true,
    items: [{ text: '阶段总览', link: '/guide/advanced/' }],
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
  description: '从第一局到白金神的中文以撒学习路线，对齐 Repentance+ 版本',
  cleanUrls: true,
  lastUpdated: true,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { name: 'theme-color', content: '#b3261e' }],
  ],
  themeConfig: {
    logo: '/favicon.svg',
    nav: [
      { text: '学习路线', link: '/guide/', activeMatch: '/guide/' },
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
    lastUpdated: { text: '最后更新' },
    darkModeSwitchLabel: '深色模式',
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
