import React from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import Layout from './components/Layout'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import CaseTracker from './pages/CaseTracker'
import Analytics from './pages/Analytics'
import AlertManagement from './pages/AlertManagement'
import Reports from './pages/Reports'
import Profile from './pages/Profile'
import ProtectedRoute from './components/ProtectedRoute'
import { ThemeProvider } from './components/ThemeProvider'

function App() {
  const { t, i18n } = useTranslation()
  const token = localStorage.getItem('access_token')

  if (!token && !['/login'].some(path => window.location.pathname.includes(path))) {
    return <Navigate to="/login" replace />
  }

  return (
    <ThemeProvider>
      <Routes>
        <Route path="/login" element={token ? <Navigate to="/" replace /> : <Login />} />
        <Route path="/" element={<ProtectedRoute><Layout /></ProtectedRoute>}>
          <Route index element={<Dashboard />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="cases" element={<CaseTracker />} />
          <Route path="analytics" element={<Analytics />} />
          <Route path="alerts" element={<AlertManagement />} />
          <Route path="reports" element={<Reports />} />
          <Route path="profile" element={<Profile />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </ThemeProvider>
  )
}

export default App
