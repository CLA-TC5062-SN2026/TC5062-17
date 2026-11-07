<script setup>
import { computed, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseInput from '@/components/BaseInput.vue'
import { useSessionStore } from '@/stores/session'

const router = useRouter()
const route = useRoute()
const session = useSessionStore()

const formulario = reactive({
  correo: '',
  contrasena: '',
})

const error = ref(null)

const destino = computed(() =>
  typeof route.query.redirect === 'string' ? route.query.redirect : '/',
)

async function entrar() {
  error.value = null
  try {
    await session.iniciarSesion({ ...formulario })
    router.replace(destino.value)
  } catch (err) {
    error.value = err
  }
}
</script>

<template>
  <section class="page-container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-5">
        <BaseCard cuerpo-class="p-4">
          <h1 class="h3 fw-bold mb-1">Iniciar sesión</h1>
          <p class="text-secondary mb-4">Accede para guardar y consultar tu historial.</p>

          <div v-if="route.query.registro === 'ok'" class="alert alert-success" role="status">
            Cuenta creada. Ya puedes iniciar sesión.
          </div>

          <BaseAlert
            v-if="error"
            :codigo="error.codigo"
            :mensaje="error.mensaje"
            :trace-id="error.traceId"
          />

          <form novalidate @submit.prevent="entrar">
            <div class="mb-3">
              <BaseInput
                id="correo"
                v-model="formulario.correo"
                label="Correo electrónico"
                type="email"
                autocomplete="email"
                inputmode="email"
                required
              />
            </div>
            <div class="mb-4">
              <BaseInput
                id="contrasena"
                v-model="formulario.contrasena"
                label="Contraseña"
                type="password"
                autocomplete="current-password"
                required
              />
            </div>
            <BaseButton
              type="submit"
              size="lg"
              block
              :loading="session.cargando"
              loading-text="Entrando…"
            >
              Entrar
            </BaseButton>
          </form>

          <p class="text-center text-secondary mt-4 mb-0">
            ¿No tienes cuenta?
            <RouterLink :to="{ name: 'registro' }">Crear cuenta</RouterLink>
          </p>
        </BaseCard>
      </div>
    </div>
  </section>
</template>
