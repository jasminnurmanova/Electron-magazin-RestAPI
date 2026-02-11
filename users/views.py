from functools import partial
from logging import raiseExceptions

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import SignUpSerializer, LoginSerializer, ProfileUpdateSerializer, PhotoUploadSerializer, \
    ChangePasswordSerializer
from rest_framework import permissions

class SignUpView(APIView):
    serializer_class = SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = {
            'status': status.HTTP_201_CREATED,
            'username': serializer.data['username'],
            'message': 'Akkount yaratildi'
        }
        return Response(data=data)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Siz tizimga kirdingiz'
            },
            status=status.HTTP_200_OK
        )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    def post(self, request):
        refresh_token = self.request.data.get('refresh')
        if not refresh_token:
            raise ValidationError({'refresh': 'Refresh token yuborilmadi'})
        try:
            refresh = RefreshToken(refresh_token)
            refresh.blacklist()
        except Exception:
            raise ValidationError({'refresh': 'Noto‘g‘ri token'})
        data = {
            'success': True,
            'message': 'Siz tizimdan chiqdingiz'
        }
        return Response(data)

class ProfileView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def get(self,request):
        user=request.user
        data={
            'username':user.username,
            'first_name':user.first_name,
            'email':user.email,
            'phone':user.phone,
            'user_role':user.user_role
        }
        return Response(data,status=status.HTTP_200_OK)

class ProfileUpdateView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def patch(self,request):
        serializer=ProfileUpdateSerializer(instance=request.user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message":"Profile yangilandi",
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )

class PhotoUploadView(APIView):
    permission_classes=[permissions.IsAuthenticated]

    def patch(self,request):
        serializer=PhotoUploadSerializer(instance=request.user,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"mess":"Rasm yangilandi"},status=status.HTTP_200_OK)

class ChangePasswordView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=ChangePasswordSerializer
    def post(self,request):
        serializer=self.serializer_class(
            data=request.data,
            context={'request':request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data={
            'status':status.HTTP_200_OK,
            'message':'Parol yangilani'
        }
        return Response(data)