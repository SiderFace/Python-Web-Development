from django.shortcuts import render

def welcome(request):
   return render(request, 'recipes/recipes_home.html')

