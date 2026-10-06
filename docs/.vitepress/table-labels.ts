import type MarkdownIt from 'markdown-it'

// 在静态 HTML 中就生成手机表格标记，避免浏览器首次定位锚点后才改变表格高度。
// 主题里的客户端处理仍为组件动态生成的表格提供标签。
export function tableLabels(md: MarkdownIt) {
  // VitePress 的默认 table_open 固定输出标签，会丢掉 token 上的 class。
  // 保留它的键盘聚焦支持，同时输出构建时生成的属性。
  md.renderer.rules.table_open = (tokens, index, options, _env, renderer) => {
    tokens[index].attrSet('tabindex', '0')
    return renderer.renderToken(tokens, index, options)
  }
  md.core.ruler.after('inline', 'table-labels', (state) => {
    const tokens = state.tokens
    for (let start = 0; start < tokens.length; start++) {
      if (tokens[start].type !== 'table_open') continue
      let end = start + 1
      while (end < tokens.length && tokens[end].type !== 'table_close') end++
      const heads: string[] = []
      for (let i = start + 1; i < end; i++) {
        if (tokens[i].type !== 'th_open') continue
        const inline = tokens[i + 1]
        heads.push((inline.children ?? [])
          .filter((token) => ['text', 'code_inline', 'image'].includes(token.type))
          .map((token) => token.content).join('').trim())
      }
      if (heads.length >= 3) {
        tokens[start].attrJoin('class', 'stack')
        let column = 0
        for (let i = start + 1; i < end; i++) {
          if (tokens[i].type === 'tr_open') column = 0
          if (tokens[i].type === 'td_open') tokens[i].attrSet('data-label', heads[column++] ?? '')
        }
      }
      start = end
    }
  })
}
