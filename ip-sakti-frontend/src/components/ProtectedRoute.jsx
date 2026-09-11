import React from 'react'
import { Navigate } from 'react-router-dom'
import { useTranslation } from 'react-i18next'

export default function ProtectedRoute({ children }) {
  const { t } = useTranslation()
  const token = localStorage.getItem('access_token')

  if (!token) {
    return <Navigate to="/login" replace />
  }

  return children
}
