# Generated by Django 4.2.5 on 2023-09-17 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_ingredient_delete_recipeingredient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='ingredient',
        ),
        migrations.AddField(
            model_name='recipe',
            name='ingredient',
            field=models.ManyToManyField(to='recipes.ingredient', verbose_name='ингредиент'),
        ),
    ]