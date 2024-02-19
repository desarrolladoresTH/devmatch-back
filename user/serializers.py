import email
from rest_framework import serializers
from user.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
import json
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

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
            "updated_at",
            'flag',
            'username',
        ]

        extra_kwargs = {
            'password' : {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs["password"]

        #validar la longitud del password
        if len(password) < 6 or len(password) > 20:
            raise serializers.ValidationError('El password debe tener de 6-20 caracteres')
        
        return attrs #porqué estoy devolviendo esto si ni siquiera ha sido modificado

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=50)
    tokens = serializers.SerializerMethodField()
    class Meta: 
        model= User
        fields=['email','password','tokens']
    

    def get_tokens(self,obj):
        user = User.objects.get(email=obj['email'])
        return{
            'access': user.tokens()['access'],
            'refresh': user.tokens()['refresh']
        }


    def validate(self, attrs):
        email=attrs.get('email', '')
        password=attrs.get('password', '')
        
        #flag=attrs.get('flag', '')

        try:
            realuser = User.objects.get(email=email)
        except:
            raise AuthenticationFailed('No existe el email')

    

        user = auth.authenticate(username=email, password=password) #por qué es None
            #si está mal las credenciales, o si el usuario está mal (no existe)
     
        #if not realuser

        if not user:#por qué sería none? porque el correo no existe o porque la contraseña está mal


            realuser = User.objects.get(email=email)
            realuser.flag=realuser.flag+1
            realuser.save()
            print("flag")
            print(realuser.flag)
            if realuser.flag>=3:
                realuser.flag=3
                realuser.is_active = False
                realuser.save()
                raise AuthenticationFailed('Too many attempts')
                    

            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        
        
        realuser.flag = 0
        realuser.save()

        #print(json.dumps(user.tokens()))

        return {
            'email': user.email,
            'tokens': user.tokens()
        }
        
        return super().validate(attrs)
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

  

    class Meta:
        fields = ['email']

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')