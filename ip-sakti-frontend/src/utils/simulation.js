import { alertsAPI } from '../services/api'
import toast from 'react-hot-toast'

export async function simulateAlert() {
  try {
    const response = await alertsAPI.getAll()
    const alerts = response.data?.results || response.data || []
    if (alerts.length > 0) {
      return alerts[0]
    }
    return null
  } catch {
    return null
  }
}

export function downloadCSV(data, filename) {
  const headers = Object.keys(data[0] || {})
  const csv = [
    headers.join(','),
    ...data.map(row => headers.map(h => `"${row[h] || ''}"`).join(','))
  ].join('\n')

  const blob = new Blob([csv], { type: 'text/csv' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${filename}.csv`
  a.click()
}

export function downloadPDF(data, filename) {
  toast.success('PDF export feature - use browser print or external library')
}

export function formatNumber(num) {
  return new Intl.NumberFormat('en-IN').format(num || 0)
}

export function formatCurrency(num) {
  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0,
  }).format(num || 0)
}

export function formatDate(date) {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function debounce(func, wait) {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

export function getStatusColor(status) {
  const colors = {
    RESOLVED: 'bg-green-100 text-green-800',
    PENDING: 'bg-yellow-100 text-yellow-800',
    DETECTED: 'bg-red-100 text-red-800',
    FILED: 'bg-blue-100 text-blue-800',
    GRANTED: 'bg-green-100 text-green-800',
    REGISTERED: 'bg-green-100 text-green-800',
  }
  return colors[status] || 'bg-gray-100 text-gray-800'
}
