import { describe, it, expect } from 'vitest'
import {
  SilverLineageResponseFromJSON,
  instanceOfSilverLineageResponse
} from '~/utils/api/models/SilverLineageResponse'
import {
  GoldLineageResponseFromJSON,
  instanceOfGoldLineageResponse
} from '~/utils/api/models/GoldLineageResponse'
import {
  instanceOfSilverMetadataResponse
} from '~/utils/api/models/SilverMetadataResponse'
import {
  instanceOfGoldMetadataResponse
} from '~/utils/api/models/GoldMetadataResponse'

describe('SilverLineageResponse', () => {
  const valid = {
    id: 1,
    resource_id: 2,
    delta_version: 0,
    from_resource_id: 5,
    created_at: '2025-06-01T00:00:00Z'
  }

  it('deserializes from JSON', () => {
    expect(SilverLineageResponseFromJSON(valid)).toEqual(valid)
  })

  it('returns null for null input', () => {
    expect(SilverLineageResponseFromJSON(null)).toBeNull()
  })

  it('validates correct object', () => {
    expect(instanceOfSilverLineageResponse(valid)).toBe(true)
  })

  it('rejects object missing delta_version', () => {
    const { delta_version, ...partial } = valid
    expect(instanceOfSilverLineageResponse(partial)).toBe(false)
  })

  it('rejects object missing from_resource_id', () => {
    const { from_resource_id, ...partial } = valid
    expect(instanceOfSilverLineageResponse(partial)).toBe(false)
  })
})

describe('GoldLineageResponse', () => {
  const valid = {
    id: 1,
    resource_id: 3,
    delta_version: 1,
    from_resource_id: 2,
    created_at: '2025-06-01T00:00:00Z'
  }

  it('deserializes from JSON', () => {
    expect(GoldLineageResponseFromJSON(valid)).toEqual(valid)
  })

  it('returns null for null input', () => {
    expect(GoldLineageResponseFromJSON(null)).toBeNull()
  })

  it('validates correct object', () => {
    expect(instanceOfGoldLineageResponse(valid)).toBe(true)
  })

  it('rejects object missing delta_version', () => {
    const { delta_version, ...partial } = valid
    expect(instanceOfGoldLineageResponse(partial)).toBe(false)
  })

  it('rejects object missing from_resource_id', () => {
    const { from_resource_id, ...partial } = valid
    expect(instanceOfGoldLineageResponse(partial)).toBe(false)
  })
})

describe('SilverMetadataResponse', () => {
  it('validates correct object', () => {
    expect(instanceOfSilverMetadataResponse({ id: 1, name: 'x', description: null, project_id: 1, created_at: 'y' })).toBe(true)
  })

  it('rejects incomplete object', () => {
    expect(instanceOfSilverMetadataResponse({ id: 1 })).toBe(false)
  })
})

describe('GoldMetadataResponse', () => {
  it('validates correct object', () => {
    expect(instanceOfGoldMetadataResponse({ id: 1, name: 'x', description: null, project_id: 1, created_at: 'y' })).toBe(true)
  })

  it('rejects incomplete object', () => {
    expect(instanceOfGoldMetadataResponse({ name: 'x' })).toBe(false)
  })
})
