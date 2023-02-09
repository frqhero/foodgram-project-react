from django.core.validators import MinValueValidator
from django.db import models
from ingredients.models import Ingredient
from users.models import User
from tags.models import Tag


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField(blank=True, null=True)
    ingredients = models.ManyToManyField(
        Ingredient, through="recipes.RecipeIngredient")
    tags = models.ManyToManyField(Tag, blank=True)
    cooking_time = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()

    def __str__(self):
        return str(self.quantity)
