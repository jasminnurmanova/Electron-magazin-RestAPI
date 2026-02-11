from django.contrib.auth.views import PasswordChangeView
from django.urls import path

from .serializers import ChangePasswordSerializer
from .views import SignUpView,LoginView,LogoutView,ProfileView,PhotoUploadView,ProfileUpdateView,ChangePasswordView

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    path('profile/photo/', PhotoUploadView.as_view()),
    path('profile/change-pass/', ChangePasswordView.as_view()),
]