import React from 'react'
import { useTranslation } from 'react-i18next'
import { Award } from 'lucide-react'

export default function SuccessStories() {
  const { t } = useTranslation()

  const stories = [
    {
      id: 1,
      title: t('turmeric_patent_case'),
      year: 1995,
      description: t('turmeric_case_desc'),
      outcome: 'Patent Revoked',
      country: 'USA',
    },
    {
      id: 2,
      title: 'Neem Patent Challenge',
      year: 2000,
      description: 'Successfully challenged European patent on neem-based fungicide. EPO revoked the patent after TKDL prior art submission.',
      outcome: 'Patent Revoked',
      country: 'Europe',
    },
    {
      id: 3,
      title: 'Basmati Rice Patent',
      year: 2001,
      description: 'US company tried to patent basmati rice varieties. India successfully opposed and the patent was rejected.',
      outcome: 'Patent Rejected',
      country: 'USA',
    },
  ]

  return (
    <div className="space-y-4">
      {stories.map((story) => (
        <div
          key={story.id}
          className="flex gap-4 p-4 bg-gradient-to-r from-primary-50 to-transparent dark:from-primary-900/20 rounded-lg border border-primary-100 dark:border-primary-800"
        >
          <div className="flex-shrink-0">
            <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
              <Award className="w-6 h-6 text-primary-600 dark:text-primary-400" />
            </div>
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h4 className="font-semibold text-gray-900 dark:text-white">{story.title}</h4>
              <span className="text-xs bg-primary-100 text-primary-800 px-2 py-0.5 rounded-full">
                {story.year}
              </span>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
              {story.description}
            </p>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-xs bg-green-100 text-green-800 px-2 py-0.5 rounded-full">
                {story.outcome}
              </span>
              <span className="text-xs text-gray-500">{story.country}</span>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
