# Generated by Django 4.1.5 on 2023-02-23 22:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0005_alter_ingredient_options_and_more"),
        ("recipes", "0002_initial"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="recipeingredient",
            unique_together={("ingredient", "recipe")},
        ),
    ]
