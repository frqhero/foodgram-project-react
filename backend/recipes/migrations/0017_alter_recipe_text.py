# Generated by Django 4.1.5 on 2023-02-06 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0016_recipe_cooking_time_recipe_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="text",
            field=models.TextField(blank=True, null=True),
        ),
    ]