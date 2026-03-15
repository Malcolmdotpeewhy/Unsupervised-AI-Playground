<template>
  <div
    class="flex flex-col items-center justify-between rounded-lg px-3 py-1 transition cursor-pointer border-2"
    :class="
      conversations.activeKey === conversationKey
        ? 'border-primary bg-muted hover:bg-muted/80'
        : 'border-transparent bg-muted hover:bg-muted/80'
    "
    @click="selectConversation"
  >
    <div class="flex items-center justify-between w-full">
      <span class="truncate text-sm text-foreground">
        {{ conversationTitle }}
      </span>
      <DropdownMenu :open="menuOpenKey === conversationKey" @update:open="onMenuOpenChange">
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
                if (!open) {
                  renameDialogOpen = false
                  emits('updateMenuOpenKey', null)
                }
              }
            "
          >
            <DialogTrigger asChild>
              <DropdownMenuItem
                @select="
                  (e: Event) => {
                    e.preventDefault()
                    openRenameDialog()
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
                <AlertDialogAction @click="() => conversations.deleteConversation(conversationKey)">
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
    <ThumbnailPreviewStrip :items="images" />
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import ThumbnailPreviewStrip from './ThumbnailPreviewStrip.vue'
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from '@/components/ui/dropdown-menu'
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { useConversations } from '@/assets/js/store/conversations'

const props = defineProps<{
  conversationKey: string
  menuOpenKey: string | null
}>()

const emits = defineEmits<{
  (e: 'conversationSelected', key: string): void
  (e: 'updateMenuOpenKey', key: string | null): void
}>()

const conversations = useConversations()

// ⚡ Bolt Performance Optimization: Extract complex loop body into dedicated child component.
// Why: Naturally isolates reactivity, allowing `computed` properties to safely memoize array filtering/mappings and ensuring that updates to a single item only trigger a re-render for that specific child component.
const EMPTY_ARRAY: never[] = []

// ⚡ Bolt Performance Optimization: Memoize images mapping using computed property
// Why: Prevents render thrashing in Vue `v-for` loops during frequent updates. Avoids returning new array references inline which causes O(N) re-renders.
const images = computed(() => {
  const conversation = conversations.conversationList[props.conversationKey]
  if (!conversation) return EMPTY_ARRAY

  const result = conversation.flatMap((msg, msgIndex) =>
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

  // ⚡ Bolt Performance Optimization: Return static constant empty array
  // Why: When helper function called from a Vue template needs to return an empty array, return a predefined static constant `never[]` to prevent Vue from detecting a new reference and unnecessarily re-rendering.
  return result.length > 0 ? result : EMPTY_ARRAY
})

// ⚡ Bolt Performance Optimization: Memoize conversationTitle using computed property
// Why: Prevents redundant recalculations on every render cycle for unmodified list items.
const conversationTitle = computed(() => {
  const conversation = conversations.conversationList[props.conversationKey]
  if (!conversation || conversation.length === 0) {
    return 'New Conversation'
  }
  if (conversation[0].metadata?.conversationTitle) {
    return conversation[0].metadata.conversationTitle
  }
  const firstMessage = conversation[0]

  // todo: can be deleted eventually
  if (firstMessage.parts === undefined) {
    conversations.deleteConversation(props.conversationKey)
    return 'New Conversation'
  }

  const titlePart = firstMessage.parts?.find((part) => part.type === 'text')
  return titlePart ? titlePart.text.substring(0, 50) : 'New Conversation'
})

function onMenuOpenChange(open: boolean) {
  emits('updateMenuOpenKey', open ? props.conversationKey : null)
}

// Rename dialog state
const renameDialogOpen = ref(false)
const renameTitle = ref('')

function openRenameDialog() {
  const existingTitle = conversationTitle.value
  renameTitle.value = existingTitle ?? ''
  renameDialogOpen.value = true
}

function cancelRename() {
  renameDialogOpen.value = false
  emits('updateMenuOpenKey', null)
}

function saveRename() {
  const newTitle = renameTitle.value.trim()
  if (newTitle.length === 0) return
  conversations.renameConversationTitle(props.conversationKey, newTitle)
  renameDialogOpen.value = false
  emits('updateMenuOpenKey', null)
}

const selectConversation = () => {
  conversations.activeKey = props.conversationKey
  console.log('Selected conversation:', props.conversationKey)
  emits('conversationSelected', props.conversationKey)
}
</script>

<style scoped></style>
