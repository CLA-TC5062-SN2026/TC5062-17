import { ref } from 'vue'
import { defineStore } from 'pinia'
import { obtenerCatalogosRequest } from '@/services/catalogos'

export const useCatalogosStore = defineStore('catalogos', () => {
  const catalogos = ref(null)
  const cargando = ref(false)
  const error = ref(null)

  async function cargar() {
    if (catalogos.value) return catalogos.value

    cargando.value = true
    error.value = null
    try {
      catalogos.value = await obtenerCatalogosRequest()
      return catalogos.value
    } catch (err) {
      error.value = err
      throw err
    } finally {
      cargando.value = false
    }
  }

  function limpiar() {
    catalogos.value = null
    error.value = null
  }

  return { catalogos, cargando, error, cargar, limpiar }
})
