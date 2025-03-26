from django.contrib import admin
from scrandemonium.models import User, Comment, Tag, RecipeTag, Recipe, RecipeIngredient, Ingredient, Media, Favourite, Rating, CommentLike

# Register your models here.

admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(RecipeTag)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
admin.site.register(Media)
admin.site.register(Favourite)
admin.site.register(Rating)
admin.site.register(CommentLike)