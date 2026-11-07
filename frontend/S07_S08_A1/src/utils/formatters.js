const formatoMoneda = new Intl.NumberFormat('es-MX', {
  style: 'currency',
  currency: 'MXN',
  maximumFractionDigits: 0,
})

export function formatearMoneda(valor) {
  if (valor === null || valor === undefined || Number.isNaN(Number(valor))) return '—'
  return formatoMoneda.format(Number(valor))
}

export function formatearFecha(valor) {
  if (!valor) return '—'

  if (typeof valor === 'string') {
    const soloFecha = valor.slice(0, 10)
    if (/^\d{4}-\d{2}-\d{2}$/.test(soloFecha)) return soloFecha
  }

  const fecha = new Date(valor)
  if (Number.isNaN(fecha.getTime())) return '—'

  const anio = fecha.getFullYear()
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')
  return `${anio}-${mes}-${dia}`
}
