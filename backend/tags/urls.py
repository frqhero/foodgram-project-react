from django.urls import include, path

from .views import TagViewSet
from rest_framework.routers import SimpleRouter


tags_router = SimpleRouter()
tags_router.register('', TagViewSet)

urlpatterns = [
    path('', include(tags_router.urls))
]
