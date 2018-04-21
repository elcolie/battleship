from django.conf import settings
from rest_framework import serializers
from rest_framework.compat import MinValueValidator, MaxValueValidator

from fleets.models import Fleet
from fleets.utils import add_battleship


class FleetSerializer(serializers.ModelSerializer):
    """Ordinary serializer"""

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
    x_axis = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(settings.OCEAN_SIZE)])
    y_axis = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(settings.OCEAN_SIZE)])
    vertical = serializers.BooleanField(default=True)

    class Meta:
        model = Fleet
        fields = [
            'id',
            'board',
            'fleet_type',
            'vertical',
            'x_axis',
            'y_axis',
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        board = attrs.get('board')
        if Fleet.objects.filter(board=board, fleet_type=Fleet.FleetType.battleship).count() > 1:
            raise serializers.ValidationError(detail={'board': f"{board} has battleship already"})
        return attrs

    def create(self, validated_data):
        # Add battleship
        if validated_data.get('fleet_type') == 'battleship':
            objs = add_battleship(
                validated_data.get('board'),
                validated_data.get('x_axis'),
                validated_data.get('y_axis'),
                validated_data.get('vertical')
            )
            return objs[0]

