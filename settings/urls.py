from rest_framework.routers import DefaultRouter
from school.views import SchoolViewSet
from teacher.views import SubjectViewSet, TeacherTypeViewSet, ClassToolsViewSet

router = DefaultRouter()
router.register('get_schools', SchoolViewSet, basename='school')
router.register('get_subjects', SubjectViewSet, basename='subject')
router.register('get_teacher_types', TeacherTypeViewSet, basename='teacher_type')
router.register('get_classes_tools', ClassToolsViewSet, basename='class_tools')

settings_router = router.urls
