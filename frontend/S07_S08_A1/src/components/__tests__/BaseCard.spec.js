import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BaseCard from '@/components/BaseCard.vue'

describe('BaseCard', () => {
  it('renderiza título, subtítulo y contenido', () => {
    const wrapper = mount(BaseCard, {
      props: { titulo: 'Resumen', subtitulo: 'Datos del inmueble' },
      slots: { default: 'Contenido de la tarjeta' },
    })

    expect(wrapper.find('.card-header').text()).toContain('Resumen')
    expect(wrapper.find('.card-header').text()).toContain('Datos del inmueble')
    expect(wrapper.find('.card-body').text()).toContain('Contenido de la tarjeta')
  })

  it('renderiza el slot footer cuando se proporciona', () => {
    const wrapper = mount(BaseCard, {
      slots: { footer: 'Pie de la tarjeta' },
    })

    expect(wrapper.find('.card-footer').text()).toContain('Pie de la tarjeta')
  })

  it('omite header y footer si no hay contenido', () => {
    const wrapper = mount(BaseCard)

    expect(wrapper.find('.card-header').exists()).toBe(false)
    expect(wrapper.find('.card-footer').exists()).toBe(false)
  })

  it('permite cambiar la etiqueta semántica del contenedor', () => {
    const wrapper = mount(BaseCard, {
      props: { etiqueta: 'article' },
    })

    expect(wrapper.element.tagName).toBe('ARTICLE')
  })
})
