from django.urls import path, include
from .views import MyViewSet


urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
    path('users/', MyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('users/<int:id>/', MyViewSet.as_view({'get': 'retrieve'})),
    path('users/me/', MyViewSet.as_view({'get': 'me'})),
    path('users/set_password/', MyViewSet.as_view({'post': 'set_password'})),
    path('djoser/', include('djoser.urls')),
    path("heck/", include("django.contrib.auth.urls")),
]
