from rest_framework import generics
from user.serializers import UserSerializer
# Create your views here.


class CreateUserView(generics.CreateAPIView):
    """Crear nuevo user en el sistema"""

    serializer_class = UserSerializer
