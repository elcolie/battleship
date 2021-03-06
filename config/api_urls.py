from rest_framework import routers

from boards.api.viewsets import BoardViewSet
from fleets.api.viewsets import FleetViewSet
from missiles.api.viewsets import MissileViewSet

app_name = 'api'
router = routers.DefaultRouter()

router.register(r'boards', BoardViewSet, base_name='board')
router.register(r'fleets', FleetViewSet, base_name='fleet')
router.register(r'missiles', MissileViewSet, base_name='missile')

urlpatterns = router.urls
