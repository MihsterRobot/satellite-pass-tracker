'''Routes API requests to the appropriate viewset.'''

from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, SatelliteViewSet, PassViewSet


router = DefaultRouter()
router.register(r'locations', LocationViewSet)
router.register(r'satellites', SatelliteViewSet)
router.register(r'passes', PassViewSet)

urlpatterns = router.urls
