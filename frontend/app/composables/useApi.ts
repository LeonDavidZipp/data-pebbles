import {
  APIEndpointsForInteractingWithTheBronzeLayerApi,
  APIEndpointsForInteractingWithTheSilverLayerApi,
  APIEndpointsForInteractingWithTheGoldLayerApi,
  APIEndpointsForManagingProjectsApi,
  Configuration
} from '~/utils/api'

export function useApi() {
  const config = new Configuration({ basePath: '/api' })
  const projects = new APIEndpointsForManagingProjectsApi(config)
  const bronze = new APIEndpointsForInteractingWithTheBronzeLayerApi(config)
  const silver = new APIEndpointsForInteractingWithTheSilverLayerApi(config)
  const gold = new APIEndpointsForInteractingWithTheGoldLayerApi(config)

  return { projects, bronze, silver, gold }
}
