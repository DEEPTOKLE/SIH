import React, { useState, useEffect } from 'react'
import { useTranslation } from 'react-i18next'
import { useQuery } from 'react-query'
import { biopiracyAPI } from '../services/api'
import { Filter, Download, Search } from 'lucide-react'

export default function CaseTracker() {
  const { t } = useTranslation()
  const [filters, setFilters] = useState({
    state: '',
    status: '',
    priority: '',
    date_from: '',
    date_to: '',
    search: '',
  })
  const [page, setPage] = useState(1)

  const { data, isLoading } = useQuery(
    ['biopiracy-cases', filters, page],
    () => biopiracyAPI.getAll({
      ...filters,
      page,
    }),
    { keepPreviousData: true }
  )

  const cases = data?.data?.results || data?.data || []
  const handleExport = () => {
    const csv = [
      ['ID', 'Patent', 'Status', 'Priority', 'Date', 'Assigned To'].join(','),
      ...cases.map(c => [
        c.id,
        `"${c.patent_title || ''}"`,
        c.status_display || c.status,
        c.priority_display || c.priority,
        c.detected_date,
        c.assigned_to_name || 'Unassigned',
      ].join(','))
    ].join('\n')

    const blob = new Blob([csv], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'biopiracy_cases.csv'
    a.click()
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('case_tracker')}</h1>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
            Track and manage biopiracy cases
          </p>
        </div>
        <button onClick={handleExport} className="btn-primary">
          <Download className="w-4 h-4" />
          {t('export_csv')}
        </button>
      </div>

      <div className="kpi-card">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-2.5 w-4 h-4 text-gray-400" />
            <input
              type="text"
              placeholder={t('search')}
              value={filters.search}
              onChange={(e) => setFilters({ ...filters, search: e.target.value })}
              className="form-input pl-10"
            />
          </div>
          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            className="form-input"
          >
            <option value="">{t('all_status')}</option>
            <option value="DETECTED">{t('detected')}</option>
            <option value="UNDER_REVIEW">{t('under_review')}</option>
            <option value="ESCALATED">Escalated</option>
            <option value="PRIOR_ART_FILED">Prior Art Filed</option>
            <option value="RESOLVED">{t('resolved')}</option>
            <option value="FALSE_POSITIVE">False Positive</option>
            <option value="CLOSED">Closed</option>
          </select>
          <select
            value={filters.priority}
            onChange={(e) => setFilters({ ...filters, priority: e.target.value })}
            className="form-input"
          >
            <option value="">{t('all')} {t('priority')}</option>
            <option value="CRITICAL">{t('critical')}</option>
            <option value="HIGH">{t('high')}</option>
            <option value="MEDIUM">{t('medium')}</option>
            <option value="LOW">{t('low')}</option>
          </select>
          <input
            type="date"
            value={filters.date_from}
            onChange={(e) => setFilters({ ...filters, date_from: e.target.value })}
            className="form-input"
            placeholder={t('from_date')}
          />
          <input
            type="date"
            value={filters.date_to}
            onChange={(e) => setFilters({ ...filters, date_to: e.target.value })}
            className="form-input"
            placeholder={t('to_date')}
          />
        </div>
      </div>

      <div className="kpi-card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">ID</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Patent Title</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('status')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('priority')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('date')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('assigned_to')}</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">{t('actions')}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
              {isLoading ? (
                <tr>
                  <td colSpan="7" className="px-4 py-8 text-center text-gray-500">
                    {t('loading')}
                  </td>
                </tr>
              ) : cases.length === 0 ? (
                <tr>
                  <td colSpan="7" className="px-4 py-8 text-center text-gray-500">
                    {t('no_results_found')}
                  </td>
                </tr>
              ) : (
                cases.map((c) => (
                  <tr key={c.id} className="table-row">
                    <td className="px-4 py-3 text-sm text-gray-900 dark:text-white font-mono">
                      {c.id?.slice(0, 8)}...
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 dark:text-white">
                      {c.patent_title}
                    </td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        c.status === 'RESOLVED' ? 'bg-green-100 text-green-800' :
                        c.status === 'CRITICAL' || c.priority === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                      }`}>
                        {c.status_display || c.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <span className={`text-xs px-2 py-1 rounded-full ${
                        c.priority === 'CRITICAL' ? 'bg-red-100 text-red-800' :
                        c.priority === 'HIGH' ? 'bg-orange-100 text-orange-800' :
                        c.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-blue-100 text-blue-800'
                      }`}>
                        {c.priority_display || c.priority}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                      {new Date(c.detected_date).toLocaleDateString('en-IN')}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-600 dark:text-gray-400">
                      {c.assigned_to_name || '-'}
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <button className="text-primary-600 hover:text-primary-700 text-sm">
                          {t('view')}
                        </button>
                        {c.status !== 'RESOLVED' && (
                          <button className="text-green-600 hover:text-green-700 text-sm">
                            {t('resolve')}
                          </button>
                        )}
                      </div>
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
