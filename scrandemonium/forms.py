from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import modelformset_factory
from .models import Recipe, User, Tag, RecipeIngredient

# -- ADD RECIPE --
class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'meal_type', 'servings', 'cooking_time']

# -- USER/PROFILE --
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('biography', 'profile_picture')

# -- LOGIN -- 
class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

# -- REVIEW --
class ReviewForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, label='Your Comment')
    rating = forms.IntegerField(min_value=1, max_value=5, label='Your Rating')