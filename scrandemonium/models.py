from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings

# -- RECIPE --
class Recipe(models.Model):
    MEAL_TYPES = [
        ('Breakfast', 'Breakfast'),
        ('Lunch', 'Lunch'),
        ('Dinner', 'Dinner'),
        ('Dessert', 'Dessert'),
        ('Snack', 'Snack'),
    ]

    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=32)
    step = models.TextField(max_length=5000)
    meal_type = models.CharField(max_length=10, choices=MEAL_TYPES)
    servings = models.PositiveIntegerField(null=True, blank=True)
    cooking_time = models.PositiveIntegerField(null=True, blank=True)
    fav_count = models.PositiveIntegerField(default=0)  # Optional, can also be calculated

    def __str__(self):
        return self.title
    
# -- COMMENT --
class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField(max_length=5000)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.recipe}"


# -- RATING (Separate from Comment) --
class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ratings')
    rating = models.IntegerField()

    class Meta:
        unique_together = ('user', 'recipe')  # Ensure one rating per user per recipe

    def __str__(self):
        return f"{self.user} rated {self.recipe} as {self.rating}"


# -- COMMENT LIKES --
class CommentLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_comments')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        unique_together = ('user', 'comment')  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user} liked comment {self.comment_id}"


# -- FAVOURITE --
class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favourites')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='favourited_by')

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user} favourited {self.recipe}"


# -- TAG --
class Tag(models.Model):
    name = models.CharField(max_length=16, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tags')

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'tag')


# -- INGREDIENT --
class Ingredient(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=16)

    class Meta:
        unique_together = ('recipe', 'ingredient')


# -- MEDIA --
class Media(models.Model):
    MEDIA_TYPES = [
        ('Video', 'Video'),
        ('Image', 'Image'),
    ]

    media_id = models.AutoField(primary_key=True)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='media')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    media_url = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.media_type} for {self.recipe}"

# -- USER --
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)
    
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(max_length=128, blank=True, null=True)
    biography = models.TextField(max_length=5000, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_staff = models.BooleanField(default=False)  # Used to access admin site
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
