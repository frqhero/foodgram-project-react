from django.urls import include, path

from .views import TagViewSet

urlpatterns = [
    path('', TagViewSet.as_view({'get': 'list'})),
    path('<int:pk>/', TagViewSet.as_view({'get': 'retrieve'})),
]
