from rest_framework.routers import DefaultRouter
from .views import LoginViewSet
router = DefaultRouter()
router.register('', LoginViewSet, basename='login')

login_router = router.urls
