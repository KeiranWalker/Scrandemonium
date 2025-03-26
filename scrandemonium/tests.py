from django.test import TestCase
from django.db import IntegrityError
from scrandemonium.models import User, Recipe, Rating, Comment, CommentLike, Favourite, Tag, Ingredient, Media, RecipeTag, RecipeIngredient
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime
from scrandemonium_project.settings import STATIC_URL

class UserTest(TestCase):

    # Checks User Creation
    def test_user_creation(self):
        test_user = User.objects.create(username="test", email="test123@sky.com")
        User.set_password(self=test_user, raw_password="Password1")
        self.assertEqual("test", test_user.username)
        self.assertEqual("test123@sky.com", test_user.email)
        self.assertTrue(test_user.check_password(raw_password="Password1"))
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)
        self.assertFalse(test_user.is_staff)

    # Check Email None When Not Specified
    def test_user_creation_no_email(self):
        test_user = User.objects.create(username="test")
        User.set_password(self=test_user, raw_password="Password1")
        self.assertEqual("test", test_user.username)
        self.assertEqual(None, test_user.email)
        self.assertTrue(test_user.check_password(raw_password="Password1"))
        self.assertFalse(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    # Check is_superuser
    def test_user_creation_superuser(self):
        test_user = User.objects.create(username="test", email="test123@sky.com", is_superuser=True)
        User.set_password(self=test_user, raw_password="Password1")
        self.assertEqual("test", test_user.username)
        self.assertEqual("test123@sky.com", test_user.email)
        self.assertTrue(test_user.check_password(raw_password="Password1"))
        self.assertFalse(test_user.is_staff)
        self.assertTrue(test_user.is_superuser)

    # Check is_staff
    def test_user_creation_staff(self):
        test_user = User.objects.create(username="test", email="test123@sky.com", is_staff=True)
        User.set_password(self=test_user, raw_password="Password1")
        self.assertEqual("test", test_user.username)
        self.assertEqual("test123@sky.com", test_user.email)
        self.assertTrue(test_user.check_password(raw_password="Password1"))
        self.assertTrue(test_user.is_staff)
        self.assertFalse(test_user.is_superuser)

    # Check User String Rep
    def test_user_string_representation(self):
        test_user = User.objects.create(username="test")
        self.assertEqual("test", str(test_user))


class RecipeTest(TestCase):

    # Check Recipes Creation
    def test_recipe_created_successfully(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name", step="step1;step2", meal_type="Breakfast", servings=4, cooking_time=30, fav_count=7)
        self.assertEqual(test_user, test_recipe.user)
        self.assertEqual("test_name", test_recipe.title)
        self.assertEqual("step1;step2", test_recipe.step)
        self.assertEqual("Breakfast", test_recipe.meal_type)
        self.assertEqual(4, test_recipe.servings)
        self.assertEqual(30, test_recipe.cooking_time)
        self.assertEqual(7, test_recipe.fav_count)

    # Check Recipe String Rep
    def test_recipe_string_representation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name", step="step1;step2", meal_type="Breakfast", servings=4, cooking_time=30, fav_count=7)
        self.assertEqual("test_name", str(test_recipe))
    
    # Check Default Fav Count
    def test_recipe_default_fav_count(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name", step="step1;step2", meal_type="Breakfast", servings=4, cooking_time=30)
        self.assertEqual(0, test_recipe.fav_count)

    # Ensure Validation Error when invalid meal type passed
    def test_recipe_meal_type_invalid(self):
        with self.assertRaises(ValidationError):
            test_user = User.objects.create(username="test")
            test_recipe = Recipe.objects.create(user=test_user, title="test_name", step="step1;step2", servings=4, cooking_time=30, meal_type = "Brunch")
            test_recipe.full_clean()


class RatingTests(TestCase):

    # Check Rating Creation
    def test_rating_creation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_rating = Rating.objects.create(user=test_user, recipe=test_recipe, rating=5)
        self.assertEqual(test_user, test_rating.user)
        self.assertEqual(test_recipe, test_rating.recipe)
        self.assertEqual(5, test_rating.rating)

    # Check Rating Unique Property
    def test_rating_unique(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_rating = Rating.objects.create(user=test_user, recipe=test_recipe, rating=5)
        with self.assertRaises(IntegrityError):
            test_user2 = User.objects.create(username="test")
            test_recipe2 = Recipe.objects.create(user=test_user2, title="test_name")
            test_rating2 = Rating.objects.create(user=test_user2, recipe=test_recipe2, rating=4)
    
    # Check Rating String Rep
    def test_rating_string_representation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_rating = Rating.objects.create(user=test_user, recipe=test_recipe, rating=5)
        self.assertEqual("test rated test_name as 5", str(test_rating))

class CommentTests(TestCase):

    # Check Comment Creation
    def test_comment_creation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_comment = Comment.objects.create(user=test_user, recipe=test_recipe, comment="This is my comment")
        self.assertEqual(test_user, test_comment.user)
        self.assertEqual(test_recipe, test_comment.recipe)
        self.assertAlmostEqual(timezone.now(), test_comment.date, delta=datetime.timedelta(seconds=1))
    
    # Check Comment String Rep
    def test_comment_string_representation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_comment = Comment.objects.create(user=test_user, recipe=test_recipe, comment="This is my comment")
        self.assertEqual("Comment by test on test_name", str(test_comment))


class CommentLikeTests(TestCase):

    # Check CommentLike Creation
    def test_comment_like_creation(self):
        test_user = User.objects.create(username="test") # User can like their own comment
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_comment = Comment.objects.create(user=test_user, recipe=test_recipe, comment="This is my comment")
        test_comment_like = CommentLike.objects.create(user=test_user, comment=test_comment)
        self.assertEqual(test_user, test_comment_like.user)
        self.assertEqual(test_comment, test_comment_like.comment)
    
    # Check Unique Property
    def test_comment_like_unique(self):
        test_user = User.objects.create(username="test") 
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_comment = Comment.objects.create(user=test_user, recipe=test_recipe, comment="This is my comment")
        test_comment_like = CommentLike.objects.create(user=test_user, comment=test_comment)
        
        with self.assertRaises(IntegrityError):
            test_comment_like2 = CommentLike.objects.create(user=test_user, comment=test_comment)

    # Check CommentLike String Rep
    def test_comment_like_string_representation(self):
        test_user = User.objects.create(username="test") 
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_comment = Comment.objects.create(user=test_user, recipe=test_recipe, comment="This is my comment")
        test_comment_like = CommentLike.objects.create(user=test_user, comment=test_comment)
        self.assertEqual("test liked comment 1", str(test_comment_like))

class FavouriteTest(TestCase):

    # Check Favourite Creation
    def test_favourite_creation(self):
        test_user = User.objects.create(username="test") 
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_favourite = Favourite.objects.create(user=test_user, recipe=test_recipe)
        self.assertEqual(test_user, test_favourite.user)
        self.assertEqual(test_recipe, test_favourite.recipe)

    # ChecK Unique Property
    def test_favourite_unique(self):
        test_user = User.objects.create(username="test") 
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_favourite = Favourite.objects.create(user=test_user, recipe=test_recipe)
        
        with self.assertRaises(IntegrityError):
            test_favourite2 = Favourite.objects.create(user=test_user, recipe=test_recipe)

    # Check String Rep
    def test_favourite_string_representation(self):
        test_user = User.objects.create(username="test") 
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_favourite = Favourite.objects.create(user=test_user, recipe=test_recipe)
        self.assertEqual("test favourited test_name", str(test_favourite))


class TagTests(TestCase):

    # Check Tag Creation
    def test_tag_creation(self):
        test_user = User.objects.create(username="test")
        test_tag = Tag.objects.create(name="my_tag", user=test_user)
        self.assertEqual("my_tag", test_tag.name)
        self.assertEquals(test_user, test_tag.user)

    # Check Tag String Rep
    def test_tag_string_representation(self):
        test_user = User.objects.create(username="test")
        test_tag = Tag.objects.create(name="my_tag", user=test_user)
        self.assertEqual("my_tag", str(test_tag))


class IngredientTests(TestCase):
    
    # Check Ingredient Creation
    def test_ingredient_creation(self):
        test_ingredient = Ingredient.objects.create(name="my_ingredient")
        self.assertEqual("my_ingredient", test_ingredient.name)

    # Check Ingredient String Rep
    def test_ingredient_string_representation(self):
        test_ingredient = Ingredient.objects.create(name="my_ingredient")
        self.assertEqual("my_ingredient", str(test_ingredient))


class RecipeTagTests(TestCase):

    # Check RecipeTag Creation
    def test_recipe_tag_creation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_tag = Tag.objects.create(name="my_tag", user=test_user)
        test_recipe_tag = RecipeTag.objects.create(recipe=test_recipe, tag=test_tag)
        self.assertEqual(test_recipe, test_recipe_tag.recipe)
        self.assertEqual(test_tag, test_recipe_tag.tag)

    # Check Unique Property
    def test_recipe_tag_unique(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_tag = Tag.objects.create(name="my_tag", user=test_user)
        test_recipe_tag = RecipeTag.objects.create(recipe=test_recipe, tag=test_tag)
        
        with self.assertRaises(IntegrityError):
            test_recipe_tag2 = RecipeTag.objects.create(recipe=test_recipe, tag=test_tag)


class RecipeIngredientTests(TestCase):

    # Check RecipeIngredient Creation
    def test_recipe_ingredient_creation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_ingredient = Ingredient.objects.create(name="my_ingredient")
        test_recipe_ingredient = RecipeIngredient.objects.create(recipe=test_recipe, ingredient=test_ingredient, quantity="2 cups")
        self.assertEqual(test_recipe, test_recipe_ingredient.recipe)
        self.assertEqual(test_ingredient, test_recipe_ingredient.ingredient)
        self.assertEqual("2 cups", test_recipe_ingredient.quantity)

    # Check Unique Property
    def test_recipe_ingredient_unique(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_ingredient = Ingredient.objects.create(name="my_ingredient")
        test_recipe_ingredient = RecipeIngredient.objects.create(recipe=test_recipe, ingredient=test_ingredient, quantity="2 cups")
        
        with self.assertRaises(IntegrityError):
            test_recipe_ingredient2 = RecipeIngredient.objects.create(recipe=test_recipe, ingredient=test_ingredient, quantity="2 cups")
          

class MediaTests(TestCase):

    # Check Media Creation
    def test_media_creation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_media = Media.objects.create(recipe=test_recipe, media_type="Video", media_url=STATIC_URL + "steak_dinner.jpg")
        self.assertEqual(test_recipe, test_media.recipe)
        self.assertEqual("Video", test_media.media_type)
        self.assertEqual(STATIC_URL + "steak_dinner.jpg", test_media.media_url)

    # Ensure Validation Error when invalid media type passed
    def test_media_media_type_invalid(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_media = Media.objects.create(recipe=test_recipe, media_type="Colouring in picture", media_url=STATIC_URL + "steak_dinner.jpg")
        
        with self.assertRaises(ValidationError):
            test_media.full_clean()
     
    # Check Media String Rep
    def test_media_string_representation(self):
        test_user = User.objects.create(username="test")
        test_recipe = Recipe.objects.create(user=test_user, title="test_name")
        test_media = Media.objects.create(recipe=test_recipe, media_type="Video", media_url=STATIC_URL + "steak_dinner.jpg")
        self.assertEqual("Video for test_name", str(test_media))