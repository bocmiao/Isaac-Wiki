<script setup lang="ts">
// 每篇文章顶部标注适用版本和校对日期，版本更新后一眼能看出是否过时
defineProps<{ version?: string; checked?: string; draft?: boolean }>()
</script>

<template>
  <div class="badge-row">
    <span class="badge version">适用版本 · {{ version ?? '忏悔 / 忏悔+' }}</span>
    <span v-if="checked" class="badge">校对于 {{ checked }}</span>
    <span v-if="draft" class="badge draft">草稿 · 待校对</span>
  </div>
</template>

<style scoped>
.badge-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 4px 0 22px;
}
.badge {
  font-size: 12.5px;
  font-weight: 700;
  line-height: 1;
  padding: 6px 10px;
  border-radius: 999px;
  border: 2px solid var(--ib-line);
  color: var(--ib-ink-2);
}
.version {
  border-color: var(--ib-outline);
  background: var(--ib-blood-btn);
  color: var(--ib-on-dark);
}
.draft {
  border-color: var(--ib-gold);
  color: var(--ib-gold);
}
</style>
