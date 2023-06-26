from logging import raiseExceptions
from urllib import response
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from users.serializers import UserSignUpSerializer
# Create your views here.

#donde se manejan las peticiones, se crea el crud
class UserSignUpView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data = request.data) # el serializador recibe la data del request

        serializer.is_valid(raise_exception=True) #m
        serializer.save() #esta automaticamente guardando la info en la BD

        return Response(serializer.data, status = status.HTTP_200_OK)
        #una repsuesta con unbody y codigo status

#lastar 
class UsersListView(APIView):
    def get(self,request):
        users = User.objects.all() #URM de Django
        serializer = UserSignUpSerializer(users, many=True) #mostrar vrios res

        return Response(serializer.data, status = status.HTTP_200_OK)


