from rest_framework.viewsets import ReadOnlyModelViewSet
from school.models import School
from school.serializers import SchoolSerializer


# Create your views here.
class SchoolViewSet(ReadOnlyModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
