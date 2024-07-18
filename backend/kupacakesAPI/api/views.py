from django.shortcuts import render
from rest_framework import status, permissions, generics, viewsets, filters
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from .models import Cupcake, KeyIngredient
from django.contrib.auth.models import User
from .serializers import (
    InvalidCupcakeSerializer,
    CupcakeSerializer,
    KeyIngredientSerializer,
    UserSerializer,
)


# Create your views here.
# use the generate_cupcake method to create a new cupcake instance, convert the ingredients in the request into ingredient instances, link those ingredients and user to cupcake, save to database, send the cupcake data in the response
class CupcakeCreate(APIView):

    def post(self, request):
        user = request.user
        data = request.data
        cupcake = Cupcake.generate_cupcake(data)
        if not cupcake.valid:
            invalid_cupcake_serializer = InvalidCupcakeSerializer(cupcake)
            return Response(
                invalid_cupcake_serializer, status=status.HTTP_400_BAD_REQUEST
            )
        ingredients = data.pop("key_ingredients")
        ingredients_instances = []
        cupcake.save()
        for ingredient in ingredients:
            ingredient_instance = KeyIngredient.objects.get_or_create(
                name=ingredient.lower()
            )[0]
            if hasattr(ingredient_instance, "id"):
                ingredient_instance.save()
            ingredients_instances.append(ingredient_instance)
        cupcake.user = user
        cupcake.key_ingredients.set(ingredients_instances)
        cupcake.save()
        serializer = CupcakeSerializer(instance=cupcake)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CupcakeRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cupcake.objects.all()
    serializer_class = CupcakeSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


class CupcakeListByUserId(generics.ListAPIView):
    serializer_class = CupcakeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Cupcake.objects.filter(user=user)


class UserRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


# get all ingredients, can be filtered by name, or which cupcakes contain it
class IngredientsList(generics.ListAPIView):
    queryset = KeyIngredient.objects.all()
    serializer_class = KeyIngredientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "cupcake__name"]


# get all cupcakes ordered from created_at, can be filtered by name, and if it contains one or more ingredients
class CupcakeList(generics.ListAPIView):
    queryset = Cupcake.objects.all().order_by("-created_at")
    serializer_class = CupcakeSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "key_ingredients"]
