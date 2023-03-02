from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    favorites = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        related_name='favorites',
        verbose_name=_('favorites'),
    )
    subscriptions = models.ManyToManyField(
        'users.User', blank=True, verbose_name=_('subscriptions')
    )
    shopping_cart = models.ManyToManyField(
        'recipes.Recipe',
        blank=True,
        related_name='purchases',
        verbose_name=_('shopping cart'),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['id']
        verbose_name = _('user')
        verbose_name_plural = _('users')
