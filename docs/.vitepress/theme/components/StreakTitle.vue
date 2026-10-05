<script setup lang="ts">
// 仿游戏里捡到道具、进入新楼层时出现的黑色笔刷横幅：大字标题 + 一行小字说明
defineProps<{ title: string; sub?: string; tag?: 'h1' | 'h2' | 'h3' | 'div'; size?: 'lg' | 'md' | 'sm' }>()
</script>

<template>
  <component :is="tag ?? 'h2'" class="streak" :class="size ?? 'md'">
    <span class="streak-title">{{ title }}</span>
    <span v-if="sub" class="streak-sub">{{ sub }}</span>
  </component>
</template>

<style scoped>
.streak {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  margin: 0;
  padding: 10px 34px 12px;
  background: var(--ib-outline);
  color: var(--ib-on-dark);
  border: none;
  line-height: 1.25;
  letter-spacing: 0.04em;
  /* 不规则的笔刷边缘 */
  clip-path: polygon(
    2% 18%, 6% 6%, 14% 10%, 22% 2%, 34% 8%, 46% 0%, 58% 7%, 70% 1%, 82% 8%, 92% 3%, 98% 14%,
    100% 46%, 97% 72%, 100% 90%, 90% 97%, 78% 92%, 64% 100%, 50% 93%, 36% 100%, 24% 94%, 12% 100%, 4% 92%, 0% 70%, 3% 44%
  );
}
.streak-title {
  font-family: var(--ib-font-display);
  font-weight: 400;
  letter-spacing: 0.06em;
}
.streak-sub {
  font-size: 13px;
  font-weight: 500;
  opacity: 0.82;
  letter-spacing: 0.02em;
  margin-top: 2px;
}
.lg .streak-title {
  font-size: 32px;
}
.md .streak-title {
  font-size: 25px;
}
.sm {
  padding: 6px 22px 8px;
}
.sm .streak-title {
  font-size: 19px;
}
</style>
