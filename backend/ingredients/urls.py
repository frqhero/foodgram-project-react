from django.urls import path, include
from .views import IngredientViewSet


urlpatterns = [
    path('', IngredientViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', IngredientViewSet.as_view({'get': 'retrieve'})),
]
