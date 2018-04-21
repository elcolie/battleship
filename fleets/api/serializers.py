from django.conf import settings
from rest_framework import serializers
from rest_framework.compat import MinValueValidator, MaxValueValidator

from fleets.models import Fleet


class FleetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fleet
        fields = [
            'id',
            'board',
            'fleet_type',
            'x_axis',
            'y_axis',
            'occupied',
            'created_at',
            'updated_at',
            ]


class BattleShipSerializer(serializers.ModelSerializer):
    """
    Read
    fleet_type: battleship, cruiser, ...
    is_horizontal: True/False
    staring poink: (1,1)
    board: board_id
    """
    x = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(settings.OCEAN_SIZE)])
    y = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(settings.OCEAN_SIZE)])
    is_horizontal = serializers.BooleanField(default=True)

    class Meta:
        model = Fleet
        fields = [
            'id',
            'board',
            'fleet_type',
            'is_horizontal',
            'x',
            'y',
        ]
        read_only_fields = ['id']

    def create(self, validated_data):
        return
