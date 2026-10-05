import type MarkdownIt from 'markdown-it'
import items from './theme/data/item-links.json'

// 文章里写成「中文（English）」的道具、饰品、卡牌、胶囊，自动链到 wiki.gg 中文站，并附 IsaacGuru 小链接。
// 只认英文名在 EID 名称表里的写法，避免把楼层、Boss 之类同名词误当成道具。每页每个道具只链第一次出现。
// 数据由 scripts/gen-item-links.py 生成。

type Entry = [zh: string, kind: 'c' | 't' | 'k' | 'p', id: number, en: string]
const table = items as Record<string, Entry>

const PAIR = /([一-鿿·0-9A-Za-z\-？?！!.…]{0,16})（([A-Za-z0-9][A-Za-z0-9 .,'’!?&+\-]*?)）/g

function lookup(en: string): Entry | undefined {
  const k = en.trim().toLowerCase().replace(/’/g, "'")
  return table[k] ?? table['the ' + k] ?? table[k.replace(/^the /, '')]
}

const esc = (s: string) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;')
const wikiUrl = (zh: string) => `https://bindingofisaacrebirth.wiki.gg/zh/index.php?search=${encodeURIComponent(zh)}&go=Go`
const guruUrl = ([, kind, id]: Entry) => `https://isaacguru.com/wiki/isaac/${kind}${id}`

function link(text: string, e: Entry) {
  return (
    `<a class="item-ref" href="${wikiUrl(e[0])}" target="_blank" rel="noreferrer" title="在 wiki.gg 中文站查看${esc(e[0])}">${esc(text)}</a>` +
    `<a class="item-guru" href="${guruUrl(e)}" target="_blank" rel="noreferrer" title="在 IsaacGuru 查看（英文）" aria-label="${esc(e[0])}：IsaacGuru">IG</a>`
  )
}

export function itemLinks(md: MarkdownIt) {
  md.core.ruler.push('item_links', (state) => {
    const seen = new Set<number | string>()
    const tokens = state.tokens
    for (let i = 0; i < tokens.length; i++) {
      const block = tokens[i]
      if (block.type !== 'inline' || !block.children) continue
      if (tokens[i - 1]?.type === 'heading_open') continue
      const children = block.children
      let inLink = 0
      for (let j = 0; j < children.length; j++) {
        const t = children[j]
        if (t.type === 'link_open') inLink++
        else if (t.type === 'link_close') inLink--
        if (t.type !== 'text' || inLink > 0 || !t.content.includes('（')) continue

        let html = ''
        let last = 0
        let changed = false
        for (const m of t.content.matchAll(PAIR)) {
          const e = lookup(m[2])
          if (!e) continue
          const key = `${e[1]}${e[2]}`
          if (seen.has(key)) continue
          const before = m[1]
          const start = m.index!
          // 中文名在括号前：只链中文名本身（前面可能连着别的字）
          if (before.endsWith(e[0])) {
            const pre = before.slice(0, before.length - e[0].length)
            html += esc(t.content.slice(last, start)) + esc(pre) + link(e[0], e) + esc(`（${m[2]}）`)
          } else if (before === '') {
            // 中文名在前一个 token 里（例如加粗了），链英文名
            html += esc(t.content.slice(last, start)) + '（' + link(m[2], e) + '）'
          } else continue
          last = start + m[0].length
          seen.add(key)
          changed = true
        }
        if (!changed) continue
        html += esc(t.content.slice(last))
        t.type = 'html_inline'
        t.content = html
      }
    }
  })
}
