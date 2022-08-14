from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Tag
from recipe.serializers import TagSerializer

class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manejar los TAgs en la base de datos"""
    serializer_class = TagSerializer
    authentication_class = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    queryset = Tag.objects.all()

    def get_queryset(self):
        """Retorna los tags del user autenticado"""
        return self.queryset.filter(user=self.request.user).order_by('-name')