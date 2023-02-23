from django.db.models import Count
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import User
from .paginations import CustomPageNumberPagination
from .serializers import SubSrl


class MyViewSet(DjoserUserViewSet):
    pagination_class = CustomPageNumberPagination

    def get_permissions(self):
        if self.action == "me":
            self.permission_classes = [IsAuthenticated]
            return [permission() for permission in self.permission_classes]
        else:
            return super().get_permissions()


class SubViewSet(
    mixins.ListModelMixin, GenericViewSet):
    serializer_class = SubSrl
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = serializer.data
            recipes_limit = request.query_params.get("recipes_limit", None)
            if recipes_limit is not None and recipes_limit.isnumeric():
                for item in data:
                    item['recipes'] = item['recipes'][:int(recipes_limit)]
            return self.get_paginated_response(data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        user = self.request.user
    #     filter_value = self.request.query_params.get('recipes_limit', None)
    #     if filter_value:
    #         return user.subscriptions.annotate(
    #             recipes_count=Count('recipe')).filter(
    #             recipes_count=filter_value)
        return user.subscriptions.all()

    def post(self, request, id):
        following = get_object_or_404(User, id=id)
        user = request.user
        try:
            if user == following:
                raise Exception('Follower cannot follow themselves')
            in_subs = bool(user.subscriptions.filter(id=id))
            if in_subs:
                raise Exception('Already in subs')
            request.user.subscriptions.add(following)
            srl = SubSrl(instance=following, context={'request': request})
            return Response(srl.data, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        following = get_object_or_404(User, id=id)
        try:
            in_subs = bool(request.user.subscriptions.filter(id=id))
            if not in_subs:
                raise Exception('Not in subs')
            request.user.subscriptions.remove(following)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
