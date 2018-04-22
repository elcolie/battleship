from rest_framework import viewsets, status
from rest_framework.response import Response

from fleets.api.serializers import FleetSerializer, BattleShipSerializer
from fleets.models import Fleet
from fleets.utils import OutOceanException, NearShipException


class FleetViewSet(viewsets.ModelViewSet):
    """View the overall of Ocean"""
    permission_classes = ()  # No permission for now
    queryset = Fleet.objects.all()
    serializer_class = FleetSerializer

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return self.serializer_class
        elif self.request.method == 'POST':
            return BattleShipSerializer
        else:
            self.serializer_class

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
        except OutOceanException as err:
            return Response({'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
        except NearShipException as err:
            return Response({'message': f"{err}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)