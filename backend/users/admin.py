from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe
from users.models import User


class RecipeInline(admin.TabularInline):
    model = Recipe


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        ((_('favorites')), {'fields': ('favorites',)}),
        ((_('subscriptions')), {'fields': ('subscriptions',)}),
        ((_('shopping cart')), {'fields': ('shopping_cart',)}),
    )


admin.site.register(User, UserAdmin)
