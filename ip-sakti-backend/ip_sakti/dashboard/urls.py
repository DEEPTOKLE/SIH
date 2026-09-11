from django.urls import path
from .views import DashboardViewSet

urlpatterns = [
    path('kpis/', DashboardViewSet.as_view({'get': 'kpis'}), name='dashboard-kpis'),
    path('state-analytics/', DashboardViewSet.as_view({'get': 'state_analytics'}), name='dashboard-state-analytics'),
    path('compare-states/', DashboardViewSet.as_view({'post': 'compare_states'}), name='dashboard-compare-states'),
]
