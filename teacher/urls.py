from rest_framework.routers import DefaultRouter
from changepassword.views import ChangePasswordView
from .views import RegisterTeacherFirstViewSet, RegisterTeacherSecondViewSet, RegisterTeacherViewSet

router = DefaultRouter()
router.register('register-teacher-first-step', RegisterTeacherFirstViewSet)
router.register('register-teacher-second-step', RegisterTeacherSecondViewSet)
router.register('register-teacher', RegisterTeacherViewSet)
router.register('change-password', ChangePasswordView, basename='change_password')

teacher_router = router.urls
