from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """"Serializer for User objects"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password','name')
        extra_kwargs = {'password':{'write_only':True, 'min_length':8}}
    
    def create(self,validated_data):
        """"Crear nuevo user con clave encriptada y retornarla"""
        return get_user_model().objects.create_user(
            **validated_data
        )
    
    def update(self, instance, validated_data):
        """Actualiza el usuario, configura el password correctamente y lo retorna"""
        password = validated_data.pop('password',None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

class AuthTokenSerializer(serializers.Serializer):
    """Serializador para el objeto de autenticacion del user"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """validar y autenticar user"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            message = _("Unable to authencticate with provider credentials")
            raise serializers.ValidationError(message, code='authorization')
        attrs['user'] = user
        return  attrs