from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


# Create your views here.

class AuthViewSets(ViewSet):
    def list(self, request):
        return Response([
            "Auth API endpoints",
            {
                "Student Register": f"{request.build_absolute_uri()}register-student/",
                "Teacher Register First Step Checker API": f"{request.build_absolute_uri()}register-teacher-first-step/",
                "Teacher Register Second Step Checker API": f"{request.build_absolute_uri()}register-teacher-second-step/",
                "Teacher Register": f"{request.build_absolute_uri()}register-teacher/",
                # "Register Account Active": f"{request.build_absolute_uri()}register-account-active/",
                "Login": f"{request.build_absolute_uri()}login/",
                # "Reset password send": f"{request.build_absolute_uri()}reset-password/send/",
                # "Reset password": f"{request.build_absolute_uri()}reset-password/",
                "Change password": f"{request.build_absolute_uri()}change-password/",
                # "Account": f"{request.build_absolute_uri()}account/",
                "Profile Info": f"{request.build_absolute_uri()}profile-info/",
                # "Social student profile complete": f"{request.build_absolute_uri()}social_register_student/",
                # "Social teacher profile complete": f"{request.build_absolute_uri()}social_register_teacher/"
            }
        ])
