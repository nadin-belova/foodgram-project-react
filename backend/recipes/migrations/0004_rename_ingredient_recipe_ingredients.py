# Generated by Django 4.2.5 on 2023-09-17 17:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_remove_recipe_ingredient_recipe_ingredient'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='ingredient',
            new_name='ingredients',
        ),
    ]