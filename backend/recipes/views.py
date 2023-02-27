from django.db.models import F, Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.paginations import CustomPageNumberPagination

from .filters import RecipeFilter
from .mixins import PerformCreateAndDestroy
from .models import Recipe
from .permissions import IsAuthor
from .serializers import RecipeCreateSerializer, RecipeReadSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        anon = user.is_anonymous
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and not anon:
            if is_favorited == '0':
                queryset = queryset.exclude(favorites__user=user)
            elif is_favorited == '1':
                queryset = queryset.filter(favorites__user=user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart', None
        )
        if is_in_shopping_cart is not None and not anon:
            if is_in_shopping_cart == '0':
                queryset = queryset.exclude(purchases__user=user)
            elif is_in_shopping_cart == '1':
                queryset = queryset.filter(purchases__user=user)
        return queryset

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


class FavoriteAPIView(APIView, PerformCreateAndDestroy):
    def get(self, request):
        res = request.user.shopping_cart.values(
            ingredient=F('recipeingredient__ingredient__name'),
            measurement_unit=F(
                'recipeingredient__ingredient__measurement_unit'
            ),
        ).annotate(amount=Sum('recipeingredient__amount'))
        content = ''
        for item in res:
            if item['ingredient']:
                content += (
                    f"{item['ingredient']} ({item['measurement_unit']}) - {item['amount']}"
                    + '\n'
                )

        # Create the text file
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="myfile.txt"'

        # Return the text file as a response
        return response

    def post(self, request, id):
        self.list_type = 'favorites'
        self.error_msg = 'Already in favorites'
        return self.create(request, id)

    def delete(self, request, id):
        self.list_type = 'favorites'
        self.error_msg = 'Not in favorites'
        return self.destroy(request, id)


class CartViewSet(APIView, PerformCreateAndDestroy):
    def post(self, request, id):
        self.list_type = 'shopping_cart'
        self.error_msg = 'Already in shopping cart'
        return self.create(request, id)

    def delete(self, request, id):
        self.list_type = 'shopping_cart'
        self.error_msg = 'Not in shopping cart'
        return self.destroy(request, id)
