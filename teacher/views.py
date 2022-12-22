from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet, ModelViewSet

from classroom.serializer import EmptySerializer
from student.models import StudentProfile
from student.serializers import StudentProfileInfoSerializer, StudentListSerializer, \
    StudentProfileUpdateSerializer, StudentAvatarChangeSerializer
from .models import TeacherProfile, Subject, TeacherType, ClassTool
from .serializers import TeacherProfileSerializer, TeachersListSerializer, SubjectSerializer, TeacherTypeSerializer, \
    ClassToolsSerializer, TeacherProfileSecondStepSerializer, RegisterTeacher, TeacherProfileInfoSerializer, \
    TeacherProfileInfoUpdateSerializer, TeacherAvatarChangeSerializer


# Create your views here.
class AuthViewSet(ModelViewSet):
    queryset = []

    def get_serializer_class(self):
        if self.action == 'register_teacher_first_step':
            return TeacherProfileSerializer

        elif self.action == 'register_teacher_second_step':
            return TeacherProfileSecondStepSerializer

        elif self.action == 'register_teacher':
            return RegisterTeacher

        elif self.action == 'profile_info':
            group_list = [group.name for group in self.request.user.groups.all()]

            if 'Teacher' in group_list:

                if self.request.method == 'GET':
                    return TeacherProfileInfoSerializer
                elif self.request.method == 'PUT':
                    return TeacherProfileInfoUpdateSerializer

            elif 'Student' in group_list:
                if self.request.method == 'GET':
                    return StudentProfileInfoSerializer
                elif self.request.method == 'PUT':
                    return StudentProfileUpdateSerializer

        elif self.action == 'profile_avatar':
            group_list = [group.name for group in self.request.user.groups.all()]

            if 'Teacher' in group_list:
                return TeacherAvatarChangeSerializer

            elif 'Student' in group_list:
                return StudentAvatarChangeSerializer
        return EmptySerializer

    @action(detail=False, methods=['POST'], name='Teacher Register First Step', url_path='register-teacher-first-step')
    def register_teacher_first_step(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "ok"})

        return Response(serializer.errors)

    @action(detail=False, methods=['POST'], name='Teacher Register Second Step',
            url_path='register-teacher-second-step')
    def register_teacher_second_step(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({"msg": "ok"})

        return Response(serializer.errors)

    @action(detail=False, methods=['POST'], name='Teacher Register',
            url_path='register-teacher')
    def register_teacher(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account created successfully"})

        return Response(serializer.errors)

    @action(detail=False, methods=['GET', 'PUT'], name='Profile Info', url_path='profile-info')
    def profile_info(self, request):
        serializer = None
        user = User.objects.get(id=request.user.id)
        group_list = [group.name for group in user.groups.all()]
        if request.method == 'GET':
            if 'Teacher' in group_list:
                user = TeacherProfile.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(user)
            elif 'Student' in group_list:
                user = StudentProfile.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(user)
            return Response(serializer.data)

        if request.method == 'PUT':
            if 'Teacher' in group_list:
                user = TeacherProfile.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(user, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                updated_user = TeacherProfile.objects.get(user_id=request.user.id)
                serializer = TeachersListSerializer(updated_user)
                return Response(serializer.data)
            elif 'Student' in group_list:
                user = StudentProfile.objects.get(user_id=request.user.id)
                serializer = self.get_serializer(user, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                user = StudentProfile.objects.get(user_id=request.user.id)
                serializer = StudentListSerializer(user)
                return Response(serializer.data)
        return Response(serializer.errors)

    @action(detail=False, methods=['PUT'], name='Change Profile Avatar ', url_path='profile-avatar')
    def profile_avatar(self, request):
        user = User.objects.get(id=request.user.id)
        group_list = [group.name for group in user.groups.all()]

        if 'Teacher' in group_list:
            user = TeacherProfile.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        elif 'Student' in group_list:
            user = StudentProfile.objects.get(user_id=request.user.id)
            serializer = self.get_serializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({"message": "You are not a valid user"})


# class RegisterTeacherFirstViewSet(ViewSet):
#     queryset = TeacherProfile.objects.all()
#     serializer_class = TeacherProfileSerializer
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             return Response({"msg": "ok"})
#
#         return Response(serializer.errors)
#
#
# class RegisterTeacherSecondViewSet(ViewSet):
#     queryset = TeacherProfile.objects.all()
#     serializer_class = TeacherProfileSecondStepSerializer
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             return Response({"msg": "ok"})
#
#         return Response(serializer.errors)
#
#
# class RegisterTeacherViewSet(ViewSet):
#     queryset = TeacherProfile.objects.all()
#     serializer_class = RegisterTeacher
#
#     def create(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Account created successfully"})
#
#         return Response(serializer.errors)


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

