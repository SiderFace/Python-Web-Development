import mysql.connector

conn = mysql.connector.connect(
   host="localhost", 
   user="cf-python", 
   passwd="password"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")

cursor.execute("""
   CREATE TABLE IF NOT EXISTS Recipes (
      id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(50),
      ingredients VARCHAR(255),
      cooking_time INT,
      difficulty VARCHAR(20)
   )
""")



def main_menu(conn, cursor):
   while True:
      print("\nMain Menu:")
      print("1. Create a new recipe")
      print("2. Search for a recipe by ingredient")
      print("3. Update an existing recipe")
      print("4. Delete a recipe")
      print("5. Exit")

      choice = input("Enter your choice (1-5): ")

      if choice == '1':
         create_recipe(conn, cursor)
      elif choice == '2':
         search_recipe(conn, cursor)
      elif choice == '3':
         update_recipe(conn, cursor)
      elif choice == '4':
         delete_recipe(conn, cursor)
      elif choice == '5':
         print("Exiting the program.")
         break
      else:
         print("Invalid choice. Please enter a number between 1 and 5.")


def create_recipe(conn, cursor):
   print("\nCreating a New Recipe:")

   name = input("Enter the name of the recipe: ")
   
   while True:
      try:
         cooking_time = int(input("Enter the cooking time (in minutes): "))
         break
      except ValueError:
         print("Invalid input. Please enter a valid integer for cooking time.")

   ingredients = []
   while True:
      ingredient = input("Enter one ingredient at a time, or type 'done' when finished: ")
      if ingredient.lower() == 'done':
         break
      else:
         ingredients.append(ingredient)

   ingredients_str = ", ".join(ingredients)

   difficulty = calculate_difficulty(cooking_time, ingredients)

   sql_query = f"""
   INSERT INTO Recipes (
      name, 
      ingredients, 
      cooking_time, 
      difficulty
   ) 
   VALUES (
      '{name}', 
      '{ingredients_str}', 
      {cooking_time}, 
      '{difficulty}'
   )
   """
   
   cursor.execute(sql_query)

   print("Recipe added successfully!")
   conn.commit()

def calculate_difficulty(cooking_time, ingredients):
   if cooking_time < 10 and len(ingredients) < 4:
      difficulty = 'Easy'
   elif cooking_time < 10 and len(ingredients) >= 4:
      difficulty = 'Medium'
   elif cooking_time >= 10 and len(ingredients) < 4:
      difficulty = 'Intermediate'
   else:
      difficulty = 'Hard'
   
   return difficulty


def search_recipe(conn, cursor):   
   cursor.execute("SELECT DISTINCT ingredients FROM Recipes")
   results = cursor.fetchall()

   all_ingredients = set()
    
   for result in results:
      ingredients_tuple = result[0].split(", ")
      all_ingredients.update(ingredients_tuple)

   print("\nAvailable Ingredients:")
   for index, ingredient in enumerate(all_ingredients, start=1):
      print(f"{index}. {ingredient}")

   while True:
      try:
         choice = int(input("\nEnter the number corresponding to the ingredient you want to search for: "))
         if 1 <= choice <= len(all_ingredients):
            search_ingredient = list(all_ingredients)[choice - 1]
            print(f"Searching for recipes with {search_ingredient}...")
            break
         else:
            print("Invalid choice. Please enter a valid number.")
      except ValueError:
         print("Invalid input. Please enter a number.")

   sql_query = "SELECT * FROM Recipes WHERE ingredients LIKE %s"
   cursor.execute(sql_query, (f"%{search_ingredient}%",))
   search_results = cursor.fetchall()

   if search_results:
      print("Search Results:")
      for result in search_results:
         print(f"Recipe Name: {result[1]}")
         print(f"Ingredients: {result[2]}")
         print(f"Cooking Time: {result[3]} minutes")
         print(f"Difficulty: {result[4]}")
         print("\n---")
   else:
      print(f"No recipes found with {search_ingredient}.")


def update_recipe(conn, cursor):
   cursor.execute("SELECT * FROM Recipes")
   recipes = cursor.fetchall()

   print("\nAvailable Recipes:")
   for recipe in recipes:
      print(f"{recipe[0]}. {recipe[1]}")

   while True:
      try:
         recipe_id = int(input("\nEnter the number corresponding to the recipe you want to update: "))
         selected_recipe = next((recipe for recipe in recipes if recipe[0] == recipe_id), None)
         if selected_recipe:
            break
         else:
            print("Invalid recipe id. Please enter a valid number.")
      except ValueError:
         print("Invalid input. Please enter a number.")

   print("\nColumns Available for Modification:")
   print("1. Name")
   print("2. Cooking Time")
   print("3. Ingredients")

   while True:
      column_choice = input("Enter the number corresponding to the column you want to update: ")
      if column_choice in ['1', '2', '3']:
         break
      else:
         print("Invalid choice. Please enter a valid number (1-3).")

   if column_choice == '1':
      column_name = 'name'
   elif column_choice == '2':
      column_name = 'cooking_time'
   else:
      column_name = 'ingredients'

   new_value = input(f"Enter the new value for {column_name}: ")

   sql_query = f"UPDATE Recipes SET {column_name} = %s WHERE id = %s"
   cursor.execute(sql_query, (new_value, recipe_id))

   if column_name in ['cooking_time', 'ingredients']:
      new_cooking_time = selected_recipe[3] if column_name == 'cooking_time' else int(selected_recipe[3])
      new_ingredients = new_value if column_name == 'ingredients' else selected_recipe[2]
      new_difficulty = calculate_difficulty(new_cooking_time, new_ingredients)

      sql_query_difficulty = "UPDATE Recipes SET difficulty = %s WHERE id = %s"
      cursor.execute(sql_query_difficulty, (new_difficulty, recipe_id))

   print(f"Recipe updated successfully! {column_name} set to {new_value}.")


def delete_recipe(conn, cursor):
   print("\nDelete a Recipe:")

   cursor.execute("SELECT * FROM Recipes")
   recipes = cursor.fetchall()

   print("\nAvailable Recipes:")
   for recipe in recipes:
      print(f"{recipe[0]}. {recipe[1]}")

   while True:
      try:
         recipe_id = int(input("\nEnter the number corresponding to the recipe you want to delete: "))
         selected_recipe = next((recipe for recipe in recipes if recipe[0] == recipe_id), None)
         if selected_recipe:
            break
         else:
            print("Invalid recipe id. Please enter a valid number.")
      except ValueError:
         print("Invalid input. Please enter a number.")

   confirm = input(f"Are you sure you want to delete the recipe '{selected_recipe[1]}'? (yes/no): ").lower()

   if confirm == 'yes':
      try:
         sql_query = "DELETE FROM Recipes WHERE id = %s"
         cursor.execute(sql_query, (recipe_id,))

         conn.commit()

         print(f"Recipe '{selected_recipe[1]}' deleted successfully!")

      except mysql.connector.Error as err:
         print(f"Error: {err}")
         conn.rollback()

   else:
      print("Deletion canceled.")



main_menu(conn, cursor)

conn.commit()
conn.close()

