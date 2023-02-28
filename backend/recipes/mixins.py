from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Recipe
from .serializers import RecipeFavSrl


class PerformCreateAndDestroy:
    def check(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        return (
            getattr(request.user, self.list_type)
                .filter(id=id)
                .exists()
        ), recipe

    def create(self, request, id):
        in_list, recipe = self.check(request, id)
        if in_list:
            raise Exception(self.error_msg)
        getattr(request.user, self.list_type).add(recipe)
        srl = RecipeFavSrl(instance=recipe, context={'request': request})
        return Response(srl.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, id):
        in_list, recipe = self.check(request, id)
        if not in_list:
            raise Exception(self.error_msg)
        getattr(request.user, self.list_type).remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)
