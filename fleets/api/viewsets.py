from rest_framework import viewsets

from fleets.api.serializers import FleetSerializer
from fleets.models import Fleet


class FleetViewSet(viewsets.ModelViewSet):
    """View the overall of Ocean"""
    permission_classes = ()  # No permission for now
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer


class BattleViewSet(viewsets.ModelViewSet):
    """Place battleship"""
    permission_classes = ()
    queryset = Fleet