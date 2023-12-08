from sqlalchemy import create_engine, Column
from sqlalchemy.types import Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.expression import or_

engine = create_engine("mysql://cf-python:password@localhost/task_database")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Recipe(Base):
   __tablename__ = 'final_recipes'

   id = Column(Integer, primary_key=True, autoincrement=True)
   name = Column(String(50))
   ingredients = Column(String(255))
   cooking_time = Column(Integer)
   difficulty = Column(String(20))

   def __repr__(self):
      return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"
   
   def __str__(self):
      return (
         f"Recipe ID: {self.id}\n"
         f"Name: {self.name}\n"
         f"Ingredients: {self.ingredients}\n"
         f"Cooking Time: {self.cooking_time} minutes\n"
         f"Difficulty: {self.difficulty}\n"
      )
   
   def calculate_difficulty(self):
      if self.cooking_time < 10 and len(self.ingredients.split(',')) < 4:
         self.difficulty = 'Easy'
      elif self.cooking_time < 10 and len(self.ingredients.split(',')) >= 4:
         self.difficulty = 'Medium'
      elif self.cooking_time >= 10 and len(self.ingredients.split(',')) < 4:
         self.difficulty = 'Intermediate'
      else:
         self.difficulty = 'Hard'

   def return_ingredients_as_list(self):
      if not self.ingredients:
         return []
      else:
         return self.ingredients.split(', ')
      
Base.metadata.create_all(engine)


def is_valid_name(name):
   return len(name) <= 50 and name.isalpha()

def is_valid_ingredients(ingredients):
    return len(ingredients) <= 250 and all(char.isalnum() or char.isspace() for char in ingredients)

def is_valid_cooking_time(cooking_time):
   return cooking_time.isnumeric()


def create_recipe():
   name = input("Enter the name of the recipe: ")
   while not is_valid_name(name):
      print("Invalid name.  Ensure it doesn't exceed 50 characters and contains only alphabetical characters.")
      name = input("Enter the name of the recipe: ")

   num_ingredients = int(input("How many ingredients would you like to enter? "))
   ingredients = []
   for _ in range(num_ingredients):
      ingredient = input("Enter an ingredient: ")
      while not is_valid_ingredients(ingredient):
         print("Invalid ingredient.  Ensure it doesn't exceed 250 characters and contains only alphanumeric characters and spaces.")
         ingredient = input("Enter an ingredient: ")
      ingredients.append(ingredient)

   cooking_time = input("Enter the cooking time (in minutes): ")
   while not is_valid_cooking_time(cooking_time):
      print("Invalid cooking time.  Ensure it contains only numeric characters.")
      cooking_time = input("Enter the cooking time (in minutes): ")

   cooking_time = int(cooking_time)

   ingredients_str = ', '.join(ingredients)

   recipe_entry = Recipe(
      name=name, 
      ingredients=ingredients_str, 
      cooking_time=cooking_time
   )
   recipe_entry.calculate_difficulty()

   session.add(recipe_entry)
   session.commit()
   print("Recipe created successfully!")


def view_all_recipes():
    recipes = session.query(Recipe).all()

    if not recipes:
        print("There are no entries in the database.")
        return None

    for recipe in recipes:
        print(recipe)


def search_by_ingredients():
   num_entries = session.query(Recipe).count()

   if num_entries == 0:
      print("There are no entries in the database.")
      return None

   results = session.query(Recipe.ingredients).all()

   all_ingredients = []

   for result in results:
      ingredients_list = result[0].split(', ')
      for ingredient in ingredients_list:
         if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)

   print("Ingredients:")
   for i, ingredient in enumerate(all_ingredients, start=1):
      print(f"{i}. {ingredient}")

   user_selection = input("Select ingredients by entering numbers (separated by spaces): ")

   selected_numbers = [int(num) for num in user_selection.split()]

   if any(num <= 0 or num > len(all_ingredients) for num in selected_numbers):
      print("Invalid selection.  Please enter valid numbers.")
      return None

   search_ingredients = [all_ingredients[num - 1] for num in selected_numbers]

   conditions = []
    
   for ingredient in search_ingredients:
      like_term = f"%{ingredient}%"
      conditions.append(Recipe.ingredients.like(like_term))

   recipes = session.query(Recipe).filter(or_(*conditions)).all()

   if not recipes:
      print("No recipes found.")
   else:
      for recipe in recipes:
         print(recipe)


def edit_recipe():
   num_entries = session.query(Recipe).count()

   if num_entries == 0:
      print("There are no entries in the database.")
      return None

   results = session.query(Recipe.id, Recipe.name).all()

   print("Recipes available for editing:")
   for result in results:
      print(f"{result[0]}. {result[1]}")

   selected_id = int(input("Enter the ID of the recipe you want to edit: "))

   if selected_id not in [result[0] for result in results]:
      print("Invalid ID.  No recipe found with the provided ID.")
      return None

   recipe_to_edit = session.query(Recipe).filter(Recipe.id == selected_id).first()

   print(f"\nEditing Recipe ID: {recipe_to_edit.id}")
   print(f"1. Name: {recipe_to_edit.name}")
   print(f"2. Ingredients: {recipe_to_edit.ingredients}")
   print(f"3. Cooking Time: {recipe_to_edit.cooking_time} minutes")

   selected_attribute = int(input("Enter the number of the attribute you want to edit: "))

   if selected_attribute not in [1, 2, 3]:
      print("Invalid selection.  Please enter a valid number.")
      return None

   if selected_attribute == 1:
      new_name = input("Enter the new name: ")
      recipe_to_edit.name = new_name
   elif selected_attribute == 2:
      new_ingredients = input("Enter the new ingredients: ")
      recipe_to_edit.ingredients = new_ingredients
   elif selected_attribute == 3:
      new_cooking_time = input("Enter the new cooking time (in minutes): ")
      while not is_valid_cooking_time(new_cooking_time):
         print("Invalid cooking time.  Ensure it contains only numeric characters.")
         new_cooking_time = input("Enter the new cooking time (in minutes): ")
      recipe_to_edit.cooking_time = int(new_cooking_time)

   recipe_to_edit.calculate_difficulty()

   session.commit()

   print("Recipe edited successfully!")


def delete_recipe():
   num_entries = session.query(Recipe).count()

   if num_entries == 0:
      print("There are no entries in the database.")
      return None

   results = session.query(Recipe.id, Recipe.name).all()

   print("Recipes available for deletion:")
   for result in results:
      print(f"{result[0]}. {result[1]}")

   selected_id = int(input("Enter the ID of the recipe you want to delete: "))

   if selected_id not in [result[0] for result in results]:
      print("Invalid ID. No recipe found with the provided ID.")
      return None

   recipe_to_delete = session.query(Recipe).filter(Recipe.id == selected_id).first()

   confirm_delete = input(f"Are you sure you want to delete {recipe_to_delete.name}? (yes/no): ").lower()

   if confirm_delete == 'yes':
      session.delete(recipe_to_delete)
      session.commit()
      print("Recipe deleted successfully!")
   else:
      print("Deletion canceled.")


def main_menu():
   while True:
      print("\nMain Menu:")
      print("1. Create a new recipe")
      print("2. View all recipes")
      print("3. Search for recipes by ingredients")
      print("4. Edit a recipe")
      print("5. Delete a recipe")
      print("6. Quit")

      choice = input("Enter your choice (1-6): ")

      if choice == '1':
         create_recipe()
      elif choice == '2':
         view_all_recipes()
      elif choice == '3':
         search_by_ingredients()
      elif choice == '4':
         edit_recipe()
      elif choice == '5':
         delete_recipe()
      elif choice == '6':
         print("Quitting the application. Goodbye!")
         session.close()
         engine.dispose()
         break
      else:
         print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
   main_menu()


