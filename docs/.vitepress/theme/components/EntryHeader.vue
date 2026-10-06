<script setup lang="ts">
import GameIcon from './GameIcon.vue'
import type { IconName } from './GameIcon.vue'
defineProps<{ en?: string; category: string; icon: IconName; code?: string }>()
</script>

<template>
  <div class="entry-header">
    <span class="entry-emblem"><GameIcon :name="icon" :size="38" /></span>
    <div class="entry-identity">
      <p v-if="en" class="english">{{ en }}</p>
      <div class="entry-badges">
        <span>{{ category }}</span>
        <code v-if="code">{{ code }}</code>
      </div>
    </div>
  </div>
</template>

<style scoped>
.entry-header { display: flex; align-items: center; gap: 16px; margin: 14px 0 22px; }
.entry-emblem { display: grid; place-items: center; flex: 0 0 60px; height: 60px; border: 2px solid var(--ib-outline); border-radius: 12px; background: var(--ib-paper); box-shadow: 0 3px 0 var(--ib-outline); }
.entry-identity { min-width: 0; }
.english { margin: 0 0 8px; color: var(--ib-ink-3); overflow-wrap: anywhere; }
.entry-badges { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; font-size: 13px; }
.entry-badges span { padding: 2px 9px; border: 1.5px solid var(--ib-outline); border-radius: 999px; background: var(--ib-gold-soft); }
</style>
