from rest_framework import viewsets

from boards.api.serializers import BoardSerializer
from boards.models import Board
from commons.utils import NonSecurePermission


class BoardPermission(NonSecurePermission):
    pass


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = (BoardPermission,)
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
