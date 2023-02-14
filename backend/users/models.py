from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    favorites = models.ManyToManyField('recipes.Recipe', blank=True, related_name='favorites')
    subscriptions = models.ManyToManyField('users.User', blank=True)
    shopping_cart = models.ManyToManyField('recipes.Recipe', blank=True, related_name='purchases')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
