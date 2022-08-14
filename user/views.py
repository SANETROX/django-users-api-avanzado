from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer, AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings


class CreateUserView(generics.CreateAPIView):
    """Crear nuevo user en el sistema"""

    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """ crear un token para nuestro user"""
    serializer_class = AuthTokenSerializer
    render_class = api_settings.DEFAULT_RENDERER_CLASSES

class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_class = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Obtener y retorna usuario autenticado"""
        return self.request.user