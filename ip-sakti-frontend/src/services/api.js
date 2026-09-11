import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
            refresh: refreshToken,
          })
          const { access } = response.data
          localStorage.setItem('access_token', access)
          originalRequest.headers.Authorization = `Bearer ${access}`
          return api(originalRequest)
        }
      } catch {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export const authAPI = {
  login: (credentials) => api.post('/auth/token/', credentials),
  refresh: (refreshToken) => api.post('/auth/token/refresh/', { refresh: refreshToken }),
  verify: (token) => api.post('/auth/token/verify/', { token }),
  me: () => api.get('/users/me/'),
}

export const usersAPI = {
  getProfile: () => api.get('/users/me/'),
  updateProfile: (data) => api.patch('/users/me/', data),
  switchLanguage: (lang) => api.post('/users/switch_language/', { language: lang }),
}

export const dashboardAPI = {
  getKPIs: () => api.get('/dashboard/kpis/'),
  getStateAnalytics: (stateId) => api.get(`/dashboard/state-analytics/?state_id=${stateId}`),
  compareStates: (stateIds, metrics) => api.post('/dashboard/compare-states/', { state_ids: stateIds, metrics }),
}

export const giTagsAPI = {
  getAll: (params) => api.get('/gi-tags/', { params }),
  getStatistics: (params) => api.get('/gi-tags/statistics/', { params }),
}

export const patentsAPI = {
  getAll: (params) => api.get('/patents/', { params }),
  getStatistics: () => api.get('/patents/statistics/'),
  getRecent: (days) => api.get(`/patents/recent/?days=${days}`),
}

export const biopiracyAPI = {
  getAll: (params) => api.get('/biopiracy-cases/', { params }),
  getSummary: () => api.get('/biopiracy-cases/dashboard_summary/'),
  assign: (id, userId) => api.post(`/biopiracy-cases/${id}/assign/`, { user_id: userId }),
  resolve: (id, notes) => api.post(`/biopiracy-cases/${id}/resolve/`, { resolution_notes: notes }),
}

export const alertsAPI = {
  getAll: (params) => api.get('/alerts/', { params }),
  getUnreadCount: () => api.get('/alerts/unread-count/'),
  markAsRead: (id) => api.post(`/alerts/${id}/mark_read/`),
  markAllAsRead: () => api.post('/alerts/mark-all-read/'),
  getRecent: () => api.get('/alerts/recent/'),
}

export const tkdlAPI = {
  getAll: (params) => api.get('/tkdl/', { params }),
  getCoverageStats: () => api.get('/tkdl/coverage_stats/'),
}

export const statesAPI = {
  getAll: (params) => api.get('/states/', { params }),
}

export const activitiesAPI = {
  getAll: (params) => api.get('/activities/', { params }),
}

export const reportsAPI = {
  exportCSV: (endpoint) => api.get(`/${endpoint}/export_csv/`, { responseType: 'blob' }),
  exportPDF: (endpoint) => api.get(`/${endpoint}/export_pdf/`, { responseType: 'blob' }),
}

export default api
