from django.db import models

from boards.models import Board
from commons.utils import AbstractTimestamp


class Missile(AbstractTimestamp):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='missiles', related_query_name='missiles')
    x_axis = models.PositiveSmallIntegerField(default=1)
    y_axis = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = (('board', 'x_axis', 'y_axis'),)
        index_together = [
            ['board', 'x_axis', 'y_axis'],
        ]
