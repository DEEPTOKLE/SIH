import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from 'react-query'
import { dashboardAPI } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { BarChart3 } from 'lucide-react'

export default function Analytics() {
  const { t } = useTranslation()
  const [selectedMetric, setSelectedMetric] = useState('gi_tags')

  const { data: stateData, isLoading } = useQuery(
    'state-analytics',
    () => dashboardAPI.getKPIs(),
    { refetchInterval: 300000 }
  )

  const kpis = stateData?.data || {}

  const stateWiseData = kpis.state_wise_data || []
  const chartData = stateWiseData.slice(0, 15).map(state => ({
    name: state.state_name,
    gi_tags: state.gi_tags || 0,
    patents: state.patents || 0,
    formulations: state.formulations || 0,
    biopiracy_cases: state.biopiracy_cases || 0,
  }))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('analytics')}</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Comparative analysis and insights for policy decisions
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="kpi-card">
          <p className="text-sm text-gray-600 dark:text-gray-400">{t('total_gi_tags')}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {kpis.total_gi_tags || 0}
          </p>
        </div>
        <div className="kpi-card">
          <p className="text-sm text-gray-600 dark:text-gray-400">{t('total_patents')}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {kpis.total_patents || 0}
          </p>
        </div>
        <div className="kpi-card">
          <p className="text-sm text-gray-600 dark:text-gray-400">{t('active_biopiracy_cases')}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {kpis.active_biopiracy_cases || 0}
          </p>
        </div>
        <div className="kpi-card">
          <p className="text-sm text-gray-600 dark:text-gray-400">{t('texts_digitized')}</p>
          <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">
            {kpis.texts_digitized || 0}
          </p>
        </div>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          {t('state_wise_analytics')} - Top 15 States
        </h3>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
            <XAxis dataKey="name" className="text-xs fill-gray-600 dark:fill-gray-400" angle={-45} textAnchor="end" height={100} />
            <YAxis className="text-xs fill-gray-600 dark:fill-gray-400" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgb(255, 255, 255)',
                border: '1px solid rgb(203, 213, 225)',
                borderRadius: '0.5rem',
              }}
            />
            <Legend />
            <Bar dataKey="gi_tags" fill="#22c55e" name={t('gi_tags_count')} />
            <Bar dataKey="patents" fill="#3b82f6" name={t('patents_count')} />
            <Bar dataKey="formulations" fill="#f59e0b" name={t('formulations_count')} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Biopiracy Cases by State
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
            <XAxis dataKey="name" className="text-xs fill-gray-600 dark:fill-gray-400" />
            <YAxis className="text-xs fill-gray-600 dark:fill-gray-400" />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgb(255, 255, 255)',
                border: '1px solid rgb(203, 213, 225)',
                borderRadius: '0.5rem',
              }}
            />
            <Legend />
            <Bar dataKey="biopiracy_cases" fill="#ef4444" name={t('biopiracy_cases_count')} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          {t('category_distribution')}
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {Object.entries(kpis.category_distribution || {}).map(([category, values]) => (
            <div key={category} className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                {category}
              </h4>
              <div className="space-y-1">
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  GI Tags: {values?.gi_tags || 0}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Patents: {values?.patents || 0}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Formulations: {values?.formulations || 0}
                </p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
