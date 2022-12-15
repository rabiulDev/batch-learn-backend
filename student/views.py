from rest_framework import status
from rest_framework.viewsets import ViewSet, ReadOnlyModelViewSet
from rest_framework import views
from .models import StudentProfile
from .serializers import StudentProfileSerializer, StudentListSerializer, EmailVerificationSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from .utils import Util
import jwt
from backend.settings import SIMPLE_JWT
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
# Create your views here.


class RegisterStudentViewSet(ViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()

            user_data = request.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            abs_url = 'http://' + current_site + relative_link + "?token=" + str(token)
            email_body = 'Hi ' + user.first_name + \
                         ' Use the link below to verify your email \n' + abs_url
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Verify your email'}

            Util.send_activation_email(data)
            return Response({"msg": "Account created Successfully. Go to your Email account for verify"})

        return Response(serializer.errors)


class StudentsProfileList(ReadOnlyModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentListSerializer


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']],)
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
