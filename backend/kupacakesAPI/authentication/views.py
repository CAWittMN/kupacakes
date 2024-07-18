from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth.models import User

# Create your views here.


# sign up view to create a new user instance, save to database, and create a login token
class SignUpView(APIView):
    permission_classes = []

    def post(self, request):
        email = request.data["email"]
        username = request.data["username"]
        password = request.data["password"]
        user = User.objects.create_user(
            username=username, password=password, email=email
        )
        user.save()
        token = RefreshToken.for_user(user)
        response = {
            "refresh": str(token),
            "access": str(token.access_token),
        }
        return Response(response, status=status.HTTP_201_CREATED)


class LogoutView(APIView):

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
