# Generated by Django 4.1.5 on 2023-02-02 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ingredients", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="name",
            field=models.CharField(max_length=100),
        ),
    ]
