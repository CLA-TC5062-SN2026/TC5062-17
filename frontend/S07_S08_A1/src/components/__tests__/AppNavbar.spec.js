import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createMemoryHistory, createRouter } from 'vue-router'
import { afterEach, describe, expect, it } from 'vitest'
import AppNavbar from '@/components/AppNavbar.vue'
import { useSessionStore } from '@/stores/session'

const rutas = [
  { path: '/', name: 'inicio', component: { template: '<div />' } },
  { path: '/estimar', name: 'estimar', component: { template: '<div />' } },
  { path: '/historial', name: 'historial', component: { template: '<div />' } },
  { path: '/componentes', name: 'componentes', component: { template: '<div />' } },
  { path: '/login', name: 'login', component: { template: '<div />' } },
  { path: '/registro', name: 'registro', component: { template: '<div />' } },
]

async function montar({ autenticado = false, props = {} } = {}) {
  const pinia = createPinia()
  setActivePinia(pinia)

  if (autenticado) {
    const session = useSessionStore()
    session.token = 'token-demo'
    session.usuario = { nombre: 'Ana Martínez', correo: 'ana@ejemplo.mx' }
  }

  const router = createRouter({
    history: createMemoryHistory(),
    routes: rutas,
  })

  await router.push('/')
  await router.isReady()

  return mount(AppNavbar, {
    props,
    attachTo: document.body,
    global: { plugins: [pinia, router] },
  })
}

afterEach(() => {
  document.body.innerHTML = ''
})

describe('AppNavbar', () => {
  it('muestra acciones de invitado cuando no hay sesión', async () => {
    const wrapper = await montar()

    expect(wrapper.text()).toContain('Iniciar sesión')
    expect(wrapper.text()).toContain('Crear cuenta')
    expect(wrapper.text()).not.toContain('Historial')
    expect(wrapper.text()).not.toContain('Cerrar sesión')
  })

  it('muestra el usuario y las acciones autenticadas', async () => {
    const wrapper = await montar({ autenticado: true })

    expect(wrapper.text()).toContain('Historial')
    expect(wrapper.text()).toContain('Ana Martínez')
    expect(wrapper.text()).toContain('Cerrar sesión')
    expect(wrapper.text()).not.toContain('Iniciar sesión')
  })

  it('permite forzar el estado autenticado y personalizar la etiqueta', async () => {
    const wrapper = await montar({
      props: { estadoForzado: 'autenticado', ariaLabel: 'Vista previa autenticada' },
    })

    expect(wrapper.find('nav').attributes('aria-label')).toBe('Vista previa autenticada')
    expect(wrapper.text()).toContain('Broker de ejemplo')
    expect(wrapper.text()).toContain('Cerrar sesión')
  })

  it('actualiza el nombre del botón, oculta el ícono y cierra con Escape', async () => {
    const wrapper = await montar()
    const boton = wrapper.find('.navbar-toggler')

    expect(boton.attributes('aria-label')).toBe('Abrir menú')
    expect(wrapper.find('.navbar-toggler-icon').attributes('aria-hidden')).toBe('true')

    await boton.trigger('click')

    expect(boton.attributes('aria-expanded')).toBe('true')
    expect(boton.attributes('aria-label')).toBe('Cerrar menú')

    await wrapper.find('nav').trigger('keydown', { key: 'Escape' })

    expect(boton.attributes('aria-expanded')).toBe('false')
    expect(boton.attributes('aria-label')).toBe('Abrir menú')
    expect(wrapper.find('.navbar-collapse').classes()).not.toContain('show')
    expect(document.activeElement).toBe(boton.element)
  })
})
