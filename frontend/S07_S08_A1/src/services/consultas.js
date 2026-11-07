import { api } from '@/services/api'

export function obtenerConsultaAnonimaRequest(consultaId) {
  return api.get(`/consultas/${consultaId}`)
}
