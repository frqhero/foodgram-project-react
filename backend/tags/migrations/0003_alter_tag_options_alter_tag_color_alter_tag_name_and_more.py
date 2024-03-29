# Generated by Django 4.1.5 on 2023-03-04 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_alter_tag_color_alter_tag_name_alter_tag_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'tag', 'verbose_name_plural': 'tags'},
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, verbose_name='color'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=16, unique=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.CharField(max_length=16, unique=True, verbose_name='slug'),
        ),
    ]
