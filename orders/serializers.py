from rest_framework import serializers
from .models import OrderItem,Order

class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id","product", "product_title", "price", "quantity",]
        read_only_fields = fields

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id","status","total_price","created_at","items",]
        read_only_fields = fields