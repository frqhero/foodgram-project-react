from django.db import models


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, blank=False, null=False, verbose_name="name"
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name="measurement unit",
    )

    class Meta:
        verbose_name = 'ingredient'
        verbose_name_plural = 'ingredients'

    def __str__(self):
        return self.name
