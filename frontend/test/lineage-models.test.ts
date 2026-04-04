import { describe, it, expect } from 'vitest'
import {
  LineageResponseFromJSON,
  instanceOfLineageResponse
} from '~/utils/api/models/LineageResponse'
import {
  instanceOfMetadataResponse
} from '~/utils/api/models/MetadataResponse'

describe('LineageResponse', () => {
  const valid = {
    id: 1,
    resource_id: 2,
    delta_version: 0,
    from_resource_id: 5,
    created_at: '2025-06-01T00:00:00Z'
  }

  it('deserializes from JSON', () => {
    expect(LineageResponseFromJSON(valid)).toEqual(valid)
  })

  it('returns null for null input', () => {
    expect(LineageResponseFromJSON(null)).toBeNull()
  })

  it('validates correct object', () => {
    expect(instanceOfLineageResponse(valid)).toBe(true)
  })

  it('rejects object missing delta_version', () => {
    const { delta_version, ...partial } = valid
    expect(instanceOfLineageResponse(partial)).toBe(false)
  })

  it('rejects object missing from_resource_id', () => {
    const { from_resource_id, ...partial } = valid
    expect(instanceOfLineageResponse(partial)).toBe(false)
  })
})

describe('MetadataResponse', () => {
  it('validates correct object', () => {
    expect(instanceOfMetadataResponse({ id: 1, name: 'x', description: null, project_id: 1, created_at: 'y' })).toBe(true)
  })

  it('rejects incomplete object', () => {
    expect(instanceOfMetadataResponse({ id: 1 })).toBe(false)
  })
})
