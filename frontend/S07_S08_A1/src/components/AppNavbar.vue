<script setup>
import { computed, ref, useId } from 'vue'
import { useRouter } from 'vue-router'
import BaseButton from '@/components/BaseButton.vue'
import { useSessionStore } from '@/stores/session'

const props = defineProps({
  estadoForzado: {
    type: String,
    default: null,
    validator: (valor) => valor === null || ['autenticado', 'invitado'].includes(valor),
  },
  ariaLabel: {
    type: String,
    default: 'Navegación principal',
  },
})

const router = useRouter()
const session = useSessionStore()
const menuAbierto = ref(false)
const botonMenu = ref(null)
const menuId = `menu-principal-${useId()}`
const mostrarDemo = import.meta.env.DEV

const autenticado = computed(() => {
  if (props.estadoForzado === 'autenticado') {
    return true
  }
  if (props.estadoForzado === 'invitado') {
    return false
  }
  return session.estaAutenticado
})

const nombreUsuario = computed(() => {
  if (props.estadoForzado === 'autenticado' && !session.usuario) {
    return 'Broker de ejemplo'
  }
  return session.usuario?.nombre ?? session.usuario?.correo ?? 'Broker'
})

function alternarMenu() {
  menuAbierto.value = !menuAbierto.value
}

function cerrarMenu() {
  menuAbierto.value = false
}

function cerrarMenuConFoco() {
  menuAbierto.value = false
  botonMenu.value?.focus()
}

function alPresionarEscape() {
  if (!menuAbierto.value) {
    return
  }

  cerrarMenuConFoco()
}

async function salir() {
  if (props.estadoForzado) {
    return
  }

  cerrarMenu()
  await session.cerrarSesion()
  router.push({ name: 'inicio' })
}
</script>

<template>
  <header class="border-bottom bg-white">
    <nav
      class="navbar navbar-expand-lg page-container"
      :aria-label="ariaLabel"
      @keydown.esc="alPresionarEscape"
    >
      <RouterLink class="navbar-brand fw-bold" :to="{ name: 'inicio' }" @click="cerrarMenu">
        MLState
      </RouterLink>
      <button
        ref="botonMenu"
        class="navbar-toggler"
        type="button"
        :aria-expanded="menuAbierto"
        :aria-controls="menuId"
        :aria-label="menuAbierto ? 'Cerrar menú' : 'Abrir menú'"
        @click="alternarMenu"
      >
        <span class="navbar-toggler-icon" aria-hidden="true"></span>
      </button>
      <div
        :id="menuId"
        class="navbar-collapse"
        :class="{ collapse: !menuAbierto, show: menuAbierto }"
      >
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            <RouterLink
              class="nav-link"
              active-class="active"
              :to="{ name: 'estimar' }"
              @click="cerrarMenu"
            >
              Estimar
            </RouterLink>
          </li>
          <li v-if="autenticado" class="nav-item">
            <RouterLink
              class="nav-link"
              active-class="active"
              :to="{ name: 'historial' }"
              @click="cerrarMenu"
            >
              Historial
            </RouterLink>
          </li>
          <li v-if="mostrarDemo" class="nav-item">
            <RouterLink
              class="nav-link"
              active-class="active"
              :to="{ name: 'componentes' }"
              @click="cerrarMenu"
            >
              Componentes
            </RouterLink>
          </li>
        </ul>
        <div class="d-flex flex-column flex-lg-row align-items-lg-center gap-2 pb-3 pb-lg-0">
          <template v-if="autenticado">
            <span class="navbar-text nombre-usuario text-truncate" :title="nombreUsuario">
              {{ nombreUsuario }}
            </span>
            <BaseButton variant="outline-secondary" @click="salir">Cerrar sesión</BaseButton>
          </template>
          <template v-else>
            <RouterLink
              class="btn btn-outline-primary"
              :to="{ name: 'login' }"
              @click="cerrarMenu"
            >
              Iniciar sesión
            </RouterLink>
            <RouterLink class="btn btn-primary" :to="{ name: 'registro' }" @click="cerrarMenu">
              Crear cuenta
            </RouterLink>
          </template>
        </div>
      </div>
    </nav>
  </header>
</template>

<style scoped>
.navbar {
  min-width: 0;
}

.navbar-brand {
  flex-shrink: 0;
}

.navbar-collapse {
  min-width: 0;
}

.nombre-usuario {
  max-width: 16rem;
}

@media (max-width: 991.98px) {
  .nombre-usuario {
    max-width: 100%;
  }
}
</style>
