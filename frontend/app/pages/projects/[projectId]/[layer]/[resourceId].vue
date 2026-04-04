<script setup lang="ts">
import type {
  MetadataResponse,
  VersionResponse,
  LineageResponse,
  SchemaResponse
} from '~/utils/api'

const route = useRoute()
const { raw, bronze, silver, gold } = useApi()
const { copiedId, copyId } = useCopyId()

const projectId = computed(() => Number(route.params.projectId))
const layer = computed(() => route.params.layer as string)
const resourceId = computed(() => Number(route.params.resourceId))

const validLayers = ['raw', 'bronze', 'silver', 'gold']
if (!validLayers.includes(layer.value)) {
  throw createError({ statusCode: 404, message: 'Layer not found' })
}

const isRaw = computed(() => layer.value === 'raw')
const hasSchema = computed(() => ['bronze', 'silver', 'gold'].includes(layer.value))

const resource = ref<MetadataResponse | null>(null)
const versions = ref<
  (VersionResponse | LineageResponse)[]
>([])
const loading = ref(true)
const showUploadModal = ref(false)
const showRenameModal = ref(false)
const uploading = ref(false)
const renameName = ref('')
const renameDescription = ref('')
const renaming = ref(false)

const schemaMap = ref<Map<number, SchemaResponse>>(new Map())
const schemaLoadingSet = ref<Set<number>>(new Set())

// Raw file preview
interface RawPreview {
  type: 'table' | 'text'
  columns?: string[]
  rows?: Record<string, unknown>[]
  text?: string
}
const rawPreviewMap = ref<Map<number, RawPreview>>(new Map())
const rawPreviewLoadingSet = ref<Set<number>>(new Set())

// Raw upload
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

async function fetchResource() {
  if (layer.value === 'raw') {
    resource.value = await raw.getResourceRawResourceIdGet({
      resourceId: resourceId.value
    })
  } else if (layer.value === 'bronze') {
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
  if (layer.value === 'raw') {
    versions.value = await raw.listVersionsRawResourceIdVersionsGet({
      resourceId: resourceId.value
    })
  } else if (layer.value === 'bronze') {
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
  if (!selectedFile || !isRaw.value) return

  uploading.value = true
  try {
    const file = selectedFile as unknown as string

    await raw.uploadVersionRawResourceIdVersionsPost({
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
  await raw.activateVersionRawResourceIdVersionsVersionPatch({
    resourceId: resourceId.value,
    version
  })
  await fetchVersions()
}

async function deleteVersion(version: number) {
  await raw.deleteVersionRawResourceIdVersionsVersionDelete({
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
    const desc = renameDescription.value || null
    if (layer.value === 'raw') {
      resource.value = await raw.updateResourceRawResourceIdPatch({
        resourceId: resourceId.value,
        updateResourceRequest: { name: renameName.value, description: desc }
      })
    } else if (layer.value === 'bronze') {
      resource.value = await bronze.updateResourceBronzeResourceIdPatch({
        resourceId: resourceId.value,
        updateResourceRequest: { name: renameName.value, description: desc }
      })
    } else if (layer.value === 'silver') {
      resource.value = await silver.updateResourceSilverResourceIdPatch({
        resourceId: resourceId.value,
        updateResourceRequest: { name: renameName.value, description: desc }
      })
    } else {
      resource.value = await gold.updateResourceGoldResourceIdPatch({
        resourceId: resourceId.value,
        updateResourceRequest: { name: renameName.value, description: desc }
      })
    }
    showRenameModal.value = false
  } finally {
    renaming.value = false
  }
}

function openRename() {
  renameName.value = resource.value?.name ?? ''
  renameDescription.value = resource.value?.description ?? ''
  showRenameModal.value = true
}

async function toggleSchema(version: number) {
  if (!hasSchema.value) return
  if (schemaMap.value.has(version)) {
    schemaMap.value.delete(version)
    return
  }
  schemaLoadingSet.value.add(version)
  try {
    let result: SchemaResponse | undefined
    if (layer.value === 'bronze') {
      result = await bronze.getSchemaBronzeResourceIdVersionsVersionSchemaGet({
        resourceId: resourceId.value,
        version
      })
    } else if (layer.value === 'silver') {
      result = await silver.getSchemaSilverResourceIdVersionsVersionSchemaGet({
        resourceId: resourceId.value,
        version
      })
    } else if (layer.value === 'gold') {
      result = await gold.getSchemaGoldResourceIdVersionsVersionSchemaGet({
        resourceId: resourceId.value,
        version
      })
    }
    if (result) schemaMap.value.set(version, result)
  } finally {
    schemaLoadingSet.value.delete(version)
  }
}

function getFileExtension(v: VersionResponse): string {
  const key = v.s3_key || ''
  const dot = key.lastIndexOf('.')
  return dot >= 0 ? key.slice(dot + 1).toLowerCase() : ''
}

function parseCSV(text: string, delimiter = ','): { columns: string[], rows: Record<string, unknown>[] } {
  const lines = text.split(/\r?\n/).filter(l => l.trim())
  if (lines.length === 0) return { columns: [], rows: [] }
  const columns = lines[0]!.split(delimiter).map(c => c.trim().replace(/^"|"$/g, ''))
  const rows = lines.slice(1, 6).map((line) => {
    const values = line.split(delimiter).map(v => v.trim().replace(/^"|"$/g, ''))
    return Object.fromEntries(columns.map((col, i) => [col, values[i] ?? '']))
  })
  return { columns, rows }
}

async function toggleRawPreview(version: number) {
  if (!isRaw.value) return
  if (rawPreviewMap.value.has(version)) {
    rawPreviewMap.value.delete(version)
    return
  }

  const v = versions.value.find(ver => getVersionNumber(ver) === version) as VersionResponse | undefined
  if (!v) return

  rawPreviewLoadingSet.value.add(version)
  try {
    const ext = getFileExtension(v)
    const response = await fetch(`/api/raw/${resourceId.value}/versions/${version}`)

    if (ext === 'json') {
      const text = await response.text()
      try {
        const parsed = JSON.parse(text)
        if (Array.isArray(parsed) && parsed.length > 0 && typeof parsed[0] === 'object' && parsed[0] !== null) {
          const items = parsed.slice(0, 5)
          const columns = [...new Set(items.flatMap((item: Record<string, unknown>) => Object.keys(item)))]
          const rows = items.map((item: Record<string, unknown>) =>
            Object.fromEntries(columns.map(col => [col, item[col]]))
          )
          rawPreviewMap.value.set(version, { type: 'table', columns, rows })
        } else {
          rawPreviewMap.value.set(version, { type: 'text', text: JSON.stringify(parsed, null, 2).slice(0, 5000) })
        }
      } catch {
        rawPreviewMap.value.set(version, { type: 'text', text: text.slice(0, 5000) })
      }
    } else if (ext === 'xlsx' || ext === 'xls') {
      const buffer = await response.arrayBuffer()
      try {
        const XLSX = await import('xlsx')
        const wb = XLSX.read(buffer, { type: 'array' })
        const sheetName = wb.SheetNames[0]
        const sheet = sheetName ? wb.Sheets[sheetName] : undefined
        if (sheet) {
          const jsonData = XLSX.utils.sheet_to_json<Record<string, unknown>>(sheet)
          const items = jsonData.slice(0, 5)
          const columns = items.length > 0 ? [...new Set(items.flatMap(item => Object.keys(item)))] : []
          const rows = items.map(item =>
            Object.fromEntries(columns.map(col => [col, item[col]]))
          )
          rawPreviewMap.value.set(version, { type: 'table', columns, rows })
        } else {
          rawPreviewMap.value.set(version, { type: 'text', text: '(empty workbook)' })
        }
      } catch {
        rawPreviewMap.value.set(version, { type: 'text', text: '(unable to parse spreadsheet)' })
      }
    } else if (ext === 'csv') {
      const text = await response.text()
      try {
        const { columns, rows } = parseCSV(text, ',')
        if (columns.length > 0) {
          rawPreviewMap.value.set(version, { type: 'table', columns, rows })
        } else {
          rawPreviewMap.value.set(version, { type: 'text', text: text.slice(0, 5000) })
        }
      } catch {
        rawPreviewMap.value.set(version, { type: 'text', text: text.slice(0, 5000) })
      }
    } else if (ext === 'tsv') {
      const text = await response.text()
      try {
        const { columns, rows } = parseCSV(text, '\t')
        if (columns.length > 0) {
          rawPreviewMap.value.set(version, { type: 'table', columns, rows })
        } else {
          rawPreviewMap.value.set(version, { type: 'text', text: text.slice(0, 5000) })
        }
      } catch {
        rawPreviewMap.value.set(version, { type: 'text', text: text.slice(0, 5000) })
      }
    } else {
      // Try reading as text for any other extension
      try {
        const text = await response.text()
        // If text looks like binary (lots of null bytes or control chars), show a message
        const controlCount = [...text.slice(0, 500)].filter((c) => {
          const code = c.charCodeAt(0)
          return code < 32 && code !== 9 && code !== 10 && code !== 13
        }).length
        if (controlCount > 50) {
          rawPreviewMap.value.set(version, { type: 'text', text: '(binary file \u2014 cannot preview)' })
        } else {
          const lines = text.split(/\r?\n/).slice(0, 20).join('\n')
          rawPreviewMap.value.set(version, { type: 'text', text: lines.slice(0, 5000) })
        }
      } catch {
        rawPreviewMap.value.set(version, { type: 'text', text: '(unable to read file)' })
      }
    }
  } catch {
    rawPreviewMap.value.set(version, { type: 'text', text: '(failed to load preview)' })
  } finally {
    rawPreviewLoadingSet.value.delete(version)
  }
}

function getSchemaColumns(schema: SchemaResponse) {
  return Object.keys(schema.data_schema)
}

function getSchemaRows(schema: SchemaResponse) {
  const cols = getSchemaColumns(schema)
  const firstCol = cols[0]
  if (!firstCol) return []
  const rowCount = schema.data[firstCol]?.length ?? 0
  return Array.from({ length: rowCount }, (_, i) =>
    Object.fromEntries(cols.map(col => [col, schema.data[col]?.[i]]))
  )
}

function formatCell(value: unknown): string {
  if (value == null) return '\u2014'
  if (typeof value === 'number' && !Number.isInteger(value)) {
    return value.toFixed(3)
  }
  return String(value)
}

function getVersionNumber(
  v: VersionResponse | LineageResponse
): number {
  return 'version' in v ? v.version : v.delta_version
}

function getDisplayVersion(
  v: VersionResponse | LineageResponse
): number {
  return 'version' in v ? v.version : v.delta_version + 1
}

function getStatus(
  v: VersionResponse | LineageResponse
): string | null {
  return 'status' in v ? v.status : null
}

function hasPreview(version: number): boolean {
  if (isRaw.value) return rawPreviewMap.value.has(version)
  return schemaMap.value.has(version)
}

function isPreviewLoading(version: number): boolean {
  if (isRaw.value) return rawPreviewLoadingSet.value.has(version)
  return schemaLoadingSet.value.has(version)
}

function togglePreview(version: number) {
  if (isRaw.value) return toggleRawPreview(version)
  return toggleSchema(version)
}

const layerButtonClass = computed(() => {
  switch (layer.value) {
    case 'raw': return 'bg-blue-600 hover:bg-blue-700 text-white'
    case 'silver': return 'bg-gray-400 hover:bg-gray-500 text-white'
    case 'gold': return 'bg-yellow-500 hover:bg-yellow-600 text-white'
    default: return 'bg-amber-700 hover:bg-amber-800 text-white'
  }
})

const layerDragActiveClass = computed(() => {
  switch (layer.value) {
    case 'raw': return 'border-blue-600 bg-blue-600/5'
    case 'silver': return 'border-gray-400 bg-gray-400/5'
    case 'gold': return 'border-yellow-500 bg-yellow-500/5'
    default: return 'border-amber-700 bg-amber-700/5'
  }
})

const layerTextClass = computed(() => {
  switch (layer.value) {
    case 'raw': return 'text-blue-600'
    case 'silver': return 'text-gray-400'
    case 'gold': return 'text-yellow-500'
    default: return 'text-amber-700'
  }
})

const backTo = computed(() => `/projects/${projectId.value}`)

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
              to="/projects"
              class="hover:text-gray-900 dark:hover:text-white transition-colors"
            >
              Projects
            </NuxtLink>
            <span>/</span>
            <NuxtLink
              :to="backTo"
              class="hover:text-gray-900 dark:hover:text-white transition-colors capitalize"
            >
              {{ resource?.name ? '' : '...' }}{{ layer }}
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
            label="Edit"
            variant="outline"
            color="neutral"
            size="sm"
            @click="openRename"
          />
          <UButton
            v-if="isRaw"
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
          <div class="grid grid-cols-3 gap-4 text-sm">
            <div>
              <span class="text-gray-500 dark:text-gray-400">Resource ID</span>
              <div class="flex items-center gap-1 mt-0.5">
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ resource.id }}
                </p>
                <UButton
                  :icon="copiedId === `resource-${resource.id}` ? 'i-lucide-check' : 'i-lucide-copy'"
                  variant="ghost"
                  color="neutral"
                  size="xs"
                  class="size-5 cursor-pointer"
                  @click="copyId(`resource-${resource.id}`, resource.id)"
                />
              </div>
            </div>
            <div>
              <span class="text-gray-500 dark:text-gray-400">Layer</span>
              <p class="font-medium text-gray-900 dark:text-white capitalize mt-0.5">
                {{ layer }}
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
              <template v-if="isRaw">
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
                <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                  ID
                </th>
                <th
                  v-if="isRaw"
                  class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider"
                >
                  Status
                </th>
                <th
                  v-if="!isRaw"
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
              <template
                v-for="v in versions"
                :key="getVersionNumber(v)"
              >
                <tr
                  class="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
                  @click="togglePreview(getVersionNumber(v))"
                >
                  <td class="py-2.5 px-4 font-mono text-gray-900 dark:text-white">
                    <div class="flex items-center gap-1.5">
                      <UIcon
                        :name="hasPreview(getVersionNumber(v)) ? 'i-lucide-chevron-down' : 'i-lucide-chevron-right'"
                        class="size-3.5 text-gray-400 shrink-0"
                      />
                      v{{ getDisplayVersion(v) }}
                    </div>
                  </td>
                  <td class="py-2.5 px-4">
                    <div
                      class="flex items-center gap-1"
                      @click.stop
                    >
                      <span class="font-mono text-gray-500 dark:text-gray-400 text-xs">{{ v.id }}</span>
                      <UButton
                        :icon="copiedId === `version-${v.id}` ? 'i-lucide-check' : 'i-lucide-copy'"
                        variant="ghost"
                        color="neutral"
                        size="xs"
                        class="size-5 cursor-pointer"
                        @click.stop="copyId(`version-${v.id}`, v.id)"
                      />
                    </div>
                  </td>
                  <td
                    v-if="isRaw"
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
                    v-if="!isRaw"
                    class="py-2.5 px-4 text-gray-500 dark:text-gray-400"
                  >
                    #{{ (v as LineageResponse).from_resource_id }}
                  </td>
                  <td class="py-2.5 px-4 text-gray-500 dark:text-gray-400">
                    {{ new Date(v.created_at).toLocaleDateString() }}
                  </td>
                  <td class="py-2.5 px-4 text-right">
                    <div
                      class="flex justify-end gap-1"
                      @click.stop
                    >
                      <UButton
                        v-if="isRaw && getStatus(v) !== 'active'"
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
                        icon="i-lucide-table-2"
                        variant="ghost"
                        color="neutral"
                        size="xs"
                        :loading="isPreviewLoading(getVersionNumber(v))"
                        @click="togglePreview(getVersionNumber(v))"
                      />
                      <UButton
                        v-if="isRaw"
                        icon="i-lucide-trash-2"
                        variant="ghost"
                        color="error"
                        size="xs"
                        @click="deleteVersion(getVersionNumber(v))"
                      />
                    </div>
                  </td>
                </tr>
                <!-- Inline schema preview (bronze/silver/gold) -->
                <tr
                  v-if="hasSchema && schemaMap.has(getVersionNumber(v))"
                  class="border-b border-gray-100 dark:border-gray-800"
                >
                  <td
                    :colspan="isRaw ? 6 : 6"
                    class="p-4"
                  >
                    <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                      <div class="overflow-x-auto">
                        <table class="text-sm min-w-max">
                          <thead>
                            <tr class="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                              <th
                                v-for="col in getSchemaColumns(schemaMap.get(getVersionNumber(v))!)"
                                :key="col"
                                class="text-left py-2.5 px-4 font-medium text-xs border-r border-gray-200 dark:border-gray-700"
                              >
                                <div class="text-gray-900 dark:text-white whitespace-nowrap">
                                  {{ col }}
                                </div>
                                <div class="text-gray-400 font-normal whitespace-nowrap">
                                  {{ schemaMap.get(getVersionNumber(v))!.data_schema[col] }}
                                </div>
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr
                              v-for="(row, i) in getSchemaRows(schemaMap.get(getVersionNumber(v))!)"
                              :key="i"
                              class="border-b border-gray-200 dark:border-gray-700 last:border-0"
                            >
                              <td
                                v-for="col in getSchemaColumns(schemaMap.get(getVersionNumber(v))!)"
                                :key="col"
                                class="py-2 px-4 text-gray-700 dark:text-gray-300 font-mono text-xs whitespace-nowrap border-r border-gray-200 dark:border-gray-700"
                              >
                                {{ formatCell(row[col]) }}
                              </td>
                            </tr>
                            <tr v-if="getSchemaRows(schemaMap.get(getVersionNumber(v))!).length === 0">
                              <td
                                :colspan="getSchemaColumns(schemaMap.get(getVersionNumber(v))!).length"
                                class="py-3 px-4 text-center text-gray-400 text-xs"
                              >
                                No data rows available.
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>
                  </td>
                </tr>
                <!-- Inline raw file preview -->
                <tr
                  v-if="isRaw && rawPreviewMap.has(getVersionNumber(v))"
                  class="border-b border-gray-100 dark:border-gray-800"
                >
                  <td
                    colspan="6"
                    class="p-4"
                  >
                    <div class="bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
                      <!-- Table preview for tabular raw data -->
                      <template v-if="rawPreviewMap.get(getVersionNumber(v))!.type === 'table'">
                        <div class="overflow-x-auto">
                          <table class="text-sm min-w-max">
                            <thead>
                              <tr class="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-900">
                                <th
                                  v-for="col in rawPreviewMap.get(getVersionNumber(v))!.columns"
                                  :key="col"
                                  class="text-left py-2.5 px-4 font-medium text-xs border-r border-gray-200 dark:border-gray-700 text-gray-900 dark:text-white whitespace-nowrap"
                                >
                                  {{ col }}
                                </th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr
                                v-for="(row, i) in rawPreviewMap.get(getVersionNumber(v))!.rows"
                                :key="i"
                                class="border-b border-gray-200 dark:border-gray-700 last:border-0"
                              >
                                <td
                                  v-for="col in rawPreviewMap.get(getVersionNumber(v))!.columns"
                                  :key="col"
                                  class="py-2 px-4 text-gray-700 dark:text-gray-300 font-mono text-xs whitespace-nowrap border-r border-gray-200 dark:border-gray-700"
                                >
                                  {{ formatCell(row[col]) }}
                                </td>
                              </tr>
                              <tr v-if="rawPreviewMap.get(getVersionNumber(v))!.rows?.length === 0">
                                <td
                                  :colspan="rawPreviewMap.get(getVersionNumber(v))!.columns?.length"
                                  class="py-3 px-4 text-center text-gray-400 text-xs"
                                >
                                  No data rows available.
                                </td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </template>
                      <!-- Text preview for non-tabular / malformed raw data -->
                      <template v-else>
                        <pre class="p-4 text-xs text-gray-700 dark:text-gray-300 font-mono whitespace-pre-wrap break-all overflow-x-auto max-h-80">{{ rawPreviewMap.get(getVersionNumber(v))!.text }}</pre>
                      </template>
                    </div>
                  </td>
                </tr>
              </template>
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

    <!-- Edit Modal -->
    <UModal
      v-model:open="showRenameModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Edit Resource
          </h2>
          <UInput
            v-model="renameName"
            placeholder="Name"
            color="neutral"
            class="mb-3 w-full"
          />
          <UTextarea
            v-model="renameDescription"
            placeholder="Description (optional)"
            color="neutral"
            class="mb-4 w-full"
            :rows="3"
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
