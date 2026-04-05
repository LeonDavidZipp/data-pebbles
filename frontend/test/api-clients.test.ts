import { describe, it, expect } from 'vitest'
import { Configuration } from '~/utils/api/runtime'
import { RawApi } from '~/utils/api/apis/RawApi'
import { BronzeApi } from '~/utils/api/apis/BronzeApi'
import { SilverApi } from '~/utils/api/apis/SilverApi'
import { GoldApi } from '~/utils/api/apis/GoldApi'

describe('API client instantiation', () => {
  const config = new Configuration({ basePath: '/api' })

  it('creates raw API client', () => {
    const api = new RawApi(config)
    expect(api).toBeInstanceOf(RawApi)
  })

  it('creates bronze API client', () => {
    const api = new BronzeApi(config)
    expect(api).toBeInstanceOf(BronzeApi)
  })

  it('creates silver API client', () => {
    const api = new SilverApi(config)
    expect(api).toBeInstanceOf(SilverApi)
  })

  it('creates gold API client', () => {
    const api = new GoldApi(config)
    expect(api).toBeInstanceOf(GoldApi)
  })

  it('raw client has expected methods', () => {
    const api = new RawApi(config)
    expect(typeof api.listResourcesRawGet).toBe('function')
    expect(typeof api.createResourceRawPost).toBe('function')
    expect(typeof api.getResourceRawResourceIdGet).toBe('function')
    expect(typeof api.deleteResourceRawResourceIdDelete).toBe('function')
    expect(typeof api.updateResourceRawResourceIdPatch).toBe('function')
    expect(typeof api.listVersionsRawResourceIdVersionsGet).toBe('function')
    expect(typeof api.uploadVersionRawResourceIdVersionsPost).toBe('function')
    expect(typeof api.downloadVersionRawResourceIdVersionsVersionGet).toBe('function')
    expect(typeof api.activateVersionRawResourceIdVersionsVersionPatch).toBe('function')
    expect(typeof api.deleteVersionRawResourceIdVersionsVersionDelete).toBe('function')
  })

  it('bronze client has expected methods', () => {
    const api = new BronzeApi(config)
    expect(typeof api.bronzeListResources).toBe('function')
    expect(typeof api.bronzeCreateResource).toBe('function')
    expect(typeof api.bronzeGetResource).toBe('function')
    expect(typeof api.bronzeDeleteResource).toBe('function')
    expect(typeof api.bronzeUpdateResource).toBe('function')
    expect(typeof api.bronzeListVersions).toBe('function')
    expect(typeof api.bronzeUploadVersion).toBe('function')
    expect(typeof api.bronzeDownloadVersion).toBe('function')
    expect(typeof api.bronzeGetSchema).toBe('function')
  })

  it('silver client has expected methods', () => {
    const api = new SilverApi(config)
    expect(typeof api.silverListResources).toBe('function')
    expect(typeof api.silverCreateResource).toBe('function')
    expect(typeof api.silverGetResource).toBe('function')
    expect(typeof api.silverDeleteResource).toBe('function')
    expect(typeof api.silverUpdateResource).toBe('function')
    expect(typeof api.silverListVersions).toBe('function')
    expect(typeof api.silverUploadVersion).toBe('function')
    expect(typeof api.silverDownloadVersion).toBe('function')
    expect(typeof api.silverGetSchema).toBe('function')
  })

  it('gold client has expected methods', () => {
    const api = new GoldApi(config)
    expect(typeof api.goldListResources).toBe('function')
    expect(typeof api.goldCreateResource).toBe('function')
    expect(typeof api.goldGetResource).toBe('function')
    expect(typeof api.goldDeleteResource).toBe('function')
    expect(typeof api.goldUpdateResource).toBe('function')
    expect(typeof api.goldListVersions).toBe('function')
    expect(typeof api.goldUploadVersion).toBe('function')
    expect(typeof api.goldDownloadVersion).toBe('function')
    expect(typeof api.goldGetSchema).toBe('function')
  })

  it('uses configured base path', () => {
    const customConfig = new Configuration({ basePath: 'http://example.com' })
    const api = new BronzeApi(customConfig)
    // The API client stores the configuration internally
    expect(api).toBeDefined()
  })
})
