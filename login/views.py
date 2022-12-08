from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
# Create your views here.


class LoginViewSet(ViewSet):
    serializer_class = LoginSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=serializer.data['email'])
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })

        else:
            return Response(serializer.errors)

