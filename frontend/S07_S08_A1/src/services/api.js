import { API_BASE_URL, API_TIMEOUT_MS } from '@/config/env'

const DEFAULT_TIMEOUT_MS = API_TIMEOUT_MS

let accessToken = null
let unauthorizedHandler = null

export function setAccessToken(token) {
  accessToken = token
}

export function setUnauthorizedHandler(handler) {
  unauthorizedHandler = handler
}

export class ApiError extends Error {
  constructor({
    status = 0,
    codigo = 'ERROR_DESCONOCIDO',
    mensaje = 'Ocurrió un error inesperado',
    traceId = null,
    errores = null,
  } = {}) {
    super(mensaje)
    this.name = 'ApiError'
    this.status = status
    this.codigo = codigo
    this.traceId = traceId
    this.errores = errores
  }
}

function buildUrl(path, query) {
  const url = `${API_BASE_URL}${path}`
  if (!query) return url

  const params = new URLSearchParams()
  Object.entries(query).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      params.append(key, String(value))
    }
  })

  const serialized = params.toString()
  return serialized ? `${url}?${serialized}` : url
}

async function readBody(response) {
  const text = await response.text()
  if (!text) return null
  try {
    return JSON.parse(text)
  } catch {
    return null
  }
}

async function request(
  path,
  {
    method = 'GET',
    body,
    query,
    headers = {},
    timeout = DEFAULT_TIMEOUT_MS,
    responseType = 'json',
  } = {},
) {
  const controller = new AbortController()
  const timer = globalThis.setTimeout(() => controller.abort(), timeout)

  try {
    const response = await fetch(buildUrl(path, query), {
      method,
      credentials: 'include',
      headers: {
        Accept: responseType === 'blob' ? 'application/pdf' : 'application/json',
        ...(body !== undefined ? { 'Content-Type': 'application/json' } : {}),
        ...(accessToken ? { Authorization: `Bearer ${accessToken}` } : {}),
        ...headers,
      },
      body: body !== undefined ? JSON.stringify(body) : undefined,
      signal: controller.signal,
    })

    if (response.status === 401 && unauthorizedHandler) {
      unauthorizedHandler()
    }

    if (!response.ok) {
      const payload = await readBody(response)
      throw new ApiError({
        status: response.status,
        codigo: payload?.codigo ?? 'ERROR_DESCONOCIDO',
        mensaje: payload?.mensaje ?? 'La solicitud no pudo completarse',
        traceId: payload?.traceId ?? null,
        errores: payload?.errores ?? null,
      })
    }

    if (responseType === 'blob') return response.blob()
    if (response.status === 204) return null
    return readBody(response)
  } catch (error) {
    if (error instanceof ApiError) throw error
    if (error?.name === 'AbortError') {
      throw new ApiError({
        status: 0,
        codigo: 'TIEMPO_DE_ESPERA_AGOTADO',
        mensaje: 'La solicitud excedió el tiempo de espera',
      })
    }
    throw new ApiError({
      status: 0,
      codigo: 'ERROR_DE_RED',
      mensaje: 'No fue posible conectar con el servicio',
    })
  } finally {
    globalThis.clearTimeout(timer)
  }
}

export const api = {
  get: (path, options = {}) => request(path, { ...options, method: 'GET' }),
  post: (path, body, options = {}) => request(path, { ...options, method: 'POST', body }),
  put: (path, body, options = {}) => request(path, { ...options, method: 'PUT', body }),
  delete: (path, options = {}) => request(path, { ...options, method: 'DELETE' }),
}
