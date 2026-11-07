# Revisión de componentes esenciales de UI

**Proyecto:** MLState  
**Componentes revisados:** `BaseButton`, `BaseInput`, `BaseCard`, `AppNavbar`  
**Fecha:** 2026-11-06

## Criterios de revisión

En equipo revisamos cada componente contra estos criterios:

1. **Configuración explícita:** props tipadas, con valores por defecto y validadores cuando aplica.
2. **Comportamiento predecible:** eventos y slots documentados, sin efectos secundarios ocultos.
3. **Responsive básico:** ancho fluido, sin dimensiones fijas, adaptación a móvil y escritorio.
4. **Accesibilidad:** etiquetas asociadas, estados `aria-*`, foco visible y objetivos táctiles.
5. **Reutilización:** sin dependencias nuevas y con estilos encapsulados por componente.

## Resumen de cambios respecto a la propuesta inicial

| Componente | Propuesta inicial | Implementación final | Motivo del cambio |
|---|---|---|---|
| `BaseButton` | `variant`, `loading`, `disabled`, `size`, `block`, `type` | Se agregaron `loadingText` y la variante `outline-danger`; se añadieron estilos responsivos | Permitir textos de carga específicos (“Entrando…”, “Calculando…”) y cubrir acciones destructivas como eliminar |
| `BaseInput` | Solo `<input>` con `label`, `v-model`, `hint`, `error` | Se agregó `as` (`input`/`select`/`textarea`), `valido`, `disabled`, `autocomplete`, `inputmode`, `min`, `max`, `step`, `rows`, `id` autogenerado y estilos responsivos | Evitar duplicar el campo en los selects del formulario de estimación y mejorar teclados móviles y validación visual |
| `BaseCard` | `titulo`, `subtitulo`, slots `header`, default y `footer` | Se agregaron `etiqueta`, `cuerpoClass` y validación de etiquetas semánticas; se añadieron estilos responsivos | Permitir HTML semántico (`article`, `section`) y ajustar el padding sin romper el contenedor |
| `AppNavbar` | Navbar basado en el estado global de sesión | Se creó como reemplazo de `AppHeader`; se agregaron `estadoForzado`, `ariaLabel`, IDs únicos, enlace de demo solo en desarrollo y estilos responsivos | Poder mostrar ambos estados en la demo y pruebas, evitar IDs/landmarks duplicados y mejorar el comportamiento móvil |

## BaseButton

### Props y configuración

| Prop | Tipo | Default | Validación / uso |
|---|---|---|---|
| `variant` | `String` | `primary` | `primary`, `secondary`, `outline-primary`, `outline-secondary`, `outline-danger` |
| `size` | `String` | `md` | `sm`, `md`, `lg` |
| `type` | `String` | `button` | `button`, `submit`, `reset` |
| `loading` | `Boolean` | `false` | Muestra spinner, aplica `aria-busy` y deshabilita el botón |
| `disabled` | `Boolean` | `false` | Deshabilita el botón |
| `block` | `Boolean` | `false` | Aplica `w-100` |
| `loadingText` | `String` | `Cargando…` | Texto mostrado durante `loading` |

- **Evento:** `click`, emitido solo cuando el botón no está cargando ni deshabilitado.
- **Atributos adicionales:** se heredan al `<button>` (`aria-label`, `id`, etc.).

### Revisión responsiva

- Ancho máximo del 100 % y texto con salto de línea permitido.
- En pantallas menores a 576 px, los botones `size="lg"` ocupan el 100 % del ancho.
- La prop `block` permite ancho completo en cualquier tamaño.
- La altura mínima táctil de 48 px se hereda de `main.scss`.

### Cambios realizados y justificación

- Se agregó `loadingText` para que cada flujo muestre un mensaje coherente con la acción.
- Se agregó `outline-danger` para el botón de eliminar del historial sin crear estilos ad hoc.
- Se añadieron reglas `scoped` para evitar desbordes en móvil.

## BaseInput

### Props y configuración

| Prop | Tipo | Default | Validación / uso |
|---|---|---|---|
| `modelValue` | `String \| Number` | `''` | Valor del control |
| `label` | `String` | Requerido | Etiqueta asociada al control |
| `as` | `String` | `input` | `input`, `select`, `textarea` |
| `id` | `String` | Autogenerado | ID del control; se genera con `useId()` si se omite |
| `type` | `String` | `text` | Tipo del `<input>` |
| `required` | `Boolean` | `false` | Aplica `required` y muestra “(Obligatorio)” |
| `optional` | `Boolean` | `false` | Muestra “(Opcional)” cuando no es obligatorio |
| `hint` | `String` | `''` | Texto de ayuda asociado con `aria-describedby` |
| `error` | `String` | `''` | Activa `is-invalid`, `aria-invalid` y mensaje con `role="alert"` |
| `valido` | `Boolean` | `false` | Activa `is-valid` cuando no hay error |
| `disabled` | `Boolean` | `false` | Deshabilita el control |
| `placeholder` | `String` | `''` | Placeholder para input/textarea |
| `autocomplete` | `String` | `undefined` | Autocompletado del navegador |
| `inputmode` | `String` | `undefined` | Teclado móvil (`email`, `numeric`, `decimal`, etc.) |
| `min` / `max` | `String \| Number` | `undefined` | Límites para campos numéricos |
| `step` | `String \| Number` | `undefined` | Incremento para campos numéricos |
| `rows` | `String \| Number` | `3` | Filas del textarea |

- **Eventos:** `update:modelValue`, `blur`, `focus`.
- **Slot:** `options` para los `<option>` cuando `as="select"`.
- **Atributos adicionales:** se aplican al control interno (`minlength`, `name`, `pattern`, etc.).

### Revisión responsiva

- El componente ocupa el 100 % del ancho de su columna y usa `min-width: 0` para evitar desbordes en grids.
- Los controles conservan el ancho fluido de Bootstrap (`form-control` / `form-select`).
- El textarea permite redimensionamiento vertical.
- Los mensajes de error usan `overflow-wrap: anywhere` para no romper el layout.
- La fuente base de 1 rem evita el zoom automático en iOS.

### Cambios realizados y justificación

- Se amplió de solo `<input>` a `input`/`select`/`textarea` porque el formulario de estimación usa los tres controles y se buscaba una sola fuente de verdad para etiqueta, ayuda y validación.
- Se agregó `valido` para representar el estado correcto, no solo el error.
- Se agregó `id` autogenerado para que los consumidores no tengan que crear IDs manualmente.
- Se agregaron props para teclado móvil (`inputmode`) y validación nativa (`min`, `max`, `step`, `rows`).

## BaseCard

### Props y configuración

| Prop | Tipo | Default | Validación / uso |
|---|---|---|---|
| `titulo` | `String` | `''` | Título del header |
| `subtitulo` | `String` | `''` | Texto secundario del header |
| `etiqueta` | `String` | `div` | `div`, `section`, `article`, `aside` |
| `cuerpoClass` | `String` | `''` | Clases adicionales para el `card-body` |

- **Slots:** `header`, default y `footer`.
- **Atributos adicionales:** se heredan al contenedor raíz (`class`, `id`, etc.).

### Revisión responsiva

- Ancho fluido dentro del grid de Bootstrap, sin medidas fijas.
- `min-width: 0` y `overflow-wrap: anywhere` evitan desbordes por textos largos.
- Respeta las columnas responsive de las páginas (`col-12`, `col-md-6`, `col-lg-5`, etc.).
- Las tablas internas siguen usando `table-responsive`.

### Cambios realizados y justificación

- Se agregó `etiqueta` para permitir HTML semántico sin crear variantes del componente.
- Se agregó `cuerpoClass` para conservar paddings existentes (`p-4`, `py-5`) durante la refactorización.
- Se añadió validación de etiquetas para evitar valores arbitrarios.

## AppNavbar

### Props y configuración

| Prop | Tipo | Default | Validación / uso |
|---|---|---|---|
| `estadoForzado` | `String` | `null` | `autenticado`, `invitado`; útil para demo y pruebas |
| `ariaLabel` | `String` | `Navegación principal` | Etiqueta accesible del elemento `<nav>` |

- **Estado real:** se obtiene de `useSessionStore()` (`session.estaAutenticado`, `session.usuario`).
- **Menú móvil:** controlado con estado local, sin depender del JS de Bootstrap.
- **IDs:** generados con `useId()` para permitir varias instancias en la página de demo.

### Revisión responsiva

- Usa `navbar-expand-lg`: menú colapsable por debajo de 992 px.
- El botón de menú conserva el objetivo táctil de 48 px.
- En móvil, las acciones se apilan en columna y ocupan el ancho disponible.
- El nombre del usuario se trunca con `text-truncate` y muestra el valor completo en `title`.
- `min-width: 0` y `flex-shrink: 0` evitan que el navbar rompa el layout.

### Cambios realizados y justificación

- `AppHeader` se reemplazó por `AppNavbar` para que el nombre refleje su responsabilidad y cumpla el requisito del componente solicitado.
- Se agregó `estadoForzado` para poder mostrar los estados autenticado e invitado en una sola página de demo y probarlos de forma aislada.
- Se agregó `ariaLabel` para personalizar la etiqueta del landmark y evitar etiquetas duplicadas en la demo.
- El enlace “Componentes” solo se muestra en desarrollo para no exponer la demo en producción.
- El cierre de sesión usa `BaseButton`, manteniendo consistencia con el resto de la interfaz.

## Verificación

- `npm run test:run`: **22 pruebas aprobadas** (5 archivos).
- `npm run build`: compilación de producción correcta.

## Observaciones para siguientes iteraciones

- Validar visualmente la página `/componentes` en anchos de 320, 576, 768 y 992 px.
- Si se necesita un botón que navegue, mantener `RouterLink` con clases de Bootstrap o evaluar una prop `to` en `BaseButton` en una iteración futura.
- `BaseInput` reenvía los atributos no declarados al control interno; para espaciado del bloque conviene envolverlo en un contenedor o usar las clases del formulario.
