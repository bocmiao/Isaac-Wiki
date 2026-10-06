import rewards from '../../docs/.vitepress/theme/data/completion-rewards.json'
import { flag, type SaveProgress } from './save-reader'

type Character = { id: string; marks: { id: string; name: string; counter: number }[] }

export function rewardsForMark(characterId: string, markId: string) {
  return rewards.find(row => row.id === characterId)?.rewards.filter(reward => reward.marks.includes(markId)) ?? []
}

export function completionRewardDetail(save: SaveProgress, character: Character, markId: string) {
  const matched = rewardsForMark(character.id, markId)
  if (!matched.length) return '这一格没有独立的里角色奖励，但仍属于全套困难 / 极贪标记条件；不从合并奖励成就倒推本格。'
  return matched.map(reward => {
    const unlocked = flag(save.achievements, reward.id)
    const names = reward.items.map(item => item.name).join('、') || reward.name
    const remaining = reward.marks.flatMap(id => {
      const mark = character.marks.find(row => row.id === id)
      const value = mark ? save.counters[mark.counter] : undefined
      if (value === 1 || value === 2) {
        if (value >= reward.minimum) return []
        return [`${mark?.name ?? id}（仅${id === 'greed' ? '普通贪婪' : '普通'}，需${id === 'greed' ? '极贪' : '困难'}）`]
      }
      return [`${mark?.name ?? id}（${value === 0 ? '未完成' : '记录不足 / 无法判断'}）`]
    })
    return `${reward.label}：${names}（成就 #${reward.id}）\n奖励解锁状态：${unlocked === null ? '记录不足 / 无法判断' : unlocked ? '已解锁' : '未解锁'}\n条件：${reward.conditionZh}\n` +
      (remaining.length ? `本角色此标记途径还缺：${remaining.join('、')}` : '本角色所列标记条件已满足；奖励是否开放仍以成就位为准。') +
      (reward.notes ? `\n${reward.notes}` : '')
  }).join('\n\n')
}

export function completionRewardLink(characterId: string, markId: string) {
  const first = rewardsForMark(characterId, markId).find(reward => reward.kind !== 'all-hard')
  return `/characters/${characterId}#${first ? `reward-${first.kind}` : 'completion-rewards'}`
}
