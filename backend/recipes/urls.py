from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet
from django.urls import path, include


my_router = DefaultRouter()
my_router.register(r'', RecipeViewSet)


urlpatterns = [
    path('', include(my_router.urls)),
]
