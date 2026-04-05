import {
  RawApi,
  BronzeApi,
  SilverApi,
  GoldApi,
  ProjectsApi,
  Configuration
} from '~/utils/api'

export function useApi() {
  const config = new Configuration({ basePath: '/api' })
  const projects = new ProjectsApi(config)
  const raw = new RawApi(config)
  const bronze = new BronzeApi(config)
  const silver = new SilverApi(config)
  const gold = new GoldApi(config)

  return { projects, raw, bronze, silver, gold }
}
