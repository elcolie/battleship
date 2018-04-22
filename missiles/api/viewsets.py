from rest_framework import viewsets, status
from rest_framework.response import Response

from commons.utils import NonSecurePermission
from fleets.models import Fleet
from missiles.api.serializers import MissileSerializer
from missiles.models import Missile
from missiles.utils import is_dead


class MissilePermission(NonSecurePermission):
    pass


class MissileViewSet(viewsets.ModelViewSet):
    permission_classes = (MissilePermission,)
    queryset = Missile.objects.all()
    serializer_class = MissileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # Game logic start here. Logic will be messed since data is backward when ship is sunk!
        point = Fleet.objects.filter(**request.data).first()  # prepare for ship sinks
        if point is None:
            return Response(data={'message': f"Miss"}, status=status.HTTP_201_CREATED, headers=headers)
        else:
            point.hit = True
            point.save()
        qs = Fleet.objects.filter(ship_number=point.ship_number)

        if is_dead(qs):
            if Fleet.objects.filter(board=point.board, hit=False).exists():
                return Response(data={'message': f"You just sank the {point.fleet_type}"},
                                status=status.HTTP_201_CREATED, headers=headers)
            else:
                missile_count = Missile.objects.filter(board=point.board).count()
                hit_points = Fleet.objects.filter(board=point.board).count()
                msg = f"Win ! You completed the game in {missile_count} moves. You missed {missile_count - hit_points}"
                return Response(data={'message': msg}, status=status.HTTP_201_CREATED)
        elif point is not None:
            return Response(data={'message': f"Hit"}, status=status.HTTP_201_CREATED, headers=headers)
