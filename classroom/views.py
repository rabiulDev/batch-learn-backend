from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from school.models import School
from student.models import StudentProfile
from teacher.models import TeacherProfile
from .models import Classroom, ClassRoomComments, ClassroomStudent, ClassRoomStudentAttachments, \
    ClassRoomTeacherAttachments
from .serializer import ClassroomSerializer, ClassroomCreateSerializer, EmptySerializer, JoinStudentSerializer, \
    ClassRoomCommentCreateSerializer, ClassRoomReplyCommentCreateSerializer, ClassRoomCommentListSerializer, \
    ClassRoomTeacherAttachmentSerializer, ClassRoomStudentAttachmentSerializer, \
    ClassRoomStudentAttachmentListSerializer, ClassRoomTeacherAttachmentListSerializer


# Create your views here.
class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ClassroomCreateSerializer
        elif self.action == 'create_classroom':
            return ClassroomCreateSerializer
        elif self.action == 'join_student':
            return JoinStudentSerializer
        elif self.action == 'list':
            return ClassroomSerializer
        elif self.action == 'retrieve':
            return ClassroomSerializer
        elif self.action == 'classroom_comment_create':
            return ClassRoomCommentCreateSerializer
        elif self.action == 'classroom_reply_comment_create':
            return ClassRoomReplyCommentCreateSerializer
        elif self.action == 'classroom_comments':
            return ClassRoomCommentListSerializer
        elif self.action == 'teacher_attachment_create':
            return ClassRoomTeacherAttachmentSerializer
        elif self.action == 'student_attachment_create':
            return ClassRoomStudentAttachmentSerializer
        elif self.action == 'student_attachment_list':
            return ClassRoomStudentAttachmentListSerializer
        elif self.action == 'teacher_attachment_list':
            return ClassRoomTeacherAttachmentListSerializer

        return EmptySerializer

    @action(methods=['POST'], detail=False, name='Create Classroom')
    def create_classroom(self, request):
        try:
            student = StudentProfile.objects.get(user_id=request.user.id)
            class_for_school = School.objects.get(id=student.school_id)
            serializer = self.get_serializer(data=request.data)
            if student and serializer.is_valid():
                serializer.save(creator=student, school=class_for_school)
                created_classroom = Classroom.objects.get(id=serializer.data['id'])
                created_classroom.students.add(student)
                return Response(ClassroomSerializer(Classroom.objects.get(id=serializer.data['id'])).data)
            else:
                return Response("Something went wrong!")
        except Exception:
            return Response({"message": "You are not student for create a class room"})

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

    @action(methods=['POST'], detail=True, name='Join Teacher To ClassRoom')
    def join_teacher(self, request, pk=None):
        classroom = Classroom.objects.get(pk=pk)
        add_teacher = classroom.accept_teacher(request.user)
        if add_teacher == 'True':
            return Response({"message": "Congratulations! you're the teacher of this class"})
        return Response({"none_field_error": add_teacher}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='Start Class', url_path='start-class')
    def start_class(self, request, pk=None):
        classroom = Classroom.objects.get(pk=pk)
        res = classroom.start_class(request.user)
        if res == 'Start':
            return Response({"message": "Class is live now"})
        return Response({"none_field_error": res}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='End Class', url_path='end-class')
    def end_class(self, request, pk=None):
        classroom = Classroom.objects.get(pk=pk)
        res = classroom.end_class(request.user)
        if res == 'End':
            return Response({"message": "Class is ended"})
        return Response({"none_field_error": res}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='ClassRoom Comment Create', url_path='classroom-comment-create')
    def classroom_comment_create(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            serializer = self.get_serializer(data=request.data)
            if classroom.has_profile(request.user.id) and serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        except Exception:
            return Response({"message": "Your have no access in this classroom comment"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='ClassRoom Reply Comment Create',
            url_path='classroom-reply-comment-create')
    def classroom_reply_comment_create(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            if classroom.has_profile(request.user.id):
                parent_comment = ClassRoomComments.objects.get(id=request.data.get('parent_comment'))
                serializer = self.get_serializer(data=request.data)
                if parent_comment and serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors)
            return Response({"message": "Your have no access in this classroom comment"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"message": "Class room does not exist"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, name="ClassRoom Comment List", url_path='classroom-comments')
    def classroom_comments(self, request, pk=None):
        try:
            classroom_comments = ClassRoomComments.objects.filter(classroom_id=pk)
            serializer = self.get_serializer(classroom_comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "Classroom does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='ClassRoom Student Attachment', url_path='student-attachment-create')
    def student_attachment_create(self, request, pk=None):
        try:
            student = StudentProfile.objects.get(user_id=request.user.id).id
            classroom = Classroom.objects.get(pk=pk)
            classroom_student = ClassroomStudent.objects.filter(classroom_id=classroom.id)
            classroom_student_id = [student.student_id for student in classroom_student]
            if student in classroom_student_id:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You have no access to this classroom attachment"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"message": "You have no access to this classroom attachment"})

    @action(methods=['GET'], detail=True, name='ClassRoom Student Attachment List', url_path='student-attachment-list')
    def student_attachment_list(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            if classroom.has_profile(request.user.id):
                classroom_student_attachments = ClassRoomStudentAttachments.objects.filter(classroom_id=pk)
                serializer = self.get_serializer(classroom_student_attachments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "You have no access to this classroom attachment"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, name='ClassRoom Teacher Attachment', url_path='teacher-attachment-create')
    def teacher_attachment_create(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            teacher = TeacherProfile.objects.get(id=classroom.teacher_id)
            if teacher.user_id == request.user.id:
                serializer = self.get_serializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"message": "You have no access to this classroom attachment"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({"message": "You have no access to this classroom attachment"},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=True, name='ClassRoom Teacher Attachment List', url_path='teacher-attachment-list')
    def teacher_attachment_list(self, request, pk=None):
        try:
            classroom = Classroom.objects.get(pk=pk)
            if classroom.has_profile(request.user.id):
                classroom_teacher_attachments = ClassRoomTeacherAttachments.objects.filter(classroom_id=pk)
                serializer = self.get_serializer(classroom_teacher_attachments, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response({"message": "You have no access to this classroom attachment"},
                            status=status.HTTP_400_BAD_REQUEST)
