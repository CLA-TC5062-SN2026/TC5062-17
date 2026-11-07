<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import BaseAlert from '@/components/BaseAlert.vue'
import BaseButton from '@/components/BaseButton.vue'
import BaseCard from '@/components/BaseCard.vue'
import BaseInput from '@/components/BaseInput.vue'
import { registrarUsuarioRequest } from '@/services/auth'

const router = useRouter()

const formulario = reactive({
  nombre: '',
  correo: '',
  contrasena: '',
})

const enviando = ref(false)
const error = ref(null)

async function registrar() {
  error.value = null
  enviando.value = true
  try {
    await registrarUsuarioRequest({ ...formulario })
    router.push({ name: 'login', query: { registro: 'ok' } })
  } catch (err) {
    error.value = err
  } finally {
    enviando.value = false
  }
}
</script>

<template>
  <section class="page-container py-5">
    <div class="row justify-content-center">
      <div class="col-12 col-md-8 col-lg-5">
        <BaseCard cuerpo-class="p-4">
          <h1 class="h3 fw-bold mb-1">Crear cuenta de broker</h1>
          <p class="text-secondary mb-4">
            La contraseña debe tener al menos 10 caracteres, una mayúscula, una minúscula y un número.
          </p>

          <BaseAlert
            v-if="error"
            :codigo="error.codigo"
            :mensaje="error.mensaje"
            :trace-id="error.traceId"
          />

          <form novalidate @submit.prevent="registrar">
            <div class="mb-3">
              <BaseInput
                id="nombre"
                v-model="formulario.nombre"
                label="Nombre"
                autocomplete="name"
                required
              />
            </div>
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
                autocomplete="new-password"
                minlength="10"
                required
              />
            </div>
            <BaseButton
              type="submit"
              size="lg"
              block
              :loading="enviando"
              loading-text="Creando cuenta…"
            >
              Crear cuenta
            </BaseButton>
          </form>

          <p class="text-center text-secondary mt-4 mb-0">
            ¿Ya tienes cuenta?
            <RouterLink :to="{ name: 'login' }">Iniciar sesión</RouterLink>
          </p>
        </BaseCard>
      </div>
    </div>
  </section>
</template>
