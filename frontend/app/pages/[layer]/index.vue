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

const resources = ref<
  (MetadataResponse | SilverMetadataResponse | GoldMetadataResponse)[]
>([])
const loading = ref(true)
const showCreateModal = ref(false)
const newResourceName = ref('')
const creating = ref(false)

async function fetchResources() {
  loading.value = true
  try {
    if (layer.value === 'bronze') {
      resources.value = await bronze.listResourcesBronzeGet()
    } else if (layer.value === 'silver') {
      resources.value = await silver.listResourcesSilverGet()
    } else {
      resources.value = await gold.listResourcesGoldGet()
    }
  } finally {
    loading.value = false
  }
}

async function createResource() {
  if (!newResourceName.value.trim()) return
  creating.value = true
  try {
    if (layer.value === 'bronze') {
      await bronze.createResourceBronzePost({
        createResourceRequest: { name: newResourceName.value }
      })
    } else if (layer.value === 'silver') {
      await silver.createResourceSilverPost({
        createSilverResourceRequest: { name: newResourceName.value }
      })
    } else {
      await gold.createResourceGoldPost({
        createGoldResourceRequest: { name: newResourceName.value }
      })
    }
    newResourceName.value = ''
    showCreateModal.value = false
    await fetchResources()
  } finally {
    creating.value = false
  }
}

async function deleteResource(id: number) {
  if (layer.value === 'bronze') {
    await bronze.deleteResourceBronzeResourceIdDelete({ resourceId: id })
  } else if (layer.value === 'silver') {
    await silver.deleteResourceSilverResourceIdDelete({ resourceId: id })
  } else {
    await gold.deleteResourceGoldResourceIdDelete({ resourceId: id })
  }
  await fetchResources()
}

watch(layer, fetchResources, { immediate: true })

const layerButtonClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'bg-gray-400 hover:bg-gray-500 text-white'
    case 'gold': return 'bg-yellow-500 hover:bg-yellow-600 text-white'
    default: return 'bg-amber-700 hover:bg-amber-800 text-white'
  }
})

const layerIconClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'bg-gray-400/10 text-gray-400'
    case 'gold': return 'bg-yellow-500/10 text-yellow-500'
    default: return 'bg-amber-700/10 text-amber-700'
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
          {{ layer }} Resources
        </h1>
      </div>
      <UButton
        icon="i-lucide-plus"
        label="New Resource"
        color="neutral"
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
        v-else-if="resources.length === 0"
        class="text-center py-16 text-gray-500 dark:text-gray-400"
      >
        <UIcon
          name="i-lucide-inbox"
          class="size-12 mx-auto mb-3 text-gray-300 dark:text-gray-600"
        />
        <p class="text-sm">
          No resources yet. Create one to get started.
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
              v-for="resource in resources"
              :key="resource.id"
              class="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
              @click="navigateTo(`/${layer}/${resource.id}`)"
            >
              <td class="py-3 px-4">
                <div class="flex items-center gap-2.5">
                  <div
                    class="size-8 rounded flex items-center justify-center"
                    :class="layerIconClass"
                  >
                    <UIcon
                      name="i-lucide-file-box"
                      class="size-4"
                    />
                  </div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ resource.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 dark:text-gray-400">
                {{ new Date(resource.created_at).toLocaleDateString() }}
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
                    :to="`/${layer}/${resource.id}`"
                  />
                  <UButton
                    icon="i-lucide-trash-2"
                    variant="ghost"
                    color="error"
                    size="xs"
                    @click="deleteResource(resource.id)"
                  />
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <UModal
      v-model:open="showCreateModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Create {{ layer }} resource
          </h2>
          <UInput
            v-model="newResourceName"
            placeholder="Resource name"
            color="neutral"
            class="mb-4 w-full"
            @keyup.enter="createResource"
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
              color="neutral"
              variant="solid"
              :loading="creating"
              @click="createResource"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
