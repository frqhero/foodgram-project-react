import djoser.views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, MyViewSet
from djoser import views


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet)

urlpatterns = [
    # path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', MyViewSet.as_view({'get': 'list'})),
    path('djoser/', include('djoser.urls')),
    path("heck/", include("django.contrib.auth.urls")),
    # re_path(r'^auth/', include('djoser.urls.authtoken')),
]
x = 1