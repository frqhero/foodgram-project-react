from djoser.views import UserViewSet as DjoserUserViewSet
from .paginations import CustomPageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from .serializers import SubSrl
from django.db.models import Count


class MyViewSet(DjoserUserViewSet):
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        else:
            return super().get_permissions()


class FavsViewSet(mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubSrl
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        filter_value = self.request.query_params.get('recipes_limit', None)
        if filter_value:
            return user.subscriptions.annotate(
                recipes_count=Count('recipe')).filter(
                recipes_count=filter_value)
        return user.subscriptions.all()
