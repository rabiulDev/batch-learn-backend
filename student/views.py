from rest_framework.viewsets import ViewSet, ModelViewSet, ReadOnlyModelViewSet
from .models import StudentProfile
from .serializers import StudentProfileSerializer, StudentListSerializer
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
# Create your views here.


class RegisterStudentViewSet(ViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Created Successfully"})

        return Response(serializer.errors)


class StudentsProfileList(ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentListSerializer

