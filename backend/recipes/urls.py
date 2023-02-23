from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CartViewSet, FavoriteAPIView, RecipeViewSet

my_router = DefaultRouter()
my_router.register(r'', RecipeViewSet)


urlpatterns = [
    path('download_shopping_cart/', FavoriteAPIView.as_view()),
    path('', include(my_router.urls)),
    path('<int:id>/favorite/', FavoriteAPIView.as_view()),
    path('<int:id>/shopping_cart/', CartViewSet.as_view()),
]
