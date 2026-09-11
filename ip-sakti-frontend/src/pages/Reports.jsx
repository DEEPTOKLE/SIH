import React, { useState } from 'react'
import { useTranslation } from 'react-i18next'
import { Download, FileText, FileSpreadsheet, Calendar } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Reports() {
  const { t } = useTranslation()
  const [selectedReport, setSelectedReport] = useState('')
  const [dateRange, setDateRange] = useState({ from: '', to: '' })

  const reports = [
    {
      id: 'gi_tags',
      name: 'GI Tags Report',
      description: 'Comprehensive report on all GI tags issued across India',
      icon: FileText,
    },
    {
      id: 'patents',
      name: 'Patents Report',
      description: 'Analysis of AYUSH-related patents filed and granted',
      icon: FileText,
    },
    {
      id: 'biopiracy_cases',
      name: 'Biopiracy Cases Report',
      description: 'Summary of biopiracy detection and resolution',
      icon: FileText,
    },
    {
      id: 'tkdl_coverage',
      name: 'TKDL Coverage Report',
      description: 'Digital library coverage and verification status',
      icon: FileText,
    },
    {
      id: 'state_analytics',
      name: 'State-wise Analytics',
      description: 'Comparative analysis across Indian states',
      icon: FileSpreadsheet,
    },
    {
      id: 'monthly_trends',
      name: 'Monthly Trends',
      description: 'IP activity trends over the past 12 months',
      icon: FileSpreadsheet,
    },
  ]

  const handleExport = (reportId, format) => {
    toast.success(`${t('export_complete')} - ${reportId}`)

    const csvContent = `Report: ${reportId}\nGenerated: ${new Date().toLocaleString()}\n\n`
    const blob = new Blob([csvContent], { type: 'text/csv' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `${reportId}_${new Date().toISOString().split('T')[0]}.${format === 'pdf' ? 'pdf' : 'csv'}`
    a.click()
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('reports')}</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Generate and export reports for analysis
        </p>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          {t('date')} Range
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-700 dark:text-gray-300 mb-1">
              {t('from_date')}
            </label>
            <input
              type="date"
              value={dateRange.from}
              onChange={(e) => setDateRange({ ...dateRange, from: e.target.value })}
              className="form-input"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-700 dark:text-gray-300 mb-1">
              {t('to_date')}
            </label>
            <input
              type="date"
              value={dateRange.to}
              onChange={(e) => setDateRange({ ...dateRange, to: e.target.value })}
              className="form-input"
            />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {reports.map((report) => {
          const Icon = report.icon
          return (
            <div key={report.id} className="kpi-card">
              <div className="flex items-start gap-4">
                <div className="p-3 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                  <Icon className="w-6 h-6 text-primary-600" />
                </div>
                <div className="flex-1">
                  <h3 className="font-semibold text-gray-900 dark:text-white">
                    {report.name}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {report.description}
                  </p>
                  <div className="flex items-center gap-2 mt-4">
                    <button
                      onClick={() => handleExport(report.id, 'csv')}
                      className="btn-secondary text-sm"
                    >
                      <FileSpreadsheet className="w-4 h-4" />
                      CSV
                    </button>
                    <button
                      onClick={() => handleExport(report.id, 'pdf')}
                      className="btn-primary text-sm"
                    >
                      <FileText className="w-4 h-4" />
                      PDF
                    </button>
                  </div>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
