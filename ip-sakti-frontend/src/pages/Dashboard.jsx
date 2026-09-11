import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from 'react-query'
import { dashboardAPI, alertsAPI } from '../services/api'
import KPICards from '../components/KPICards'
import IndiaMap from '../components/IndiaMap'
import CategoryChart from '../components/CategoryChart'
import MonthlyTrends from '../components/MonthlyTrends'
import RecentAlerts from '../components/RecentAlerts'
import SuccessStories from '../components/SuccessStories'
import { simulateAlert } from '../utils/simulation'
import { Play, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const { t } = useTranslation()
  const [selectedState, setSelectedState] = useState(null)

  const { data, isLoading, refetch } = useQuery('dashboard-kpis', dashboardAPI.getKPIs, {
    refetchInterval: 60000,
  })

  const { data: alertsData } = useQuery('recent-alerts', alertsAPI.getRecent, {
    refetchInterval: 30000,
  })

  const kpis = data?.data || {}

  const handleSimulateAlert = async () => {
    try {
      await simulateAlert()
      toast.success(t('simulate_alert') + ' - Done!')
      refetch()
    } catch {
      toast.error('Simulation failed')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('dashboard')}</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            {t('welcome_subtitle')}
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={handleSimulateAlert} className="btn-primary">
            <Play className="w-4 h-4" />
            {t('live_simulation')}
          </button>
          <button onClick={() => refetch()} className="btn-secondary">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </button>
        </div>
      </div>

      <KPICards kpis={kpis} isLoading={isLoading} />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="kpi-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t('state_wise_analytics')}
          </h3>
          <IndiaMap
            data={kpis.state_wise_data || []}
            onStateClick={setSelectedState}
            selectedState={selectedState}
          />
        </div>

        <div className="kpi-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t('category_distribution')}
          </h3>
          <CategoryChart data={kpis.category_distribution || {}} />
        </div>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          {t('monthly_trends')}
        </h3>
        <MonthlyTrends data={kpis.monthly_trends || {}} />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="kpi-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t('recent_alerts')}
          </h3>
          <RecentAlerts alerts={alertsData?.data?.slice(0, 5) || []} />
        </div>

        <div className="kpi-card">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
            {t('success_stories')}
          </h3>
          <SuccessStories />
        </div>
      </div>

      {selectedState && (
        <div className="kpi-card border-2 border-primary-500">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {selectedState.name} - {t('state_wise_analytics')}
            </h3>
            <button
              onClick={() => setSelectedState(null)}
              className="text-sm text-gray-500 hover:text-gray-700"
            >
              Close
            </button>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p className="text-2xl font-bold text-primary-600">{selectedState.gi_tags || 0}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('gi_tags_count')}</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p className="text-2xl font-bold text-primary-600">{selectedState.patents || 0}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('patents_count')}</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p className="text-2xl font-bold text-primary-600">{selectedState.formulations || 0}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('formulations_count')}</p>
            </div>
            <div className="text-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <p className="text-2xl font-bold text-primary-600">{selectedState.biopiracy_cases || 0}</p>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('biopiracy_cases_count')}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
