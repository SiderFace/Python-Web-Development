recipes_list = []
ingredients_list = []


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
   }

   return recipe


while True:
   try:
      n = int(input("How many recipes would you like to enter? "))
      if n > 0:
         break
      else:
         print("Please enter a positive integer.")
   except ValueError:
      print("Invalid input. Please only enter a valid positive integer. ")


for i in range(n):
   recipe_data = take_recipe()

   for ingredient in recipe_data['ingredients']:
      if ingredient not in ingredients_list:
         ingredients_list.append(ingredient)

   recipes_list.append(recipe_data)
   
   print("Your", recipe_data['name'], "recipe has been added.  Cooking time:", recipe_data['cooking_time'], "minutes.  Ingredients:", recipe_data['ingredients'])
   print("---")


for recipe in recipes_list:
   cooking_time = recipe['cooking_time']
   num_ingredients = len(recipe['ingredients'])

   if cooking_time < 10 and num_ingredients < 4:
      recipe['difficulty'] = 'Easy'

   elif cooking_time < 10 and num_ingredients >= 4:
      recipe['difficulty'] = 'Medium'

   elif cooking_time >= 10 and num_ingredients < 4:
      recipe['difficulty'] = 'Intermediate'

   else:
      recipe['difficulty'] = 'Hard'


for recipe in recipes_list:
   print("Recipe: ", recipe["name"])
   print("Cooking time (min): ", recipe["cooking_time"])
   print("Ingredients:")
   for ingredient in recipe["ingredients"]:
      print(ingredient)
   print("Difficulty: ", recipe["difficulty"])
   print()

sorted_ingredients = sorted(ingredients_list)
print("Ingredients Available Across All Recipes (Alphabetical) : ")
print("_______________________________________________________")
for ingredient in sorted_ingredients:
   print(ingredient)
print("_______________________________________________________")