import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { alertsAPI } from '../services/api'
import { CheckCircle, XCircle, Clock, Filter, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

export default function AlertManagement() {
  const { t } = useTranslation()
  const queryClient = useQueryClient()
  const [filter, setFilter] = useState({ type: '', severity: '', is_read: '' })

  const { data, isLoading } = useQuery(['alerts', filter], () => alertsAPI.getAll(filter))

  const markReadMutation = useMutation(alertsAPI.markAsRead, {
    onSuccess: () => {
      queryClient.invalidateQueries('alerts')
      queryClient.invalidateQueries('unread-alerts')
    },
  })

  const markAllReadMutation = useMutation(alertsAPI.markAllAsRead, {
    onSuccess: () => {
      queryClient.invalidateQueries('alerts')
      queryClient.invalidateQueries('unread-alerts')
      toast.success(t('success'))
    },
  })

  const alerts = data?.data?.results || data?.data || []

  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'CRITICAL':
      case 'HIGH':
        return <XCircle className="w-5 h-5 text-red-500" />
      case 'MEDIUM':
        return <Clock className="w-5 h-5 text-yellow-500" />
      default:
        return <CheckCircle className="w-5 h-5 text-green-500" />
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('alerts')}</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Manage and resolve biopiracy alerts
          </p>
        </div>
        <button
          onClick={() => markAllReadMutation.mutate()}
          className="btn-secondary"
        >
          <CheckCircle className="w-4 h-4" />
          {t('mark_all_read')}
        </button>
      </div>

      <div className="kpi-card">
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <select
            value={filter.type}
            onChange={(e) => setFilter({ ...filter, type: e.target.value })}
            className="form-input"
          >
            <option value="">All Types</option>
            <option value="BIOPIRACY">Biopiracy</option>
            <option value="PATENT">Patent</option>
            <option value="GI_TAG">GI Tag</option>
            <option value="SYSTEM">System</option>
            <option value="TKDL">TKDL</option>
          </select>
          <select
            value={filter.severity}
            onChange={(e) => setFilter({ ...filter, severity: e.target.value })}
            className="form-input"
          >
            <option value="">All Severities</option>
            <option value="CRITICAL">Critical</option>
            <option value="HIGH">High</option>
            <option value="MEDIUM">Medium</option>
            <option value="LOW">Low</option>
            <option value="INFO">Info</option>
          </select>
          <select
            value={filter.is_read}
            onChange={(e) => setFilter({ ...filter, is_read: e.target.value })}
            className="form-input"
          >
            <option value="">All Status</option>
            <option value="false">Unread</option>
            <option value="true">Read</option>
          </select>
        </div>
      </div>

      <div className="kpi-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('status')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Title</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Type</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('priority')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('date')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('actions')}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {isLoading ? (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    {t('loading')}
                  </td>
                </tr>
              ) : alerts.length === 0 ? (
                <tr>
                  <td colSpan="6" className="px-4 py-8 text-center text-gray-500">
                    {t('no_notifications')}
                  </td>
                </tr>
              ) : (
                alerts.map((alert) => (
                  <tr key={alert.id} className={`table-row ${!alert.is_read ? 'bg-blue-50 dark:bg-blue-900/20' : ''}`}>
                    <td className="px-4 py-3">
                      {getSeverityIcon(alert.severity)}
                    </td>
                    <td className="px-4 py-3">
                      <p className="text-sm font-medium text-gray-900 dark:text-white">
                        {alert.title}
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-1">
                        {alert.message}
                      </p>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs px-2 py-1 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-300">
                        {alert.type_display || alert.type}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        alert.severity === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                        alert.severity === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {alert.severity_display || alert.severity}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                      {new Date(alert.created_at).toLocaleString('en-IN')}
                    </td>
                    <td className="px-4 py-3">
                      {!alert.is_read && (
                        <button
                          onClick={() => markReadMutation.mutate(alert.id)}
                          className="text-primary-600 hover:text-primary-700 text-sm"
                        >
                          Mark Read
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
