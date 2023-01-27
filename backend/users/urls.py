from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from djoser import views


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls')),
    # path('', include('djoser.urls')),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]