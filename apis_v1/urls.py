from rest_framework.routers import DefaultRouter

from settings.views import SettingsViewSet
from .views import AuthViewSets
from student.views import StudentsProfileList
from teacher.views import TeachersListViewSet, SubjectViewSet
from school.views import SchoolViewSet
from classroom.views import ClassroomViewSet

router = DefaultRouter()
router.register('auth', AuthViewSets, basename='auth_apis')
router.register('students', StudentsProfileList, basename='students_list')
router.register('teachers', TeachersListViewSet, basename='teachers_list')
router.register('subjects', SubjectViewSet, basename='subjects_list')
router.register('schools', SchoolViewSet, basename='schools_list')
router.register('classrooms', ClassroomViewSet, basename='classrooms')
router.register('settings', SettingsViewSet, basename='settings')

auth_routes = router.urls
