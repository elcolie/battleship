from rest_framework import serializers

from boards.models import Board


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = [
            'id',
            'defender',
            'attacker',
            'is_done',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
