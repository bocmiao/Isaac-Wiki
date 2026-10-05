import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import './style.css'

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
  enhanceApp({ app }) {
    app.component('HomeLanding', HomeLanding)
    app.component('UnlockTracker', UnlockTracker)
    app.component('VersionBadge', VersionBadge)
    app.component('FloorTrack', FloorTrack)
    app.component('StrategyGrid', StrategyGrid)
    app.component('StreakTitle', StreakTitle)
    app.component('GameIcon', GameIcon)
    app.component('KeyCap', KeyCap)
  },
} satisfies Theme
