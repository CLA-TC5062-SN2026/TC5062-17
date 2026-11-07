import { h } from 'vue'
import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import BaseInput from '@/components/BaseInput.vue'

describe('BaseInput', () => {
  it('asocia la etiqueta con el control', () => {
    const wrapper = mount(BaseInput, {
      props: { id: 'correo', label: 'Correo electrónico' },
    })

    expect(wrapper.find('label').attributes('for')).toBe('correo')
    expect(wrapper.find('input#correo').exists()).toBe(true)
  })

  it('emite update:modelValue al escribir', async () => {
    const wrapper = mount(BaseInput, {
      props: { label: 'Nombre', modelValue: '' },
    })

    await wrapper.find('input').setValue('Ana')

    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['Ana'])
  })

  it('muestra el error y aplica atributos de accesibilidad', () => {
    const wrapper = mount(BaseInput, {
      props: { id: 'correo', label: 'Correo', error: 'Correo inválido' },
    })

    const input = wrapper.find('input')

    expect(input.classes()).toContain('is-invalid')
    expect(input.attributes('aria-invalid')).toBe('true')
    expect(input.attributes('aria-describedby')).toContain('correo-error')
    expect(wrapper.find('.invalid-feedback').text()).toContain('Correo inválido')
  })

  it('renderiza un select con sus opciones', async () => {
    const wrapper = mount(BaseInput, {
      props: { id: 'tipo', label: 'Tipo', as: 'select', modelValue: '' },
      slots: {
        options: () => [
          h('option', { value: '' }, 'Selecciona'),
          h('option', { value: 'casa' }, 'Casa'),
        ],
      },
    })

    expect(wrapper.find('select#tipo').exists()).toBe(true)
    expect(wrapper.findAll('option')).toHaveLength(2)

    await wrapper.find('select').setValue('casa')

    expect(wrapper.emitted('update:modelValue')[0]).toEqual(['casa'])
  })

  it('renderiza un textarea', () => {
    const wrapper = mount(BaseInput, {
      props: { label: 'Notas', as: 'textarea', rows: 4 },
    })

    expect(wrapper.find('textarea').exists()).toBe(true)
    expect(wrapper.find('textarea').attributes('rows')).toBe('4')
  })
})
