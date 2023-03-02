from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True, verbose_name=_('name'))
    color = models.CharField(
        max_length=16, unique=True, verbose_name=_('color')
    )
    slug = models.CharField(max_length=16, unique=True, verbose_name=_('slug'))

    class Meta:
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.name
