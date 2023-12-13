from django.db import models

class Recipe(models.Model):
   recipe_name = models.CharField(max_length=255)
   ingredients = models.TextField()
   cooking_time = models.IntegerField()
   difficulty_rating = models.CharField(max_length=50)
   description_details = models.TextField()

   def __str__(self):
      return self.recipe_name
   
