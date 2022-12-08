from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from student.models import StudentProfile
from .models import Classroom
from .serializer import ClassroomSerializer, ClassroomCreateSerializer, EmptySerializer


# Create your views here.
class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClassroomCreateSerializer
        if self.action == 'create_classroom':
            return ClassroomCreateSerializer
        if self.action == 'list':
            return ClassroomSerializer
        if self.action == 'retrieve':
            return ClassroomSerializer
        return EmptySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = Classroom.objects.all()
    #     serializer = ClassroomSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(methods=['POST'], detail=False, name='create_classroom')
    def create_classroom(self, request):
        student = StudentProfile.objects.get(user_id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=student)
            return Response(serializer.data)
        else:
            return Response("Something went wrong!")
