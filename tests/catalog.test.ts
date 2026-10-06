import assert from 'node:assert/strict'
import { filterCatalog, type CatalogEntry } from '../docs/.vitepress/theme/data/catalog'
import source from '../docs/.vitepress/theme/data/catalog/items.json'

const entries = source as CatalogEntry[]
const ids = (query: string, group = '') => filterCatalog(entries, query, group).map(entry => entry.id)
assert.deepEqual(ids('118'), ['c118', 't118'])
assert.deepEqual(ids(' t39 '), ['t39'])
assert.deepEqual(ids('c118'), ['c118'])
assert.equal(ids('BRIMSTONE')[0], 'c118') // exact name ranks above Larynx / Brimstone Bombs
assert.deepEqual(ids('Cancer').slice(0, 2), ['c301', 't39'])
assert.deepEqual(ids('Cancer', '饰品').slice(0, 1), ['t39'])
assert(ids('飞行').includes('c20'))
assert.equal(ids('不存在的搜索词').length, 0)
assert.equal(ids('9999').length, 0) // golden-pill sentinel is not an engine effect ID
assert.deepEqual(ids('p9999'), ['p9999'])
assert.equal(filterCatalog(entries, '', '饰品').length, 188)
assert.equal(new Set(entries.map(entry => entry.id)).size, entries.length)
console.log('PASS catalog numeric IDs, duplicate names, type filters, effect search and golden-pill sentinel')
