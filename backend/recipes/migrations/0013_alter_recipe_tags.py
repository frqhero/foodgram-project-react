# Generated by Django 4.1.5 on 2023-02-03 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tags", "0002_alter_tag_color_alter_tag_name_alter_tag_slug"),
        ("recipes", "0012_alter_recipe_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="recipe",
            name="tags",
            field=models.ManyToManyField(blank=True, to="tags.tag"),
        ),
    ]
