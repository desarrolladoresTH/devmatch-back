
from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None): ## es lo unoico que llega en el json del cliente

        if username is None:
            raise TypeError('Se necesita un username')
        
        if email is None:
            raise TypeError('Se necesita un email')
        
        if password is None:
            raise TypeError('Se necesita una password')

        user = self.model(email = self.normalize_email(email))
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password=None):
        if username is None:
            raise TypeError('Se necesita un username')
        

        if password is None:
            raise TypeError('Se necesita un password')
        
        if email is None:
            raise TypeError('Se necesita un email')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.save()

        return user

#creo que tiene que ir después porque usa la clase anterior
class User(AbstractBaseUser, PermissionsMixin): #reperesnenta un solo usuario
    email = models.EmailField(max_length=50,unique=True)
    username=models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False) #si con
    is_superuser = models.BooleanField(default=False)#superusario es un admin
    is_verified = models.BooleanField(default=False)#si confirmo el reistro
    created_at = models.DateTimeField(auto_now_add=True) #cuando se crea un usuario se asigna la fecha y hora de creacion una sola vez, nunca se movera
    updated_at = models.DateTimeField(auto_now=True) #se puede actualizar a futuro, cada vez que haya un PUT 
    flag = models.IntegerField(default=0)


    objects = UserManager() #una clase que especifica cómo los objeto son creados o retrieved
    USERNAME_FIELD = "email"
    #REQUIRED_FIELDS = ["email", "password "]

    class Meta:
        ordering = ["-updated_at"] #ver la info por fecha (más reciente)

    def __str__(self):
        return self.email #ver por email todos lo susuarios registrados

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

   