import type { Plugin } from 'vite'

// VitePress 1.6.4 leaves a debounced scroll callback queued when a detail-page
// outline unmounts. Returning to an aside:false catalog can then dereference
// the old component's null DOM refs. Guard both refs without editing dependencies.
export function outlineGuard(): Plugin {
  return {
    name: 'isaac-outline-lifecycle-guard',
    enforce: 'pre',
    transform(code, id) {
      const path = id.split('?')[0].replace(/\\/g, '/')
      if (!path.endsWith('/vitepress/dist/client/theme-default/composables/outline.js')) return
      const signature = 'function activateLink(hash) {'
      if (!code.includes(signature) || code.indexOf(signature) !== code.lastIndexOf(signature)) {
        throw new Error('VitePress outline implementation changed; review the outline lifecycle guard.')
      }
      return {
        code: code.replace(signature, signature + '\n        if (!container.value || !marker.value) return;'),
        map: null,
      }
    },
  }
}
