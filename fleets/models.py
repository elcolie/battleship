from django.conf import settings
from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from boards.models import Board
from commons.utils import AbstractTimestamp


class FleetManager(models.Manager):
    def add_ship(self, board, x_axis, y_axis, vertical: None = True):
        tmp = []
        if vertical:
            for j in range(y_axis, settings.BATTLESHIP_SIZE + 1):
                tmp.append(Fleet(board=board, x_axis=x_axis, y_axis=j, occupied=True))
            Fleet.objects.bulk_create(tmp)
        else:
            for i in range(x_axis, settings.BATTLESHIP_SIZE + 1):
                tmp.append(Fleet(board=board, x_axis=x_axis, y_axis=y_axis, occupied=True))
            Fleet.objects.bulk_create(tmp)


class Fleet(AbstractTimestamp):
    class FleetType(DjangoChoices):
        battleship = ChoiceItem("battleship")
        cruiser = ChoiceItem("cruiser")
        destroyer = ChoiceItem("destroyer")
        submarine = ChoiceItem("submarine")

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='fleets', related_query_name='fleets')
    fleet_type = models.CharField(max_length=20, default=FleetType.battleship, choices=FleetType.choices)
    x_axis = models.PositiveSmallIntegerField(default=1)
    y_axis = models.PositiveSmallIntegerField(default=1)
    occupied = models.BooleanField(default=False)  # True is ship, False is vicinity

    objects = FleetManager()

    class Meta:
        unique_together = (
            ('board', 'x_axis', 'y_axis'),
        )
        index_together = [
            ['board', 'x_axis', 'y_axis'],
        ]
