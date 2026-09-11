import React from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useTranslation } from 'react-i18next'

export default function MonthlyTrends({ data }) {
  const { t } = useTranslation()

  const chartData = Object.entries(data).map(([month, values]) => ({
    month: new Date(month + '-01').toLocaleDateString('en-IN', { month: 'short', year: '2-digit' }),
    gi_tags: values.gi_tags || 0,
    patents: values.patents || 0,
    biopiracy_cases: values.biopiracy_cases || 0,
  }))

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" className="stroke-gray-200 dark:stroke-gray-700" />
        <XAxis
          dataKey="month"
          className="text-xs fill-gray-600 dark:fill-gray-400"
        />
        <YAxis className="text-xs fill-gray-600 dark:fill-gray-400" />
        <Tooltip
          contentStyle={{
            backgroundColor: 'rgb(255, 255, 255)',
            border: '1px solid rgb(203, 213, 225)',
            borderRadius: '0.5rem',
          }}
        />
        <Legend />
        <Line
          type="monotone"
          dataKey="gi_tags"
          stroke="#22c55e"
          strokeWidth={2}
          name={t('total_gi_tags')}
        />
        <Line
          type="monotone"
          dataKey="patents"
          stroke="#3b82f6"
          strokeWidth={2}
          name={t('patents_filed')}
        />
        <Line
          type="monotone"
          dataKey="biopiracy_cases"
          stroke="#ef4444"
          strokeWidth={2}
          name={t('biopiracy_alerts')}
        />
      </LineChart>
    </ResponsiveContainer>
  )
}
