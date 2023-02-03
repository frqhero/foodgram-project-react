from django.contrib import admin
from .models import Recipe, RecipeTag


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
    ]

@admin.register(RecipeTag)
class RecipeTagAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tag',
        'recipe',
        'quantity',
    ]
