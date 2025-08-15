# accounts/urls.py
from django.urls import path
from .views import LoginView
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
