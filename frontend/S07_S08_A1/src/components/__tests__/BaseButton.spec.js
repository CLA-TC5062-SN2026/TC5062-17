import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BaseButton from '@/components/BaseButton.vue'

describe('BaseButton', () => {
  it('aplica la variante primaria por defecto', () => {
    const wrapper = mount(BaseButton, {
      slots: { default: 'Guardar' },
    })

    expect(wrapper.classes()).toContain('btn')
    expect(wrapper.classes()).toContain('btn-primary')
    expect(wrapper.text()).toBe('Guardar')
  })

  it('aplica la variante secundaria y el tamaño', () => {
    const wrapper = mount(BaseButton, {
      props: { variant: 'secondary', size: 'lg' },
    })

    expect(wrapper.classes()).toContain('btn-secondary')
    expect(wrapper.classes()).toContain('btn-lg')
  })

  it('muestra el spinner y se deshabilita en estado loading', () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true, loadingText: 'Guardando…' },
    })

    expect(wrapper.attributes('disabled')).toBeDefined()
    expect(wrapper.attributes('aria-busy')).toBe('true')
    expect(wrapper.find('.spinner-border').exists()).toBe(true)
    expect(wrapper.find('.spinner-border').attributes('aria-hidden')).toBe('true')
    expect(wrapper.text()).toContain('Guardando…')
  })

  it('no emite click mientras está cargando', async () => {
    const wrapper = mount(BaseButton, {
      props: { loading: true },
    })

    await wrapper.trigger('click')

    expect(wrapper.emitted('click')).toBeUndefined()
  })

  it('emite click cuando está habilitado', async () => {
    const wrapper = mount(BaseButton)

    await wrapper.trigger('click')

    expect(wrapper.emitted('click')).toHaveLength(1)
  })
})
