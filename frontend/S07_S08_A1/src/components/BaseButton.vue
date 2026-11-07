<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (valor) =>
      ['primary', 'secondary', 'outline-primary', 'outline-secondary', 'outline-danger'].includes(valor),
  },
  size: {
    type: String,
    default: 'md',
    validator: (valor) => ['sm', 'md', 'lg'].includes(valor),
  },
  type: {
    type: String,
    default: 'button',
  },
  loading: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  block: {
    type: Boolean,
    default: false,
  },
  loadingText: {
    type: String,
    default: 'Cargando…',
  },
})

const emit = defineEmits(['click'])

const clasesVariante = {
  primary: 'btn-primary',
  secondary: 'btn-secondary',
  'outline-primary': 'btn-outline-primary',
  'outline-secondary': 'btn-outline-secondary',
  'outline-danger': 'btn-outline-danger',
}

const estaDeshabilitado = computed(() => props.disabled || props.loading)

const clases = computed(() => [
  'btn',
  clasesVariante[props.variant],
  {
    'btn-sm': props.size === 'sm',
    'btn-lg': props.size === 'lg',
    'w-100': props.block,
  },
])

function alHacerClic(event) {
  if (estaDeshabilitado.value) {
    return
  }

  emit('click', event)
}
</script>

<template>
  <button
    :type="type"
    :class="clases"
    :disabled="estaDeshabilitado"
    :aria-busy="loading ? 'true' : undefined"
    @click="alHacerClic"
  >
    <span
      v-if="loading"
      class="spinner-border spinner-border-sm me-2"
      aria-hidden="true"
    ></span>
    <slot v-if="!loading" />
    <span v-else>{{ loadingText }}</span>
  </button>
</template>

<style scoped>
.btn {
  max-width: 100%;
  white-space: normal;
}

.btn[aria-busy='true']:disabled {
  opacity: 1;
}

@media (max-width: 575.98px) {
  .btn-lg {
    width: 100%;
  }
}
</style>
