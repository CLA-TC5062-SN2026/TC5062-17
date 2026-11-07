import { describe, expect, it } from 'vitest'
import { formatearFecha, formatearMoneda } from '@/utils/formatters'

describe('formatearMoneda', () => {
  it('formatea un monto en MXN sin decimales', () => {
    expect(formatearMoneda(4000000)).toContain('4,000,000')
  })

  it('devuelve un guion para valores ausentes', () => {
    expect(formatearMoneda(null)).toBe('—')
    expect(formatearMoneda(undefined)).toBe('—')
  })
})

describe('formatearFecha', () => {
  it('conserva el formato AAAA-MM-DD', () => {
    expect(formatearFecha('2026-09-25T00:00:00Z')).toBe('2026-09-25')
    expect(formatearFecha('2026-09-25')).toBe('2026-09-25')
  })

  it('devuelve un guion para valores ausentes', () => {
    expect(formatearFecha(null)).toBe('—')
    expect(formatearFecha('')).toBe('—')
  })
})
