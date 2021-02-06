from rest_framework import serializers

from .models import Favorite, Ingredient, Purchase, Follow


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Follow


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Favorite


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Purchase
