from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from accounts.api.serializers import CreateUserSerializer
from django.contrib.auth import get_user_model
from accounts.api.permissions import UpdateOwnProfile
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email',)

class LoginViewSet(viewsets.ViewSet):
    serializer_class = AuthTokenSerializer
    def create(self,request):
        return ObtainAuthToken().post(request)

