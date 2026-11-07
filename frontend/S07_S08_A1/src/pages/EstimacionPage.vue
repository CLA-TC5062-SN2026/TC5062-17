<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseInput from '@/components/BaseInput.vue'
import { evaluarElegibilidadRequest } from '@/services/catalogos'
import { useCatalogosStore } from '@/stores/catalogos'
import { useEstimacionStore } from '@/stores/estimacion'

const router = useRouter()
const catalogosStore = useCatalogosStore()
const estimacionStore = useEstimacionStore()

const formulario = reactive({
  estadoId: '',
  municipioId: '',
  coloniaId: '',
  tipoInmuebleId: '',
  usoSueloId: '',
  superficieTerrenoM2: '',
  superficieConstruidaM2: '',
  habitaciones: '',
  banosCompletos: '',
  estacionamientos: '',
  antiguedadAnos: '',
  conservacion: '',
})

const enviando = ref(false)
const error = ref(null)

const estados = computed(() => catalogosStore.catalogos?.estados ?? [])
const tiposInmueble = computed(() => catalogosStore.catalogos?.tiposInmueble ?? [])
const usosSuelo = computed(() => catalogosStore.catalogos?.usosSuelo ?? [])

const municipios = computed(
  () => estados.value.find((estado) => estado.estadoId === formulario.estadoId)?.municipios ?? [],
)

const colonias = computed(
  () =>
    municipios.value.find((municipio) => municipio.municipioId === formulario.municipioId)
      ?.colonias ?? [],
)

watch(
  () => formulario.estadoId,
  () => {
    formulario.municipioId = ''
    formulario.coloniaId = ''
  },
)

watch(
  () => formulario.municipioId,
  () => {
    formulario.coloniaId = ''
  },
)

onMounted(() => {
  catalogosStore.cargar().catch((err) => {
    error.value = err
  })
})

function numeroONull(valor) {
  return valor === '' || valor === null || valor === undefined ? null : Number(valor)
}

async function enviar() {
  error.value = null
  enviando.value = true

  try {
    const elegibilidad = await evaluarElegibilidadRequest({
      estadoId: formulario.estadoId,
      municipioId: formulario.municipioId,
      coloniaId: formulario.coloniaId,
      tipoInmuebleId: formulario.tipoInmuebleId,
      usoSueloId: formulario.usoSueloId,
    })

    await estimacionStore.crearBorrador({
      coberturaId: elegibilidad.coberturaId,
      ficha: {
        superficieTerrenoM2: numeroONull(formulario.superficieTerrenoM2),
        superficieConstruidaM2: numeroONull(formulario.superficieConstruidaM2),
        habitaciones: numeroONull(formulario.habitaciones),
        banosCompletos: numeroONull(formulario.banosCompletos),
        estacionamientos: numeroONull(formulario.estacionamientos),
        antiguedadAnos: numeroONull(formulario.antiguedadAnos),
        conservacion: formulario.conservacion || null,
      },
    })

    const resultado = await estimacionStore.calcular()
    router.push({ name: 'resultado', params: { estimacionId: resultado.estimacionId } })
  } catch (err) {
    error.value = err
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <section class="page-container py-4">
    <header class="mb-4">
      <h1 class="h2 fw-bold mb-2">Nueva estimación</h1>
      <p class="text-secondary mb-0">
        Verifica la cobertura y captura las características del inmueble.
      </p>
    </header>

    <BaseAlert v-if="error" :codigo="error.codigo" :mensaje="error.mensaje" :trace-id="error.traceId" />

    <form class="row g-3" novalidate @submit.prevent="enviar">
      <div class="col-12">
        <h2 class="h5 border-bottom pb-2">Ubicación</h2>
      </div>

      <div class="col-12 col-md-4">
        <BaseInput
          id="estadoId"
          v-model="formulario.estadoId"
          as="select"
          label="Estado"
          required
        >
          <template #options>
            <option value="" disabled>Selecciona un estado</option>
            <option v-for="estado in estados" :key="estado.estadoId" :value="estado.estadoId">
              {{ estado.nombre }}
            </option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 col-md-4">
        <BaseInput
          id="municipioId"
          v-model="formulario.municipioId"
          as="select"
          label="Municipio"
          :disabled="!formulario.estadoId"
          required
        >
          <template #options>
            <option value="" disabled>Selecciona un municipio</option>
            <option
              v-for="municipio in municipios"
              :key="municipio.municipioId"
              :value="municipio.municipioId"
            >
              {{ municipio.nombre }}
            </option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 col-md-4">
        <BaseInput
          id="coloniaId"
          v-model="formulario.coloniaId"
          as="select"
          label="Colonia"
          :disabled="!formulario.municipioId"
          required
        >
          <template #options>
            <option value="" disabled>Selecciona una colonia</option>
            <option
              v-for="colonia in colonias"
              :key="colonia.coloniaId"
              :value="colonia.coloniaId"
            >
              {{ colonia.nombre }}
            </option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 col-md-6">
        <BaseInput
          id="tipoInmuebleId"
          v-model="formulario.tipoInmuebleId"
          as="select"
          label="Tipo de inmueble"
          required
        >
          <template #options>
            <option value="" disabled>Selecciona un tipo</option>
            <option v-for="tipo in tiposInmueble" :key="tipo.id" :value="tipo.id">
              {{ tipo.nombre }}
            </option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 col-md-6">
        <BaseInput
          id="usoSueloId"
          v-model="formulario.usoSueloId"
          as="select"
          label="Uso de suelo"
          required
        >
          <template #options>
            <option value="" disabled>Selecciona un uso</option>
            <option v-for="uso in usosSuelo" :key="uso.id" :value="uso.id">
              {{ uso.nombre }}
            </option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 mt-4">
        <h2 class="h5 border-bottom pb-2">Características</h2>
      </div>

      <div class="col-12 col-md-6">
        <BaseInput
          id="superficieTerrenoM2"
          v-model="formulario.superficieTerrenoM2"
          label="Superficie de terreno (m²)"
          type="number"
          min="0.01"
          step="0.01"
          inputmode="decimal"
          required
        />
      </div>

      <div class="col-12 col-md-6">
        <BaseInput
          id="superficieConstruidaM2"
          v-model="formulario.superficieConstruidaM2"
          label="Superficie construida (m²)"
          type="number"
          min="0.01"
          step="0.01"
          inputmode="decimal"
          required
        />
      </div>

      <div class="col-6 col-md-3">
        <BaseInput
          id="habitaciones"
          v-model="formulario.habitaciones"
          label="Habitaciones"
          type="number"
          min="1"
          step="1"
          inputmode="numeric"
          required
        />
      </div>

      <div class="col-6 col-md-3">
        <BaseInput
          id="banosCompletos"
          v-model="formulario.banosCompletos"
          label="Baños completos"
          type="number"
          min="1"
          step="1"
          inputmode="numeric"
          required
        />
      </div>

      <div class="col-6 col-md-3">
        <BaseInput
          id="estacionamientos"
          v-model="formulario.estacionamientos"
          label="Estacionamientos"
          type="number"
          min="0"
          step="1"
          inputmode="numeric"
          optional
        />
      </div>

      <div class="col-6 col-md-3">
        <BaseInput
          id="antiguedadAnos"
          v-model="formulario.antiguedadAnos"
          label="Antigüedad (años)"
          type="number"
          min="0"
          step="1"
          inputmode="numeric"
          optional
        />
      </div>

      <div class="col-12 col-md-6">
        <BaseInput
          id="conservacion"
          v-model="formulario.conservacion"
          as="select"
          label="Conservación"
          optional
        >
          <template #options>
            <option value="">Sin especificar</option>
            <option value="buena">Buena</option>
            <option value="regular">Regular</option>
            <option value="mala">Mala</option>
          </template>
        </BaseInput>
      </div>

      <div class="col-12 d-flex flex-wrap gap-2 pt-3">
        <BaseButton
          type="submit"
          size="lg"
          :loading="enviando"
          loading-text="Calculando…"
        >
          Calcular estimación
        </BaseButton>
        <RouterLink class="btn btn-outline-secondary btn-lg" :to="{ name: 'inicio' }">
          Cancelar
        </RouterLink>
      </div>
    </form>
  </section>
</template>
