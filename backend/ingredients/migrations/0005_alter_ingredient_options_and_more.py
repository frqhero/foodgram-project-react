# Generated by Django 4.1.5 on 2023-02-23 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0004_alter_ingredient_measurement_unit_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'verbose_name': 'ingredient',
                'verbose_name_plural': 'ingredients',
            },
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='measurement_unit',
            field=models.CharField(
                max_length=200, verbose_name='measurement unit'
            ),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='name',
            field=models.CharField(max_length=200, verbose_name='name'),
        ),
    ]