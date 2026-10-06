import type { IconName } from '../components/GameIcon.vue'

export interface CatalogEntry {
  id: string
  name: string
  en: string
  group: string
  summary: string
  icon: IconName
  link: string
  aliases: string[]
  gameId?: number
  search?: string
}

/** Numeric queries select IDs; kind-prefixed IDs distinguish a collectible from a same-ID trinket. */
export function filterCatalog(entries: CatalogEntry[], query: string, group = ''): CatalogEntry[] {
  const normalize = (value: string) => value.normalize('NFKC').toLowerCase().replace(/\s+/g, ' ').trim()
  const q = normalize(query)
  const candidates = entries.filter(entry => !group || entry.group === group)
  if (!q) return candidates
  const numeric = /^\d+$/.test(q) ? Number(q) : null
  return candidates.map(entry => {
    const name = normalize(entry.name)
    const en = normalize(entry.en)
    const id = normalize(entry.id)
    const content = normalize(entry.search ?? entry.summary)
    const aliases = entry.aliases.map(normalize)
    const score = numeric !== null ? (entry.gameId === numeric ? 0 : -1)
      : id === q ? 0
      : name === q || en === q ? 1
      : name.startsWith(q) || en.startsWith(q) ? 2
      : name.includes(q) || en.includes(q) || id.includes(q) || aliases.some(alias => alias.includes(q)) ? 3
      : content.includes(q) ? 4 : -1
    return { entry, score }
  }).filter(result => result.score >= 0)
    .sort((a, b) => a.score - b.score)
    .map(result => result.entry)
}
