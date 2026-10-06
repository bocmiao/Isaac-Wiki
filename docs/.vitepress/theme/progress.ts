import { characters, marks } from './data/characters'

// 解锁清单的进度只存在访客自己的浏览器里。首页 HUD 和清单页共用这里的读写与计算。
export const STORAGE_KEY = 'isaac-roadbook-progress-v1'

export type MarkState = 0 | 1 | 2 // 0 未完成 · 1 普通 · 2 困难
export interface Progress {
  v: 1
  chars: Record<string, boolean>
  tainted: Record<string, boolean>
  marks: Record<string, MarkState>
}

export const emptyProgress = (): Progress => ({ v: 1, chars: { isaac: true }, tainted: {}, marks: {} })

const characterIds = new Set(characters.map((c) => c.id))
const markKeys = new Set(characters.flatMap((c) =>
  [c.id, `${c.id}-t`].flatMap((id) => marks.map((m) => `${id}:${m.id}`)),
))

const isRecord = (value: unknown): value is Record<string, unknown> =>
  value !== null && typeof value === 'object' && !Array.isArray(value)

// Keep valid v1 exports compatible; reject unknown IDs before replacing any progress.
export function parseProgress(value: unknown): Progress | null {
  if (!isRecord(value) || value.v !== 1) return null
  if (!isRecord(value.chars) || !isRecord(value.tainted) || !isRecord(value.marks)) return null
  const result = emptyProgress()
  for (const field of ['chars', 'tainted'] as const) {
    for (const [id, unlocked] of Object.entries(value[field])) {
      if (!characterIds.has(id)) return null
      if (typeof unlocked !== 'boolean') return null
      result[field][id] = unlocked
    }
  }
  result.chars.isaac = true
  for (const [key, state] of Object.entries(value.marks)) {
    if (!markKeys.has(key)) return null
    if (state !== 0 && state !== 1 && state !== 2) return null
    if (state !== 0) result.marks[key] = state
  }
  return result
}

export function loadProgress(): Progress | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return parseProgress(JSON.parse(raw))
  } catch {
    return null
  }
}

export function saveProgress(p: Progress): boolean {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(p))
    return true
  } catch {
    return false
  }
}

/** Merging an older snapshot never downgrades a hard mark or erases an unlock. */
export function mergeProgress(current:Progress,next:Progress):Progress {
  const result=emptyProgress()
  for(const field of ['chars','tainted'] as const)for(const id of characterIds)result[field][id]=!!(current[field][id]||next[field][id])
  for(const key of markKeys){const state=Math.max(current.marks[key]??0,next.marks[key]??0) as MarkState;if(state)result.marks[key]=state}
  return result
}

export const totalMarks = characters.length * 2 * marks.length

export function summarize(p: Progress) {
  const unlocked = characters.filter((c) => p.chars[c.id]).length
  const tainted = characters.filter((c) => p.tainted[c.id]).length
  const marksDone = Object.entries(p.marks).filter(([key, v]) => markKeys.has(key) && (v === 1 || v === 2)).length
  const overall = (unlocked + tainted + marksDone) / (characters.length * 2 + totalMarks)
  return { unlocked, tainted, marksDone, overall }
}
