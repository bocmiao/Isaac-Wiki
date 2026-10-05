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

export function loadProgress(): Progress | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const data = JSON.parse(raw)
    return data?.v === 1 ? data : null
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

export const totalMarks = characters.length * 2 * marks.length

export function summarize(p: Progress) {
  const unlocked = characters.filter((c) => p.chars[c.id]).length
  const tainted = characters.filter((c) => p.tainted[c.id]).length
  const marksDone = Object.values(p.marks).filter((v) => v > 0).length
  const overall = (unlocked + tainted + marksDone) / (characters.length * 2 + totalMarks)
  return { unlocked, tainted, marksDone, overall }
}
