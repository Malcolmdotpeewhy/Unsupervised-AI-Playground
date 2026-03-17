<template>
  <div class="flex flex-col space-y-2 pr-3 h-full overflow-y-auto">
    <HistoryChatItem
      v-for="key in reversedConversationKeys"
      :key="key"
      :conversation-key="key"
      @conversation-selected="() => emits('conversationSelected')"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
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
</script>

<style scoped></style>
