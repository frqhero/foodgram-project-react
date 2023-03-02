from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name=_('author')
    )
    name = models.CharField(max_length=200, verbose_name=_('name'))
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        verbose_name=_('image'),
    )
    text = models.TextField(blank=True, null=True, verbose_name=_('text'))
    ingredients = models.ManyToManyField(
        Ingredient,
        through='recipes.RecipeIngredient',
        verbose_name=_('ingredients'),
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_('tags'))
    cooking_time = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_('cooking time'),
    )

    class Meta:
        ordering = ['id']
        verbose_name = _('recipe')
        verbose_name_plural = _('recipes')

    def __str__(self):
        return f'{self.id} {self.name}'


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name=_('ingredient')
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name=_('recipe')
    )
    amount = models.PositiveIntegerField(verbose_name=_('amount'))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='unique recipe ingredient',
            )
        ]
        verbose_name = _('recipe ingredient')
        verbose_name_plural = _('recipes ingredients')

    def __str__(self):
        return str(self.amount)
