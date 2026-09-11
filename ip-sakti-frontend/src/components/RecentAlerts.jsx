import React from 'react'
import { useTranslation } from 'react-i18next'
import { AlertTriangle, CheckCircle, Clock } from 'lucide-react'

const SEVERITY_COLORS = {
  CRITICAL: 'bg-red-100 text-red-800 border-red-200',
  HIGH: 'bg-orange-100 text-orange-800 border-orange-200',
  MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  LOW: 'bg-blue-100 text-blue-800 border-blue-200',
  INFO: 'bg-gray-100 text-gray-800 border-gray-200',
}

export default function RecentAlerts({ alerts }) {
  const { t } = useTranslation()

  if (!alerts?.length) {
    return (
      <div className="text-center py-8 text-gray-500">
        {t('no_notifications')}
      </div>
    )
  }

  return (
    <div className="space-y-3 max-h-80 overflow-y-auto scrollbar-thin">
      {alerts.map((alert) => (
        <div
          key={alert.id}
          className="flex items-start gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600"
        >
          <div className="flex-shrink-0 mt-0.5">
            {alert.severity === 'CRITICAL' || alert.severity === 'HIGH' ? (
              <AlertTriangle className="w-5 h-5 text-red-500" />
            ) : (
              <Clock className="w-5 h-5 text-gray-400" />
            )}
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
              {alert.title}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
              {alert.message}
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className={`text-xs px-2 py-0.5 rounded-full border ${SEVERITY_COLORS[alert.severity] || SEVERITY_COLORS.INFO}`}>
                {alert.severity_display || alert.severity}
              </span>
              <span className="text-xs text-gray-400">
                {new Date(alert.created_at).toLocaleDateString('en-IN')}
              </span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
