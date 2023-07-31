from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(max_length=50,unique=True)
    password = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    

    class Meta: 
        ordering = ["-updated_at"]
    def __str__(self) -> str:
        return self.email 