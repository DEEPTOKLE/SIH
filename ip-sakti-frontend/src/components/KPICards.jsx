import React from 'react'
import { useTranslation } from 'react-i18next'
import { Award, FileText, AlertTriangle, BookOpen, TrendingUp, CheckCircle } from 'lucide-react'

const KPI_CONFIG = [
  { key: 'total_gi_tags', label: 'total_gi_tags', icon: Award, color: 'text-green-600', bg: 'bg-green-50' },
  { key: 'total_patents', label: 'patents_filed', icon: FileText, color: 'text-blue-600', bg: 'bg-blue-50' },
  { key: 'total_biopiracy_alerts', label: 'biopiracy_alerts', icon: AlertTriangle, color: 'text-red-600', bg: 'bg-red-50' },
  { key: 'texts_digitized', label: 'texts_digitized', icon: BookOpen, color: 'text-purple-600', bg: 'bg-purple-50' },
  { key: 'active_biopiracy_cases', label: 'active_cases', icon: TrendingUp, color: 'text-orange-600', bg: 'bg-orange-50' },
  { key: 'india_prior_art_success', label: 'india_prior_art_success', icon: CheckCircle, color: 'text-primary-600', bg: 'bg-primary-50' },
]

export default function KPICards({ kpis, isLoading }) {
  const { t } = useTranslation()

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      {KPI_CONFIG.map((item) => {
        const Icon = item.icon
        const value = kpis[item.key] || 0
        return (
          <div key={item.key} className="kpi-card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">{t(item.label)}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white mt-1">
                  {isLoading ? '...' : value.toLocaleString()}
                </p>
              </div>
              <div className={`p-3 rounded-lg ${item.bg}`}>
                <Icon className={`w-6 h-6 ${item.color}`} />
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
