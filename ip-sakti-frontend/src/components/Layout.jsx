import React, { useState, useEffect } from 'react'
import { Outlet, NavLink, useNavigate, Link } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { Menu, X, Search, Bell, Globe, Sun, Moon, LogOut, ChevronLeft, ChevronRight, User } from 'lucide-react'
import { useQuery } from 'react-query'
import { alertsAPI } from '../services/api'
import { useTheme } from './ThemeProvider'

export default function Layout() {
  const { t, i18n } = useTranslation()
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [showNotifications, setShowNotifications] = useState(false)
  const { darkMode, toggleDarkMode } = useTheme()
  const navigate = useNavigate()

  const { data: unreadData } = useQuery('unread-alerts', alertsAPI.getUnreadCount, {
    refetchInterval: 30000,
  })

  const unreadCount = unreadData?.data?.unread_count || 0

  const navItems = [
    { path: '/', label: t('dashboard'), icon: 'LayoutDashboard' },
    { path: '/cases', label: t('case_tracker'), icon: 'FileSearch' },
    { path: '/analytics', label: t('analytics'), icon: 'BarChart3' },
    { path: '/alerts', label: t('alerts'), icon: 'AlertTriangle', badge: unreadCount },
    { path: '/reports', label: t('reports'), icon: 'FileText' },
  ]

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  const toggleLanguage = () => {
    const newLang = i18n.language === 'en' ? 'hi' : 'en'
    i18n.changeLanguage(newLang)
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <div className="flex h-screen overflow-hidden">
        {mobileMenuOpen && (
          <div className="fixed inset-0 bg-black/50 z-40 lg:hidden" onClick={() => setMobileMenuOpen(false)} />
        )}

        <aside
          className={`
            fixed inset-y-0 left-0 z-50 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700
            transform transition-transform duration-300 ease-in-out
            ${sidebarOpen ? 'w-64' : 'w-16'}
            ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          `}
        >
          <div className="flex items-center justify-between h-16 px-4 border-b border-gray-200 dark:border-gray-700">
            {sidebarOpen && (
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-sm">IP</span>
                </div>
                <div>
                  <h1 className="text-sm font-bold text-gray-900 dark:text-white">IP-SAKTI</h1>
                  <p className="text-xs text-gray-500 dark:text-gray-400">Ministry of Ayush</p>
                </div>
              </div>
            )}
            <button
              onClick={() => setMobileMenuOpen(false)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              <X className="w-5 h-5" />
            </button>
            <button
              onClick={() => setSidebarOpen(!sidebarOpen)}
              className="hidden lg:block p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
            >
              {sidebarOpen ? <ChevronLeft className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
            </button>
          </div>

          <nav className="p-4 space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `
                  sidebar-link ${isActive ? 'active' : ''}
                  ${!sidebarOpen && 'justify-center'}
                `}
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="flex-shrink-0">{item.label}</span>
                {item.badge && item.badge > 0 && (
                  <span className="ml-auto bg-red-500 text-white text-xs font-bold px-2 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                )}
              </NavLink>
            ))}
          </nav>

          {sidebarOpen && (
            <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200 dark:border-gray-700">
              <div className="flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                <div className="w-8 h-8 bg-primary-100 dark:bg-primary-900 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-primary-600 dark:text-primary-400" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-gray-900 dark:text-white truncate">Admin User</p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 truncate">admin@ipsakti.gov.in</p>
                </div>
              </div>
            </div>
          )}
        </aside>

        <div className={`flex-1 flex flex-col transition-all duration-300 ${sidebarOpen ? 'lg:ml-64' : 'lg:ml-16'}`}>
          <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 h-16 flex items-center justify-between px-4 lg:px-6">
            <div className="flex items-center gap-4">
              <button
                onClick={() => setMobileMenuOpen(true)}
                className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
              >
                <Menu className="w-5 h-5" />
              </button>
              <div className="hidden md:flex items-center gap-2 bg-gray-100 dark:bg-gray-700 rounded-lg px-3 py-2 w-96">
                <Search className="w-4 h-4 text-gray-500" />
                <input
                  type="text"
                  placeholder={t('search_placeholder')}
                  className="bg-transparent border-none outline-none text-sm w-full text-gray-900 dark:text-white placeholder-gray-500"
                />
              </div>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={toggleLanguage}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                title={i18n.language === 'en' ? t('switch_to_hindi') : t('switch_to_english')}
              >
                <Globe className="w-5 h-5" />
              </button>

              <button
                onClick={toggleDarkMode}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
              >
                {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
              </button>

              <div className="relative">
                <button
                  onClick={() => setShowNotifications(!showNotifications)}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 relative"
                >
                  <Bell className="w-5 h-5" />
                  {unreadCount > 0 && (
                    <span className="absolute -top-0.5 -right-0.5 bg-red-500 text-white text-xs font-bold w-5 h-5 rounded-full flex items-center justify-center">
                      {unreadCount}
                    </span>
                  )}
                </button>

                {showNotifications && (
                  <div className="absolute right-0 mt-2 w-80 bg-white dark:bg-gray-800 rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 z-50">
                    <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                      <h3 className="font-semibold text-gray-900 dark:text-white">{t('notifications')}</h3>
                    </div>
                    <div className="max-h-64 overflow-y-auto">
                      <div className="p-4 text-center text-gray-500 dark:text-gray-400 text-sm">
                        No new notifications
                      </div>
                    </div>
                    <div className="p-2 border-t border-gray-200 dark:border-gray-700">
                      <Link to="/alerts" className="block text-center text-sm text-primary-600 hover:text-primary-700 py-2">
                        {t('view_all')}
                      </Link>
                    </div>
                  </div>
                )}
              </div>

              <button
                onClick={handleLogout}
                className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300"
                title={t('logout')}
              >
                <LogOut className="w-5 h-5" />
              </button>
            </div>
          </header>

          <main className="flex-1 overflow-y-auto p-4 lg:p-6 scrollbar-thin">
            <Outlet />
          </main>

          <footer className="bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700 px-4 lg:px-6 py-3">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-2 text-sm text-gray-600 dark:text-gray-400">
              <div className="flex items-center gap-2">
                <div className="w-6 h-6 bg-gradient-to-br from-primary-500 to-primary-600 rounded flex items-center justify-center">
                  <span className="text-white font-bold text-xs">IP</span>
                </div>
                <span>{t('ministry_of_ayush')}</span>
              </div>
              <p>
                {t('government_of_india')} | {t('all_rights_reserved')} © {new Date().getFullYear()}
              </p>
            </div>
          </footer>
        </div>
      </div>
    </div>
  )
}
