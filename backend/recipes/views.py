from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Recipe, RecipeIngredient
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RecipeReadSerializer, RecipeCreateSerializer, RecipeFavSrl
)
from users.paginations import CustomPageNumberPagination
from .filters import RecipeFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsAuthor
from rest_framework.response import Response
from rest_framework import status


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return RecipeReadSerializer
        elif self.action == 'create' or self.action == 'partial_update':
            return RecipeCreateSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            self.permission_classes = [AllowAny]
        elif self.action == 'create':
            self.permission_classes = [IsAuthenticated]
        elif self.action == 'partial_update' or self.action == 'destroy':
            self.permission_classes = [IsAuthor]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        RecipeIngredient.objects.filter(recipe=instance).delete()
        instance.delete()


class FavoriteAPIView(APIView):
    def post(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_favs = bool(request.user.favorites.filter(pk=id))
            if in_favs:
                raise Exception('Already in favs')
            request.user.favorites.add(recipe)
            srl = RecipeFavSrl(instance=recipe, context={'request': request})
            return Response(srl.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_favs = bool(request.user.favorites.filter(pk=id))
            if not in_favs:
                raise Exception('Not in favs')
            request.user.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'errors': e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
