/** Legacy numeric arrays and current v1 exports; reject the whole malformed payload. */
export function parseAchievementIds(value: unknown): number[] | null {
  const list = Array.isArray(value) ? value : value && typeof value === 'object' &&
    (value as { v?: unknown }).v === 1 ? (value as { done?: unknown }).done : null
  if (!Array.isArray(list) || !list.every(id => Number.isInteger(id) && id >= 1 && id <= 641)) return null
  return [...new Set<number>(list)].sort((a, b) => a - b)
}
