from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Recipe, Rating, Comment, Favourite, Media, RecipeIngredient, Ingredient, RecipeTag, Tag, User
from django.db.models import Avg
from .forms import CustomUserCreationForm, ProfileForm, AddRecipeForm, LoginForm, ReviewForm
from django.templatetags.static import static
from django.core.files.storage import FileSystemStorage

#from forms import AddRecipeForm  # Ozi needs to create this

# INDEX PAGE
def index(request):
    newest_recipes = Recipe.objects.order_by('-recipe_id')[:5]
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
        form = AddRecipeForm(request.POST)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.step = request.POST.get('step')
            recipe.save()

            # Tags (create if new)
            tag_names = request.POST.getlist('tags')
            for name in tag_names:
                name = name.strip()
                if name:
                    tag, _ = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name, 'user': request.user})
                    RecipeTag.objects.get_or_create(recipe=recipe, tag=tag)

            # Ingredients (create if new) + quantity
            ingredient_names = request.POST.getlist('ingredients')
            for name in ingredient_names:
                name = name.strip()
                quantity = request.POST.get(f'quantity_{name}', '').strip()
                if name and quantity:
                    ingredient, _ = Ingredient.objects.get_or_create(name__iexact=name, defaults={'name': name})
                    RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

            # MEDIA: Handle file uploads (IMAGE + VIDEO)
            image_file = request.FILES.get('recipe_picture_file')
            if image_file:
                fs = FileSystemStorage()
                filename = fs.save(f"recipe_pictures/{image_file.name}", image_file)
                image_url = fs.url(filename)
                Media.objects.create(recipe=recipe, media_type='IMAGE', media_url=image_url)

            video_file = request.FILES.get('recipe_video_file')
            if video_file:
                fs = FileSystemStorage()
                filename = fs.save(f"recipe_videos/{video_file.name}", video_file)
                video_url = fs.url(filename)
                Media.objects.create(recipe=recipe, media_type='VIDEO', media_url=video_url)

            return redirect('scrandemonium:recipe_page', recipe_id=recipe.recipe_id)
    else:
        form = AddRecipeForm()

    # Used for populating dropdowns
    all_ingredients = Ingredient.objects.all()
    all_tags = Tag.objects.all()

    return render(request, 'scrandemonium/add_recipe.html', {
        'form': form,
        'all_ingredients': all_ingredients,
        'all_tags': all_tags,
    })

# RECIPE PAGE
def recipe(request, recipe_id):

    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
    ingredients = RecipeIngredient.objects.filter(recipe=recipe)
    media = Media.objects.filter(recipe=recipe)
    comments = Comment.objects.filter(recipe=recipe)
    avg_rating = Rating.objects.filter(recipe=recipe).aggregate(Avg('rating'))['rating__avg']
    recipe_ratings = Rating.objects.filter(recipe=recipe)
    steps = recipe.step.split(';')

    # Handle POST: Toggle favourite
    if request.method == "POST" and request.user.is_authenticated:
        fav_obj, created = Favourite.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            fav_obj.delete()

        return redirect('scrandemonium:recipe_page', recipe_id=recipe_id)
    
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = Favourite.objects.filter(user=request.user, recipe=recipe).exists()

    favourite_count = recipe.favourited_by.count()

    return render(request, 'scrandemonium/recipe.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'media': media,
        'comments': comments,
        'avg_rating': avg_rating,
        'steps': steps,
        'recipe_ratings': recipe_ratings,
        'favourite_count': favourite_count,
        'is_favourite': is_favourite,
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
    recipe_image = {"Breakfast": static('breakfast.jpg'),
                    "Lunch": static('lunch.jpg'),
                    "Dinner": static('dinner.jpg'),
                    "Dessert": static('dessert.jpg'),
                    "Baking": static('baking.jpg'),
                    "Snacks": static('snack.jpg')}
    recipe_desc = {"Breakfast": "Breakfast... the first and the most important meal of the da., Providing energy and nutrients to start your morning. Breakfasts can range from eggs, to toast, to bacon, while healthier options feature oatmeal, yogurt, or fruit. Sweet or savory, breakfast fuels our bodies and boosts our metabolism. A balanced meal sets the tone for a productive day ahead.",
                  "Lunch": "Lunch - the middle of the day. It can range from light to filling, with options like a fresh salad, sandwiches, or wraps. Pasta, rice bowls, or soups can also make an appearance. Have some lunch to nourish your body and recharge you for the afternoon ahead.",
                  "Dinner": "Dinner is the evening meal, often the largest of the day. It’s a time to unwind and enjoy a variety of dishes, from simple pesto pasta, to a nice steak dinner. Family-style dinners or intimate meals with close friends, every dinner should be special.",
                  "Dessert": "Dessert is the bit we really all are looking forward to. Popular choices include cakes, pies, or pastries. Classic desserts like ice cream, sticky toffee, and apple pie hold a special place in all our hearts.  No matter what, dessert is a celebration of sweetness that adds a touch of joy to any dining experience.",
                  "Baking": "Baking is a method of cooking that involves using dry heat to prepare foods.  This can include pastries, biscuits, cakes, and cookies. Baking isn't easy and takes a lot of practise, but is so massively rewarding. From the smell of freshly baked bread to a perfectly golden pie, baking fills ours homes, and ourselves, with warmth.",
                  "Snacks": "Snacks are small, quick bites. Savory? Sweet? Healthy or indulgent?  What every floats your boat really.  Snacks can be enjoyed on-the-go, during a break at work, or as a cheeky little addition to the day. They bring joy in their convenience and variety."}
    # Filter recipes by meal_type (e.g. "Lunch", "Dinner", etc.)
    recipes = Recipe.objects.filter(meal_type=meal_type)
    # Annotate with average rating
    recipes = recipes.annotate(rating_avg=Avg('ratings__rating'))

    return render(request, 'scrandemonium/recipes.html', {
        'MealType': meal_type,
        'recipes': recipes,
        'image': recipe_image[meal_type],
        'description':recipe_desc[meal_type]
    })

# REVIEWRECIPE PAGE
@login_required
def review_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, recipe_id=recipe_id)
    media = Media.objects.filter(recipe=recipe, media_type="IMAGE").first()

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
            return redirect('scrandemonium:recipe_page', recipe_id=recipe.recipe_id)
    else:
        form = ReviewForm()

    return render(request, 'scrandemonium/review_recipe.html', {
        'recipe': recipe,
        'form': form,
        'media': media
    })

#LOGOUT
@login_required
def logout_user(request):
    auth_logout(request)
    return redirect(reverse('scrandemonium:index'))

# PROFILE PAGE
@login_required
def my_profile(request):
    user_recipes = Recipe.objects.filter(user=request.user)
    print(request.user.profile_picture)
    user_recipes = user_recipes.annotate(rating_avg=Avg('ratings__rating'))
    user_favourites = Favourite.objects.filter(user=request.user)

    for fav in user_favourites:
        image = fav.recipe.media.filter(media_type='IMAGE').first()
        fav.media_url = image.media_url if image else None

    user_comments = Comment.objects.filter(user=request.user)

    return render(request, 'scrandemonium/profile.html', {
        'user_recipes': user_recipes,
        'user_favourites': user_favourites,
        'user_comments': user_comments,
    })

# ABOUT PAGE
def about(request):
    return render(request, 'scrandemonium/about.html')

# Other User Profile Page
def other_profile(request, id):
    other_user = User.objects.get(id=id)
    other_user_recipes = Recipe.objects.filter(user=other_user)
    other_user_recipes = other_user_recipes.annotate(rating_avg=Avg('ratings__rating'))
    other_user_favourites = Favourite.objects.filter(user=other_user)
    
    for fav in other_user_favourites:
        image = fav.recipe.media.filter(media_type='IMAGE').first()
        fav.media_url = image.media_url if image else None

    other_user_comments = Comment.objects.filter(user=other_user)

    return render(request, 'scrandemonium/other_profile.html',{"other_user": other_user,
                            "other_user_recipes": other_user_recipes,
                            "other_user_favourites": other_user_favourites,
                            "other_user_comments": other_user_comments})

# Search
def search_result(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        recipes_by_title = Recipe.objects.filter(title__contains=searched)
        recipes_tag_by_tag = RecipeTag.objects.filter(tag__name__contains=searched)
        profiles = User.objects.filter(username__contains=searched)
        return render(request, 'scrandemonium/search_result.html', {'searched': searched,
                                                                    'recipes_by_title': recipes_by_title,
                                                                    'recipes_tag_by_tag': recipes_tag_by_tag,
                                                                    'profiles': profiles})
    else:
        return redirect('scrandemonium:index')
    
# Search Recipes
def recipe_search_result(request, meal_type):
    if request.method == 'POST':
        searched = request.POST.get('searched', '').strip()
        recipes = Recipe.objects.filter(title__contains=searched, meal_type=meal_type)

        return render(request, 'scrandemonium/recipe_search_result.html', {'searched': searched,
                                                                    'recipes': recipes, 'meal_type': meal_type})
    else:
        return redirect('scrandemonium:index')