<script setup lang="ts">
// 每篇文章顶部标注适用版本和校对日期，版本更新后一眼能看出是否过时
defineProps<{ version?: string; checked?: string; draft?: boolean }>()
</script>

<template>
  <div class="badge-row">
    <span class="badge version">适用版本 · {{ version ?? 'Repentance+' }}</span>
    <span v-if="checked" class="badge checked">校对于 {{ checked }}</span>
    <span v-if="draft" class="badge draft">草稿 · 待校对</span>
  </div>
</template>

<style scoped>
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 4px 0 20px;
}
.badge {
  font-size: 12.5px;
  line-height: 1;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--ib-line);
  color: var(--ib-ink-2);
  background: var(--vp-c-bg-elv);
}
.version {
  border-color: var(--ib-blood);
  color: var(--ib-blood);
  background: var(--ib-blood-soft);
  font-weight: 600;
}
.draft {
  border-color: var(--ib-gold);
  color: var(--ib-gold);
  background: var(--ib-gold-soft);
}
</style>
