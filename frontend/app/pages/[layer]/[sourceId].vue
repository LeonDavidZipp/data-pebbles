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

const layer = computed(() => route.params.layer as string)
const sourceId = computed(() => Number(route.params.sourceId))

const validLayers = ['bronze', 'silver', 'gold']
if (!validLayers.includes(layer.value)) {
  throw createError({ statusCode: 404, message: 'Layer not found' })
}

const source = ref<
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

async function fetchSource() {
  if (layer.value === 'bronze') {
    source.value = await bronze.getSourceBronzeSourceIdGet({
      sourceId: sourceId.value
    })
  } else if (layer.value === 'silver') {
    source.value = await silver.getSourceSilverSourceIdGet({
      sourceId: sourceId.value
    })
  } else {
    source.value = await gold.getSourceGoldSourceIdGet({
      sourceId: sourceId.value
    })
  }
}

async function fetchVersions() {
  if (layer.value === 'bronze') {
    versions.value = await bronze.listVersionsBronzeSourceIdVersionsGet({
      sourceId: sourceId.value
    })
  } else if (layer.value === 'silver') {
    versions.value = await silver.listVersionsSilverSourceIdVersionsGet({
      sourceId: sourceId.value
    })
  } else {
    versions.value = await gold.listVersionsGoldSourceIdVersionsGet({
      sourceId: sourceId.value
    })
  }
}

async function fetchAll() {
  loading.value = true
  try {
    await Promise.all([fetchSource(), fetchVersions()])
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

    await bronze.uploadVersionBronzeSourceIdVersionsPost({
      sourceId: sourceId.value,
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
  await bronze.activateVersionBronzeSourceIdVersionsVersionPatch({
    sourceId: sourceId.value,
    version
  })
  await fetchVersions()
}

async function deleteVersion(version: number) {
  await bronze.deleteVersionBronzeSourceIdVersionsVersionDelete({
    sourceId: sourceId.value,
    version
  })
  await fetchVersions()
}

function downloadVersion(version: number) {
  window.open(
    `/api/${layer.value}/${sourceId.value}/versions/${version}`,
    '_blank'
  )
}

async function renameSource() {
  if (!renameName.value.trim()) return
  renaming.value = true
  try {
    if (layer.value === 'bronze') {
      source.value = await bronze.updateSourceBronzeSourceIdPatch({
        sourceId: sourceId.value,
        updateSourceRequest: { name: renameName.value }
      })
    } else if (layer.value === 'silver') {
      source.value = await silver.updateSourceSilverSourceIdPatch({
        sourceId: sourceId.value,
        updateSilverSourceRequest: { name: renameName.value }
      })
    } else {
      source.value = await gold.updateSourceGoldSourceIdPatch({
        sourceId: sourceId.value,
        updateGoldSourceRequest: { name: renameName.value }
      })
    }
    showRenameModal.value = false
  } finally {
    renaming.value = false
  }
}

function openRename() {
  renameName.value = source.value?.name ?? ''
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

fetchAll()
</script>

<template>
  <div class="p-6">
    <div
      v-if="loading"
      class="flex justify-center py-12"
    >
      <UIcon
        name="i-lucide-loader-2"
        class="size-6 animate-spin"
      />
    </div>

    <template v-else-if="source">
      <div class="flex items-center gap-3 mb-6">
        <UButton
          icon="i-lucide-arrow-left"
          variant="ghost"
          color="neutral"
          :to="`/${layer}`"
        />
        <div class="flex-1">
          <h1 class="text-2xl font-semibold">
            {{ source.name }}
          </h1>
          <p class="text-sm text-muted">
            {{ layer }} source #{{ source.id }} &middot; Created
            {{ new Date(source.created_at).toLocaleDateString() }}
          </p>
        </div>
        <UButton
          icon="i-lucide-pencil"
          label="Rename"
          variant="outline"
          color="neutral"
          @click="openRename"
        />
        <UButton
          v-if="layer === 'bronze'"
          icon="i-lucide-upload"
          label="Upload Version"
          @click="showUploadModal = true"
        />
      </div>

      <div
        v-if="versions.length === 0"
        class="text-center py-12 text-muted"
      >
        <UIcon
          name="i-lucide-file-x"
          class="size-12 mx-auto mb-3"
        />
        <p>
          No versions yet.
          <template v-if="layer === 'bronze'">
            Upload a file to create the first version.
          </template><template v-else>
            Use the SDK to upload versions to {{ layer }} sources.
          </template>
        </p>
      </div>

      <table
        v-else
        class="w-full text-sm"
      >
        <thead>
          <tr class="border-b border-default text-left">
            <th class="py-2 px-3 font-medium">
              Version
            </th>
            <th
              v-if="layer === 'bronze'"
              class="py-2 px-3 font-medium"
            >
              Status
            </th>
            <th
              v-if="layer !== 'bronze'"
              class="py-2 px-3 font-medium"
            >
              From Source
            </th>
            <th class="py-2 px-3 font-medium">
              Created
            </th>
            <th class="py-2 px-3 font-medium text-right">
              Actions
            </th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="v in versions"
            :key="getVersionNumber(v)"
            class="border-b border-default hover:bg-elevated transition-colors"
          >
            <td class="py-2 px-3">
              v{{ getVersionNumber(v) }}
            </td>
            <td
              v-if="layer === 'bronze'"
              class="py-2 px-3"
            >
              <UBadge
                :color="getStatus(v) === 'active' ? 'success' : 'neutral'"
                variant="subtle"
                size="sm"
              >
                {{ getStatus(v) }}
              </UBadge>
            </td>
            <td
              v-if="layer !== 'bronze'"
              class="py-2 px-3"
            >
              #{{
                (v as SilverLineageResponse | GoldLineageResponse)
                  .from_source_id
              }}
            </td>
            <td class="py-2 px-3">
              {{ new Date(v.created_at).toLocaleDateString() }}
            </td>
            <td class="py-2 px-3 text-right">
              <div class="flex justify-end gap-1">
                <UButton
                  icon="i-lucide-download"
                  variant="ghost"
                  color="neutral"
                  size="xs"
                  @click="downloadVersion(getVersionNumber(v))"
                />
                <UButton
                  v-if="layer === 'bronze' && getStatus(v) !== 'active'"
                  icon="i-lucide-check-circle"
                  variant="ghost"
                  color="primary"
                  size="xs"
                  @click="activateVersion(getVersionNumber(v))"
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
    </template>

    <!-- Upload Modal -->
    <UModal v-model:open="showUploadModal">
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
                ? 'border-primary bg-primary/5'
                : 'border-gray-500/40 hover:border-gray-400'
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
            <p class="text-sm text-gray-400">
              <template v-if="uploading">
                Uploading...
              </template>
              <template v-else>
                Drag & drop a file here, or
                <span class="text-primary underline">browse</span>
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
    <UModal v-model:open="showRenameModal">
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Rename Source
          </h2>
          <UInput
            v-model="renameName"
            placeholder="New name"
            class="mb-4"
            @keyup.enter="renameSource"
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
              :loading="renaming"
              @click="renameSource"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
