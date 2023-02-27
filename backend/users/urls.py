from django.urls import include, path

from .routers import UsersSimpleRouter
from .views import SubViewSet, UserViewSet

users_router = UsersSimpleRouter()
users_router.register('', UserViewSet)

urlpatterns = [
    path('', include(users_router.urls)),
    path('subscriptions/', SubViewSet.as_view({'get': 'list'})),
    path('<int:id>/subscribe/', SubViewSet.as_view({'post': 'post'})),
]
