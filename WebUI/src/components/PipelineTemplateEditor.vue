<template>
  <div class="mt-4 flex flex-col gap-2 border border-border rounded-md p-4 bg-background">
    <div class="flex justify-between items-center mb-2">
      <h3 class="font-semibold text-sm">Pipeline Template Editor</h3>
      <Button variant="outline" size="sm" @click="$emit('close')">Close</Button>
    </div>
    
    <div class="flex flex-col gap-2">
      <label class="text-xs">Select Preset to Edit:</label>
      <select 
        v-model="selectedPresetId" 
        class="p-2 border border-border rounded-md bg-card text-foreground text-sm"
        @change="loadSelectedPreset"
      >
        <option disabled value="">-- Select a Preset --</option>
        <option v-for="preset in availablePresets" :key="preset.id" :value="preset.id">
          {{ preset.id }} - {{ preset.name }}
        </option>
      </select>
    </div>

    <div v-if="selectedPresetId" class="mt-4 flex flex-col gap-2 h-full">
      <label class="text-xs">Raw JSON Workflow Structure:</label>
      <textarea 
        v-model="templateJson" 
        class="w-full h-[250px] p-2 border border-border rounded-md bg-card text-foreground font-mono text-xs whitespace-pre"
      ></textarea>
      
      <div class="flex justify-end gap-2 mt-2">
        <Button variant="default" size="sm" @click="saveTemplate">Save Template</Button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { usePresets } from '@/assets/js/store/presets'
import { Button } from '@/components/ui/button'
import * as toast from '@/assets/js/toast'

const presetsStore = usePresets()
const availablePresets = computed(() => presetsStore.presets.comfyUiPresets)

const selectedPresetId = ref('')
const templateJson = ref('')
const _emit = defineEmits(['close'])

function loadSelectedPreset() {
  const preset = availablePresets.value.find(p => p.id === selectedPresetId.value)
  if (preset) {
    templateJson.value = JSON.stringify(preset.workflow, null, 2)
  }
}

function saveTemplate() {
  try {
    const preset = availablePresets.value.find(p => p.id === selectedPresetId.value)
    if (preset) {
      const parsed = JSON.parse(templateJson.value)
      preset.workflow = parsed
      // We would ideally save it to the actual file here if the backend supports rewriting presets
      toast.success('Template updated in memory for the current session')
    }
  } catch (e) {
    toast.error('Invalid JSON syntax: ' + e.message)
  }
}
</script>
