from django.shortcuts import render, get_object_or_404, redirect
from .models import Recipe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def welcome(request):
   recipes = Recipe.objects.all() 
   return render(request, 'recipes/recipes_home.html', {'recipes': recipes}) 

@login_required
def recipe_list(request):
   recipes = Recipe.objects.all()
   return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, recipe_id):
   recipe = get_object_or_404(Recipe, pk=recipe_id)
   return render(request, 'recipes/recipe_details.html', {'recipe': recipe})

def user_login(request):
   if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user:
         login(request, user)
         return redirect('recipes:recipe_list') 
      else:
         messages.error(request, "Invalid username or password. Please try again.")
   return render(request, 'recipes/user_login.html')

def user_logout(request):
   logout(request)
   messages.success(request, "You've successfully logged out.")
   return render(
      request, 
      'recipes/success.html', 
      {'message': "You've successfully logged out."})
