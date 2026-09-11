import React from 'react'
import { useTranslation } from 'react-i18next'
import { User, Mail, Phone, Briefcase, Shield } from 'lucide-react'

export default function Profile() {
  const { t } = useTranslation()

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{t('profile_settings')}</h1>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Manage your account settings and preferences
        </p>
      </div>

      <div className="kpi-card">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
            <User className="w-8 h-8 text-primary-600" />
          </div>
          <div>
            <h2 className="text-xl font-semibold text-gray-900 dark:text-white">Admin User</h2>
            <p className="text-sm text-gray-600 dark:text-gray-400">Administrator</p>
          </div>
        </div>

        <div className="space-y-4">
          <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <Mail className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('email')}</p>
              <p className="font-medium text-gray-900 dark:text-white">admin@ipsakti.gov.in</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <Phone className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('phone')}</p>
              <p className="font-medium text-gray-900 dark:text-white">+91-11-2338xxxx</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <Briefcase className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('designation')}</p>
              <p className="font-medium text-gray-900 dark:text-white">System Administrator</p>
            </div>
          </div>
          <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
            <Shield className="w-5 h-5 text-gray-400" />
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400">{t('department')}</p>
              <p className="font-medium text-gray-900 dark:text-white">Ministry of AYUSH</p>
            </div>
          </div>
        </div>
      </div>

      <div className="kpi-card">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Preferences
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-gray-700 dark:text-gray-300">{t('language')}</span>
            <span className="text-sm text-gray-600 dark:text-gray-400">English</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-700 dark:text-gray-300">{t('theme')}</span>
            <span className="text-sm text-gray-600 dark:text-gray-400">System Default</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-gray-700 dark:text-gray-300">Notifications</span>
            <span className="text-sm text-gray-600 dark:text-gray-400">Enabled</span>
          </div>
        </div>
      </div>
    </div>
  )
}
