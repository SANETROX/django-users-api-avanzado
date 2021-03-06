from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin



class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """ Crea y guarda un nuevo user"""
        if not email:
            raise ValueError('Users must have an email')

        user  = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password,**extra_fields):
        """"Crea super user"""
        if not email and password:
            raise ValueError('Users must have an email and password')

        user = self.create_user(
            email=self.normalize_email(email),
            is_superuser=True,
            is_staff=True
        )
        user.set_password(password)
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    """" Modelo Personalizado de Usuario que soporta hacer Login con Email en vez de Usuario"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    