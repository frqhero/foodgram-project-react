from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16)
    color = models.CharField(max_length=16)
    slug = models.CharField(max_length=16)
