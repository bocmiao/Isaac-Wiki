import { defineAsyncComponent, h, nextTick, onMounted, watch } from 'vue'
import DefaultTheme from 'vitepress/theme'
import { useRoute, type Theme } from 'vitepress'
import '@fontsource/zcool-kuaile/index.css'
import './style.css'

import SketchDefs from './components/SketchDefs.vue'
import HomeLanding from './components/HomeLanding.vue'
import UnlockTracker from './components/UnlockTracker.vue'
import VersionBadge from './components/VersionBadge.vue'
import FloorTrack from './components/FloorTrack.vue'
import StrategyGrid from './components/StrategyGrid.vue'
import StreakTitle from './components/StreakTitle.vue'
import GameIcon from './components/GameIcon.vue'
import KeyCap from './components/KeyCap.vue'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, { 'layout-top': () => h(SketchDefs) }),
  // 手机上三列以上的表格改成一行一张卡片：给每个单元格记下所属表头，CSS 用它当小标签
  setup() {
    const route = useRoute()
    const label = () =>
      nextTick(() => {
        document.querySelectorAll<HTMLTableElement>('.vp-doc table').forEach((table) => {
          const heads = [...table.querySelectorAll('thead th')].map((th) => th.textContent?.trim() ?? '')
          if (heads.length < 3) return
          table.classList.add('stack')
          table.querySelectorAll('tbody tr').forEach((tr) => {
            ;[...tr.children].forEach((td, i) => td.setAttribute('data-label', heads[i] ?? ''))
          })
        })
      })
    onMounted(label)
    watch(() => route.path, label)
  },
  enhanceApp({ app }) {
    app.component('HomeLanding', HomeLanding)
    app.component('UnlockTracker', UnlockTracker)
    app.component('AchievementCatalog', defineAsyncComponent(() => import('./components/AchievementCatalog.vue')))
    app.component('ItemFinder', defineAsyncComponent(() => import('./components/ItemFinder.vue')))
    for (const [name,loader] of Object.entries({
      DealCalculator: () => import('./components/DealCalculator.vue'),
      SacrificeLookup: () => import('./components/SacrificeLookup.vue'),
      ChallengeChecklist: () => import('./components/ChallengeChecklist.vue'),
      DonationTracker: () => import('./components/DonationTracker.vue'),
      SynergyFinder: () => import('./components/SynergyFinder.vue'),
      RoutePlanner: () => import('./components/RoutePlanner.vue'),
      ConsoleGenerator: () => import('./components/ConsoleGenerator.vue'),
    })) app.component(name, defineAsyncComponent(loader))
    app.component('VersionBadge', VersionBadge)
    app.component('FloorTrack', FloorTrack)
    app.component('StrategyGrid', StrategyGrid)
    app.component('StreakTitle', StreakTitle)
    app.component('GameIcon', GameIcon)
    app.component('KeyCap', KeyCap)
  },
} satisfies Theme
