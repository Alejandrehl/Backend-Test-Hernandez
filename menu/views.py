from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Option, Menu
from . import serializers


class OptionViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage options in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Option.objects.all()
    serializer_class = serializers.OptionSerializer

    def get_queryset(self):
        """Return objects"""
        assigned_only = bool(
            int(self.request.query_params.get('assigned_only', 0))
        )
        queryset = self.queryset
        if assigned_only:
            queryset = queryset.filter(menu__isnull=False)

        return queryset.order_by('-description').distinct()


class MenuViewSet(viewsets.ModelViewSet):
    """Manage menus in the database"""
    serializer_class = serializers.MenuSerializer
    queryset = Menu.objects.all()

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve the menus"""
        options = self.request.query_params.get('options')
        queryset = self.queryset
        if options:
            option_ids = self._params_to_ints(options)
            queryset = queryset.filter(options__id__in=option_ids)

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return serializers.MenuDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new menu"""
        serializer.save()
