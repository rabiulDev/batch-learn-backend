from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from apis_v1.urls import auth_routes
from login.urls import login_router
from settings.urls import settings_router
from student.urls import student_router
from student.views import VerifyEmail
from teacher.urls import teacher_router

# VERSION ONE API ROUTES
urlpatterns = [
    path('', include(auth_routes)),
    path('auth/register-student/', include(student_router)),
    path('auth/', include(teacher_router)),
    path('auth/login/', include(login_router)),
    path('settings/', include(settings_router)),
    path('email-verify/', VerifyEmail.as_view(), name="email-verify"),

]

# API V1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlpatterns)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
