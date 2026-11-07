<script setup>
import { computed, useId } from 'vue'
import { ETIQUETA_OBLIGATORIO, ETIQUETA_OPCIONAL } from '@/constants'

defineOptions({ inheritAttrs: false })

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: '',
  },
  label: {
    type: String,
    required: true,
  },
  as: {
    type: String,
    default: 'input',
    validator: (valor) => ['input', 'select', 'textarea'].includes(valor),
  },
  id: {
    type: String,
    default: '',
  },
  type: {
    type: String,
    default: 'text',
  },
  required: {
    type: Boolean,
    default: false,
  },
  optional: {
    type: Boolean,
    default: false,
  },
  hint: {
    type: String,
    default: '',
  },
  error: {
    type: String,
    default: '',
  },
  valido: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  placeholder: {
    type: String,
    default: '',
  },
  autocomplete: {
    type: String,
    default: undefined,
  },
  inputmode: {
    type: String,
    default: undefined,
  },
  min: {
    type: [String, Number],
    default: undefined,
  },
  max: {
    type: [String, Number],
    default: undefined,
  },
  step: {
    type: [String, Number],
    default: undefined,
  },
  rows: {
    type: [String, Number],
    default: 3,
  },
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const idGenerado = useId()
const controlId = computed(() => props.id || `campo-${idGenerado}`)
const hintId = computed(() => `${controlId.value}-hint`)
const errorId = computed(() => `${controlId.value}-error`)

const descritoPor = computed(() => {
  const ids = []
  if (props.hint) {
    ids.push(hintId.value)
  }
  if (props.error) {
    ids.push(errorId.value)
  }
  return ids.length ? ids.join(' ') : undefined
})

const clasesControl = computed(() => [
  props.as === 'select' ? 'form-select' : 'form-control',
  {
    'is-invalid': Boolean(props.error),
    'is-valid': props.valido && !props.error,
  },
])

function actualizarValor(event) {
  emit('update:modelValue', event.target.value)
}
</script>

<template>
  <div class="campo">
    <label :for="controlId" class="form-label">
      {{ label }}
      <span v-if="required" class="text-secondary small">({{ ETIQUETA_OBLIGATORIO }})</span>
      <span v-else-if="optional" class="text-secondary small">({{ ETIQUETA_OPCIONAL }})</span>
    </label>

    <input
      v-if="as === 'input'"
      :id="controlId"
      :type="type"
      :value="modelValue"
      :class="clasesControl"
      :placeholder="placeholder || undefined"
      :autocomplete="autocomplete"
      :inputmode="inputmode"
      :min="min"
      :max="max"
      :step="step"
      :disabled="disabled"
      :required="required"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="descritoPor"
      v-bind="$attrs"
      @input="actualizarValor"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    />

    <select
      v-else-if="as === 'select'"
      :id="controlId"
      :value="modelValue"
      :class="clasesControl"
      :disabled="disabled"
      :required="required"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="descritoPor"
      v-bind="$attrs"
      @change="actualizarValor"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    >
      <slot name="options" />
    </select>

    <textarea
      v-else
      :id="controlId"
      :value="modelValue"
      :class="clasesControl"
      :placeholder="placeholder || undefined"
      :rows="rows"
      :disabled="disabled"
      :required="required"
      :aria-invalid="error ? 'true' : undefined"
      :aria-describedby="descritoPor"
      v-bind="$attrs"
      @input="actualizarValor"
      @blur="emit('blur', $event)"
      @focus="emit('focus', $event)"
    ></textarea>

    <div v-if="hint" :id="hintId" class="form-text">{{ hint }}</div>
    <div v-if="error" :id="errorId" class="invalid-feedback d-block" role="alert">
      {{ error }}
    </div>
  </div>
</template>

<style scoped>
.campo {
  width: 100%;
  min-width: 0;
}

.campo textarea {
  resize: vertical;
}

.campo .invalid-feedback {
  overflow-wrap: anywhere;
}
</style>
