import {
  APIEndpointsForInteractingWithTheBronzeLayerApi,
  APIEndpointsForInteractingWithTheSilverLayerApi,
  APIEndpointsForInteractingWithTheGoldLayerApi,
  Configuration
} from '~/utils/api'

export function useApi() {
  const config = new Configuration({ basePath: '/api' })
  const bronze = new APIEndpointsForInteractingWithTheBronzeLayerApi(config)
  const silver = new APIEndpointsForInteractingWithTheSilverLayerApi(config)
  const gold = new APIEndpointsForInteractingWithTheGoldLayerApi(config)

  return { bronze, silver, gold }
}
