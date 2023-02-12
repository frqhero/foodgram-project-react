from django.urls import path
from .views import MyViewSet, FavsViewSet


urlpatterns = [
    path('', MyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:id>/', MyViewSet.as_view({'get': 'retrieve'})),
    path('me/', MyViewSet.as_view({'get': 'me'})),
    path('set_password/', MyViewSet.as_view({'post': 'set_password'})),
    path('subscriptions/', FavsViewSet.as_view({'get': 'list'}))
]
