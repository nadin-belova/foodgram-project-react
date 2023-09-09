from django.contrib import admin
from .models import MyUser
from recipes.models import (
    Unit,
    Tag,
    Ingredient,
    RecipeIngredient,
    Recipe
)


admin.site.register(MyUser)
admin.site.register(Unit)
admin.site.register(Tag)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(Recipe)
