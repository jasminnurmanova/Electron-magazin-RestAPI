from users.models import CustomUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from products.serializers import ProductDetailSerializer
from .models import Cart,CartItem

class CartItemSerializer(serializers.ModelSerializer):
    product=ProductDetailSerializer(read_only=True)

    class Meta:
        model=CartItem
        fields=("id","product","quantity")


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("id", "items")



class CartAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartUpdateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=0)

class CartRemoveSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()