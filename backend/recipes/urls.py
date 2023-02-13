from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, FavoriteAPIView, CartViewSet
from django.urls import path, include


my_router = DefaultRouter()
my_router.register(r'', RecipeViewSet)


urlpatterns = [
    path('', include(my_router.urls)),
    path('<int:id>/favorite/', FavoriteAPIView.as_view()),
    path('<int:id>/shopping_cart/', CartViewSet.as_view()),
]
