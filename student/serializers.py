import phonenumbers
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.models import Q
from rest_framework import serializers

from school.serializers import SchoolSerializer
from .models import StudentProfile


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = StudentProfile
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'school', 'password', 'is_accept', 'is_lead',
                  'coupon']

    def validate(self, attrs):
        if attrs['phone_number']:
            try:
                phone_number = phonenumbers.parse(attrs['phone_number'])
                if not phonenumbers.is_valid_number(phone_number):
                    raise Exception('Invalid phone number')
            except Exception:
                raise serializers.ValidationError({"phone_number": "Please use valid phone number"})

            if StudentProfile.objects.filter(phone_number=attrs['phone_number']).exists():
                raise serializers.ValidationError({"phone_number": "Already have an account with this phone number"})

        if User.objects.filter(Q(email=attrs['email']) | Q(username=attrs['email'])).exists():
            raise serializers.ValidationError({"email": "Already have an account with this email"})

        if attrs['is_accept'] is not True:
            raise serializers.ValidationError({"is_accept": "Terms must be accepted"})

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
            new_group = Group.objects.get(name='Student')
            user.groups.add(new_group)
        except Group.DoesNotExist:
            new_group = Group.objects.create(name='Student')
            user.groups.add(new_group)

        student_profile = StudentProfile.objects.create(
            user=user,
            school=validated_data['school'],
            is_lead=validated_data['is_lead'],
            is_accept=True,
            phone_number=validated_data['phone_number'],
            coupon=validated_data['coupon']
        )
        student_profile.save()

        return user


class StudentListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True, source='user.id')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    email = serializers.EmailField(read_only=True, source='user.email')
    phone_number = serializers.CharField(read_only=True)
    school = SchoolSerializer()
    avatar = serializers.ImageField(read_only=True)
    is_active = serializers.BooleanField(read_only=True, source='user.is_active')

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'school', 'avatar', 'is_active']


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']


class StudentProfileInfoSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_only=True, source='user.id')
    first_name = serializers.CharField(read_only=True, source='user.first_name')
    last_name = serializers.CharField(read_only=True, source='user.last_name')
    email = serializers.EmailField(read_only=True, source='user.email')
    phone_number = serializers.CharField(read_only=True, )
    avatar = serializers.ImageField(read_only=True, )
    school = SchoolSerializer()

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'first_name', 'last_name', 'email', 'phone_number', 'school', 'avatar']


class StudentProfileUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = StudentProfile
        fields = ['first_name', 'last_name', 'phone_number', 'school']

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


class StudentAvatarChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['avatar']
