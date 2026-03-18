import { describe, it, expect } from 'vitest'
import { exists, mapValues, canConsumeForm } from '~/utils/api/runtime'

describe('exists', () => {
  it('returns true when key has a value', () => {
    expect(exists({ foo: 'bar' }, 'foo')).toBe(true)
  })

  it('returns true for falsy values (0, empty string, false)', () => {
    expect(exists({ n: 0 }, 'n')).toBe(true)
    expect(exists({ s: '' }, 's')).toBe(true)
    expect(exists({ b: false }, 'b')).toBe(true)
  })

  it('returns false for null', () => {
    expect(exists({ foo: null }, 'foo')).toBe(false)
  })

  it('returns false for undefined', () => {
    expect(exists({ foo: undefined }, 'foo')).toBe(false)
  })

  it('returns false for missing key', () => {
    expect(exists({}, 'foo')).toBe(false)
  })
})

describe('mapValues', () => {
  it('transforms all values with provided function', () => {
    const result = mapValues({ a: 1, b: 2, c: 3 }, v => v * 2)
    expect(result).toEqual({ a: 2, b: 4, c: 6 })
  })

  it('returns empty object for empty input', () => {
    expect(mapValues({}, v => v)).toEqual({})
  })

  it('preserves keys', () => {
    const result = mapValues({ key: 'value' }, v => v.toUpperCase())
    expect(result).toEqual({ key: 'VALUE' })
  })
})

describe('canConsumeForm', () => {
  it('returns true when multipart/form-data is present', () => {
    expect(canConsumeForm([{ contentType: 'multipart/form-data' }])).toBe(true)
  })

  it('returns true when multipart/form-data is among others', () => {
    expect(
      canConsumeForm([
        { contentType: 'application/json' },
        { contentType: 'multipart/form-data' }
      ])
    ).toBe(true)
  })

  it('returns false when multipart/form-data is not present', () => {
    expect(canConsumeForm([{ contentType: 'application/json' }])).toBe(false)
  })

  it('returns false for empty array', () => {
    expect(canConsumeForm([])).toBe(false)
  })
})
