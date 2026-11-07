import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import { setAccessToken, setUnauthorizedHandler } from '@/services/api'
import { cerrarSesionRequest, iniciarSesionRequest } from '@/services/auth'

export const useSessionStore = defineStore('session', () => {
  const token = ref(null)
  const usuario = ref(null)
  const cargando = ref(false)
  const error = ref(null)

  const estaAutenticado = computed(() => Boolean(token.value && usuario.value))

  function aplicarSesion(payload) {
    const nuevoToken = payload?.accessToken ?? payload?.access_token ?? payload?.token ?? null
    token.value = nuevoToken
    usuario.value = payload?.usuario ?? payload?.user ?? null
    setAccessToken(nuevoToken)
  }

  function limpiarSesion() {
    token.value = null
    usuario.value = null
    setAccessToken(null)
  }

  async function iniciarSesion(credenciales) {
    cargando.value = true
    error.value = null
    try {
      const payload = await iniciarSesionRequest(credenciales)
      aplicarSesion(payload)
      return payload
    } catch (err) {
      error.value = err
      throw err
    } finally {
      cargando.value = false
    }
  }

  async function cerrarSesion() {
    try {
      await cerrarSesionRequest()
    } finally {
      limpiarSesion()
    }
  }

  setUnauthorizedHandler(limpiarSesion)

  return {
    token,
    usuario,
    cargando,
    error,
    estaAutenticado,
    iniciarSesion,
    cerrarSesion,
    limpiarSesion,
  }
})
