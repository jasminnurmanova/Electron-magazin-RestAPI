from django.shortcuts import render
from .serializers import CartSerializer, CartAddSerializer, CartRemoveSerializer, CartUpdateSerializer, CartUpdateSerializer
from http.client import HTTPResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.template.context_processors import request
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import status
from .models import Cart,CartItem
from django.shortcuts import get_object_or_404, render
from products.models import Product
def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

#cart korish ucun
class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        if not serializer.data['items']:
            return Response({"id":serializer.data['id'],"message":"Hali mahsulot yuq"})
        return Response(serializer.data)

#mahsulot qoshish
class CartAddAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product = get_object_or_404(Product, pk=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        item, created = CartItem.objects.get_or_create(cart=cart,product=product,defaults={"quantity": quantity})

        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartSerializer(cart).data,status=status.HTTP_200_OK)


class CartUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = CartUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(Product, pk=product_id)
        item = get_object_or_404(CartItem, cart=cart, product=product)

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

        return Response(
            CartSerializer(cart).data,
            status=status.HTTP_200_OK
        )

class CartRemoveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        serializer = CartRemoveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=product_id)

        item = CartItem.objects.filter(cart=cart, product=product).first()

        if not item:
            return Response(
                {"detail": "Product not in cart"},
                status=status.HTTP_400_BAD_REQUEST
            )

        item.delete()

        return Response({
            "message":"O'chirildi",
            "cart":CartSerializer(cart).data,
            "status":status.HTTP_200_OK
        }
        )

class CartClearAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = get_or_create_cart(request.user)
        cart.items.all().delete()

        return Response(
            {"message": "Cart cleared successfully."},
            status=status.HTTP_204_NO_CONTENT
        )