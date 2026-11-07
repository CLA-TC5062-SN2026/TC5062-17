<script setup>
import BaseCard from '@/components/BaseCard.vue'
import { useSessionStore } from '@/stores/session'

const session = useSessionStore()
</script>

<template>
  <section class="page-container py-5">
    <div class="row align-items-center g-4">
      <div class="col-12 col-lg-7">
        <p class="text-uppercase text-primary fw-semibold small mb-2">MLState</p>
        <h1 class="display-6 fw-bold mb-3">Estimación orientativa de inmuebles</h1>
        <p class="lead text-secondary mb-4">
          Captura las características del inmueble, consulta un rango de valor y guarda el
          resultado en tu historial.
        </p>
        <div class="d-flex flex-wrap gap-2">
          <RouterLink class="btn btn-primary btn-lg" :to="{ name: 'estimar' }">
            Nueva estimación
          </RouterLink>
          <RouterLink
            v-if="session.estaAutenticado"
            class="btn btn-outline-primary btn-lg"
            :to="{ name: 'historial' }"
          >
            Ver historial
          </RouterLink>
          <RouterLink v-else class="btn btn-outline-primary btn-lg" :to="{ name: 'login' }">
            Iniciar sesión
          </RouterLink>
        </div>
      </div>
      <div class="col-12 col-lg-5">
        <BaseCard titulo="Flujo de captura" cuerpo-class="p-4">
          <ol class="mb-0 text-secondary">
            <li>Selecciona la ubicación y verifica la cobertura.</li>
            <li>Captura las características del inmueble.</li>
            <li>Confirma valores ambiguos y calcula.</li>
            <li>Revisa el rango, la confianza y los comparables.</li>
            <li>Descarga o comparte el reporte.</li>
          </ol>
        </BaseCard>
      </div>
    </div>
  </section>
</template>
