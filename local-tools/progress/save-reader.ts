/** Read-only 09R decoder. Layout sources are pinned in README.md; no game-file writer. */
export interface SaveProgress {
  format: '09R'
  version: 'rep' | 'plus'
  achievements: number[]
  collectibles: number[]
  challenges: number[]
  counters: number[]
  filename: string
}

export const MAX_SAVE_BYTES = 8 * 1024 * 1024

/** Game CRC-32 uses the standard reflected polynomial with a custom initial value. */
export function saveChecksum(bytes: Uint8Array): number {
  let crc = ~0xfedcba76
  for (let i = 16; i < bytes.length - 4; i++) {
    crc ^= bytes[i]
    for (let bit = 0; bit < 8; bit++) crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0)
  }
  return (~crc) >>> 0
}

export function readSave(buffer: ArrayBuffer, filename = ''): SaveProgress {
  if (buffer.byteLength > MAX_SAVE_BYTES) throw new Error('文件超过 8 MB，不像受支持的永久进度存档。')
  if (buffer.byteLength < 28) throw new Error('文件太短，请选择 persistentgamedata 存档，不要选择日志或游戏配置。')
  const bytes = new Uint8Array(buffer)
  const view = new DataView(buffer)
  const header = new TextDecoder('ascii').decode(bytes.subarray(0, 16))
  if (header !== 'ISAACNGSAVE09R  ') throw new Error('不支持这个存档格式。目前只读取已核对的 ISAACNGSAVE09R 永久进度文件。')
  if (saveChecksum(bytes) !== view.getUint32(bytes.length - 4, true)) {
    throw new Error('存档校验失败。请退出游戏后重新选择最新文件；工具不会把损坏或正在写入的文件猜成进度。')
  }
  let offset = 20
  const blocks = new Map<number, { data: number[]; count: number }>()
  function requireBytes(size: number) {
    if (!Number.isSafeInteger(size) || size < 0 || offset + size > bytes.length - 8) {
      throw new Error('存档区段越界或被截断，未读取进度。')
    }
  }
  function int() { requireBytes(4); const value = view.getUint32(offset, true); offset += 4; return value }
  for (let section = 0; section < 11; section++) {
    const type = int(), size = int(), count = int()
    if (type < 1 || type > 11 || blocks.has(type)) throw new Error('区段类型未知或重复，存档结构不受支持。')
    if (type === 11) {
      // Bestiary's four subblocks store a word count; each packed record occupies eight bytes.
      if (count !== 4) throw new Error('图鉴区段结构不受支持。')
      const seen = new Set<number>()
      for (let sub = 0; sub < 4; sub++) {
        const tag = int(), words = int()
        if (tag < 1 || tag > 4 || seen.has(tag) || words % 4) throw new Error('图鉴子区段结构不受支持。')
        seen.add(tag)
        requireBytes(words * 2)
        offset += words * 2
      }
      blocks.set(type, { data: [], count })
      continue
    }
    const length = [1, 2, 9].includes(type) ? size : count * ([3, 8].includes(type) ? 4 : 1)
    requireBytes(length)
    if ((type === 2 && (size % 4 || count !== size / 4)) || (type === 1 && count > size)) {
      throw new Error('计数器或成就区段长度不匹配。')
    }
    const data = type === 2 ? Array.from({ length: size / 4 }, (_, index) => view.getUint32(offset + index * 4, true))
      : [1, 4, 7].includes(type) ? Array.from(bytes.subarray(offset, offset + (type === 1 ? count : length))) : []
    blocks.set(type, { data, count })
    offset += length
  }
  if (offset !== bytes.length - 8) throw new Error('存在未识别的尾部或区段，当前工具不支持这个变体。')
  const achievements = blocks.get(1)!.data
  const collectibles = blocks.get(4)!.data
  const challenges = blocks.get(7)!.data
  const counters = blocks.get(2)!.data
  if (achievements.length < 638 || collectibles.length < 733 || challenges.length < 46 || counters.length < 496) {
    throw new Error('区段长度不足，不能按忏悔 / 忏悔+解释该存档。')
  }
  if (achievements.some(value => value > 1) || challenges.some(value => value > 1)) {
    throw new Error('解锁标志不是已核对的布尔格式，未读取进度。')
  }
  return { format: '09R', version: achievements.length > 638 || filename.includes('+') ? 'plus' : 'rep',
    achievements, collectibles, challenges, counters, filename }
}

/** Unknown / absent fields stay unknown, instead of being silently counted as missing. */
export function flag(values: number[], id: number): boolean | null {
  if (!Number.isInteger(id) || id < 0 || id >= values.length) return null
  return values[id] > 0
}

export function itemState(save: SaveProgress, item: { kind: string; id: number; unlocks: number[]; collection: boolean; hidden?: boolean }): string {
  if (item.hidden) return 'special'
  const requirements = item.unlocks.map(id => flag(save.achievements, id))
  if (requirements.includes(null)) return 'unknown'
  if (requirements.includes(false)) return 'locked'
  if (item.kind !== 'c' || !item.collection) return 'unlocked'
  const collected = flag(save.collectibles, item.id)
  return collected === null ? 'unknown' : collected ? 'collected' : 'uncollected'
}
