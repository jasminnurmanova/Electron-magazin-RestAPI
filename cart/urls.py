from django.urls import path

from cart.views import CartView, CartAddAPIView, CartUpdateAPIView,CartRemoveAPIView,CartClearAPIView

urlpatterns = [
    path('cart/',CartView.as_view()), #tick
    path('cart-add/',CartAddAPIView.as_view()), #tick
    path('cart-update/',CartUpdateAPIView.as_view()),#tick
    path('cart-remove/',CartRemoveAPIView.as_view()),#tick
    path('cart-clear/',CartClearAPIView.as_view()),#tick

]