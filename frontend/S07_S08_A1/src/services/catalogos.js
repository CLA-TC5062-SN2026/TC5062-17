import { api } from '@/services/api'

export function obtenerCatalogosRequest() {
  return api.get('/catalogos')
}

export function evaluarElegibilidadRequest(payload) {
  return api.post('/evaluaciones-elegibilidad', payload)
}
