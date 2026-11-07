<script setup>
import { onMounted, ref } from 'vue'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCard from '@/components/BaseCard.vue'
import { ADVERTENCIA_ORIENTATIVA } from '@/constants'
import { useEstimacionStore } from '@/stores/estimacion'
import { formatearFecha, formatearMoneda } from '@/utils/formatters'

const props = defineProps({
  estimacionId: {
    type: String,
    required: true,
  },
})

const estimacionStore = useEstimacionStore()
const error = ref(null)
const descargando = ref(false)

onMounted(async () => {
  try {
    await Promise.all([
      estimacionStore.cargarEstimacion(props.estimacionId),
      estimacionStore.cargarComparables(props.estimacionId),
    ])
  } catch (err) {
    error.value = err
  }
})

async function descargarReporte() {
  descargando.value = true
  error.value = null
  try {
    const blob = await estimacionStore.descargarReporte(props.estimacionId)
    const url = URL.createObjectURL(blob)
    const enlace = document.createElement('a')
    enlace.href = url
    enlace.download = 'estimacion-MLState.pdf'
    enlace.click()
    URL.revokeObjectURL(url)
  } catch (err) {
    error.value = err
  } finally {
    descargando.value = false
  }
}
</script>

<template>
  <section class="page-container py-4">
    <header class="mb-4">
      <h1 class="h2 fw-bold mb-2">Resultado de la estimación</h1>
      <p class="text-secondary mb-0">Estimación <code>{{ estimacionId }}</code></p>
    </header>

    <BaseAlert v-if="error" :codigo="error.codigo" :mensaje="error.mensaje" :trace-id="error.traceId" />

    <div v-if="estimacionStore.cargando && !estimacionStore.estimacion" class="text-center py-5">
      <span class="spinner-border text-primary" aria-hidden="true"></span>
      <p class="text-secondary mt-3 mb-0">Cargando estimación…</p>
    </div>

    <template v-else-if="estimacionStore.estimacion">
      <BaseCard cuerpo-class="p-4" class="mb-4">
        <p class="text-uppercase text-secondary small mb-1">Valor central</p>
        <p class="display-6 fw-bold mb-3">
          {{ formatearMoneda(estimacionStore.estimacion.valorCentral) }}
        </p>
        <p class="mb-2">
          Rango:
          <strong>{{ formatearMoneda(estimacionStore.estimacion.valorMinimo) }}</strong>
          –
          <strong>{{ formatearMoneda(estimacionStore.estimacion.valorMaximo) }}</strong>
        </p>
        <p class="mb-1">
          Precio por m² de construcción:
          {{ formatearMoneda(estimacionStore.estimacion.precioM2Construccion) }}
        </p>
        <p class="mb-1">
          Confianza: <strong>{{ estimacionStore.estimacion.nivelConfianza }}</strong>
          <span v-if="estimacionStore.estimacion.causaConfianza">
            · {{ estimacionStore.estimacion.causaConfianza }}
          </span>
        </p>
        <p class="mb-0">Margen de error: {{ estimacionStore.estimacion.margenErrorPorcentaje }}%</p>
      </BaseCard>

      <div class="row g-4">
        <div class="col-12 col-lg-6">
          <BaseCard titulo="Explicación" class="h-100">
            <p class="mb-0">{{ estimacionStore.estimacion.explicacion }}</p>
          </BaseCard>
        </div>
        <div class="col-12 col-lg-6">
          <BaseCard titulo="Metadatos del cálculo" class="h-100">
            <dl class="row mb-0">
              <dt class="col-6">Fecha de cálculo</dt>
              <dd class="col-6">{{ formatearFecha(estimacionStore.estimacion.fechaCalculo) }}</dd>
              <dt class="col-6">Actualización de datos</dt>
              <dd class="col-6">{{ formatearFecha(estimacionStore.estimacion.actualizacionDatos) }}</dd>
            </dl>
          </BaseCard>
        </div>
      </div>

      <BaseCard titulo="Propiedades comparables" class="mt-4">
        <p v-if="!estimacionStore.comparables?.comparables?.length" class="text-secondary mb-0">
          No hay comparables disponibles para esta estimación.
        </p>
        <div v-else class="table-responsive">
          <table class="table align-middle mb-0">
            <thead>
              <tr>
                <th scope="col">#</th>
                <th scope="col">Colonia</th>
                <th scope="col">Tipo</th>
                <th scope="col">Superficies</th>
                <th scope="col">Precio</th>
                <th scope="col">Referencia</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="comparable in estimacionStore.comparables.comparables" :key="comparable.comparableId">
                <td>{{ comparable.orden }}</td>
                <td>{{ comparable.colonia }}</td>
                <td>{{ comparable.tipoInmueble }} · {{ comparable.usoSuelo }}</td>
                <td>
                  {{ comparable.superficieTerrenoM2 }} m² terreno ·
                  {{ comparable.superficieConstruidaM2 }} m² construcción
                </td>
                <td>{{ formatearMoneda(comparable.precioMXN) }}</td>
                <td>{{ formatearFecha(comparable.fechaReferencia) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </BaseCard>

      <div class="d-flex flex-wrap gap-2 mt-4">
        <BaseButton
          type="button"
          size="lg"
          :loading="descargando"
          loading-text="Generando…"
          @click="descargarReporte"
        >
          Descargar reporte PDF
        </BaseButton>
        <RouterLink class="btn btn-outline-primary btn-lg" :to="{ name: 'estimar' }">
          Nueva estimación
        </RouterLink>
      </div>

      <p class="alert alert-warning mt-4 mb-0" role="note">{{ ADVERTENCIA_ORIENTATIVA }}</p>
    </template>
  </section>
</template>
