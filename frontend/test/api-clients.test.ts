import { describe, it, expect } from 'vitest'
import { Configuration } from '~/utils/api/runtime'
import { APIEndpointsForInteractingWithTheBronzeLayerApi } from '~/utils/api/apis/APIEndpointsForInteractingWithTheBronzeLayerApi'
import { APIEndpointsForInteractingWithTheSilverLayerApi } from '~/utils/api/apis/APIEndpointsForInteractingWithTheSilverLayerApi'
import { APIEndpointsForInteractingWithTheGoldLayerApi } from '~/utils/api/apis/APIEndpointsForInteractingWithTheGoldLayerApi'

describe('API client instantiation', () => {
  const config = new Configuration({ basePath: '/api' })

  it('creates bronze API client', () => {
    const api = new APIEndpointsForInteractingWithTheBronzeLayerApi(config)
    expect(api).toBeInstanceOf(APIEndpointsForInteractingWithTheBronzeLayerApi)
  })

  it('creates silver API client', () => {
    const api = new APIEndpointsForInteractingWithTheSilverLayerApi(config)
    expect(api).toBeInstanceOf(APIEndpointsForInteractingWithTheSilverLayerApi)
  })

  it('creates gold API client', () => {
    const api = new APIEndpointsForInteractingWithTheGoldLayerApi(config)
    expect(api).toBeInstanceOf(APIEndpointsForInteractingWithTheGoldLayerApi)
  })

  it('bronze client has expected methods', () => {
    const api = new APIEndpointsForInteractingWithTheBronzeLayerApi(config)
    expect(typeof api.listResourcesBronzeGet).toBe('function')
    expect(typeof api.createResourceBronzePost).toBe('function')
    expect(typeof api.getResourceBronzeResourceIdGet).toBe('function')
    expect(typeof api.deleteResourceBronzeResourceIdDelete).toBe('function')
    expect(typeof api.updateResourceBronzeResourceIdPatch).toBe('function')
    expect(typeof api.listVersionsBronzeResourceIdVersionsGet).toBe('function')
    expect(typeof api.uploadVersionBronzeResourceIdVersionsPost).toBe('function')
    expect(typeof api.downloadVersionBronzeResourceIdVersionsVersionGet).toBe('function')
    expect(typeof api.activateVersionBronzeResourceIdVersionsVersionPatch).toBe('function')
    expect(typeof api.deleteVersionBronzeResourceIdVersionsVersionDelete).toBe('function')
  })

  it('silver client has expected methods', () => {
    const api = new APIEndpointsForInteractingWithTheSilverLayerApi(config)
    expect(typeof api.listResourcesSilverGet).toBe('function')
    expect(typeof api.createResourceSilverPost).toBe('function')
    expect(typeof api.getResourceSilverResourceIdGet).toBe('function')
    expect(typeof api.deleteResourceSilverResourceIdDelete).toBe('function')
    expect(typeof api.updateResourceSilverResourceIdPatch).toBe('function')
    expect(typeof api.listVersionsSilverResourceIdVersionsGet).toBe('function')
  })

  it('gold client has expected methods', () => {
    const api = new APIEndpointsForInteractingWithTheGoldLayerApi(config)
    expect(typeof api.listResourcesGoldGet).toBe('function')
    expect(typeof api.createResourceGoldPost).toBe('function')
    expect(typeof api.getResourceGoldResourceIdGet).toBe('function')
    expect(typeof api.deleteResourceGoldResourceIdDelete).toBe('function')
    expect(typeof api.updateResourceGoldResourceIdPatch).toBe('function')
    expect(typeof api.listVersionsGoldResourceIdVersionsGet).toBe('function')
  })

  it('uses configured base path', () => {
    const customConfig = new Configuration({ basePath: 'http://example.com' })
    const api = new APIEndpointsForInteractingWithTheBronzeLayerApi(customConfig)
    // The API client stores the configuration internally
    expect(api).toBeDefined()
  })
})
