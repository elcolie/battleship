import typing

from django.conf import settings
from djchoices import ChoiceItem
from rest_framework import serializers
from rest_framework.compat import MinValueValidator, MaxValueValidator

from boards.models import Board
from fleets.models import Fleet
from fleets.utils import add_battleship, add_cruiser, add_destroyer, add_submarine


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

    @staticmethod
    def validate_quota(board: Board, fleet_type: ChoiceItem, ship_qty: int, ship_size: int, attrs: typing.Dict):
        """Acrobatic here because data is flowing backward"""
        if Fleet.objects.filter(
                board=board,
                fleet_type=fleet_type).count() >= ship_qty * ship_size:
            raise serializers.ValidationError(detail={'board': f"{board} has {fleet_type} over quota"})
        else:
            return attrs

    # Can not use `validate_fleet_type()` method since I have to use `board`
    def validate(self, attrs):
        board = attrs.get('board')
        if attrs.get('fleet_type') == Fleet.FleetType.battleship:
            return self.validate_quota(board, Fleet.FleetType.battleship, settings.BATTLESHIP_QTY,
                                       settings.BATTLESHIP_SIZE, attrs)
        if attrs.get('fleet_type') == Fleet.FleetType.cruiser:
            return self.validate_quota(board, Fleet.FleetType.cruiser, settings.CRUISER_QTY,
                                       settings.CRUISER_SIZE, attrs)
        if attrs.get('fleet_type') == Fleet.FleetType.destroyer:
            return self.validate_quota(board, Fleet.FleetType.destroyer, settings.DESTROYER_QTY,
                                       settings.DESTROYER_SIZE, attrs)
        if attrs.get('fleet_type') == Fleet.FleetType.submarine:
            return self.validate_quota(board, Fleet.FleetType.submarine, settings.SUBMARINE_QTY,
                                       settings.SUBMARINE_SIZE, attrs)
        else:
            raise serializers.ValidationError(detail={'fleet_type': f"Unknown fleet_type"})

    def create(self, validated_data):
        # Add battleship
        if validated_data.get('fleet_type') == Fleet.FleetType.battleship:
            objs = add_battleship(
                validated_data.get('board'),
                validated_data.get('x_axis'),
                validated_data.get('y_axis'),
                validated_data.get('vertical')
            )
        elif validated_data.get('fleet_type') == Fleet.FleetType.cruiser:
            objs = add_cruiser(
                validated_data.get('board'),
                validated_data.get('x_axis'),
                validated_data.get('y_axis'),
                validated_data.get('vertical')
            )
        elif validated_data.get('fleet_type') == Fleet.FleetType.destroyer:
            objs = add_destroyer(
                validated_data.get('board'),
                validated_data.get('x_axis'),
                validated_data.get('y_axis'),
                validated_data.get('vertical')
            )
        else:  # validated_data.get('fleet_type') == Fleet.FleetType.submarine:
            # With choices. I am sure it will be submarine
            objs = add_submarine(
                validated_data.get('board'),
                validated_data.get('x_axis'),
                validated_data.get('y_axis'),
                validated_data.get('vertical')
            )
        return objs[0]
