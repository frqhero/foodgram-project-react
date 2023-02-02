from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    measurement_unit = models.CharField(max_length=200, blank=False, null=False)

    def __str__(self):
        return self.name
