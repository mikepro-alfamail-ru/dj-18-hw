from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.models import Advertisement
from advertisements.serializers import AdvertisementSerializer
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import AccessPermission


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    
    def list(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            self.queryset = Advertisement.objects.filter(~Q(status="DRAFT"))
        else:
            self.queryset = Advertisement.objects.filter(~Q(status="DRAFT")|Q(creator=request.user))

        return super().list(self, request, *args, **kwargs)


    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create"]:
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "destroy"]:
            return [IsAuthenticated(), AccessPermission]
        return []