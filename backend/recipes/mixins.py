from .models import Recipe
from .serializers import RecipeFavSrl
from rest_framework.response import Response
from rest_framework import status


class PerformCreateAndDestroy:
    def create(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_list = getattr(request.user, self.list_type).filter(pk=recipe.id).exists()
            if in_list:
                raise Exception(self.error_msg)
            getattr(request.user, self.list_type).add(recipe)
            srl = RecipeFavSrl(instance=recipe, context={"request": request})
            return Response(srl.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, id):
        try:
            recipe = Recipe.objects.get(id=id)
            in_list = getattr(request.user, self.list_type).filter(pk=recipe.id).exists()
            if not in_list:
                raise Exception(self.error_msg)
            getattr(request.user, self.list_type).remove(recipe)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(
                {"errors": e.args[0]}, status=status.HTTP_400_BAD_REQUEST
            )
