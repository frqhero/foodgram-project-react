from django.db.models import F, Sum, Q
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from recipes.filters import RecipeFilter
from recipes.mixins import PerformCreateAndDestroy
from recipes.models import Recipe
from recipes.permissions import IsAuthor
from recipes.serializers import RecipeCreateSerializer, RecipeReadSerializer
from users.paginations import CustomPageNumberPagination


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    filterset_fields = ('author',)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        anon = user.is_anonymous
        tags = self.request.query_params.getlist('tags')
        if tags:
            q_list = [Q(tags__slug__icontains=param) for param in tags]
            q_object = q_list.pop()
            for q in q_list:
                q_object |= q
            queryset = queryset.filter(q_object).distinct()
        is_favorited = self.request.query_params.get('is_favorited')
        if is_favorited is not None and not anon:
            if is_favorited == '0':
                queryset = queryset.exclude(favorites=user)
            elif is_favorited == '1':
                queryset = queryset.filter(favorites=user)
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart'
        )
        if is_in_shopping_cart is not None and not anon:
            if is_in_shopping_cart == '0':
                queryset = queryset.exclude(purchases=user)
            elif is_in_shopping_cart == '1':
                queryset = queryset.filter(purchases=user)
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
