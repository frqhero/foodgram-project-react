from django.db import models
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    tags = models.ManyToManyField(Tag, through='RecipeTag')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class RecipeTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
