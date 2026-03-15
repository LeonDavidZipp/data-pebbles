import type { ProjectResponse } from '~/utils/api'

export function useCurrentProject() {
  const currentProject = useState<ProjectResponse | null>('currentProject', () => null)

  function selectProject(project: ProjectResponse) {
    currentProject.value = project
  }

  function clearProject() {
    currentProject.value = null
  }

  return { currentProject, selectProject, clearProject }
}
