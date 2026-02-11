from decimal import Decimal
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from cart.models import Cart,CartItem
from products.models import Product
from .models import Order,OrderItem
from .serializers import OrderSerializer,OrderItemSerializer
from django.shortcuts import get_object_or_404, render


def get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart

class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        cart = get_or_create_cart(user)
        items = list(cart.items.select_related("product").select_for_update())

        if not items:
            return Response(
                {"detail": "Savatcha bo'sh"},
                status=status.HTTP_400_BAD_REQUEST
            )

        total = Decimal("0")

        for item in items:
            product = item.product

            if product.quantity < item.quantity:
                return Response(
                    {
                        "detail": f"{product.title} uchun omborda yetarli mahsulot yo'q"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        order = Order.objects.create(
            user=user,
            status=Order.STATUS_NEW,
            total_price=Decimal("0")
        )

        for item in items:
            product = item.product
            product.quantity -= item.quantity
            product.save(update_fields=["quantity"])

            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=item.quantity
            )

            total += product.price * item.quantity

        order.total_price = total
        order.save(update_fields=["total_price"])

        cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

class OrdersListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=request.user)

        orders = orders.order_by("-created_at")

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        if request.user.is_staff:
            order = get_object_or_404(Order, pk=pk)
        else:
            order = get_object_or_404(Order, pk=pk, user=request.user)
        return Response(OrderSerializer(order).data)


class OrderStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):

        if not request.user.is_staff:
            return Response(
                {"detail": "Bu joy admin uchun"},
                status=status.HTTP_403_FORBIDDEN
            )

        order = get_object_or_404(Order, pk=pk)

        if order.status == Order.STATUS_CANCELLED:
            return Response(
                {"detail": "Buyurtma allaqachon bekor qilingan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if order.status == Order.STATUS_NEW:
            order.status = Order.STATUS_PAID

        elif order.status == Order.STATUS_PAID:
            order.status = Order.STATUS_SHIPPED

        elif order.status == Order.STATUS_SHIPPED:
            return Response(
                {"detail": "Buyurtma allaqachon jo'natilgan"},
                status=status.HTTP_400_BAD_REQUEST
            )

        order.save(update_fields=["status"])

        return Response(OrderSerializer(order).data)

class OrderCancelAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def delete(self, request, pk):

        order = get_object_or_404(Order, pk=pk, user=request.user) #userga

        if order.status != Order.STATUS_NEW:
            return Response(
                {"detail": "Faqat yangi buyurtma bekor qilinadi"},
                status=status.HTTP_400_BAD_REQUEST
            )

        items = order.items.select_related("product").select_for_update()

        for item in items:
            product = item.product
            product.stock += item.quantity
            product.save(update_fields=["quantity"])

        order.status = Order.STATUS_CANCELLED
        order.save(update_fields=["status"])

        return Response(
            {"detail": "Buyurtma bekor qilindi"},
            status=status.HTTP_200_OK
        )