from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Recipe, Rating, Comment, Favourite, Media, RecipeIngredient, Ingredient, User
from django.db.models import Avg
from .forms import CustomUserCreationForm, ProfileForm, AddRecipeForm, LoginForm, ReviewForm

#from forms import AddRecipeForm  # Ozi needs to create this

# INDEX PAGE
def index(request):
    newest_recipes = Recipe.objects.order_by('-id')[:5]
    best_rated = Recipe.objects.annotate(avg_rating=Avg('ratings__rating')).order_by('-avg_rating')[:5]

    return render(request, 'scrandemonium/index.html', {
        'newest_recipes': newest_recipes,
        'best_rated': best_rated
    })

# LOGIN PAGE
def user_login(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user:
            auth_login(request, user)
            return redirect('scrandemonium:index')
        else:
            form.add_error(None, "Invalid username or password")

    return render(request, 'scrandemonium/login.html', {'form': form})


# ADD RECIPE PAGE
@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = AddRecipeForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            recipe = form.save()
            return redirect('recipe_page', recipe_id=recipe.id)
    else:
        form = AddRecipeForm()
    return render(request, 'scrandemonium/add_recipe.html', {'form': form})

# RECIPE PAGE
def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    media = Media.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)

    return render(request, 'scrandemonium/recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'media': media,
        'comments': comments,
    })

# REGISTER PAGE
def register(request):
    registered = False

    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Save profile info into same user
            user.biography = profile_form.cleaned_data.get('biography')
            user.profile_picture = profile_form.cleaned_data.get('profile_picture')
            user.save()
            registered = True
    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'scrandemonium/register.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'registered': registered
    })

# RECIPES PAGE
def recipes(request, meal_type):
    # Filter recipes by meal_type (e.g. "Lunch", "Dinner", etc.)
    recipes = Recipe.objects.filter(meal_type=meal_type)
    # Annotate with average rating
    recipes = recipes.annotate(rating_avg=Avg('ratings__rating'))

    return render(request, 'scrandemonium/recipes.html', {
        'MealType': meal_type,
        'recipes': recipes,
    })

# REVIEWRECIPE PAGE
@login_required
def review_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Save comment
            Comment.objects.create(
                user=request.user,
                recipe=recipe,
                comment=form.cleaned_data['comment']
            )
            # Save or update rating (to avoid having multiple ratings if multiple comments from 1 user)
            Rating.objects.update_or_create(
                user=request.user,
                recipe=recipe,
                defaults={'rating': form.cleaned_data['rating']}
            )
            return redirect('recipe_page', recipe_id=recipe.id)
    else:
        form = ReviewForm()

    return render(request, 'scrandemonium/review_recipe.html', {
        'recipe': recipe,
        'form': form,
    })

#LOGOUT
@login_required
def logout_user(request):
    auth_logout(request)
    return redirect(reverse('scrandemonium:index'))

# PROFILE PAGE
@login_required
def my_profile(request):
    user_recipes = request.user.recipes.all()
    user_favourites = Favourite.objects.filter(user=request.user)
    user_comments = Comment.objects.filter(user=request.user)

    return render(request, 'scrandemonium/profile.html', {
        'user_recipes': user_recipes,
        'user_favourites': user_favourites,
        'user_comments': user_comments,
    })

# ABOUT PAGE
def about(request):
    return render(request, 'scrandemonium/about.html')
