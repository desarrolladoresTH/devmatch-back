
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status, views
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings


from user.serializers import LoginSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from user.models import User
from user.serializers import UserSignUpSerializer
from user.utils import Util
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.http import HttpResponsePermanentRedirect
import os


#donde se manejan las peticiones, se crea el crud
class CustomRedirect(HttpResponsePermanentRedirect):
    
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

# Create your views here.

#donde se manejan las peticiones, se crea el crud
class UserSignUpView(generics.GenericAPIView):
    serializer_class = UserSignUpSerializer
    #quien sea puede entrar a este endpoint
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
           
            serializer = self.serializer_class(data = request.data) # el serializador recibe la data del request
            serializer.is_valid(raise_exception=True) 
            serializer.save() #esta automaticamente guardando la info en la BD

            user_data = serializer.data
            user = User.objects.get(email=user_data['email'])
            token = RefreshToken.for_user(user).access_token #usa el user id para hacer el token

            current_site=get_current_site(request).domain

            relative_link=reverse('email-verify')
            absurl = 'http://' + current_site + relative_link + "?token=" + str(token)
            email_body =absurl
            #email_body = 'Hi ' + 'use the link below to verify your account \n' + absurl
            data={'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify email for My Money'}
            Util.send_email(data)

            return Response(serializer.data, status = status.HTTP_200_OK)
        except Exception as e:
              print(e) # les muestra el error en consola
              return Response({'message' : 'Hubo un error en el servidor'})


class UsersListView(APIView):
    def get(self,request):
        users = User.objects.all() #URM de Django
        serializer = UserSignUpSerializer(users, many=True) #mostrar vrios res

        return Response(serializer.data, status = status.HTTP_200_OK)


class VerifyEmail(APIView):
    
    def get(self, request):
        token=request.GET.get('token') #obtener el parametro de url en el token

        try:
            payload = jwt.decode(token,settings.SECRET_KEY,algorithms='HS256')
            user=User.objects.get(id=payload['user_id'])

            print('conejos')
            print(settings.SECRET_KEY)

            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()

            return render(request,'verify_email.html')
        except jwt.ExpiredSignatureError as identifier: #si el link expiró
            return Response({'error':'Token expired'}, status = status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier: #si el link expiró
            return Response({'error':'Invalid token'}, status = status.HTTP_400_BAD_REQUEST)

class LoginAPIViews(APIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
        

class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword','codigo1': uidb64,'codigo2':token,}
            Util.send_email(data)
            print(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)