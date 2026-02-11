from django.urls import path

from orders.views import OrderCreateAPIView, OrdersListAPIView, OrderDetailAPIView, OrderStatusAPIView, \
    OrderCancelAPIView

urlpatterns = [
    path('create/',OrderCreateAPIView.as_view()),#tick
    path('list/',OrdersListAPIView.as_view()),#tick
    path('detail/<int:pk>/',OrderDetailAPIView.as_view()),#tick
    path('status/<int:pk>/',OrderStatusAPIView.as_view()),#tick
    path('cancel/<int:pk>/',OrderCancelAPIView.as_view()),#tick
]