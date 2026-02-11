from django.urls import path

from products.views import ProductCreateView,CommentDetailAPIView, ProductUpdateDeleteView, CategoryCreateView, ProductListView, \
    ProductDetailView, \
    ProductUpdateDeleteView, CommentDetailAPIView,ProductCommentsAPIView,ProductSearchAPIView,CommentsListAPIView

urlpatterns = [
    path('create-product/',ProductCreateView.as_view()),#tick
    path('create-category/',CategoryCreateView.as_view()),#tick
    path('products/',ProductListView.as_view()),#tick
    path("detail/<int:id>/", ProductDetailView.as_view()),#tick
    path("delete-update/<int:pk>/", ProductUpdateDeleteView.as_view()),#tick
    path("cr-comment/<int:pk>/", ProductCommentsAPIView.as_view()),#tick
    path("ud-comment/<int:pk>/", CommentDetailAPIView.as_view()), #tick
    path("search/", ProductSearchAPIView.as_view()), #tick
    path("comment-list/", CommentsListAPIView.as_view()), #tick

]