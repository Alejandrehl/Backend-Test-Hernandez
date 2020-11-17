from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Option
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

    # def list(self, request):
    #     """List options"""
    #     print("LIST OPTIONS")
    #     print(request.user.is_staff)
    #     queryset = self.queryset

    #     return queryset
