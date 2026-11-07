<script setup>
defineProps({
  codigo: {
    type: String,
    default: '',
  },
  mensaje: {
    type: String,
    required: true,
  },
  traceId: {
    type: String,
    default: '',
  },
})
</script>

<template>
  <div class="alert alert-danger" role="alert">
    <p class="fw-semibold mb-1">{{ mensaje }}</p>
    <p v-if="codigo" class="small mb-0">
      Código: {{ codigo }}<span v-if="traceId"> · Trace: {{ traceId }}</span>
    </p>
  </div>
</template>
