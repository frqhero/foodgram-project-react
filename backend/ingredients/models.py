from django.db import models
from django.utils.translation import gettext_lazy as _


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, blank=False, null=False, verbose_name=_('name')
    )
    measurement_unit = models.CharField(
        max_length=200,
        blank=False,
        null=False,
        verbose_name=_('measurement unit'),
    )

    class Meta:
        verbose_name = _('ingredient')
        verbose_name_plural = _('ingredients')

    def __str__(self):
        return self.name
