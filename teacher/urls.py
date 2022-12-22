from rest_framework.routers import DefaultRouter
from changepassword.views import ChangePasswordView
from .views import AuthViewSet

router = DefaultRouter()
router.register('', AuthViewSet, basename='auth_teacher')
router.register('change-password', ChangePasswordView, basename='change_password')
teacher_router = router.urls
