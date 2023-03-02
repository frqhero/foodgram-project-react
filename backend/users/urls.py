from django.urls import include, path

from .routers import UsersSimpleRouter
from .views import SubViewSet, UserViewSet

users_router = UsersSimpleRouter()
users_router.register('users', UserViewSet)

urlpatterns = [
    path(
        'users/subscriptions/',
        SubViewSet.as_view({'get': 'list'}),
        name='subs-list',
    ),
    path(
        'users/<int:id>/subscribe/',
        SubViewSet.as_view({'post': 'post'}),
        name='follow-unfollow',
    ),
    path('', include(users_router.urls)),
]
