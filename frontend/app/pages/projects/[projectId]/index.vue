<script setup lang="ts">
import type {
  ProjectResponse,
  MetadataResponse
} from '~/utils/api'

const route = useRoute()
const { projects, raw, bronze, silver, gold } = useApi()
const { copiedId, copyId } = useCopyId()

const projectId = computed(() => Number(route.params.projectId))

const project = ref<ProjectResponse | null>(null)
const resources = ref<MetadataResponse[]>([])
const activeTab = ref('raw')
const loading = ref(true)
const resourcesLoading = ref(false)

const showCreateModal = ref(false)
const newResourceName = ref('')
const newResourceDescription = ref('')
const creating = ref(false)

const showRenameModal = ref(false)
const renameName = ref('')
const renameDescription = ref('')
const renaming = ref(false)

const tabs = [
  { label: 'Raw', value: 'raw', icon: 'i-lucide-file-text' },
  { label: 'Bronze', value: 'bronze', icon: 'i-lucide-hard-drive' },
  { label: 'Silver', value: 'silver', icon: 'i-lucide-database' },
  { label: 'Gold', value: 'gold', icon: 'i-lucide-crown' }
]

async function fetchProject() {
  project.value = await projects.getProjectProjectsProjectIdGet({ projectId: projectId.value })
}

async function fetchResources() {
  resourcesLoading.value = true
  try {
    let all: MetadataResponse[]
    if (activeTab.value === 'raw') {
      all = await raw.listResourcesRawGet()
    } else if (activeTab.value === 'bronze') {
      all = await bronze.listResourcesBronzeGet()
    } else if (activeTab.value === 'silver') {
      all = await silver.listResourcesSilverGet()
    } else {
      all = await gold.listResourcesGoldGet()
    }
    resources.value = all.filter(r => r.project_id === projectId.value)
    resources.value.sort((a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime())
  } finally {
    resourcesLoading.value = false
  }
}

async function createResource() {
  if (!newResourceName.value.trim()) return
  creating.value = true
  try {
    if (activeTab.value === 'raw') {
      await raw.createResourceRawPost({
        createResourceRequest: {
          name: newResourceName.value,
          project_id: projectId.value,
          description: newResourceDescription.value || undefined
        }
      })
    } else if (activeTab.value === 'bronze') {
      await bronze.createResourceBronzePost({
        createResourceRequest: {
          name: newResourceName.value,
          project_id: projectId.value,
          description: newResourceDescription.value || undefined
        }
      })
    } else if (activeTab.value === 'silver') {
      await silver.createResourceSilverPost({
        createResourceRequest: {
          name: newResourceName.value,
          project_id: projectId.value,
          description: newResourceDescription.value || undefined
        }
      })
    } else {
      await gold.createResourceGoldPost({
        createResourceRequest: {
          name: newResourceName.value,
          project_id: projectId.value,
          description: newResourceDescription.value || undefined
        }
      })
    }
    newResourceName.value = ''
    newResourceDescription.value = ''
    showCreateModal.value = false
    await fetchResources()
  } finally {
    creating.value = false
  }
}

async function deleteResource(id: number) {
  if (activeTab.value === 'raw') {
    await raw.deleteResourceRawResourceIdDelete({ resourceId: id })
  } else if (activeTab.value === 'bronze') {
    await bronze.deleteResourceBronzeResourceIdDelete({ resourceId: id })
  } else if (activeTab.value === 'silver') {
    await silver.deleteResourceSilverResourceIdDelete({ resourceId: id })
  } else {
    await gold.deleteResourceGoldResourceIdDelete({ resourceId: id })
  }
  await fetchResources()
}

const layerButtonClass = computed(() => {
  switch (activeTab.value) {
    case 'raw': return 'bg-blue-600 hover:bg-blue-700 text-white'
    case 'silver': return 'bg-gray-400 hover:bg-gray-500 text-white'
    case 'gold': return 'bg-yellow-500 hover:bg-yellow-600 text-white'
    default: return 'bg-amber-700 hover:bg-amber-800 text-white'
  }
})

const layerIconClass = computed(() => {
  switch (activeTab.value) {
    case 'raw': return 'bg-blue-600/10 text-blue-600'
    case 'silver': return 'bg-gray-400/10 text-gray-400'
    case 'gold': return 'bg-yellow-500/10 text-yellow-500'
    default: return 'bg-amber-700/10 text-amber-700'
  }
})

async function renameProject() {
  if (!renameName.value.trim()) return
  renaming.value = true
  try {
    project.value = await projects.updateProjectProjectsProjectIdPatch({
      projectId: projectId.value,
      updateProjectRequest: {
        name: renameName.value,
        description: renameDescription.value || null
      }
    })
    showRenameModal.value = false
  } finally {
    renaming.value = false
  }
}

function openRename() {
  renameName.value = project.value?.name ?? ''
  renameDescription.value = project.value?.description ?? ''
  showRenameModal.value = true
}

watch(activeTab, fetchResources)

async function init() {
  loading.value = true
  try {
    await fetchProject()
    await fetchResources()
  } finally {
    loading.value = false
  }
}

init()
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header bar -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4 flex items-center justify-between">
      <div>
        <div class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 mb-1">
          <NuxtLink
            to="/projects"
            class="hover:text-gray-900 dark:hover:text-white transition-colors"
          >
            Projects
          </NuxtLink>
          <span>/</span>
          <span class="text-gray-900 dark:text-white">{{ project?.name ?? '...' }}</span>
        </div>
        <div class="flex items-center gap-3">
          <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
            {{ project?.name ?? '...' }}
          </h1>
          <div
            v-if="project"
            class="flex items-center gap-0.5 text-xs text-gray-400"
          >
            <span class="font-mono">ID: {{ project.id }}</span>
            <UButton
              :icon="copiedId === `project-${project.id}` ? 'i-lucide-check' : 'i-lucide-copy'"
              variant="ghost"
              color="neutral"
              size="xs"
              class="size-5 cursor-pointer"
              @click="copyId(`project-${project.id}`, project.id)"
            />
          </div>
        </div>
        <p
          v-if="project?.description"
          class="text-sm text-gray-500 dark:text-gray-400 mt-0.5"
        >
          {{ project.description }}
        </p>
      </div>
      <div class="flex items-center gap-2">
        <UButton
          icon="i-lucide-pencil"
          label="Edit"
          variant="outline"
          color="neutral"
          size="sm"
          @click="openRename"
        />
        <UButton
          icon="i-lucide-plus"
          label="New Resource"
          color="neutral"
          :class="layerButtonClass"
          @click="showCreateModal = true"
        />
      </div>
    </div>

    <!-- Layer tabs -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6">
      <nav class="flex gap-6">
        <button
          v-for="tab in tabs"
          :key="tab.value"
          class="flex items-center gap-1.5 py-3 text-sm font-medium border-b-2 transition-colors -mb-px"
          :class="
            activeTab === tab.value
              ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400'
              : 'border-transparent text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:border-gray-300 dark:hover:border-gray-600'
          "
          @click="activeTab = tab.value"
        >
          <UIcon
            :name="tab.icon"
            class="size-4"
          />
          {{ tab.label }}
        </button>
      </nav>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-auto p-6 bg-gray-50 dark:bg-gray-950">
      <div
        v-if="loading || resourcesLoading"
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
          No {{ activeTab }} resources yet. Create one to get started.
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
                ID
              </th>
              <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                Name
              </th>
              <th class="text-left py-2.5 px-4 font-medium text-gray-500 dark:text-gray-400 text-xs uppercase tracking-wider">
                Description
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
              @click="navigateTo(`/projects/${projectId}/${activeTab}/${resource.id}`)"
            >
              <td class="py-3 px-4">
                <div
                  class="flex items-center gap-1"
                  @click.stop
                >
                  <span class="font-mono text-gray-500 dark:text-gray-400 text-xs">{{ resource.id }}</span>
                  <UButton
                    :icon="copiedId === `resource-${resource.id}` ? 'i-lucide-check' : 'i-lucide-copy'"
                    variant="ghost"
                    color="neutral"
                    size="xs"
                    class="size-5 cursor-pointer"
                    @click="copyId(`resource-${resource.id}`, resource.id)"
                  />
                </div>
              </td>
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
                {{ resource.description || '—' }}
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
                    @click="navigateTo(`/projects/${projectId}/${activeTab}/${resource.id}`)"
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

    <!-- Edit Modal -->
    <UModal
      v-model:open="showRenameModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Edit Project
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
              @click="renameProject"
            />
          </div>
        </div>
      </template>
    </UModal>

    <UModal
      v-model:open="showCreateModal"
      class="max-w-sm"
    >
      <template #content>
        <div class="p-6">
          <h2 class="text-lg font-semibold mb-4">
            Create {{ activeTab }} resource
          </h2>
          <UInput
            v-model="newResourceName"
            placeholder="Resource name"
            color="neutral"
            class="mb-3 w-full"
            @keyup.enter="createResource"
          />
          <UInput
            v-model="newResourceDescription"
            placeholder="Description (optional)"
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
