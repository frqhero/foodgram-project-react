from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from recipes.models import Recipe

from .models import User


class RecipeInline(admin.TabularInline):
    model = Recipe
    # can_delete = False
    # verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (("Favs"), {"fields": ("favorites",)}),
        (("Subs"), {"fields": ("subscriptions",)}),
        (("Cart"), {"fields": ("shopping_cart",)}),
    )


# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(User, UserAdmin)
