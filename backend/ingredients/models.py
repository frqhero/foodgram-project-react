from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=50, blank=False, null=False)
    measurement_unit = models.CharField(max_length=10, blank=False, null=False)
