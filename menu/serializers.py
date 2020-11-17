from rest_framework import serializers
from core.models import Option


class OptionSerializer(serializers.ModelSerializer):
    """Serializer for option objects"""

    class Meta:
        model = Option
        fields = ('id', 'description')
        read_only_fields = ('id',)
