<script setup lang="ts">
import type { ProjectResponse } from '~/utils/api'

const { projects } = useApi()

const projectList = ref<ProjectResponse[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const newProjectName = ref('')
const newProjectDescription = ref('')
const creating = ref(false)

async function fetchProjects() {
  loading.value = true
  try {
    projectList.value = await projects.listProjectsProjectsGet()
  } finally {
    loading.value = false
  }
}

async function createProject() {
  if (!newProjectName.value.trim()) return
  creating.value = true
  try {
    await projects.createProjectProjectsPost({
      createProjectRequest: {
        name: newProjectName.value,
        description: newProjectDescription.value || undefined
      }
    })
    newProjectName.value = ''
    newProjectDescription.value = ''
    showCreateModal.value = false
    await fetchProjects()
  } finally {
    creating.value = false
  }
}

async function deleteProject(id: number) {
  await projects.deleteProjectProjectsProjectIdDelete({ projectId: id })
  await fetchProjects()
}

fetchProjects()
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header bar -->
    <div class="border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 px-6 py-4 flex items-center justify-between">
      <div>
        <div class="flex items-center gap-1.5 text-xs text-gray-500 dark:text-gray-400 mb-1">
          <span>Projects</span>
        </div>
        <h1 class="text-xl font-semibold text-gray-900 dark:text-white">
          Projects
        </h1>
      </div>
      <UButton
        icon="i-lucide-plus"
        label="New Project"
        color="neutral"
        class="bg-indigo-600 hover:bg-indigo-700 text-white"
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
        v-else-if="projectList.length === 0"
        class="text-center py-16 text-gray-500 dark:text-gray-400"
      >
        <UIcon
          name="i-lucide-folder-kanban"
          class="size-12 mx-auto mb-3 text-gray-300 dark:text-gray-600"
        />
        <p class="text-sm">
          No projects yet. Create one to get started.
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
              v-for="project in projectList"
              :key="project.id"
              class="border-b border-gray-100 dark:border-gray-800 last:border-0 hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors cursor-pointer"
              @click="navigateTo(`/projects/${project.id}`)"
            >
              <td class="py-3 px-4">
                <div class="flex items-center gap-2.5">
                  <div class="size-8 rounded flex items-center justify-center bg-indigo-500/10 text-indigo-500">
                    <UIcon
                      name="i-lucide-folder-kanban"
                      class="size-4"
                    />
                  </div>
                  <span class="font-medium text-gray-900 dark:text-white">{{ project.name }}</span>
                </div>
              </td>
              <td class="py-3 px-4 text-gray-500 dark:text-gray-400">
                {{ project.description || '—' }}
              </td>
              <td class="py-3 px-4 text-gray-500 dark:text-gray-400">
                {{ new Date(project.created_at).toLocaleDateString() }}
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
                    @click="navigateTo(`/projects/${project.id}`)"
                  />
                  <UButton
                    icon="i-lucide-trash-2"
                    variant="ghost"
                    color="error"
                    size="xs"
                    @click="deleteProject(project.id)"
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
            Create Project
          </h2>
          <UInput
            v-model="newProjectName"
            placeholder="Project name"
            color="neutral"
            class="mb-3 w-full"
            @keyup.enter="createProject"
          />
          <UInput
            v-model="newProjectDescription"
            placeholder="Description (optional)"
            color="neutral"
            class="mb-4 w-full"
            @keyup.enter="createProject"
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
              @click="createProject"
            />
          </div>
        </div>
      </template>
    </UModal>
  </div>
</template>
