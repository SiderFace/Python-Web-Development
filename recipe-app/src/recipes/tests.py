from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):
   def test_recipe_creation(self):
      recipe = Recipe.objects.create(
         recipe_name='Spaghetti Bolognese',
         ingredients='...',
         cooking_time=30,
         difficulty_rating='Easy',
         description_details='...'
      )
      self.assertEqual(recipe.recipe_name, 'Spaghetti Bolognese')
      self.assertEqual(recipe.ingredients, '...')
      self.assertEqual(recipe.cooking_time, 30)
      self.assertEqual(recipe.difficulty_rating, 'Easy')
      self.assertEqual(Recipe.objects.count(), 1)