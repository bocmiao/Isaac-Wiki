<template>
  <kbd class="keycap"><slot /></kbd>
</template>

<style scoped>
.keycap {
  display: inline-block;
  min-width: 1.9em;
  padding: 1px 7px;
  margin: 0 2px;
  font-family: var(--vp-font-family-mono);
  font-size: 0.85em;
  text-align: center;
  color: var(--ib-ink);
  background: var(--vp-c-bg-elv);
  border: 1px solid var(--ib-line);
  border-bottom-width: 3px;
  border-radius: 6px;
}
</style>
