import { api } from '@/services/api'

export function crearBorradorRequest(payload) {
  return api.post('/borradores', payload)
}

export function calcularEstimacionRequest(borradorId, idempotencyKey) {
  return api.post(
    '/estimaciones',
    { borradorId },
    { headers: { 'Idempotency-Key': idempotencyKey } },
  )
}

export function obtenerEstimacionRequest(estimacionId) {
  return api.get(`/estimaciones/${estimacionId}`)
}

export function obtenerComparablesRequest(estimacionId) {
  return api.get(`/estimaciones/${estimacionId}/comparables`)
}

export function listarHistorialRequest(filtros = {}) {
  return api.get('/estimaciones-guardadas', { query: filtros })
}

export function obtenerHistorialDetalleRequest(estimacionId) {
  return api.get(`/estimaciones-guardadas/${estimacionId}`)
}

export function eliminarEstimacionRequest(estimacionId) {
  return api.delete(`/estimaciones-guardadas/${estimacionId}`)
}

export function generarReportePdfRequest(estimacionId) {
  return api.put(`/estimaciones/${estimacionId}/reportes/principal`, undefined, {
    responseType: 'blob',
  })
}
