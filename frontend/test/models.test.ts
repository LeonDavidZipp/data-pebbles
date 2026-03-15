import { describe, it, expect } from 'vitest'
import {
  MetadataResponseFromJSON,
  MetadataResponseToJSON,
  instanceOfMetadataResponse
} from '~/utils/api/models/MetadataResponse'
import {
  VersionResponseFromJSON,
  VersionResponseToJSON,
  instanceOfVersionResponse
} from '~/utils/api/models/VersionResponse'

describe('MetadataResponse', () => {
  const validJson = { id: 1, name: 'test_resource', created_at: '2025-01-01T00:00:00Z' }

  it('deserializes from JSON', () => {
    const result = MetadataResponseFromJSON(validJson)
    expect(result).toEqual(validJson)
  })

  it('serializes to JSON', () => {
    const result = MetadataResponseToJSON(validJson)
    expect(result).toEqual(validJson)
  })

  it('returns null for null input', () => {
    expect(MetadataResponseFromJSON(null)).toBeNull()
  })

  it('validates correct object', () => {
    expect(instanceOfMetadataResponse(validJson)).toBe(true)
  })

  it('rejects object missing id', () => {
    expect(instanceOfMetadataResponse({ name: 'x', created_at: 'y' })).toBe(false)
  })

  it('rejects object missing name', () => {
    expect(instanceOfMetadataResponse({ id: 1, created_at: 'y' })).toBe(false)
  })

  it('rejects object missing created_at', () => {
    expect(instanceOfMetadataResponse({ id: 1, name: 'x' })).toBe(false)
  })
})

describe('VersionResponse', () => {
  const validJson = {
    id: 1,
    resource_id: 10,
    version: 3,
    status: 'active',
    s3_key: 'bronze/10/3.csv',
    created_at: '2025-01-01T00:00:00Z',
    updated_at: '2025-01-02T00:00:00Z'
  }

  it('deserializes from JSON', () => {
    const result = VersionResponseFromJSON(validJson)
    expect(result).toEqual(validJson)
  })

  it('serializes to JSON', () => {
    const result = VersionResponseToJSON(validJson)
    expect(result).toEqual(validJson)
  })

  it('returns null for null input', () => {
    expect(VersionResponseFromJSON(null)).toBeNull()
  })

  it('validates correct object', () => {
    expect(instanceOfVersionResponse(validJson)).toBe(true)
  })

  it('rejects object missing resource_id', () => {
    const { resource_id, ...partial } = validJson
    expect(instanceOfVersionResponse(partial)).toBe(false)
  })

  it('rejects object missing version', () => {
    const { version, ...partial } = validJson
    expect(instanceOfVersionResponse(partial)).toBe(false)
  })

  it('rejects object missing status', () => {
    const { status, ...partial } = validJson
    expect(instanceOfVersionResponse(partial)).toBe(false)
  })

  it('rejects object missing s3_key', () => {
    const { s3_key, ...partial } = validJson
    expect(instanceOfVersionResponse(partial)).toBe(false)
  })
})
