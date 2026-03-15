<template>
  <div
    class="flex flex-col items-center justify-between rounded-lg px-3 py-1 transition cursor-pointer border-2"
    :class="
      isActive
        ? 'border-primary bg-muted hover:bg-muted/80'
        : 'border-transparent bg-muted hover:bg-muted/80'
    "
    @click="selectConversation"
  >
    <div class="flex items-center justify-between w-full">
      <span class="truncate text-sm text-foreground">
        {{ title }}
      </span>
      <DropdownMenu
        :open="menuOpen"
        @update:open="onMenuOpenChange"
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
                if (!open) menuOpen = false
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
                <AlertDialogAction @click="deleteConversation">
                  Delete
                </AlertDialogAction>
              </AlertDialogFooter>
            </AlertDialogContent>
          </AlertDialog>
        </DropdownMenuContent>
      </DropdownMenu>
    </div>
    <ThumbnailPreviewStrip :items="conversationImages" />
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
}>()

const emits = defineEmits<{
  (e: 'conversationSelected', key: string): void
}>()

const conversations = useConversations()

// ⚡ Bolt Performance Optimization: Extracting HistoryChatItem isolates reactivity.
// Why: When LLM streams text, frequent updates cause the parent component to re-render.
// Memoizing array returning functions here prevents O(N) re-renders for unchanged items.
const conversation = computed(() => conversations.conversationList[props.conversationKey] || [])

const isActive = computed(() => conversations.activeKey === props.conversationKey)

const conversationImages = computed(() => {
  return conversation.value.flatMap((msg, msgIndex) =>
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
})

const title = computed(() => {
  const conv = conversation.value
  if (!conv || conv.length === 0) {
    return 'New Conversation'
  }
  if (conv[0].metadata?.conversationTitle) {
    return conv[0].metadata.conversationTitle
  }
  const firstMessage = conv[0]

  // todo: can be deleted eventually
  if (firstMessage.parts === undefined) {
    conversations.deleteConversation(props.conversationKey)
  }

  const titlePart = firstMessage.parts?.find((part) => part.type === 'text')
  return titlePart ? titlePart.text.substring(0, 50) : 'New Conversation'
})

const menuOpen = ref(false)

function onMenuOpenChange(open: boolean) {
  menuOpen.value = open
}

// Rename dialog state
const renameDialogOpen = ref(false)
const renameTitle = ref('')

function openRenameDialog() {
  renameTitle.value = title.value ?? ''
  renameDialogOpen.value = true
}

function cancelRename() {
  renameDialogOpen.value = false
  menuOpen.value = false
}

function saveRename() {
  const newTitle = renameTitle.value.trim()
  if (newTitle.length === 0) return
  conversations.renameConversationTitle(props.conversationKey, newTitle)
  renameDialogOpen.value = false
  menuOpen.value = false
}

function selectConversation() {
  conversations.activeKey = props.conversationKey
  console.log('Selected conversation:', props.conversationKey)
  emits('conversationSelected', props.conversationKey)
}

function deleteConversation() {
  conversations.deleteConversation(props.conversationKey)
}
</script>

<style scoped></style>
