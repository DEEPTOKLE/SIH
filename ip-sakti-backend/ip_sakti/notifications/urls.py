from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, CaseTrackerViewSet

router = DefaultRouter()
router.register(r'', AlertViewSet, basename='alerts')

urlpatterns = [
    path('unread-count/', AlertViewSet.as_view({'get': 'unread_count'}), name='alert-unread-count'),
    path('mark-all-read/', AlertViewSet.as_view({'post': 'mark_all_read'}), name='alert-mark-all-read'),
    path('recent/', AlertViewSet.as_view({'get': 'recent'}), name='alert-recent'),
    path('case-tracker/', CaseTrackerViewSet.as_view({'get': 'table_data'}), name='case-tracker'),
    path('', include(router.urls)),
]
