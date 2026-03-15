<template>
  <div class="flex flex-col space-y-2 pr-3 h-full overflow-y-auto">
    <HistoryChatItem
      v-for="key in reversedConversationKeys"
      :key="key"
      :conversationKey="key"
      :menuOpenKey="menuOpenKey"
      @updateMenuOpenKey="onUpdateMenuOpenKey"
      @conversationSelected="onConversationSelected"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import HistoryChatItem from './HistoryChatItem.vue'
import { useConversations } from '@/assets/js/store/conversations'

const conversations = useConversations()
const emits = defineEmits<{
  (e: 'conversationSelected'): void
}>()

const reversedConversationKeys = computed(() => {
  const list = conversations.conversationList ?? {}
  const keys = Object.keys(list).reverse()
  console.log('Reversed conversation keys:', list, keys)
  return keys
})

const menuOpenKey = ref<string | null>(null)

function onUpdateMenuOpenKey(key: string | null) {
  menuOpenKey.value = key
}

function onConversationSelected() {
  emits('conversationSelected')
}
</script>

<style scoped></style>
