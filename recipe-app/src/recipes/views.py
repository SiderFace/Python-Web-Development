from django.shortcuts import render, get_object_or_404
from .models import Recipe

def welcome(request):
   recipes = Recipe.objects.all() 
   return render(request, 'recipes/recipes_home.html', {'recipes': recipes}) 

def recipe_list(request):
   recipes = Recipe.objects.all()
   return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, recipe_id):
   recipe = get_object_or_404(Recipe, pk=recipe_id)
   return render(request, 'recipes/recipe_details.html', {'recipe': recipe})

