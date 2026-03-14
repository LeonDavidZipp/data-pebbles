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
</script>

<template>
  <div class="p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-semibold capitalize">
        {{ layer }} Sources
      </h1>
      <UButton
        icon="i-lucide-plus"
        label="New Source"
        @click="showCreateModal = true"
      />
    </div>

    <div
      v-if="loading"
      class="flex justify-center py-12"
    >
      <UIcon
        name="i-lucide-loader-2"
        class="size-6 animate-spin"
      />
    </div>

    <div
      v-else-if="sources.length === 0"
      class="text-center py-12 text-muted"
    >
      <UIcon
        name="i-lucide-inbox"
        class="size-12 mx-auto mb-3"
      />
      <p>No sources yet. Create one to get started.</p>
    </div>

    <div
      v-else
      class="grid gap-3"
    >
      <div
        v-for="source in sources"
        :key="source.id"
        class="flex items-center justify-between p-4 border border-default rounded-lg hover:bg-elevated transition-colors"
      >
        <NuxtLink
          :to="`/${layer}/${source.id}`"
          class="flex-1"
        >
          <p class="font-medium">
            {{ source.name }}
          </p>
          <p class="text-sm text-muted">
            Created {{ new Date(source.created_at).toLocaleDateString() }}
          </p>
        </NuxtLink>

        <div class="flex gap-2">
          <UButton
            icon="i-lucide-arrow-right"
            variant="ghost"
            color="neutral"
            :to="`/${layer}/${source.id}`"
          />
          <UButton
            icon="i-lucide-trash-2"
            variant="ghost"
            color="error"
            @click="deleteSource(source.id)"
          />
        </div>
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
