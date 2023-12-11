import pickle

def take_recipe():
   name = input("Enter the recipe name: ")

   while True:
      try:
         cooking_time = int(input("Enter the cooking time (in minutes): "))
         break
      except ValueError:
         print("Invalid input. Please enter only valid integers for the cooking time in minutes.")

   ingredients = []
   while True:
      ingredient = input("Enter one ingredient at a time, or type \"done\" when you are finished adding ingredients: ")
      if ingredient == 'done':
         break
      else:
         ingredients.append(ingredient)

   recipe = {
      'name': name,
      'cooking_time': cooking_time,
      'ingredients': ingredients,
      'difficulty': calc_difficulty(cooking_time, len(ingredients))
   }

   print("---")
   print(f"Your {recipe['name']} recipe has been added.")
   print(f"Cooking time: {recipe['cooking_time']} minutes.")
   print(f"Ingredients: {recipe['ingredients']}")
   print("---")
   
   return recipe

# Function to define recipe difficulty
def calc_difficulty(cooking_time, num_ingredients):

   if cooking_time < 10 and num_ingredients < 4:
      difficulty = 'Easy'
   elif cooking_time < 10 and num_ingredients >= 4:
      difficulty = 'Medium'
   elif cooking_time >= 10 and num_ingredients < 4:
      difficulty = 'Intermediate'
   else:
      difficulty = 'Hard'
    
   return difficulty
   
# Main code 
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

   finally:
      recipes_list = data.get('recipes_list', [])
      all_ingredients = data.get('all_ingredients', [])

      print("Recipes List:", recipes_list)
      print("All Ingredients:", all_ingredients)

   while True:
    try:
        num_recipes = int(input("How many recipes would you like to enter? "))
        break
    except ValueError:
        print("Invalid input. Please enter only valid integers for the number of recipes you are adding.")

   for _ in range(num_recipes):
      recipe = take_recipe()
      recipes_list.append(recipe)

      for ingredient in recipe['ingredients']:
         if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

   data['recipes_list'] = recipes_list
   data['all_ingredients'] = all_ingredients

   print("Updated Recipes List:", data['recipes_list'])
   print("Updated All Ingredients:", data['all_ingredients'])

   with open(filename, 'wb') as file:
      pickle.dump(data, file)

   print(f"Data written to '{filename}'.")

