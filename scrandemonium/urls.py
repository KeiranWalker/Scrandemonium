from django.urls import path
from scrandemonium import views

app_name = 'scrandemonium'

urlpatterns = [
    path('', views.index, name='index'),
    #path('register/', views.register, name='register'),
    #path('recipes/', views.recipes, name='recipes'),
    #path('recipes/<str:meal_type>/', views.recipes, name='recipes_by_category'),
    path('recipes/<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    #path('recipes/<int:recipe_id>/review/', views.review_recipe, name='review_recipe'),
    path('login/', views.login_view, name='login'),
    path('login/profile/<int:user_id>/', views.profile, name='profile'),
    path('login/addRecipe/', views.add_recipe, name='add_recipe'),
    path('about/', views.about, name='about'),
 ]