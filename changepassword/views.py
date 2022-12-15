from rest_framework import status
from .serializer import ChangePasswordSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.contrib.auth.models import User


class ChangePasswordView(ViewSet):
    serializer_class = ChangePasswordSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not user.check_password(request.data.get("old_password")):
                return Response({"old_password": "The old password is wrong."}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            user.set_password(request.data.get("confirm_password"))
            user.save()
            response = {'message': 'Password updated successfully'}

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
