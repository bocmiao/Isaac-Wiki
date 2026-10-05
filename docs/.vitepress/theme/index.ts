import DefaultTheme from 'vitepress/theme'
import type { Theme } from 'vitepress'
import './style.css'

import HomeLanding from './components/HomeLanding.vue'
import UnlockTracker from './components/UnlockTracker.vue'
import VersionBadge from './components/VersionBadge.vue'
import StageHeader from './components/StageHeader.vue'
import KeyCap from './components/KeyCap.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('HomeLanding', HomeLanding)
    app.component('UnlockTracker', UnlockTracker)
    app.component('VersionBadge', VersionBadge)
    app.component('StageHeader', StageHeader)
    app.component('KeyCap', KeyCap)
  },
} satisfies Theme
