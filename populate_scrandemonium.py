from datetime import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrandemonium_project.settings')

import django
django.setup()

from scrandemonium.models import User, Comment, Tag, RecipeTag, Recipe, RecipeIngredient, Ingredient, Media, Favourite, Rating, CommentLike
from scrandemonium_project.settings import MEDIA_URL

def populate():

    # User
    users_data = [
        {"username": "JohnDoe123",
          "password": "Password1",
          "biography": "I am a fun, food loving, culinary genius.  Looking to share my gift with the world.", 
          "email": "JoeDoe123@gmail.com", 
          "profile_picture": "profile_pictures/PopulationScriptJohnDoe.png",
          "is_superuser": False},
        {"username": "Marge1967", 
         "password": "Password3", 
         "biography": "Hello Dears.  Grandmother of 2 xx", 
         "email": "MargeSmith67@sky.com", 
         "profile_picture": "profile_pictures/PopulationScriptMarge.jpg", 
         "is_superuser": False}
    ]

    user_mapping = {}

    for user in users_data:

        u = User.objects.create_user(username=user["username"], email=user["email"], is_staff=user["is_superuser"], biography=user["biography"], password=user["password"], profile_picture=user["profile_picture"])
            
        user_mapping[user["username"]] = u.id

        print(f"{u.username} => USERPROFILE created")

    # Recipe
    recipe_data = [
        {"meal_type": "Breakfast",
        "user": "JohnDoe123",
        "title": "Pancakes",
        "step": "Mix flour, sugar, baking powder, and salt; In a separate bowl, whisk eggs, milk, and butter; Combine wet and dry ingredients; Pour batter onto a heated pan; Flip when bubbles form; Cook until golden brown; Serve with syrup or fruits",
        "servings": 4,
        "cooking_time": 20,
        "fav_count": 25},

        {"meal_type": "Dinner",
        "user": "Marge1967",
        "title": "Spaghetti Bolognese",
        "step": "Heat olive oil in a pan; Cook onions and garlic until soft; Add ground beef and cook until browned; Stir in tomato sauce and herbs; Simmer for 20 minutes; Cook spaghetti according to package; Serve with grated Parmesan cheese",
        "servings": 4,
        "cooking_time": 40,
        "fav_count": 32},

        {"meal_type": "Dessert",
        "user": "JohnDoe123",
        "title": "Chocolate Lava Cake",
        "step": "Preheat oven to 220°C; Melt chocolate and butter together; Beat eggs and sugar until fluffy; Fold in melted chocolate; Pour batter into greased ramekins; Bake for 12 minutes until edges are set but center is gooey; Serve immediately",
        "servings": 2,
        "cooking_time": 15,
        "fav_count": 40}
    ]

    recipe_mapping = {}

    for recipe in recipe_data:
        user_id = user_mapping.get(recipe["user"])
        user = User.objects.get(id=user_id)
        
        r, created = Recipe.objects.get_or_create(
            title=recipe["title"],
            user=user,
            defaults={
                "meal_type": recipe["meal_type"],
                "step": recipe["step"],
                "servings": recipe["servings"],
                "cooking_time": recipe["cooking_time"],
                "fav_count": recipe["fav_count"]
            }
        )

        if created:
            r.save()
            print(f"{r.title} => RECIPE created")
            recipe_mapping[recipe["title"]] = r.recipe_id
        else:
            print(f"{r.title} => RECIPE already exists")



    # Ingredient
    ingredient_data = [
        {"name": "flour"},
        {"name": "sugar"},
        {"name": "salt"},
        {"name": "black-pepper"},
        {"name": "olive-oil"},
        {"name": "butter"},
        {"name": "milk"},
        {"name": "eggs"},
        {"name": "cheddar-cheese"},
        {"name": "chicken-breast"},
        {"name": "ground-beef"}, 
        {"name": "cheese"},
        {"name": "salmon"},
        {"name": "cream"},
        {"name": "shrimp"},
        {"name": "garlic"},
        {"name": "onion"},
        {"name": "carrot"},
        {"name": "tomato"},
        {"name": "lettuce"},
        {"name": "potato"},
        {"name": "rice"},
        {"name": "pasta"},
        {"name": "honey"},
        {"name": "soy sauce"},
        {"name": "vinegar"},
        {"name": "cinnamon"},
        {"name": "basil"},
        {"name": "oregano"},
        {"name": "cumin"},
        {"name": "coconut-milk"},
        {"name": "almonds"}
    ]

    ingredient_mapping = {}

    for ingredient in ingredient_data:
        i, created = Ingredient.objects.get_or_create(name=ingredient["name"])
        
        if created:
            i.save()
            print(f"{i.name} => INGREDIENT created")
            ingredient_mapping[ingredient["name"]] = i.id
        else:
            print(f"{i.name} => INGREDIENT already exists") 

    # RecipeIngredient
    recipe_ingredient_data = [
        # Pancakes
        {"recipe": "Pancakes", "ingredient": "flour", "quantity": "2 cups"},    
        {"recipe": "Pancakes", "ingredient": "sugar", "quantity": "2 tbsp"},    
        {"recipe": "Pancakes", "ingredient": "salt", "quantity": "1/2 tsp"},   
        {"recipe": "Pancakes", "ingredient": "milk", "quantity": "1 cup"},      
        {"recipe": "Pancakes", "ingredient": "eggs", "quantity": "2"},          
        {"recipe": "Pancakes", "ingredient": "butter", "quantity": "2 tbsp"},     
        {"recipe": "Spaghetti Bolognese", "ingredient": "ground-beef", "quantity": "500g"},     
        {"recipe": "Spaghetti Bolognese", "ingredient": "garlic", "quantity": "1"},        
        {"recipe": "Spaghetti Bolognese", "ingredient": "onion", "quantity": "1"},        
        {"recipe": "Spaghetti Bolognese", "ingredient": "carrot", "quantity": "400g"},     
        {"recipe": "Spaghetti Bolognese", "ingredient": "pasta", "quantity": "200g"},     
        {"recipe": "Spaghetti Bolognese", "ingredient": "olive-oil", "quantity": "2 tbsp"},    
        {"recipe": "Spaghetti Bolognese", "ingredient": "basil", "quantity": "1 tsp"},  
        {"recipe": "Chocolate Lava Cake", "ingredient": "flour", "quantity": "1/2 cup"},   
        {"recipe": "Chocolate Lava Cake", "ingredient": "sugar", "quantity": "1/4 cup"},   
        {"recipe": "Chocolate Lava Cake", "ingredient": "butter", "quantity": "4 tbsp"},    
        {"recipe": "Chocolate Lava Cake", "ingredient": "eggs", "quantity": "2"},         
        {"recipe": "Chocolate Lava Cake", "ingredient": "coconut-milk", "quantity": "100ml"}
    ]

    for recipe_ingredient in recipe_ingredient_data:
        recipe_id = recipe_mapping[recipe_ingredient["recipe"]]
        ingredient_id = ingredient_mapping[recipe_ingredient["ingredient"]]
        r, created = RecipeIngredient.objects.get_or_create(recipe_id=recipe_id, 
                                                            ingredient_id=ingredient_id, 
                                                            defaults={"quantity": recipe_ingredient["quantity"]})
        
        if created:
            print(f"=> RECIPEINGREDIENT created")
        else:
            print(f"=> RECIPEINGREDIENT already exists")

    # Media
    media_data = [
        {"recipe": "Pancakes", "media_type": "IMAGE", "media_url": MEDIA_URL+"populationScript/PopulationScriptPancakes.jpg"},
        {"recipe": "Spaghetti Bolognese", "media_type": "IMAGE", "media_url": MEDIA_URL+"populationScript/PopulationScriptSpaghetti.jpg"},
        {"recipe": "Chocolate Lava Cake", "media_type": "IMAGE", "media_url": MEDIA_URL+"populationScript/PopulationScriptLavaCake.jpg"}
    ]
    
    for media in media_data:
        recipe_id = recipe_mapping[media["recipe"]]
        m, created = Media.objects.get_or_create(recipe_id=recipe_id, media_type=media["media_type"], media_url=media["media_url"])

        if created:
            print(f"{m.media_url} => created")
        else:
            print(f"{m.media_url} => already exists")

    # Favourites
    favourite_data = [
        {"user": "JohnDoe123", "recipe": "Pancakes"},  
        {"user": "JohnDoe123", "recipe": "Spaghetti Bolognese"},  
        {"user": "Marge1967", "recipe": "Chocolate Lava Cake"},  
        {"user": "Marge1967", "recipe": "Pancakes"},  
    ]

    for favourite in favourite_data:
        user_id = user_mapping[favourite["user"]]
        recipe_id = recipe_mapping[favourite["recipe"]]
        f, created = Favourite.objects.get_or_create(user_id=user_id, recipe_id=recipe_id)

        if created:
            print(f"=> FAVOURITE created")
        else:
            print(f"=> FAVOURITE already exists")

    # Comment
    comment_data = [
        {
            "user": "JohnDoe123", "recipe": "Pancakes", "comment": "These pancakes are amazing! So fluffy and delicious.", "date_time": "2024-03-15 08:30:00"
        },
        {
            "user": "Marge1967", "recipe": "Pancakes", "comment": "Great recipe, but I added a bit more sugar for sweetness.", "date_time": "2024-03-15 09:15:00"
        },
        {
            "user": "JohnDoe123", "recipe": "Spaghetti Bolognese", "comment": "This spaghetti Bolognese was a hit with my family!", "date_time": "2024-03-16 12:45:00"
        },
        {
            "user": "JohnDoe123", "recipe": "Chocolate Lava Cake", "comment": "Easy to make, but I would use fresh tomatoes next time.", "date_time": "2024-03-17 14:10:00"
        },
        {
            "user": "Marge1967", "recipe": "Chocolate Lava Cake", "comment": "This lava cake is divine! Perfectly gooey in the center.", "date_time": "2024-03-18 19:30:00"
        }
    ]

    for comment in comment_data:
        user_id = user_mapping[comment["user"]]
        recipe_id = recipe_mapping[comment["recipe"]]
        c, created = Comment.objects.get_or_create(user_id=user_id, 
                                                   recipe_id=recipe_id,
                                                   defaults={"comment": comment["comment"],
                                                             "date": comment["date_time"]})
        if created:
            print(f"=> COMMENT created for user {comment['user']} and recipe {comment['recipe']}")
        else:
            print(f"=> COMMENT already exists for user {comment['user']} and recipe {comment['recipe']}")

    # Tag
    tag_data = [
        {"name": "vegetarian", "user": "JohnDoe123"},
        {"name": "quick & easy", "user": "Marge1967"},
        {"name": "dessert", "user": "JohnDoe123"},
        {"name": "high protein", "user": "Marge1967"},
        {"name": "spicy", "user": "Marge1967"},
        {"name": "gluten-free", "user": "JohnDoe123"},
        {"name": "breakfast", "user": "JohnDoe123"},
        {"name": "italian", "user": "Marge1967"},
        {"name": "low carb", "user": "Marge1967"},
        {"name": "vegan", "user": "JohnDoe123"},
        {"name": "comfort Food", "user": "Marge1967"},
        {"name": "keto", "user": "JohnDoe123"},
        {"name": "dairy-free", "user": "Marge1967"},
        {"name": "healthy", "user": "JohnDoe123"},
        {"name": "one-pot meal", "user": "Marge1967"},
        {"name": "family-friendly", "user": "JohnDoe123"},
        {"name": "asian cuisine", "user": "Marge1967"},
        {"name": "bbq", "user": "JohnDoe123"},
        {"name": "soup", "user": "Marge1967"},
        {"name": "salad", "user": "JohnDoe123"},
        {"name": "holiday special", "user": "Marge1967"},
        {"name": "baking", "user": "JohnDoe123"},
        {"name": "slow cooker", "user": "Marge1967"},
        {"name": "high fiber", "user": "JohnDoe123"},
        {"name": "budget-friendly", "user": "Marge1967"}
    ]

    tag_mapping = {}

    for tag in tag_data:
        user_id = user_mapping[tag["user"]]
        user = User.objects.get(id=user_id)
        
        t, created = Tag.objects.get_or_create(
            name=tag["name"],
            defaults={"user": user}
        )

        if created:
            t.save()
            print(f"{t.name} => TAG created")
            tag_mapping[tag["name"]] = t.id
        else:
            print(f"{t.name} => TAG already exists")


    # RecipeTag
    recipe_tag_data = [
        {"recipe": "Pancakes", "tag": "breakfast"},
        {"recipe": "Pancakes", "tag": "quick & easy"},
        {"recipe": "Pancakes", "tag": "vegetarian"},
        {"recipe": "Pancakes", "tag": "healthy"},  
        {"recipe": "Pancakes", "tag": "holiday special"},  
        {"recipe": "Spaghetti Bolognese", "tag": "italian"},
        {"recipe": "Spaghetti Bolognese", "tag": "high protein"},
        {"recipe": "Spaghetti Bolognese", "tag": "spicy"},
        {"recipe": "Spaghetti Bolognese", "tag": "family-friendly"},
        {"recipe": "Spaghetti Bolognese", "tag": "budget-friendly"},
        {"recipe": "Chocolate Lava Cake", "tag": "dessert"},  
        {"recipe": "Chocolate Lava Cake", "tag": "quick & easy"},
        {"recipe": "Chocolate Lava Cake", "tag": "family-friendly"}, 
        {"recipe": "Chocolate Lava Cake", "tag": "baking"},
    ]

    for recipe_tag in recipe_tag_data:
        recipe_id = recipe_mapping[recipe_tag["recipe"]]
        tag_id = tag_mapping[recipe_tag["tag"]]
        r, created = RecipeTag.objects.get_or_create(recipe_id=recipe_id, tag_id=tag_id)

        if created:
            print(f"=> RECIPETAG created for recipe {r.recipe_id} and tag {r.tag_id}")
        else:
            print (f"=> RECIPETAG already exists for recipe {r.recipe_id} and tag {r.tag_id}")

    # Rating
    rating_data = [
        {"user": "JohnDoe123", "recipe": "Pancakes", "rating": 5},
        {"user": "JohnDoe123", "recipe": "Spaghetti Bolognese", "rating": 4},
        {"user": "JohnDoe123", "recipe": "Chocolate Lava Cake", "rating": 5},
        {"user": "Marge1967", "recipe": "Pancakes", "rating": 4},
        {"user": "Marge1967", "recipe": "Chocolate Lava Cake", "rating": 5},
    ]

    for rating in rating_data:
        user_id = user_mapping[rating["user"]]
        recipe_id = recipe_mapping[rating["recipe"]]
        r, created = Rating.objects.get_or_create(user=User.objects.get(id=user_id), recipe=Recipe.objects.get(recipe_id=recipe_id), rating=rating["rating"])
        
        if created:
            print(f"=> RATING from user {user_mapping[rating['user']]} to recipe {recipe_mapping[rating['recipe']]} created")
        else:
            print(f"=> RATING from user {user_mapping[rating['user']]} to recipe {recipe_mapping[rating['recipe']]} already exists")

    # CommentLike
    comment_likes_data = [
        {"user": "JohnDoe123", "comment": Comment.objects.get(comment_id=1)},
        {"user": "Marge1967", "comment": Comment.objects.get(comment_id=2)},
        {"user": "JohnDoe123", "comment": Comment.objects.get(comment_id=3)}
    ]

    for comment_like in comment_likes_data:
        user_id = user_mapping[comment_like["user"]]
        c, created = CommentLike.objects.get_or_create(user=User.objects.get(id=user_id), comment=comment_like["comment"])

        if created:
            print(f"=> COMMENTLIKE from user {user_id} to {comment_like['comment']} created")
        else:
            print(f"=> COMMENTLIKE from user {user_id} to {comment_like['comment']} already exists")


if __name__ == '__main__':
    print("Starting Scrandemonium Population Script...")
    populate()
    print("==========\nPopulation Complete.\n==========")
