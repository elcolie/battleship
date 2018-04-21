from rest_framework import serializers

from missiles.models import Missile


class MissileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missile
        fields = [
            'id',
            'board',
            'x_axis',
            'y_axis',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']