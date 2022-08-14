from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tags objects"""
    class Meta:
        model = Tag
        fields = ('id','name','user')
        read_only_Fields = ('id',)