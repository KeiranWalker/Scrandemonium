from djanog.urls import path
from rango import views

app_name = 'scrandemonium'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('recipes/<str:meal_type>/', views.recipe_, name='recipes_by_category'),
    path('recipes/<int:recipe_id>/', views.recipe_page, name='recipe_page'),
    path('recipes/<int:recipe_id>/review/', views.review_recipe, name='review_recipe'),
    path('login/', views.user_login, name='login'),
    path('login/profile/<int:user_id>/', views.profile, name='profile'),
    path('login/addRecipe/', views.add_recipe, name='add_recipe'),
    path('about/', views.about, name='about'),
 ]