from django.urls import path
from .views import UserCreateAPIView
from .views import LoginAPIView , UserUpdateAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='user-create'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
     path('update/', UserUpdateAPIView.as_view(), name='user-update'),
]
 