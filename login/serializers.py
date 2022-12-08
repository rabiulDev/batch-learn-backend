from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=20)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
            if not user.check_password(attrs['password']):
                raise Exception('Invalid password')

        except Exception:
            raise serializers.ValidationError('Invalid email or password')

        return attrs
