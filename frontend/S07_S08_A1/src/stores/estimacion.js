import { computed, ref } from 'vue'
import { defineStore } from 'pinia'
import {
  calcularEstimacionRequest,
  crearBorradorRequest,
  generarReportePdfRequest,
  obtenerComparablesRequest,
  obtenerEstimacionRequest,
} from '@/services/estimaciones'

function nuevaClaveIdempotencia() {
  if (globalThis.crypto?.randomUUID) return globalThis.crypto.randomUUID()
  return `idem-${Date.now()}-${Math.random().toString(16).slice(2)}`
}

export const useEstimacionStore = defineStore('estimacion', () => {
  const borrador = ref(null)
  const estimacion = ref(null)
  const comparables = ref(null)
  const cargando = ref(false)
  const error = ref(null)
  const claveIdempotencia = ref(null)
  const esperaAgotada = ref(false)

  const rango = computed(() => {
    if (!estimacion.value) return null
    return {
      minimo: estimacion.value.valorMinimo,
      central: estimacion.value.valorCentral,
      maximo: estimacion.value.valorMaximo,
    }
  })

  function reiniciarClaveIdempotencia() {
    claveIdempotencia.value = nuevaClaveIdempotencia()
    esperaAgotada.value = false
  }

  async function crearBorrador(payload) {
    cargando.value = true
    error.value = null
    try {
      borrador.value = await crearBorradorRequest(payload)
      estimacion.value = null
      comparables.value = null
      reiniciarClaveIdempotencia()
      return borrador.value
    } catch (err) {
      error.value = err
      throw err
    } finally {
      cargando.value = false
    }
  }

  function marcarEsperaAgotada() {
    esperaAgotada.value = true
  }

  async function calcular() {
    if (!borrador.value?.borradorId) {
      throw new Error('No hay borrador para calcular')
    }
    if (!claveIdempotencia.value) reiniciarClaveIdempotencia()

    cargando.value = true
    error.value = null
    esperaAgotada.value = false
    try {
      estimacion.value = await calcularEstimacionRequest(
        borrador.value.borradorId,
        claveIdempotencia.value,
      )
      return estimacion.value
    } catch (err) {
      error.value = err
      throw err
    } finally {
      cargando.value = false
    }
  }

  async function cargarEstimacion(estimacionId) {
    cargando.value = true
    error.value = null
    try {
      estimacion.value = await obtenerEstimacionRequest(estimacionId)
      return estimacion.value
    } catch (err) {
      error.value = err
      throw err
    } finally {
      cargando.value = false
    }
  }

  async function cargarComparables(estimacionId) {
    comparables.value = await obtenerComparablesRequest(estimacionId)
    return comparables.value
  }

  async function descargarReporte(estimacionId) {
    return generarReportePdfRequest(estimacionId)
  }

  function limpiar() {
    borrador.value = null
    estimacion.value = null
    comparables.value = null
    error.value = null
    claveIdempotencia.value = null
    esperaAgotada.value = false
    cargando.value = false
  }

  return {
    borrador,
    estimacion,
    comparables,
    cargando,
    error,
    claveIdempotencia,
    esperaAgotada,
    rango,
    crearBorrador,
    calcular,
    cargarEstimacion,
    cargarComparables,
    descargarReporte,
    marcarEsperaAgotada,
    reiniciarClaveIdempotencia,
    limpiar,
  }
})
