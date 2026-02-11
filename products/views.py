from django.shortcuts import render
from .serializers import ProductCreateSerializer,CommentCreateSerializer,CommentSerializer,CategoryCreateSerializer,ProductListSerializer,ProductDetailSerializer,ProductUpdateSerializer
from http.client import HTTPResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.template.context_processors import request
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework import status
from .models import Product,Comment
from django.shortcuts import get_object_or_404, render
from django.db.models import Q

class ProductCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = CategoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, id):
        try:
            product = Product.objects.get(id=id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


class ProductUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)

        serializer = ProductUpdateSerializer(
            product,
            data=request.data,
            partial=True )
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(
            ProductDetailSerializer(product).data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductSearchAPIView(APIView):
    def get(self, request):
        qs = Product.objects.all()

        q = request.query_params.get("q")
        category = request.query_params.get("category")
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")
        ordering = request.query_params.get("ordering")

        if q:
            qs = qs.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        if category:
            qs = qs.filter(category_id=category)

        if min_price:
            qs = qs.filter(price__gte=min_price)

        if max_price:
            qs = qs.filter(price__lte=max_price)

        if ordering in ["price", "-price", "created_at", "-created_at"]:
            qs = qs.order_by(ordering)

        serializer = ProductListSerializer(qs, many=True)
        return Response(serializer.data)


#commentlar user korish va yozish uchun
class ProductCommentsAPIView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        comments = product.comments.all()
        serializer = CommentSerializer(comments, many=True)
        if not serializer.data:
            return Response({"message":"commentlar yoq"})
        return Response(serializer.data)

    def post(self, request, pk):
        self.permission_classes = [IsAuthenticated]
        self.check_permissions(request)

        product = get_object_or_404(Product, pk=pk)
        serializer = CommentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment = serializer.save( user=request.user,product=product)

        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)

#commentni udi
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        if comment.user != request.user:
            return Response(
                {"detail": "Not allowed"},status=status.HTTP_403_FORBIDDEN )
        return comment

    def put(self, request, pk):
        comment = self.get_object(request, pk)
        if isinstance(comment, Response):
            return comment

        serializer = CommentCreateSerializer(comment, data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_200_OK
        )

    def patch(self, request, pk):
        comment = self.get_object(request, pk)
        if isinstance(comment, Response):
            return comment

        serializer = CommentCreateSerializer(comment,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response(CommentSerializer(comment).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        comment = self.get_object(request, pk)
        if isinstance(comment, Response):
            return comment

        comment.delete()
        return Response(
            {"detail": "Comment o‘chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )

#admin uchun hamma kommentlar yoki user faqat oziniki ucun

class CommentsListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            comments = Comment.objects.all()
        else:
            comments = Comment.objects.filter(user=request.user)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)