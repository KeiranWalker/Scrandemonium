from django.urls import path
from scrandemonium import views

app_name = 'scrandemonium'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('recipes/', views.recipes, name='recipes'),
    path('recipes/<int:recipe_id>/', views.recipe, name='recipe_page'),
    path('recipes/<str:meal_type>/', views.recipes, name='recipes_by_category'),
    path('recipes/<int:recipe_id>/review/', views.review_recipe, name='review_recipe'),
    path('login/', views.user_login, name='login'),
    path('login/profile/', views.my_profile, name='my_profile'),
    path('login/add_recipe/', views.add_recipe, name='add_recipe'),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:id>/', views.other_profile, name="other_profile"),
    path('search_result/', views.search_result, name='search_result'),
    path('recipe_search_result/<str:meal_type>', views.recipe_search_result, name='recipe_search_result')
 ]