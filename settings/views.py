from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


# Create your views here.
class SettingsViewSet(ViewSet):

    def list(self, request):
        return Response([
            "Settings API endpoints",
            {
                "School List": f"{request.build_absolute_uri()}get_schools/",
                "Subject List": f"{request.build_absolute_uri()}get_subjects/",
                "Teacher Type": f"{request.build_absolute_uri()}get_teacher_types/",
                "Classes Tools": f"{request.build_absolute_uri()}get_classes_tools/",
                # "Share link json": f"{request.build_absolute_uri()}share_link_json/"
            }
        ])
