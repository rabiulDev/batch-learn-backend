from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from classroom.serializer import EmptySerializer
from .models import TeacherProfile, Subject, TeacherType, ClassTool
from .serializers import TeacherProfileSerializer, TeachersListSerializer, SubjectSerializer, TeacherTypeSerializer, \
    ClassToolsSerializer, TeacherProfileSecondStepSerializer, RegisterTeacher
from rest_framework.response import Response
# Create your views here.


class RegisterTeacherFirstViewSet(ViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "ok"})

        return Response(serializer.errors)


class RegisterTeacherSecondViewSet(ViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeacherProfileSecondStepSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "ok"})

        return Response(serializer.errors)


class RegisterTeacherViewSet(ViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = RegisterTeacher

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Class created successfully"})

        return Response(serializer.errors)


class TeachersListViewSet(ReadOnlyModelViewSet):
    queryset = TeacherProfile.objects.all()
    serializer_class = TeachersListSerializer


class SubjectViewSet(ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class TeacherTypeViewSet(ViewSet):
    def list(self, request):
        queryset = TeacherType.objects.all()
        serializer = TeacherTypeSerializer(queryset, many=True)
        return Response(serializer.data)


class ClassToolsViewSet(ViewSet):
    def list(self, request):
        queryset = ClassTool.objects.all()
        serializer = ClassToolsSerializer(queryset, many=True)
        return Response(serializer.data)
