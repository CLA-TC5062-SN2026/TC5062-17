<script setup>
import { reactive } from 'vue'
import AppNavbar from '@/components/AppNavbar.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseInput from '@/components/BaseInput.vue'

const formulario = reactive({
  nombre: 'Ana Martínez',
  correo: 'ana@ejemplo.mx',
  conservacion: 'buena',
  notas: '',
})
</script>

<template>
  <section class="page-container py-4">
    <header class="mb-4">
      <h1 class="h2 fw-bold mb-2">Componentes esenciales de UI</h1>
      <p class="text-secondary mb-0">
        Variantes y estados de los componentes reutilizables de MLState.
      </p>
    </header>

    <BaseCard titulo="Botones" subtitulo="Variantes, tamaños y estado de carga." class="mb-4">
      <div class="d-flex flex-wrap gap-2 mb-3">
        <BaseButton>Primario</BaseButton>
        <BaseButton variant="secondary">Secundario</BaseButton>
        <BaseButton variant="outline-primary">Outline primario</BaseButton>
        <BaseButton variant="outline-secondary">Outline secundario</BaseButton>
        <BaseButton variant="outline-danger">Eliminar</BaseButton>
      </div>
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        <BaseButton size="sm">Pequeño</BaseButton>
        <BaseButton size="lg">Grande</BaseButton>
        <BaseButton loading loading-text="Guardando…">Guardar</BaseButton>
        <BaseButton disabled>Deshabilitado</BaseButton>
      </div>
      <BaseButton block>Botón de ancho completo</BaseButton>
    </BaseCard>

    <BaseCard titulo="Campos de entrada" subtitulo="Input, select y textarea con validación visual." class="mb-4">
      <form class="row g-3" novalidate @submit.prevent>
        <div class="col-12 col-md-6">
          <BaseInput
            id="demo-nombre"
            v-model="formulario.nombre"
            label="Nombre"
            autocomplete="name"
            required
            hint="Escribe el nombre completo del broker."
          />
        </div>
        <div class="col-12 col-md-6">
          <BaseInput
            id="demo-correo"
            v-model="formulario.correo"
            label="Correo electrónico"
            type="email"
            inputmode="email"
            autocomplete="email"
            required
            error="Ingresa un correo electrónico válido."
          />
        </div>
        <div class="col-12 col-md-6">
          <BaseInput
            id="demo-conservacion"
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
        <div class="col-12 col-md-6">
          <BaseInput
            id="demo-superficie"
            label="Superficie de terreno (m²)"
            type="number"
            min="0.01"
            step="0.01"
            inputmode="decimal"
            required
            valido
          />
        </div>
        <div class="col-12">
          <BaseInput
            id="demo-notas"
            v-model="formulario.notas"
            as="textarea"
            label="Notas adicionales"
            optional
            rows="3"
            hint="Máximo 500 caracteres."
          />
        </div>
        <div class="col-12">
          <BaseButton type="submit">Guardar ejemplo</BaseButton>
        </div>
      </form>
    </BaseCard>

    <BaseCard titulo="Tarjetas" subtitulo="Contenedor genérico con título, cuerpo y footer." class="mb-4">
      <div class="row g-3">
        <div class="col-12 col-md-6">
          <BaseCard titulo="Tarjeta con título" subtitulo="Información estructurada">
            <p class="mb-0">El cuerpo acepta cualquier contenido o componente.</p>
          </BaseCard>
        </div>
        <div class="col-12 col-md-6">
          <BaseCard titulo="Tarjeta con footer">
            <p class="mb-0">Este contenido está en el cuerpo de la tarjeta.</p>
            <template #footer>
              <div class="d-flex justify-content-end">
                <BaseButton size="sm">Acción</BaseButton>
              </div>
            </template>
          </BaseCard>
        </div>
      </div>
    </BaseCard>

    <BaseCard titulo="Barra de navegación" subtitulo="Estados autenticado y no autenticado.">
      <p class="text-secondary">
        El navbar global está en la parte superior. Estas son vistas previas de ambos estados.
      </p>
      <div class="border rounded overflow-hidden mb-3">
        <AppNavbar estado-forzado="autenticado" aria-label="Vista previa autenticada" />
      </div>
      <div class="border rounded overflow-hidden">
        <AppNavbar estado-forzado="invitado" aria-label="Vista previa de invitado" />
      </div>
    </BaseCard>
  </section>
</template>
