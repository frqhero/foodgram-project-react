from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.paginations import CustomPageNumberPagination

from .filters import RecipeFilter
from .models import Recipe, RecipeIngredient
from .permissions import IsAuthor
from .serializers import (RecipeCreateSerializer, RecipeFavSrl,
                          RecipeReadSerializer)


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        anon = user.is_anonymous
        is_favorited = self.request.query_params.get("is_favorited", None)
        if is_favorited is not None and not anon:
            if is_favorited == "0":
                queryset = queryset.exclude(favorites__user=user)
            elif is_favorited == "1":
                queryset = queryset.filter(favorites__user=user)
        is_in_shopping_cart = self.request.query_params.get(
            "is_in_shopping_cart", None
        )
        if is_in_shopping_cart is not None and not anon:
            if is_in_shopping_cart == "0":
                queryset = queryset.exclude(purchases__user=user)
            elif is_in_shopping_cart == "1":
                queryset = queryset.filter(purchases__user=user)
        return queryset

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
    def get(self, request):
        res = request.user.shopping_cart.values(
            ingredient=F("recipeingredient__ingredient__name"),
            measurement_unit=F(
                "recipeingredient__ingredient__measurement_unit"
            ),
        ).annotate(amount=Sum("recipeingredient__amount"))
        x = 1
        content = ""
        for item in res:
            if item["ingredient"]:
                content += (
                    f"{item['ingredient']} ({item['measurement_unit']}) - {item['amount']}"
                    + "\n"
                )

        # Create the text file
        response = HttpResponse(content, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="myfile.txt"'

        # Return the text file as a response
        return response

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
