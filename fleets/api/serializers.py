from django.conf import settings
from rest_framework import serializers
from rest_framework.compat import MinValueValidator, MaxValueValidator

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

    # Should be change from attrs to `fleet_type` and refactor it by list of configuration
    def validate(self, attrs):
        board = attrs.get('board')
        if attrs.get('fleet_type') == Fleet.FleetType.battleship:
            if Fleet.objects.filter(
                    board=board,
                    fleet_type=Fleet.FleetType.battleship).count() >= settings.BATTLESHIP_QTY * settings.BATTLESHIP_SIZE:
                raise serializers.ValidationError(detail={'board': f"{board} has {Fleet.FleetType.battleship} over quota"})
            else:
                return attrs
        if attrs.get('fleet_type') == Fleet.FleetType.cruiser:
            if Fleet.objects.filter(
                    board=board,
                    fleet_type=Fleet.FleetType.cruiser).count() >= settings.CRUISER_SIZE * settings.CRUISER_QTY:
                raise serializers.ValidationError(detail={'board': f"{board} has {Fleet.FleetType.cruiser} over quota"})
            else:
                return attrs
        if attrs.get('fleet_type') == Fleet.FleetType.destroyer:
            if Fleet.objects.filter(
                    board=board,
                    fleet_type=Fleet.FleetType.destroyer).count() >= settings.DESTROYER_SIZE * settings.DESTROYER_QTY:
                raise serializers.ValidationError(detail={'board': f"{board} has {Fleet.FleetType.destroyer} over quota"})
            else:
                return attrs
        if attrs.get('fleet_type') == Fleet.FleetType.submarine:
            if Fleet.objects.filter(
                    board=board,
                    fleet_type=Fleet.FleetType.submarine).count() >= settings.SUBMARINE_SIZE * settings.SUBMARINE_QTY:
                raise serializers.ValidationError(detail={'board': f"{board} has {Fleet.FleetType.submarine} over quota"})
            else:
                return attrs
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
