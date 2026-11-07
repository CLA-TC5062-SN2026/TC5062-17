<script setup>
import { onMounted, ref } from 'vue'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCard from '@/components/BaseCard.vue'
import {
  eliminarEstimacionRequest,
  listarHistorialRequest,
} from '@/services/estimaciones'
import { formatearFecha, formatearMoneda } from '@/utils/formatters'

const elementos = ref([])
const total = ref(0)
const cargando = ref(false)
const eliminandoId = ref(null)
const error = ref(null)

async function cargar() {
  cargando.value = true
  error.value = null
  try {
    const respuesta = await listarHistorialRequest()
    elementos.value = respuesta?.elementos ?? []
    total.value = respuesta?.total ?? 0
  } catch (err) {
    error.value = err
  } finally {
    cargando.value = false
  }
}

async function eliminar(estimacionId) {
  error.value = null
  eliminandoId.value = estimacionId
  try {
    await eliminarEstimacionRequest(estimacionId)
    await cargar()
  } catch (err) {
    error.value = err
  } finally {
    eliminandoId.value = null
  }
}

onMounted(cargar)
</script>

<template>
  <section class="page-container py-4">
    <header class="d-flex flex-wrap justify-content-between align-items-center gap-2 mb-4">
      <div>
        <h1 class="h2 fw-bold mb-1">Historial de estimaciones</h1>
        <p class="text-secondary mb-0">{{ total }} estimaciones guardadas.</p>
      </div>
      <RouterLink class="btn btn-primary" :to="{ name: 'estimar' }">Nueva estimación</RouterLink>
    </header>

    <BaseAlert v-if="error" :codigo="error.codigo" :mensaje="error.mensaje" :trace-id="error.traceId" />

    <div v-if="cargando" class="text-center py-5">
      <span class="spinner-border text-primary" aria-hidden="true"></span>
      <p class="text-secondary mt-3 mb-0">Cargando historial…</p>
    </div>

    <BaseCard v-else-if="!elementos.length" cuerpo-class="text-center py-5">
      <p class="mb-2">Todavía no tienes estimaciones guardadas.</p>
      <RouterLink class="btn btn-primary" :to="{ name: 'estimar' }">Crear la primera</RouterLink>
    </BaseCard>

    <div v-else class="table-responsive">
      <table class="table table-hover align-middle">
        <thead>
          <tr>
            <th scope="col">Fecha</th>
            <th scope="col">Ubicación</th>
            <th scope="col">Valor central</th>
            <th scope="col">Confianza</th>
            <th scope="col" class="text-end">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="elemento in elementos" :key="elemento.estimacionId">
            <td>{{ formatearFecha(elemento.fechaCalculo) }}</td>
            <td>{{ elemento.municipio }} · {{ elemento.colonia }}</td>
            <td>{{ formatearMoneda(elemento.valorCentral) }}</td>
            <td>{{ elemento.nivelConfianza }}</td>
            <td class="text-end">
              <RouterLink
                class="btn btn-sm btn-outline-primary me-2"
                :to="{ name: 'resultado', params: { estimacionId: elemento.estimacionId } }"
              >
                Ver
              </RouterLink>
              <BaseButton
                variant="outline-danger"
                size="sm"
                :loading="eliminandoId === elemento.estimacionId"
                loading-text="Eliminando…"
                @click="eliminar(elemento.estimacionId)"
              >
                Eliminar
              </BaseButton>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>
