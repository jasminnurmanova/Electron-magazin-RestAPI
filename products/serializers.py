from rest_framework import serializers
from .models import Product,Category,Comment

class ProductCreateSerializer(serializers.ModelSerializer):

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    class Meta:
        model = Product
        fields = ['title','category', "quantity","description", 'price']

        def create(self, validated_data):
            category_name = validated_data.pop('category') #category alohida create bovoti

            category, _ = Category.objects.get_or_create(
                name=category_name
            )

            product = Product.objects.create(
                category=category,
                **validated_data
            )
            return product


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["id","title","category","quantity","description", "price","created_at",]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["id","title","category","quantity","description","price","created_at",]

class ProductUpdateSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = ["title","category","description","price","quantity"]

    def update(self, instance, validated_data):
        if category := validated_data.pop("category", None): #walrus operator soxranit qilib srazu ifda tekshiradi
            instance.category, _ = Category.objects.get_or_create(name=category)
            #Django ORM, birinchi bazadan qidiradi name=category obyetni qaytaradi or yangi yaratadi
        for k, v in validated_data.items():
            setattr(instance, k, v)
            #dinamik ozgartiradi

        instance.save()
        return instance

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)

    class Meta:
        model = Comment
        fields = [ "id", "user","user_id", "product","text","created_at", "updated_at",]
        read_only_fields = ["product"]

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["text"]

