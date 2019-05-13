from django.urls import path, include
from accounts.api.views import UserViewSet, LoginViewSet
from rest_framework.routers import DefaultRouter

app_name = 'accounts'

router=DefaultRouter()
router.register("profile" ,UserViewSet)
router.register("login", LoginViewSet, base_name="login")

urlpatterns = [
    path('', include(router.urls))
]