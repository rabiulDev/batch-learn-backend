import phonenumbers
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers

from .models import TeacherProfile, Subject, ClassTool, TeacherType


class TeacherProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = TeacherProfile
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'teacher_type', 'password']

    def validate(self, attrs):
        if attrs['phone_number']:
            try:
                phone_number = phonenumbers.parse(attrs['phone_number'])
                if not phonenumbers.is_valid_number(phone_number):
                    raise Exception('Invalid phone number')
            except Exception:
                raise serializers.ValidationError({"phone_number": "Please use valid phone number"})

            if TeacherProfile.objects.filter(phone_number=attrs['phone_number']).exists():
                raise serializers.ValidationError({"phone_number": "Already have an account with this phone number"})

        if User.objects.filter(Q(email=attrs['email']) | Q(username=attrs['email'])).exists():
            raise serializers.ValidationError({"email": "Already have an account with this email"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            is_active=False,
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        try:
            new_group = Group.objects.get(name='Teacher')
            user.groups.add(new_group)
        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Teacher')
            user.groups.add(new_group)

        teacher_profile = TeacherProfile.objects.create(
            user=user,
            teacher_type=validated_data['teacher_type'],
            phone_number=validated_data['phone_number']

        )
        # teacher_profile.save()

        return user


class TeacherProfileSecondStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['subjects', 'serve_or_attend_school']


class RegisterTeacher(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = TeacherProfile
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'subjects', 'teacher_type',
                  'serve_or_attend_school', 'password', 'classes_tools', 'about']

    def validate(self, attrs):
        if attrs['phone_number']:
            try:
                phone_number = phonenumbers.parse(attrs['phone_number'])
                if not phonenumbers.is_valid_number(phone_number):
                    raise Exception('Invalid phone number')
            except Exception:
                raise serializers.ValidationError({"phone_number": "Please use valid phone number"})

            if TeacherProfile.objects.filter(phone_number=attrs['phone_number']).exists():
                raise serializers.ValidationError({"phone_number": "Already have an account with this phone number"})

        if User.objects.filter(Q(email=attrs['email']) | Q(username=attrs['email'])).exists():
            raise serializers.ValidationError({"email": "Already have an account with this email"})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            is_active=False,
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()

        try:
            new_group = Group.objects.get(name='Teacher')
            user.groups.add(new_group)

        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Teacher')
            user.groups.add(new_group)

        teacher_profile = TeacherProfile.objects.create(
            user=user,
            teacher_type=validated_data['teacher_type'],
            phone_number=validated_data['phone_number'],
            about=validated_data['about'],
        )

        for subject in validated_data['subjects']:
            teacher_profile.subjects.add(subject)

        for school in validated_data['serve_or_attend_school']:
            teacher_profile.serve_or_attend_school.add(school)

        for tools in validated_data['classes_tools']:
            teacher_profile.classes_tools.add(tools)

        teacher_profile.save()

        return user


class TeacherTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherType
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class ClassToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassTool
        fields = '__all__'


class TeachersListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True, source='user.id')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    email = serializers.EmailField(read_only=True, source='user.email')
    phone_number = serializers.CharField(read_only=True, )
    subjects = SubjectSerializer(many=True)
    classes_tools = ClassToolsSerializer(many=True)
    avatar = serializers.ImageField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, source='user.is_active')

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'subjects', 'classes_tools',
                  'avatar', 'is_active']


class AddedToClassRoomSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    avatar = serializers.ImageField(read_only=True)
    subjects = SubjectSerializer(many=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'first_name', 'last_name', 'subjects', 'avatar']


# Teacher profile fields

# {
#     "id": 9,
#     "user": 38,
#     "first_name": "New",
#     "last_name": "Teacher",
#     "email": "newteacher@gmail.com",
#     "avatar": "https://batch-learn-staging.s3.amazonaws.com/",
#     "phone_number": "++880 1812 345678",
#     "subjects": [
#         {
#             "id": 1,
#             "name": "Math"
#         }
#     ],
#     "classes_tools": [
#         {
#             "id": 1,
#             "name": "Zoom"
#         }
#     ]
# }

class TeacherProfileInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True, source='user.id')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    email = serializers.EmailField(read_only=True, source='user.email')
    phone_number = serializers.CharField(read_only=True, )
    avatar = serializers.ImageField(read_only=True)
    subjects = SubjectSerializer(many=True)
    classes_tools = ClassToolsSerializer(many=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'avatar', 'subjects', 'classes_tools']


class TeacherProfileInfoUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = TeacherProfile
        fields = ['first_name', 'last_name', 'phone_number', 'subjects', 'classes_tools']

    def update(self, instance, validated_data):
        super().update(instance, validated_data)

        try:
            user = User.objects.get(id=instance.user.id)
            if validated_data.get('first_name') is not None:
                user.first_name = validated_data.get('first_name')
            if validated_data.get('last_name') is not None:
                user.last_name = validated_data.get('last_name')
            user.save()
        except user.DoesNotExist:
            pass

        return instance


class TeacherAvatarChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = ['avatar']
