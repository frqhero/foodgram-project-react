from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import TagViewSet

tags_router = SimpleRouter()
tags_router.register('', TagViewSet)

urlpatterns = [path('', include(tags_router.urls))]
