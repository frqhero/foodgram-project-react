from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import CartViewSet, FavoriteAPIView, RecipeViewSet

recipes_router = SimpleRouter()
recipes_router.register('recipes', RecipeViewSet)

urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        FavoriteAPIView.as_view(),
        name='download-purchase-list',
    ),
    path(
        'recipes/<int:id>/favorite/',
        FavoriteAPIView.as_view(),
        name='recipe-in-fav',
    ),
    path(
        'recipes/<int:id>/shopping_cart/',
        CartViewSet.as_view(),
        name='recipe-in-cart',
    ),
    path('', include(recipes_router.urls))
]
