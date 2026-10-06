<script setup lang="ts">
import EntryCatalog from './EntryCatalog.vue'
import data from '../data/catalog/items.json'
import type { CatalogEntry } from '../data/catalog'
const entries = data as CatalogEntry[]
</script>

<template>
  <EntryCatalog :entries="entries" label="道具速查" />
</template>
