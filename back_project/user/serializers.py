from rest_framework import serializers
from user.models import User

class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        #declara el modelo
        model = User
        fields = [ #la info que va a devolver al front como repsuesta
            "email",
            "password",
            "is_active",
            "is_verified",
            "created_at",
            "updated_at"
        ]