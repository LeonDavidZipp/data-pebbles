import { describe, it, expect } from 'vitest'
import { Configuration } from '~/utils/api/runtime'
import type { Middleware } from '~/utils/api/runtime'

describe('Configuration', () => {
  it('uses default base path when none provided', () => {
    const config = new Configuration()
    expect(config.basePath).toBe('http://localhost')
  })

  it('uses custom base path when provided', () => {
    const config = new Configuration({ basePath: '/api' })
    expect(config.basePath).toBe('/api')
  })

  it('returns empty middleware array by default', () => {
    const config = new Configuration()
    expect(config.middleware).toEqual([])
  })

  it('returns provided middleware', () => {
    const mw: Middleware = { pre: async () => {}, post: async () => {} }
    const config = new Configuration({ middleware: [mw] })
    expect(config.middleware).toHaveLength(1)
  })

  it('returns provided headers', () => {
    const config = new Configuration({ headers: { Authorization: 'Bearer tok' } })
    expect(config.headers).toEqual({ Authorization: 'Bearer tok' })
  })

  it('returns provided credentials', () => {
    const config = new Configuration({ credentials: 'include' })
    expect(config.credentials).toBe('include')
  })
})
