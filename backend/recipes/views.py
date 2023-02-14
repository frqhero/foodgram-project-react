from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from .models import Recipe, RecipeIngredient
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import (
    RecipeReadSerializer,
    RecipeCreateSerializer,
    RecipeFavSrl,
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

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     user = self.request.user
    #     anon = user.is_anonymous
    #     is_favorited = self.request.query_params.get("is_favorited", None)
    #     if is_favorited is not None and not anon:
    #         if is_favorited == "0":
    #             user_favs = user.favorites.all()
    #             queryset = queryset.exclude(id__in=user_favs)
    #         elif is_favorited == "1":
    #             user_favs = user.favorites.all()
    #             queryset = queryset.filter(id__in=user_favs)
    #     is_in_shopping_cart = self.request.query_params.get(
    #         "is_in_shopping_cart", None
    #     )
    #     if is_in_shopping_cart is not None and not anon:
    #         if is_in_shopping_cart == "0":
    #             user_favs = user.shopping_cart.all()
    #             queryset = queryset.exclude(id__in=user_favs)
    #         elif is_in_shopping_cart == "1":
    #             user_favs = user.favorites.all()
    #             queryset = queryset.filter(id__in=user_favs)
    #     return queryset

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return RecipeReadSerializer
        elif self.action == "create" or self.action == "partial_update":
            return RecipeCreateSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            self.permission_classes = [AllowAny]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated]
        elif self.action == "partial_update" or self.action == "destroy":
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
                raise Exception("Already in favs")
            request.user.favorites.add(recipe)
            srl = RecipeFavSrl(instance=recipe, context={"request": request})
            return Response(srl.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_favs = bool(request.user.favorites.filter(pk=id))
            if not in_favs:
                raise Exception("Not in favs")
            request.user.favorites.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )


class CartViewSet(APIView):
    def post(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_shopping_cart = bool(request.user.shopping_cart.filter(pk=id))
            if in_shopping_cart:
                raise Exception("Already in cart")
            request.user.shopping_cart.add(recipe)
            srl = RecipeFavSrl(instance=recipe, context={"request": request})
            return Response(srl.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_shopping_cart = bool(request.user.shopping_cart.filter(pk=id))
            if not in_shopping_cart:
                raise Exception("Not in cart")
            request.user.shopping_cart.remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )
