from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from student.models import StudentProfile
from .models import Classroom
from .serializer import ClassroomSerializer, ClassroomCreateSerializer, EmptySerializer, JoinStudentSerializer


# Create your views here.
class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClassroomCreateSerializer
        if self.action == 'create_classroom':
            return ClassroomCreateSerializer
        if self.action == 'join_student':
            return JoinStudentSerializer
        if self.action == 'list':
            return ClassroomSerializer
        if self.action == 'retrieve':
            return ClassroomSerializer
        return EmptySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = Classroom.objects.all()
    #     serializer = ClassroomSerializer(queryset, many=True)
    #     return Response(serializer.data)

    @action(methods=['POST'], detail=False, name='Create Classroom')
    def create_classroom(self, request):
        student = StudentProfile.objects.get(user_id=request.user.id)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=student)
            created_classroom = Classroom.objects.get(id=serializer.data['id'])
            created_classroom.students.add(student)
            return Response(ClassroomSerializer(Classroom.objects.get(id=serializer.data['id'])).data)
        else:
            return Response("Something went wrong!")

    @action(methods=['POST'], detail=False, name='Join Student To ClassRoom')
    def join_student(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            student = StudentProfile.objects.get(user_id=request.user.id)
            class_room = Classroom.objects.get(classroom_id=request.data['classroom_id'])
            class_room.students.add(student)
            return Response({"msg": "You are a part of this classroom"})
        except Exception as e:
            return Response({"non_field_errors": [str(e)]}, status=status.HTTP_400_BAD_REQUEST)

