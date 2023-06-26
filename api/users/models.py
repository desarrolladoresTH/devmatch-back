from pyexpat import model
from django.db import models

# Create your models here.
class User(models.Model): #reperesnenta un solo usuario
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False) #si con
    is_superuser = models.BooleanField(default=False)#superusario es un admin
    is_verified = models.BooleanField(default=False)#si confirmo el reistro
    created_at = models.DateTimeField(auto_now_add=True) #cuando se crea un usuario se asigna la fecha y hora de creacion una sola vez, nunca se movera
    updated_at = models.DateTimeField(auto_now=True) #se puede actualizar a futuro, cada vez que haya un PUT 

    class Meta:
        ordering = ["-updated_at"] #ver la info por fecha (más reciente)

    def __str__(self):
        return self.email #ver por email todos lo susuarios registrados