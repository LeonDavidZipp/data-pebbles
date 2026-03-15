<script setup lang="ts">
import type {
  MetadataResponse,
  SilverMetadataResponse,
  GoldMetadataResponse,
  VersionResponse,
  SilverLineageResponse,
  GoldLineageResponse
} from '~/utils/api'

const route = useRoute()
const { bronze, silver, gold } = useApi()
const { currentProject } = useCurrentProject()

const layer = computed(() => route.params.layer as string)
const resourceId = computed(() => Number(route.params.resourceId))

const validLayers = ['bronze', 'silver', 'gold']
if (!validLayers.includes(layer.value)) {
  throw createError({ statusCode: 404, message: 'Layer not found' })
}

if (!currentProject.value) {
  navigateTo('/projects')
}

const resource = ref<
  MetadataResponse | SilverMetadataResponse | GoldMetadataResponse | null
>(null)
const versions = ref<
  (VersionResponse | SilverLineageResponse | GoldLineageResponse)[]
>([])
const loading = ref(true)
const showUploadModal = ref(false)
const showRenameModal = ref(false)
const uploading = ref(false)
const renameName = ref('')
const renaming = ref(false)

// Bronze upload
const fileInput = ref<HTMLInputElement | null>(null)
const droppedFile = ref<File | null>(null)
const isDragOver = ref(false)

function onDrop(e: DragEvent) {
  isDragOver.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file) {
    droppedFile.value = file
    uploadVersion()
  }
}

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  const file = input.files?.[0]
  if (file) {
    droppedFile.value = file
    uploadVersion()
  }
}

// Silver upload
// Gold upload

async function fetchResource() {
  if (layer.value === 'bronze') {
    resource.value = await bronze.getResourceBronzeResourceIdGet({
      resourceId: resourceId.value
    })
  } else if (layer.value === 'silver') {
    resource.value = await silver.getResourceSilverResourceIdGet({
      resourceId: resourceId.value
    })
  } else {
    resource.value = await gold.getResourceGoldResourceIdGet({
      resourceId: resourceId.value
    })
  }
}

async function fetchVersions() {
  if (layer.value === 'bronze') {
    versions.value = await bronze.listVersionsBronzeResourceIdVersionsGet({
      resourceId: resourceId.value
    })
  } else if (layer.value === 'silver') {
    versions.value = await silver.listVersionsSilverResourceIdVersionsGet({
      resourceId: resourceId.value
    })
  } else {
    versions.value = await gold.listVersionsGoldResourceIdVersionsGet({
      resourceId: resourceId.value
    })
  }
}

async function fetchAll() {
  loading.value = true
  try {
    await Promise.all([fetchResource(), fetchVersions()])
  } finally {
    loading.value = false
  }
}

async function uploadVersion() {
  const selectedFile = droppedFile.value
  if (!selectedFile || layer.value !== 'bronze') return

  uploading.value = true
  try {
    const file = selectedFile as unknown as string // File object sent via FormData

    await bronze.uploadVersionBronzeResourceIdVersionsPost({
      resourceId: resourceId.value,
      file
    })
    showUploadModal.value = false
    droppedFile.value = null
    await fetchVersions()
  } finally {
    uploading.value = false
  }
}

async function activateVersion(version: number) {
  await bronze.activateVersionBronzeResourceIdVersionsVersionPatch({
    resourceId: resourceId.value,
    version
  })
  await fetchVersions()
}

async function deleteVersion(version: number) {
  await bronze.deleteVersionBronzeResourceIdVersionsVersionDelete({
    resourceId: resourceId.value,
    version
  })
  await fetchVersions()
}

function downloadVersion(version: number) {
  window.open(
    `/api/${layer.value}/${resourceId.value}/versions/${version}`,
    '_blank'
  )
}

async function renameResource() {
  if (!renameName.value.trim()) return
  renaming.value = true
  try {
    if (layer.value === 'bronze') {
      resource.value = await bronze.updateResourceBronzeResourceIdPatch({
        resourceId: resourceId.value,
        updateResourceRequest: { name: renameName.value }
      })
    } else if (layer.value === 'silver') {
      resource.value = await silver.updateResourceSilverResourceIdPatch({
        resourceId: resourceId.value,
        updateSilverResourceRequest: { name: renameName.value }
      })
    } else {
      resource.value = await gold.updateResourceGoldResourceIdPatch({
        resourceId: resourceId.value,
        updateGoldResourceRequest: { name: renameName.value }
      })
    }
    showRenameModal.value = false
  } finally {
    renaming.value = false
  }
}

function openRename() {
  renameName.value = resource.value?.name ?? ''
  showRenameModal.value = true
}

function getVersionNumber(
  v: VersionResponse | SilverLineageResponse | GoldLineageResponse
): number {
  return 'version' in v ? v.version : v.delta_version
}

function getStatus(
  v: VersionResponse | SilverLineageResponse | GoldLineageResponse
): string | null {
  return 'status' in v ? v.status : null
}

const layerButtonClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'bg-gray-400 hover:bg-gray-500 text-white'
    case 'gold': return 'bg-yellow-500 hover:bg-yellow-600 text-white'
    default: return 'bg-amber-700 hover:bg-amber-800 text-white'
  }
})

const layerDragActiveClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'border-gray-400 bg-gray-400/5'
    case 'gold': return 'border-yellow-500 bg-yellow-500/5'
    default: return 'border-amber-700 bg-amber-700/5'
  }
})

const layerTextClass = computed(() => {
  switch (layer.value) {
    case 'silver': return 'text-gray-400'
    case 'gold': return 'text-yellow-500'
    default: return 'text-amber-700'
  }
})

fetchAll()
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header bar -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4">
      <div class="flex items-center justify-between">
        <div>
          <div class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 mb-1">
            <NuxtLink
              :to="`/${layer}`"
              class="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              <span class="capitalize">{{ layer }}</span> Resources
            </NuxtLink>
            <span>/</span>
            <span class="text-gray-900 dark:text-white">{{ resource?.name ?? '...' }}</span>
          </div>
          <div
            v-if="!loading && resource"
            class="flex items-center gap-3"
          >
            <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
              {{ resource.name }}
            </h1>
            <UBadge
              variant="subtle"
              color="neutral"
              size="sm"
              class="capitalize"
            >
              {{ layer }}
            </UBadge>
          </div>
        </div>
        <div
          v-if="!loading && resource"
          class="flex items-center gap-2"
        >
          <UButton
            icon="i-lucide-pencil"
            label="Rename"
            variant="outline"
            color="neutral"
            size="sm"
            @click="openRename"
          />
          <UButton
            v-if="layer === 'bronze'"
            icon="i-lucide-upload"
            label="Upload Version"
            size="sm"
            color="neutral"
            :class="layerButtonClass"
            @click="showUploadModal = true"
          />
        </div>
      </div>
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

      <template v-else-if="resource">
        <!-- Resource details card -->
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg p-5 mb-6">
          <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400 mb-3">
            Resource Details
          </h2>
          <div class="grid grid-cols-4 gap-4 text-sm">
            <div>
              <span class="text-gray-500 dark:text-gray-400">Resource ID</span>
              <p class="font-medium text-gray-900 dark:text-white mt-0.5">
                {{ resource.id }}
              </p>
            </div>
            <div>
              <span class="text-gray-500 dark:text-gray-400">Layer</span>
              <p class="font-medium text-gray-900 dark:text-white capitalize mt-0.5">
                {{ layer }}
              </p>
            </div>
            <div>
              <span class="text-gray-500 dark:text-gray-400">Project</span>
              <p class="font-medium text-gray-900 dark:text-white mt-0.5">
                {{ currentProject?.name ?? '—' }}
              </p>
            </div>
            <div>
              <span class="text-gray-500 dark:text-gray-400">Created</span>
              <p class="font-medium text-gray-900 dark:text-white mt-0.5">
                {{ new Date(resource.created_at).toLocaleDateString() }}
              </p>
            </div>
          </div>
          <div
            v-if="resource.description"
            class="mt-3 text-sm"
          >
            <span class="text-gray-500 dark:text-gray-400">Description</span>
            <p class="font-medium text-gray-900 dark:text-white mt-0.5">
              {{ resource.description }}
            </p>
          </div>
        </div>

        <!-- Versions section -->
        <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-800 rounded-lg overflow-hidden">
          <div class="px-5 py-3 border-b border-gray-200 dark:border-gray-800 flex items-center justify-between">
            <h2 class="text-xs font-semibold uppercase tracking-wider text-gray-500 dark:text-gray-400">
              Versions
            </h2>
            <span class="text-xs text-gray-400">{{ versions.length }} total</span>
          </div>

          <div
            v-if="versions.length === 0"
            class="text-center py-12 text-gray-500 dark:text-gray-400"
          >
            <UIcon
              name="i-lucide-file-x"
              class="size-10 mx-auto mb-3 text-gray-300 dark:text-gray-600"
            />
            <p class="text-sm">
              <template v-if="layer === 'bronze'">
                No versions yet. Upload a file to create the first version.
              </template>
              <template v-else>
                Use the SDK to upload versions to {{ layer }} resources.
              </template>
            </p>
          </div>

          <table
            v-else
            class="w-full text-sm"
          >
            <thead>
              <tr class="border-b border-gray-200 dark:border-gray-800 bg-gray-50 dark:bg-gray-900/50">
                <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                  Version
                </th>
                <th
                  v-if="layer === 'bronze'"
                  class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  v-if="layer !== 'bronze'"
                  class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider"
                >
                  From Resource
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
                v-for="v in versions"
                :key="getVersionNumber(v)"
                class="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
              >
                <td class="py-2.5 px-4 font-mono text-gray-900 dark:text-white">
                  v{{ getVersionNumber(v) }}
                </td>
                <td
                  v-if="layer === 'bronze'"
                  class="py-2.5 px-4"
                >
                  <UBadge
                    :color="getStatus(v) === 'active' ? 'success' : 'neutral'"
                    variant="subtle"
                    size="sm"
                    class="w-20 justify-center"
                  >
                    {{ getStatus(v) }}
                  </UBadge>
                </td>
                <td
                  v-if="layer !== 'bronze'"
                  class="py-2.5 px-4 text-gray-500 dark:text-gray-400"
                >
                  #{{ (v as SilverLineageResponse | GoldLineageResponse).from_resource_id }}
                </td>
                <td class="py-2.5 px-4 text-gray-500 dark:text-gray-400">
                  {{ new Date(v.created_at).toLocaleDateString() }}
                </td>
                <td class="py-2.5 px-4 text-right">
                  <div class="flex justify-end gap-1">
                    <UButton
                      v-if="layer === 'bronze' && getStatus(v) !== 'active'"
                      icon="i-lucide-check-circle"
                      variant="ghost"
                      color="neutral"
                      size="xs"
                      @click="activateVersion(getVersionNumber(v))"
                    />
                    <UButton
                      icon="i-lucide-download"
                      variant="ghost"
                      color="neutral"
                      size="xs"
                      @click="downloadVersion(getVersionNumber(v))"
                    />
                    <UButton
                      v-if="layer === 'bronze'"
                      icon="i-lucide-trash-2"
                      variant="ghost"
                      color="error"
                      size="xs"
                      @click="deleteVersion(getVersionNumber(v))"
                    />
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>

    <!-- Upload Modal -->
    <UModal
      v-model:open="showUploadModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Upload Version
          </h2>
          <div
            class="relative flex flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed p-8 transition-colors"
            :class="[
              uploading ? 'pointer-events-none opacity-60' : 'cursor-pointer',
              isDragOver
                ? layerDragActiveClass
                : 'border-gray-300 dark:border-gray-600 hover:border-gray-400 dark:hover:border-gray-500'
            ]"
            @dragover.prevent="isDragOver = true"
            @dragleave.prevent="isDragOver = false"
            @drop.prevent="onDrop"
            @click="fileInput?.click()"
          >
            <UIcon
              v-if="!uploading"
              name="i-lucide-upload-cloud"
              class="text-3xl text-gray-400"
            />
            <UIcon
              v-else
              name="i-lucide-loader-circle"
              class="text-3xl text-gray-400 animate-spin"
            />
            <p class="text-sm text-gray-500 dark:text-gray-400">
              <template v-if="uploading">
                Uploading...
              </template>
              <template v-else>
                Drag & drop a file here, or <span
                  :class="layerTextClass"
                  class="underline"
                >browse</span>
              </template>
            </p>
            <input
              ref="fileInput"
              type="file"
              class="hidden"
              @change="onFileChange"
            >
          </div>
        </div>
      </template>
    </UModal>

    <!-- Rename Modal -->
    <UModal
      v-model:open="showRenameModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Rename Resource
          </h2>
          <UInput
            v-model="renameName"
            placeholder="New name"
            color="neutral"
            class="mb-4 w-full"
            @keyup.enter="renameResource"
          />
          <div class="flex justify-end gap-2">
            <UButton
              label="Cancel"
              variant="ghost"
              color="neutral"
              @click="showRenameModal = false"
            />
            <UButton
              label="Save"
              color="neutral"
              :loading="renaming"
              @click="renameResource"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
