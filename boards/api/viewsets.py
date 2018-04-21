from rest_framework import viewsets

from boards.api.serializers import BoardSerializer
from boards.models import Board


class BoardViewSet(viewsets.ModelViewSet):
    permission_classes = ()
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
