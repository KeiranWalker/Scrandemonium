from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import Recipe, Rating, Comment, Favourite, Media, RecipeIngredient, Ingredient
from django.db.models import Avg
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
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('index')
    return render(request, 'scrandemonium/login.html')

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
    return render(request, 'scrandemonium/addRecipe.html', {'form': form})

# RECIPE PAGE
def recipe_page(request, recipe_id):
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
# WAITING ON REGISTER.HTML

# RECIPES PAGE
# WAITING ON RECIPES.HTML

# PROFILE PAGE
@login_required
def profile(request):
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
