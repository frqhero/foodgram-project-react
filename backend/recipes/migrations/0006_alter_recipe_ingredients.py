# Generated by Django 4.1.5 on 2023-03-02 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0005_alter_ingredient_options_and_more'),
        ('recipes', '0005_alter_recipe_ingredients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(
                through='recipes.RecipeIngredient',
                to='ingredients.ingredient',
                verbose_name='ingredients',
            ),
        ),
    ]
