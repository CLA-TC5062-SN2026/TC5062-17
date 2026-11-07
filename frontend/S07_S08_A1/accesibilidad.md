# Evaluación de accesibilidad WCAG 2.1

**Proyecto:** MLState  
**Componentes revisados:** `BaseButton`, `BaseInput`, `BaseCard`, `AppNavbar`  
**Nivel objetivo:** WCAG 2.1 AA  
**Fecha:** 2026-11-06

## Resumen ejecutivo

Se revisaron contraste, nombres accesibles, elementos decorativos, foco visible y navegación por teclado. Se corrigieron cuatro hallazgos:

1. Contraste insuficiente de `outline-secondary` y del texto secundario sobre el fondo de la aplicación.
2. Contraste insuficiente de `outline-danger` y del mensaje de error de `BaseInput`.
3. Contraste reducido del botón en estado de carga por la opacidad de `:disabled`.
4. Nombre accesible incompleto del botón hamburguesa y falta de cierre con `Escape`.

El foco visible ya estaba cubierto globalmente; se verificó y se conservó. Resultado final: **22 pruebas aprobadas** y compilación de producción correcta.

## Metodología

Los ratios se calcularon con la fórmula de luminancia relativa de WCAG 2.1 sobre los colores hex compilados de Bootstrap y los tokens del proyecto. Para estados con transparencia se calculó el color efectivo resultante de la mezcla con el fondo.

Criterios utilizados:

- **1.4.3 Contrast (Minimum), AA:** 4.5:1 para texto normal y 3:1 para texto grande.
- **1.4.11 Non-text Contrast, AA:** 3:1 para componentes de interfaz y elementos gráficos.
- **2.1.1 Keyboard, A:** toda funcionalidad disponible con teclado.
- **2.4.3 Focus Order, A:** orden de foco lógico.
- **2.4.7 Focus Visible, AA:** indicador de foco visible.
- **4.1.2 Name, Role, Value, A:** nombre, rol y estado programáticamente determinables.

## 1. Contraste de color

### Estado final de las combinaciones revisadas

| Componente / variante | Texto | Fondo | Ratio | Cumple |
|---|---|---:|---:|---|
| `BaseButton` primary | `#ffffff` | `#0b5d8a` | 7.13:1 | Sí, AA |
| `BaseButton` primary hover | `#ffffff` | `#094f75` | 8.80:1 | Sí, AA |
| `BaseButton` secondary | `#ffffff` | `#6c757d` | 4.69:1 | Sí, AA |
| `BaseButton` secondary hover | `#ffffff` | `#5c636a` | 6.09:1 | Sí, AA |
| `BaseButton` outline-primary sobre fondo de app | `#0b5d8a` | `#f7f8fa` | 6.71:1 | Sí, AA |
| `BaseButton` outline-primary sobre blanco | `#0b5d8a` | `#ffffff` | 7.13:1 | Sí, AA |
| `BaseButton` outline-primary hover | `#ffffff` | `#0b5d8a` | 7.13:1 | Sí, AA |
| `BaseButton` outline-secondary sobre fondo de app | `#495057` | `#f7f8fa` | 7.69:1 | Sí, AA |
| `BaseButton` outline-secondary sobre blanco | `#495057` | `#ffffff` | 8.18:1 | Sí, AA |
| `BaseButton` outline-secondary hover | `#ffffff` | `#495057` | 8.18:1 | Sí, AA |
| `BaseButton` outline-danger sobre fondo de app | `#b02a37` | `#f7f8fa` | 6.11:1 | Sí, AA |
| `BaseButton` outline-danger sobre blanco | `#b02a37` | `#ffffff` | 6.50:1 | Sí, AA |
| `BaseButton` outline-danger hover | `#ffffff` | `#b02a37` | 6.50:1 | Sí, AA |
| Texto secundario (`text-secondary`) sobre fondo de app | `#495057` | `#f7f8fa` | 7.69:1 | Sí, AA |
| Texto secundario sobre blanco | `#495057` | `#ffffff` | 8.18:1 | Sí, AA |
| Error de `BaseInput` sobre fondo de app | `#b02a37` | `#f7f8fa` | 6.11:1 | Sí, AA |
| Error de `BaseInput` sobre blanco | `#b02a37` | `#ffffff` | 6.50:1 | Sí, AA |
| Texto de ayuda de `BaseInput` | `#555d65` efectivo | `#f7f8fa` | 6.31:1 | Sí, AA |
| Texto de cuerpo de `BaseCard` | `#1f2933` | `#ffffff` | 14.76:1 | Sí, AA |
| Enlace de navbar por defecto | `#565758` efectivo | `#f7f8fa` | 6.82:1 | Sí, AA |
| Enlace de navbar activo | `#000000` | `#f7f8fa` | 19.76:1 | Sí, AA |
| Icono hamburguesa (no texto) | `#555d65` efectivo | `#f7f8fa` | 6.31:1 | Sí, 1.4.11 |
| Anillo de foco (no texto) | `#0b5d8a` | `#f7f8fa` | 6.71:1 | Sí, 1.4.11 |

Los estados `disabled` conservan la excepción de componentes inactivos de WCAG 1.4.3. El estado `loading` sí se corrigió para mantener legibilidad, porque comunica una acción en curso.

## 2. Problemas encontrados y correcciones

### Problema crítico 1: texto secundario y `outline-secondary` con contraste insuficiente

- **Componentes afectados:** `BaseButton`, `BaseInput` y textos `text-secondary` sobre el fondo `#f7f8fa`.
- **Criterio WCAG incumplido:** 1.4.3 Contrast (Minimum), AA.
- **Antes:** `#6c757d` sobre `#f7f8fa` = **4.41:1**. No alcanza 4.5:1 para texto normal.

```scss
// Antes: valor por defecto de Bootstrap
.btn-outline-secondary {
  --bs-btn-color: #6c757d;
  --bs-btn-border-color: #6c757d;
  --bs-btn-hover-bg: #6c757d;
}

.text-secondary {
  color: #6c757d !important;
}
```

- **Después:** se usa `#495057`, con **7.69:1** sobre `#f7f8fa` y **8.18:1** sobre blanco.

```scss
// _variables.scss
$ml-secondary-text: #495057;

// main.scss
:root {
  --ml-color-secondary-text: #{v.$ml-secondary-text};
}

.text-secondary {
  color: var(--ml-color-secondary-text) !important;
}

.btn-outline-secondary {
  --bs-btn-color: var(--ml-color-secondary-text);
  --bs-btn-border-color: var(--ml-color-secondary-text);
  --bs-btn-hover-bg: var(--ml-color-secondary-text);
  --bs-btn-hover-border-color: var(--ml-color-secondary-text);
  --bs-btn-active-bg: var(--ml-color-secondary-text);
  --bs-btn-active-border-color: var(--ml-color-secondary-text);
  --bs-btn-disabled-color: var(--ml-color-secondary-text);
  --bs-btn-disabled-border-color: var(--ml-color-secondary-text);
}
```

### Problema crítico 2: `outline-danger` y error de formulario con contraste insuficiente

- **Componentes afectados:** `BaseButton` (`outline-danger`) y `BaseInput` (`invalid-feedback`).
- **Criterio WCAG incumplido:** 1.4.3 Contrast (Minimum), AA.
- **Antes:** `#dc3545` sobre `#f7f8fa` = **4.26:1**. No alcanza 4.5:1.

```scss
// Antes: valor por defecto de Bootstrap
:root {
  --bs-form-invalid-color: #dc3545;
  --bs-form-invalid-border-color: #dc3545;
}

.btn-outline-danger {
  --bs-btn-color: #dc3545;
  --bs-btn-border-color: #dc3545;
  --bs-btn-hover-bg: #dc3545;
}
```

- **Después:** se usa `#b02a37`, con **6.11:1** sobre `#f7f8fa` y **6.50:1** sobre blanco.

```scss
// _variables.scss
$ml-danger-text: #b02a37;

// main.scss
:root {
  --ml-color-danger-text: #{v.$ml-danger-text};
  --bs-form-invalid-color: var(--ml-color-danger-text);
  --bs-form-invalid-border-color: var(--ml-color-danger-text);
}

.btn-outline-danger {
  --bs-btn-color: var(--ml-color-danger-text);
  --bs-btn-border-color: var(--ml-color-danger-text);
  --bs-btn-hover-bg: var(--ml-color-danger-text);
  --bs-btn-hover-border-color: var(--ml-color-danger-text);
  --bs-btn-active-bg: var(--ml-color-danger-text);
  --bs-btn-active-border-color: var(--ml-color-danger-text);
  --bs-btn-disabled-color: var(--ml-color-danger-text);
  --bs-btn-disabled-border-color: var(--ml-color-danger-text);
}
```

### Problema adicional: opacidad del botón en estado de carga

- **Componente afectado:** `BaseButton`.
- **Criterio WCAG relacionado:** 1.4.3 Contrast (Minimum), AA.
- **Antes:** Bootstrap aplica `opacity: .65` a `:disabled`; el texto “Cargando…” reducía su contraste.
- **Después:** el estado de carga mantiene opacidad completa.

```vue
<!-- BaseButton.vue -->
<style scoped>
.btn[aria-busy='true']:disabled {
  opacity: 1;
}
</style>
```

## 3. Elementos sin texto visible

| Elemento | Estado | Acción |
|---|---|---|
| Spinner de `BaseButton` | Ya tenía `aria-hidden="true"` y el botón usa `aria-busy="true"` | Sin cambio; se agregó una prueba para evitar regresiones |
| Texto de carga de `BaseButton` | Es texto visible; sustituye al contenido original | Accesible por nombre del botón |
| Icono hamburguesa de `AppNavbar` | No tenía `aria-hidden` | Se agregó `aria-hidden="true"` al `<span>` decorativo |
| Botón hamburguesa | Tenía `aria-label="Abrir menú"` fijo | Se hizo dinámico: “Abrir menú” / “Cerrar menú” |
| Spinners de `ResultadoPage` e `HistorialPage` | Ya tenían `aria-hidden="true"` | Sin cambio |
| Otros iconos decorativos | No se encontraron iconos adicionales sin texto alternativo | Sin acción |

### Corrección del botón hamburguesa

- **Componente afectado:** `AppNavbar`.
- **Criterio WCAG incumplido:** 4.1.2 Name, Role, Value, A.
- **Antes:** el nombre accesible no reflejaba el estado abierto y el icono decorativo no estaba oculto.

```vue
<button
  class="navbar-toggler"
  type="button"
  :aria-expanded="menuAbierto"
  :aria-controls="menuId"
  aria-label="Abrir menú"
  @click="alternarMenu"
>
  <span class="navbar-toggler-icon"></span>
</button>
```

- **Después:**

```vue
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
```

## 4. Manejo de foco y navegación con teclado

### Foco visible

Se verificó que los elementos interactivos revisados usan un indicador visible definido en `main.scss`:

```scss
.btn:focus-visible,
.form-control:focus-visible,
.form-select:focus-visible,
.nav-link:focus-visible,
.navbar-toggler:focus-visible,
a:focus-visible {
  outline: 3px solid #0b5d8a;
  outline-offset: 2px;
}
```

- **Criterio WCAG:** 2.4.7 Focus Visible, AA.
- **Contraste del indicador:** `#0b5d8a` sobre `#f7f8fa` = **6.71:1**; sobre blanco = **7.13:1**. Supera el 3:1 exigido para componentes no textuales (1.4.11).
- **Resultado:** sin hallazgos pendientes en `BaseButton`, `BaseInput`, `BaseCard` ni `AppNavbar`.

### Navegación con teclado y cierre con Escape

- **Componente afectado:** `AppNavbar`.
- **Criterios WCAG incumplidos:** 2.1.1 Keyboard, A; 2.4.3 Focus Order, A.
- **Antes:** el menú se abría con clic o Enter/Espacio en el botón, pero `Escape` no lo cerraba ni devolvía el foco al botón.
- **Después:** `Escape` cierra el menú y devuelve el foco al botón hamburguesa.

```js
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
```

```vue
<nav
  class="navbar navbar-expand-lg page-container"
  :aria-label="ariaLabel"
  @keydown.esc="alPresionarEscape"
>
```

**Orden de tabulación revisado:**

1. Marca `MLState`.
2. Botón hamburguesa (solo visible en móvil).
3. Enlaces `Estimar`, `Historial`/`Componentes` cuando correspondan.
4. Acciones de sesión: `Iniciar sesión`/`Crear cuenta` o `Cerrar sesión`.

Cuando el menú está cerrado en móvil, `.collapse:not(.show)` mantiene los enlaces con `display: none`, por lo que no reciben foco. En escritorio el botón hamburguesa está oculto y el menú permanece visible.

## 5. Verificación posterior

- `npm run test:run`: **22 pruebas aprobadas** (5 archivos).
- Se agregaron pruebas para:
  - `aria-hidden="true"` del spinner de `BaseButton`.
  - Nombre dinámico y `aria-hidden` del icono hamburguesa.
  - Cierre del menú con `Escape` y retorno de foco al botón.
- `npm run build`: compilación de producción correcta.
- La verificación se ejecutó en una copia temporal con Node 22, sin modificar el `node_modules` instalado en Windows.

## Conclusión

Los componentes revisados cumplen los criterios WCAG 2.1 AA evaluados para contraste de texto, contraste de componentes no textuales, nombres accesibles, foco visible y navegación básica por teclado. El único punto que depende de revisión manual adicional es la validación visual en dispositivos y anchos reales, especialmente en móvil.
