import uuid

from django.db import models
from djchoices import DjangoChoices, ChoiceItem

from boards.models import Board
from commons.utils import AbstractTimestamp


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
    ship_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=False)
    hit = models.BooleanField(default=False)
    occupied = models.BooleanField(default=False)  # True is ship, False is vicinity. Will be deleted later

    class Meta:
        unique_together = (
            ('board', 'x_axis', 'y_axis', 'occupied'),
        )
        index_together = [
            ['board', 'x_axis', 'y_axis'],
        ]

    def __str__(self):
        return f"<{self.x_axis} {self.y_axis} {self.hit}>"
