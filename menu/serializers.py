from rest_framework import serializers
from core.models import Option, Menu


class OptionSerializer(serializers.ModelSerializer):
    """Serializer for option objects"""

    class Meta:
        model = Option
        fields = ('id', 'description')
        read_only_fields = ('id',)


class MenuSerializer(serializers.ModelSerializer):
    """Serialize a menu"""
    options = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Option.objects.all()
    )

    class Meta:
        model = Menu
        fields = (
            'id', 'name', 'date', 'options', 'created_at',
        )
        read_only_fields = ('id',)


class MenuDetailSerializer(MenuSerializer):
    options = OptionSerializer(many=True, read_only=True)
