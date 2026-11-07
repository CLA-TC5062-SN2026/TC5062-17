<script setup>
defineProps({
  titulo: {
    type: String,
    default: '',
  },
  subtitulo: {
    type: String,
    default: '',
  },
  etiqueta: {
    type: String,
    default: 'div',
    validator: (valor) => ['div', 'section', 'article', 'aside'].includes(valor),
  },
  cuerpoClass: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <component :is="etiqueta" class="card shadow-sm border-0">
    <div v-if="titulo || subtitulo || $slots.header" class="card-header bg-white">
      <slot name="header">
        <h2 v-if="titulo" class="h5 mb-0">{{ titulo }}</h2>
        <p v-if="subtitulo" class="text-secondary small mb-0">{{ subtitulo }}</p>
      </slot>
    </div>

    <div class="card-body" :class="cuerpoClass">
      <slot />
    </div>

    <div v-if="$slots.footer" class="card-footer bg-white">
      <slot name="footer" />
    </div>
  </component>
</template>

<style scoped>
.card {
  min-width: 0;
  overflow-wrap: anywhere;
}

.card-body {
  min-width: 0;
}
</style>
