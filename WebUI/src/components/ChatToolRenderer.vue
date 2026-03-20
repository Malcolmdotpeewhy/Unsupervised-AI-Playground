<template>
  <template
    v-for="part in toolParts"
    :key="
      part.type === 'tool-comfyUI'
        ? `tool-${part.toolCallId}`
        : part.type === 'tool-comfyUiImageEdit'
          ? `tool-${part.toolCallId}`
          : part.type === 'tool-visualizeObjectDetections'
            ? `tool-${part.toolCallId}`
            : undefined
    "
  >
    <span>I'm using the tool {{ part.type.replace('tool-', '') }}</span>
    <template v-if="part.type === 'tool-comfyUI'">
      <div class="mt-1 pt-1">
        <span
          >Generating using the preset
          <b>{{ part.input?.workflow ?? 'unknown' }}</b></span
        >
        <br />
        <br />
        <span
          ><em>{{ part.input?.prompt ?? '' }}</em></span
        >
        <ChatWorkflowResult
          :images="getToolImages(part as ToolUIPart<AipgTools>)"
          :processing="getToolProcessing(part as ToolUIPart<AipgTools>)"
          :currentState="getToolCurrentState(part as ToolUIPart<AipgTools>)"
          :stepText="getToolStepText(part as ToolUIPart<AipgTools>)"
          :toolCallId="(part as any).toolCallId"
        />
      </div>
    </template>
    <template v-else-if="part.type === 'tool-comfyUiImageEdit'">
      <div class="mt-1 pt-1">
        <span
          >Editing using the preset <b>{{ part.input?.workflow ?? 'unknown' }}</b></span
        >
        <br />
        <br />
        <span
          ><em>{{ part.input?.prompt ?? '' }}</em></span
        >
        <ChatWorkflowResult
          :images="getToolImages(part as ToolUIPart<AipgTools>)"
          :processing="getToolProcessing(part as ToolUIPart<AipgTools>)"
          :currentState="getToolCurrentState(part as ToolUIPart<AipgTools>)"
          :stepText="getToolStepText(part as ToolUIPart<AipgTools>)"
          :toolCallId="(part as any).toolCallId"
        />
      </div>
    </template>
    <template v-else-if="part.type === 'tool-visualizeObjectDetections'">
      <div class="mt-1 pt-1">
        <div
          v-if="
            part.state === 'output-available' && (part as any).output?.annotatedImageUrl
          "
        >
          <img
            :src="(part as any).output.annotatedImageUrl"
            alt="Annotated image with object detections"
            class="max-w-full rounded-md border-2 border-border"
          />
        </div>
        <div
          v-else-if="
            part.state === 'input-streaming' || part.state === 'input-available'
          "
        >
          <span class="text-muted-foreground">Visualizing object detections...</span>
        </div>
      </div>
    </template>
  </template>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import ChatWorkflowResult from './ChatWorkflowResult.vue'
import type { ToolUIPart } from 'ai'
import type { AipgTools } from '@/assets/js/tools/tools'
import type { MediaItem, GenerateState } from '@/assets/js/store/imageGenerationPresets'

interface Props {
  parts: ToolUIPart<AipgTools>[]
  toolProgressMap: Record<string, {
    processing: boolean
    currentState?: GenerateState
    stepText?: string
    images: MediaItem[]
    initialImageIds: Set<string>
  }>
}

const props = defineProps<Props>()

// By moving this here, we ensure that only when parts actually change, we recalculate this array.
// Because parts comes from a parent, we wrap it in computed so it updates correctly
const toolParts = computed(() => {
  return props.parts.filter((p: ToolUIPart<AipgTools>) => p.type && p.type.startsWith('tool-'))
})

const imageArraysCache = new Map<string, MediaItem[]>()

function getToolImages(part: ToolUIPart<AipgTools>): MediaItem[] {
  if (!(part.type === 'tool-comfyUI' || part.type === 'tool-comfyUiImageEdit')) return []
  const toolCallId = part.toolCallId
  const progress = props.toolProgressMap[toolCallId]

  // If we have progress tracking with images, use those
  if (progress && progress.images.length > 0) {
    return progress.images
  }

  // Otherwise, use output images if available
  if (part.state === 'output-available') {
    if (!part.output || !part.output.images) return []

    // Memoize the mapped array so we don't return a new reference on every Vue tick
    const cached = imageArraysCache.get(toolCallId)
    if (cached && cached.length === part.output.images.length) {
      return cached
    }

    const mapped = part.output.images.map((img: MediaItem) => ({ ...img, state: 'done' as const }))
    imageArraysCache.set(toolCallId, mapped)
    return mapped
  }

  return []
}

function getToolProcessing(part: ToolUIPart<AipgTools>): boolean {
  const toolCallId = part.toolCallId
  const progress = props.toolProgressMap[toolCallId]

  // If we have progress tracking, use that
  if (progress) {
    return progress.processing
  }

  // Otherwise, check part state
  return part.state === 'input-streaming' || part.state === 'input-available'
}

function getToolCurrentState(part: ToolUIPart<AipgTools>): GenerateState | undefined {
  const toolCallId = part.toolCallId
  const progress = props.toolProgressMap[toolCallId]

  if (progress && progress.currentState) {
    return progress.currentState as GenerateState
  }

  return undefined
}

function getToolStepText(part: ToolUIPart<AipgTools>): string | undefined {
  const toolCallId = part.toolCallId
  const progress = props.toolProgressMap[toolCallId]

  if (progress && progress.stepText) {
    return progress.stepText
  }

  return undefined
}
</script>
