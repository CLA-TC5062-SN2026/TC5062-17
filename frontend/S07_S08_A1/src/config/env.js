function leerVariable(nombre, valorPorDefecto) {
  const valor = import.meta.env[nombre]
  if (valor === undefined || valor === null || valor === '') return valorPorDefecto
  return String(valor)
}

function normalizarBaseUrl(url) {
  return url.replace(/\/+$/, '')
}

function leerTimeout(valor) {
  const numero = Number(valor)
  return Number.isFinite(numero) && numero > 0 ? numero : 30000
}

export const API_BASE_URL = normalizarBaseUrl(leerVariable('VITE_API_BASE_URL', '/api/v1'))
export const API_TIMEOUT_MS = leerTimeout(leerVariable('VITE_REQUEST_TIMEOUT_MS', '30000'))
export const ES_PRODUCCION = import.meta.env.PROD
