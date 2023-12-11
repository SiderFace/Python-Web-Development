import pickle

def display_recipe(recipe):
   print(f"Recipe Name: {recipe['name']}")
   print(f"Cooking Time: {recipe['cooking_time']} minutes")
   print(f"Number of Ingredients: {len(recipe['ingredients'])}")
   print(f"Difficulty: {recipe['difficulty']}")
   print("Ingredients:")
   for ingredient in recipe['ingredients']:
      print(f"- {ingredient}")
   print("\n")

def search_by_ingredient(recipes, ingredient):
   matching_recipes = []
   for recipe in recipes:
      if ingredient.lower() in [ing.lower() for ing in recipe['ingredients']]:
         matching_recipes.append(recipe)
   return matching_recipes

def search_ingredient(data):
   print("Available Ingredients:")
   for index, ingredient in enumerate(data.get('all_ingredients', [])):
      print(f"{index + 1}. {ingredient}")

   try:
      print("---")
      ingredient_index = int(input("Enter the number of the ingredient to search for: ")) - 1
      ingredient_searched = data['all_ingredients'][ingredient_index].lower()

   except (ValueError, IndexError):
      print("Invalid input. Please enter a valid number.")
      return

   else:
      matching_recipes = search_by_ingredient(data.get('recipes_list', []), ingredient_searched)

      if matching_recipes:
         print(f"Recipes containing '{ingredient_searched}':")
         for matching_recipe in matching_recipes:
            display_recipe(matching_recipe)
      else:
         print(f"No recipes found containing '{ingredient_searched}'.")

if __name__ == "__main__":
   try:
      filename = input("Enter the filename to open: ")

      with open(filename, 'rb') as file:
         data = pickle.load(file)

   except FileNotFoundError:
      print(f"The file '{filename}' was not found. Creating a new data structure.")
      data = {'recipes_list': [], 'all_ingredients': []}

   except Exception as e:
      print(f"An error occurred: {e}")
      data = {'recipes_list': [], 'all_ingredients': []}

   else:
      file.close()

      recipes_list = data.get('recipes_list', [])
      all_ingredients = data.get('all_ingredients', [])

      print("Recipes List:", recipes_list)
      print("All Ingredients:", all_ingredients)

      recipes_list = data.get('recipes_list', [])

      for recipe in recipes_list:
         display_recipe(recipe)

      ingredient_search = input("Enter an ingredient to search for in recipes: ").lower()

      matching_recipes = search_by_ingredient(recipes_list, ingredient_search)

      if matching_recipes:
         print(f"Recipes containing '{ingredient_search}':")
         for matching_recipe in matching_recipes:
            display_recipe(matching_recipe)
      else:
         print(f"No recipes found containing '{ingredient_search}'.")

   finally:
      search_ingredient(data)

