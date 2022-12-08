from rest_framework.routers import DefaultRouter
from .views import RegisterTeacherFirstViewSet, RegisterTeacherSecondViewSet, RegisterTeacherViewSet

router = DefaultRouter()
router.register('register-teacher-first-step', RegisterTeacherFirstViewSet)
router.register('register-teacher-second-step', RegisterTeacherSecondViewSet)
router.register('register-teacher', RegisterTeacherViewSet)

teacher_router = router.urls
