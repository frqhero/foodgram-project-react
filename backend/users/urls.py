from django.urls import path

from .views import MyViewSet, SubViewSet

urlpatterns = [
    path('', MyViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('<int:id>/', MyViewSet.as_view({'get': 'retrieve'})),
    path('me/', MyViewSet.as_view({'get': 'me'})),
    path('set_password/', MyViewSet.as_view({'post': 'set_password'})),
    path('subscriptions/', SubViewSet.as_view({'get': 'list'})),
    path('<int:id>/subscribe/', SubViewSet.as_view({'post': 'post'}))
]
