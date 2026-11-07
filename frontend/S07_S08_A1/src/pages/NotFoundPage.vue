<template>
  <section class="page-container py-5 text-center">
    <p class="display-4 fw-bold mb-2">404</p>
    <h1 class="h3 mb-3">La página que buscas no existe</h1>
    <p class="text-secondary mb-4">Verifica la dirección o vuelve al inicio.</p>
    <RouterLink class="btn btn-primary btn-lg" :to="{ name: 'inicio' }">Volver al inicio</RouterLink>
  </section>
</template>
