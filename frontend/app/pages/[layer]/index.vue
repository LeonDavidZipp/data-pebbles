<script setup lang="ts">
import type {
  MetadataResponse,
  GoldMetadataResponse,
  SilverMetadataResponse
} from '~/utils/api'

const route = useRoute()
const { bronze, silver, gold } = useApi()

const layer = computed(() => route.params.layer as string)

const validLayers = ['bronze', 'silver', 'gold']
if (!validLayers.includes(layer.value)) {
  throw createError({ statusCode: 404, message: 'Layer not found' })
}

const sources = ref<
  (MetadataResponse | SilverMetadataResponse | GoldMetadataResponse)[]
>([])
const loading = ref(true)
const showCreateModal = ref(false)
const newSourceName = ref('')
const creating = ref(false)

async function fetchSources() {
  loading.value = true
  try {
    if (layer.value === 'bronze') {
      sources.value = await bronze.listSourcesBronzeGet()
    } else if (layer.value === 'silver') {
      sources.value = await silver.listSourcesSilverGet()
    } else {
      sources.value = await gold.listSourcesGoldGet()
    }
  } finally {
    loading.value = false
  }
}

async function createSource() {
  if (!newSourceName.value.trim()) return
  creating.value = true
  try {
    if (layer.value === 'bronze') {
      await bronze.createSourceBronzePost({
        createSourceRequest: { name: newSourceName.value }
      })
    } else if (layer.value === 'silver') {
      await silver.createSourceSilverPost({
        createSilverSourceRequest: { name: newSourceName.value }
      })
    } else {
      await gold.createSourceGoldPost({
        createGoldSourceRequest: { name: newSourceName.value }
      })
    }
    newSourceName.value = ''
    showCreateModal.value = false
    await fetchSources()
  } finally {
    creating.value = false
  }
}

async function deleteSource(id: number) {
  if (layer.value === 'bronze') {
    await bronze.deleteSourceBronzeSourceIdDelete({ sourceId: id })
  } else if (layer.value === 'silver') {
    await silver.deleteSourceSilverSourceIdDelete({ sourceId: id })
  } else {
    await gold.deleteSourceGoldSourceIdDelete({ sourceId: id })
  }
  await fetchSources()
}

watch(layer, fetchSources, { immediate: true })

const layerButtonClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'bg-gray-400 hover:bg-gray-500 text-white'
    case 'gold': return 'bg-yellow-500 hover:bg-yellow-600 text-white'
    default: return 'bg-amber-700 hover:bg-amber-800 text-white'
  }
})
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header bar -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4 flex items-center justify-between">
      <div>
        <div class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 mb-1">
          <span>Layers</span>
          <span>/</span>
          <span class="capitalize text-gray-900 dark:text-white">{{ layer }}</span>
        </div>
        <h1 class="text-xl font-semibold text-gray-900 dark:text-white capitalize">
          {{ layer }} Sources
        </h1>
      </div>
      <UButton
        icon="i-lucide-plus"
        label="New Source"
        :class="layerButtonClass"
        @click="showCreateModal = true"
      />
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-auto p-6 bg-gray-50 dark:bg-gray-950">
      <div
        v-if="loading"
        class="flex justify-center py-12"
      >
        <UIcon
          name="i-lucide-loader-2"
          class="size-6 animate-spin text-gray-400"
        />
      </div>

      <div
        v-else-if="sources.length === 0"
        class="text-center py-16 text-gray-500 dark:text-gray-400"
      >
        <UIcon
          name="i-lucide-inbox"
          class="size-12 mx-auto mb-3 text-gray-300 dark:text-gray-600"
        />
        <p class="text-sm">
          No sources yet. Create one to get started.
        </p>
      </div>

      <div
        v-else
        class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden"
      >
        <table class="w-full text-sm">
          <thead>
            <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
              <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                Name
              </th>
              <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                Created
              </th>
              <th class="text-right py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="source in sources"
              :key="source.id"
              class="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
              @click="navigateTo(`/${layer}/${source.id}`)"
            >
              <td class="py-3 px-4">
                <div class="flex items-center gap-2.5">
                  <div class="size-8 rounded bg-primary/10 flex items-center justify-center">
                    <UIcon
                      name="i-lucide-file-box"
                      class="size-4 text-primary"
                    />
                  </div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ source.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 dark:text-gray-400">
                {{ new Date(source.created_at).toLocaleDateString() }}
              </td>
              <td class="py-3 px-4 text-right">
                <div
                  class="flex justify-end gap-1"
                  @click.stop
                >
                  <UButton
                    icon="i-lucide-arrow-right"
                    variant="ghost"
                    color="neutral"
                    size="xs"
                    :to="`/${layer}/${source.id}`"
                  />
                  <UButton
                    icon="i-lucide-trash-2"
                    variant="ghost"
                    color="error"
                    size="xs"
                    @click="deleteSource(source.id)"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <UModal v-model:open="showCreateModal">
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Create {{ layer }} source
          </h2>
          <UInput
            v-model="newSourceName"
            placeholder="Source name"
            class="mb-4"
            @keyup.enter="createSource"
          />
          <div class="flex justify-end gap-2">
            <UButton
              label="Cancel"
              variant="ghost"
              color="neutral"
              @click="showCreateModal = false"
            />
            <UButton
              label="Create"
              :loading="creating"
              @click="createSource"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
