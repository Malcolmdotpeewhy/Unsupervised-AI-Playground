<template>
  <div class="flex flex-col space-y-2 pr-3 h-full overflow-y-auto">
    <HistoryChatItem
      v-for="key in reversedConversationKeys"
      :key="key"
      class="flex flex-col items-center justify-between rounded-lg px-3 py-1 transition cursor-pointer border-2"
      :class="
        conversations.activeKey === key
          ? 'border-primary bg-muted hover:bg-muted/80'
          : 'border-transparent bg-muted hover:bg-muted/80'
      "
      @click="selectConversation(key)"
    >
      <div class="flex items-center justify-between w-full">
        <span class="truncate text-sm text-foreground">
          {{ conversationTitle(key) }}
        </span>
        <DropdownMenu
          :open="menuOpenKey === key"
          @update:open="(open) => onMenuOpenChange(key, open)"
        >
          <DropdownMenuTrigger as-child>
            <Button variant="ghost" size="icon" class="h-6 w-6" @click.stop>
              <span class="svg-icon i-dots-vertical w-4 h-4"></span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            class="w-28"
            :onCloseAutoFocus="
              (ev) => {
                ev.preventDefault?.()
              }
            "
          >
            <Dialog
              v-model:open="renameDialogOpen"
              @update:open="
                (open) => {
                  if (!open) menuOpenKey = null
                }
              "
            >
              <DialogTrigger asChild>
                <DropdownMenuItem
                  @select="
                    (e: Event) => {
                      e.preventDefault()
                      openRenameDialog(key)
                    }
                  "
                >
                  Rename
                </DropdownMenuItem>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Rename conversation</DialogTitle>
                  <DialogDescription>Set a new title for this conversation.</DialogDescription>
                </DialogHeader>
                <div class="mt-2">
                  <Input
                    autofocus
                    type="text"
                    placeholder="Enter title"
                    v-model="renameTitle"
                    @keydown.enter.prevent="saveRename"
                  />
                </div>
                <DialogFooter>
                  <Button variant="ghost" @click="cancelRename">Cancel</Button>
                  <Button :disabled="!renameTitle.trim()" @click="saveRename">Save</Button>
                </DialogFooter>
              </DialogContent>
            </Dialog>
            <AlertDialog>
              <AlertDialogTrigger asChild>
                <DropdownMenuItem @select="(e: Event) => e.preventDefault()">
                  Delete
                </DropdownMenuItem>
              </AlertDialogTrigger>
              <AlertDialogContent>
                <AlertDialogHeader>
                  <AlertDialogTitle>Delete conversation?</AlertDialogTitle>
                  <AlertDialogDescription>
                    This will permanently remove this conversation and its messages.
                  </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                  <AlertDialogAction @click="() => conversations.deleteConversation(key)">
                    Delete
                  </AlertDialogAction>
                </AlertDialogFooter>
              </AlertDialogContent>
            </AlertDialog>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
      <ThumbnailPreviewStrip :items="conversationImages[key] || []" />
    </div>
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

// ⚡ Bolt Performance Optimization: Memoize images mapping to prevent O(N) array allocation on every render tick for the conversation list.
// Why: Calling a function that returns a new array reference inside a v-for template binding forces the child component to re-render every time, causing render thrashing.
const conversationImages = computed(() => {
  const list = conversations.conversationList ?? {}
  const imagesMap: Record<string, { id: string; imageUrl: string }[]> = {}

  for (const [key, conversation] of Object.entries(list)) {
    imagesMap[key] = conversation.flatMap((msg, msgIndex) =>
      msg.parts
        .filter(
          (part) =>
            (part.type === 'tool-comfyUI' || part.type === 'tool-comfyUiImageEdit') &&
            part.state === 'output-available',
        )
        .map((part, partIndex) => {
          if (
            (part.type === 'tool-comfyUI' || part.type === 'tool-comfyUiImageEdit') &&
            'output' in part &&
            part.output &&
            typeof part.output === 'object' &&
            'images' in part.output
          ) {
            const images = (part.output as { images?: Array<{ imageUrl?: string }> }).images ?? []
            return images.map((img, imgIndex) => ({
              id: `${msgIndex}-${partIndex}-${imgIndex}`,
              imageUrl: img.imageUrl ?? '',
            }))
          }
          return []
        })
        .flat()
        .filter(
          (img): img is { id: string; imageUrl: string } =>
            img !== null &&
            img !== undefined &&
            'imageUrl' in img &&
            typeof img.imageUrl === 'string' &&
            img.imageUrl.trim() !== '' &&
            'id' in img &&
            typeof img.id === 'string',
        ),
    )
  }
  return imagesMap
})

const reversedConversationKeys = computed(() => {
  const list = conversations.conversationList ?? {}
  const keys = Object.keys(list).reverse()
  console.log('Reversed conversation keys:', list, keys)
  return keys
})

const selectConversation = (key: string) => {
  conversations.activeKey = key
  console.log('Selected conversation:', key)
  emits('conversationSelected')
}
</script>

<style scoped></style>
