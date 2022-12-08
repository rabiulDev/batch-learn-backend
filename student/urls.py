from rest_framework.routers import DefaultRouter
from .views import RegisterStudentViewSet

router = DefaultRouter()
router.register('', RegisterStudentViewSet)

student_router = router.urls
