from django.contrib import admin
from django.urls import path, include
from apis_v1.urls import auth_routes
from settings.urls import settings_router
from student.urls import student_router
from teacher.urls import teacher_router
from login.urls import login_router

# VERSION ONE API ROUTES
urlpatterns = [
    path('', include(auth_routes)),
    path('auth/register-student/', include(student_router)),
    path('auth/', include(teacher_router)),
    path('auth/login/', include(login_router)),
    path('settings/', include(settings_router)),


]

# API V1
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(urlpatterns)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework'))
]
