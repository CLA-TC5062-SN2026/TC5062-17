import { api } from '@/services/api'

export function iniciarSesionRequest(credenciales) {
  return api.post('/sesiones', credenciales)
}

export function registrarUsuarioRequest(datos) {
  return api.post('/usuarios', datos)
}

export function cerrarSesionRequest() {
  return api.post('/auth/logout')
}

export function obtenerUsuarioActualRequest() {
  return api.get('/usuarios/me')
}
