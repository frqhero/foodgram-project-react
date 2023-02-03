from django.db import models
from ingredients.models import Ingredient
from users.models import User
from tags.models import Tag


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    ingredients = models.ManyToManyField(
        Ingredient, through="RecipeIngredient", related_name="ingredients"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quantity)
