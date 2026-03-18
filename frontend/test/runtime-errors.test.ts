import { describe, it, expect } from 'vitest'
import {
  ResponseError,
  FetchError,
  RequiredError,
  querystring
} from '~/utils/api/runtime'

describe('ResponseError', () => {
  it('has correct name', () => {
    const response = new Response('', { status: 404 })
    const err = new ResponseError(response, 'Not found')
    expect(err.name).toBe('ResponseError')
    expect(err.message).toBe('Not found')
    expect(err.response).toBe(response)
  })

  it('is instanceof Error', () => {
    const response = new Response('', { status: 500 })
    const err = new ResponseError(response)
    expect(err).toBeInstanceOf(Error)
  })
})

describe('FetchError', () => {
  it('has correct name', () => {
    const cause = new Error('network failure')
    const err = new FetchError(cause, 'Failed to fetch')
    expect(err.name).toBe('FetchError')
    expect(err.message).toBe('Failed to fetch')
    expect(err.cause).toBe(cause)
  })
})

describe('RequiredError', () => {
  it('has correct name and field', () => {
    const err = new RequiredError('resourceId', 'resourceId is required')
    expect(err.name).toBe('RequiredError')
    expect(err.field).toBe('resourceId')
    expect(err.message).toBe('resourceId is required')
  })
})

describe('querystring', () => {
  it('encodes simple params', () => {
    const result = querystring({ foo: 'bar', num: 42 })
    expect(result).toContain('foo=bar')
    expect(result).toContain('num=42')
  })

  it('encodes array params', () => {
    const result = querystring({ ids: [1, 2, 3] })
    expect(result).toContain('ids=1')
    expect(result).toContain('ids=2')
    expect(result).toContain('ids=3')
  })

  it('returns empty string for empty params', () => {
    expect(querystring({})).toBe('')
  })

  it('encodes special characters', () => {
    const result = querystring({ q: 'hello world' })
    expect(result).toContain('q=hello%20world')
  })

  it('handles boolean values', () => {
    const result = querystring({ active: true })
    expect(result).toContain('active=true')
  })
})
