from rest_framework import serializers

from student.models import StudentProfile
from teacher.serializers import SubjectSerializer, AddedToClassRoomSerializer
from .models import Classroom, ClassRoomComments, ClassRoomReplyComments, ClassRoomStudentAttachments, \
    ClassRoomTeacherAttachments


class ClassroomSerializer(serializers.ModelSerializer):
    student_count = serializers.IntegerField(read_only=True, source='students.count')
    classroom_id = serializers.UUIDField(read_only=True)
    school = serializers.StringRelatedField()
    subject = SubjectSerializer()
    teacher = AddedToClassRoomSerializer()

    # class_total_amount = serializers.DecimalField(max_digits=5,  decimal_places=1, read_only=True)

    class Meta:
        model = Classroom
        # fields = '__all__'
        exclude = ['students']


class ClassroomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['id', 'title', 'description', 'subject', 'class_date']


class JoinStudentSerializer(serializers.ModelSerializer):
    classroom_id = serializers.UUIDField()

    class Meta:
        model = Classroom
        fields = ['classroom_id']


class ClassRoomCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomComments
        fields = ['comment', 'classroom', 'creator']


class ClassRoomReplyCommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomReplyComments
        fields = ['comment', 'parent_comment', 'creator']


class ClassRoomReplyCommentListSerializer(serializers.ModelSerializer):
    creator_first_name = serializers.CharField(read_only=True, source='creator.first_name')
    creator_last_name = serializers.CharField(read_only=True, source='creator.last_name')
    avatar = serializers.ImageField(read_only=True, source='get_profile_avatar')

    class Meta:
        model = ClassRoomReplyComments
        fields = ['id', 'creator_first_name', 'creator_last_name', 'avatar', 'comment', 'created_at', 'parent_comment',
                  'creator']


class ClassRoomCommentListSerializer(serializers.ModelSerializer):
    reply_comments = ClassRoomReplyCommentListSerializer(many=True, read_only=True)
    creator_first_name = serializers.CharField(read_only=True, source='creator.first_name')
    creator_last_name = serializers.CharField(read_only=True, source='creator.last_name')
    avatar = serializers.ImageField(read_only=True, source='get_profile_avatar')

    class Meta:
        model = ClassRoomComments
        fields = ['id', 'reply_comments', 'creator_first_name', 'creator_last_name', 'avatar', 'comment', 'created_at',
                  'classroom', 'creator']


class ClassRoomStudentAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomStudentAttachments
        fields = '__all__'


class ClassRoomTeacherAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomTeacherAttachments
        fields = '__all__'


class AttachmentStudentInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')

    class Meta:
        model = StudentProfile
        fields = ['id', 'first_name', 'last_name', 'avatar']


class ClassRoomStudentAttachmentListSerializer(serializers.ModelSerializer):
    student_info = AttachmentStudentInfoSerializer(read_only=True, source='student')

    class Meta:
        model = ClassRoomStudentAttachments
        fields = ['id', 'student_info', 'file', 'created_at', 'classroom', 'student']


class ClassRoomTeacherAttachmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassRoomTeacherAttachments
        fields = ['id', 'file', 'created_at', 'classroom', 'teacher']

class EmptySerializer(serializers.Serializer):
    pass
