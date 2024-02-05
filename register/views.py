from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from register.serializer import CustomUserSerializer
from .models import CustomUser
from .permissions import IsAdminUser


class CreateUserApiView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request: Request):
        user = CustomUser.objects.all()
        if user:
            serializer = CustomUserSerializer(user, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data='errors', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request: Request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


