from rest_framework import serializers
from .models import Cupcake, KeyIngredient

from django.contrib.auth.models import User


class KeyIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyIngredient
        fields = "__all__"


class CupcakeSerializer(serializers.ModelSerializer):
    key_ingredients = KeyIngredientSerializer(many=True)

    class Meta:
        model = Cupcake
        fields = "__all__"


class InvalidCupcakeSerializer(serializers.Serializer):
    valid = serializers.BooleanField()
    message = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    cupcakes = CupcakeSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "cupcakes"]
        read_only_fields = ["cupcakes"]
