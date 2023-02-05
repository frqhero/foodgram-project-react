# Generated by Django 4.1.5 on 2023-02-03 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0002_alter_tag_color_alter_tag_name_alter_tag_slug"),
        ("recipes", "0010_remove_recipe_tags_recipe_ingredients"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(to="tags.tag"),
        ),
    ]