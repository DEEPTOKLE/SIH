# The DashboardViewSet is defined in ip_sakti.views; re-export it so
# ip_sakti/dashboard/urls.py can do `from .views import DashboardViewSet`.
from ip_sakti.views import DashboardViewSet  # noqa: F401

__all__ = ['DashboardViewSet']
