from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)
    color = models.CharField(max_length=16, unique=True)
    slug = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return self.name
