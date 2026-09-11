from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import StateViewSet, AYUSHFormulationViewSet, GITagViewSet, PatentViewSet, BiopiracyCaseViewSet, IPActivityViewSet, TKDL_EntryViewSet

router = DefaultRouter()
router.register(r'states', StateViewSet, basename='states')
router.register(r'formulations', AYUSHFormulationViewSet, basename='formulations')
router.register(r'gi-tags', GITagViewSet, basename='gi-tags')
router.register(r'patents', PatentViewSet, basename='patents')
router.register(r'biopiracy-cases', BiopiracyCaseViewSet, basename='biopiracy-cases')
router.register(r'tkdl', TKDL_EntryViewSet, basename='tkdl')
router.register(r'activities', IPActivityViewSet, basename='activities')

urlpatterns = [
    path('', include(router.urls)),
]
