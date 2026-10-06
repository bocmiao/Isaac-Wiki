import { buildSync } from 'esbuild'
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
const root = fileURLToPath(new URL('../', import.meta.url))
const result = buildSync({ entryPoints: [root + 'local-tools/progress/main.ts'], bundle: true, write: false,
  format: 'iife', target: 'es2020', charset: 'utf8', minify: true, legalComments: 'inline' })
const template = readFileSync(root + 'local-tools/progress/template.html', 'utf8')
const script = result.outputFiles[0].text.replace(/<\/script/gi, '<\\/script')
mkdirSync(root + 'docs/public/downloads', { recursive: true })
writeFileSync(root + 'docs/public/downloads/isaac-progress.html', template.replace('/* INLINE_APP */', () => script))
console.log('Built offline local-progress HTML; no CDN, server or runtime installation required.')
