from rest_framework.viewsets import ModelViewSet
from .serializers import ProjectSerializer, MeasurementSerializer
from .models import Project, Measurement


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class MeasurementViewSet(ModelViewSet):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
