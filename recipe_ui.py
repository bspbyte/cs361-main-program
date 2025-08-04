import json
import os
import time


def recipe_loop():
    while True:
        print("Welcome to the Recipe Manager!")
        time.sleep(1)
        print("Recipe Manager helps you store, view and manage your favorite recipes. You can also remove recipes "
              "that you no longer wish to keep.")
        print("Press the 'Enter' key to begin using Recipe Manager.")
        user_input = input("Press 'Enter' now").strip()

        if user_input == "":
            print("Starting Recipe Manager...")
            break
        else:
            print("Please press the 'Enter' key to start.")


class Recipe:
    def __init__(self, name, ingredients, instructions):
        self.name = name
        self.ingredients = ingredients
        self.instructions = instructions

    def to_dict(self):
        return {
            "name": self.name,
            "ingredients": self.ingredients,
            "instructions": self.instructions
        }

    @staticmethod
    def from_dict(data):
        return Recipe(data["name"], data["ingredients"], data["instructions"])


class RecipeManager:
    def __init__(self, storage_file="recipes.json"):
        self.storage_file = storage_file
        self.recipes = self.load_recipes()

    def main_menu(self):
        while True:
            print("-------- Recipe Manager Main Menu --------")
            print("1. Add a Recipe")
            print("2. View Recipes")
            print("3. Delete a Recipe")
            print("4. Exit")
            choice = input("Please enter your number (1-4): ").strip()

            if choice == "1":
                self.add_recipe()
            elif choice == "2":
                self.view_recipes()
            elif choice == "3":
                self.delete_recipe()
            elif choice == "4":
                print("Goodbye!\n")
                break
            else:
                print("Invalid choice. Please enter 1-4.\n")

    def load_recipes(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, 'r') as file:
                try:
                    data = json.load(file)
                    recipes = []
                    for item in data:
                        recipe = Recipe.from_dict(item)
                        recipes.append(recipe)
                    return recipes
                except json.JSONDecodeError:
                    return []
        return []

    def save_recipes(self):
        with open(self.storage_file, 'w') as file:
            json.dump([r.to_dict() for r in self.recipes], file, indent=2)

    def add_recipe(self):

        print("----- Add a Recipe -----")

        while True:

            add_input = input("Please type 'add' and press 'Enter' to add a recipe or 'menu' to return to the main menu").strip()
            if add_input == 'add':
                name = input("Enter recipe name: ").strip()
                ingredients = input("Enter ingredients separated by commas: ").strip().split(",")
                instructions = []
                print("Enter instruction steps, one per line, Enter a blank line to finish.")
                while True:
                    step = input(f"Step {len(instructions) + 1}: ").strip()
                    if not step:
                        break
                    instructions.append(step)

                recipe = Recipe(name, ingredients, instructions)

                print("Save this recipe to your computer? (Y/N) 'Y' will save the recipe, 'N' will restart from beginning")
                while True:
                    save = input("Please type 'Y' or 'N' and press 'Enter'").strip()
                    if save == 'Y':
                        self.recipes.append(recipe)
                        self.save_recipes()
                        print(f"Recipe '{name}' added successfully!\n")
                        break
                    elif save == 'N':
                        break  # Restart process by entering new recipe
                    else:
                        print("Invalid choice. Please type 'Y' or 'N'.\n")
            elif add_input == 'menu':
                manager.main_menu()
            else:
                print("Invalid input, please type 'add' or 'menu'.")

    def view_recipes(self):
        print("----- Your Saved Recipes -----")
        if not self.recipes:
            print("No recipes found.\n")
            return
        time.sleep(1)
        for num, recipe in enumerate(self.recipes, start=1):
            print(f"{num}. {recipe.name}")
        print()
        
        while True:
            view_input = input("Please enter the number of the recipe you would like to view, type 'search' to search "
                               "by recipe name, or 'menu' to go back to the main menu.").strip()
            if view_input.lower() == "search":
                name_query = input("Enter the recipe name to search for: ").strip().lower()
                for recipe in self.recipes:
                    if recipe.name.lower() == name_query:
                        print("\n--- Recipe Details ---")
                        print(f"Name: {recipe.name}")
                        print("Ingredients:")
                        for ingredient in recipe.ingredients:
                            print(f"- {ingredient}")
                        print("Instructions:")
                        for i, step in enumerate(recipe.instructions, start=1):
                            print(f"Step {i}: {step}")
            elif view_input == "menu":
                manager.main_menu()
            elif view_input.isdigit():
                index = int(view_input) - 1
                if 0 <= index < len(self.recipes):
                    recipe = self.recipes[index]
                    print("\n--- Recipe Details ---")
                    print(f"Name: {recipe.name}")
                    print("Ingredients:")
                    for ingredient in recipe.ingredients:
                        print(f"- {ingredient}")
                    print("Instructions:")
                    for i, step in enumerate(recipe.instructions, start=1):
                        print(f"Step {i}: {step}")
                else:
                    print(f"Please choose a number between 1 and {len(self.recipes)}")
            else:
                print("Invalid option. Please type 'search' or the number of the recipe you would like to view.")

    def list_recipes(self):
        """ Helper function for delete_recipe(self) to show user list of recipes before they are given the option to
        delete one"""
        if not self.recipes:
            print("There are no recipes to display")
            return
        for num, recipe in enumerate(self.recipes, start=1):
            print(f"{num}. {recipe.name}")

    def delete_recipe(self):
        print("----- Delete a Recipe -----")

        if not self.recipes:
            print("There are no recipes to delete.")
            return

        self.list_recipes()

        while True:
            delete_input = (input("Please enter the number of the recipe to delete that recipe or 'menu' to return to the main menu.")).strip()
            if delete_input.lower() == 'menu':
                print("Returning to main menu.")
                manager.main_menu()

            if delete_input.isdigit():
                index = int(delete_input)
                if 1 <= index <= len(self.recipes):
                    confirm = input("Are you sure you would like to delete this recipe? (Y/N). WARNING: please note this "
                                "action cannot be undone. Typing 'Y' will delete the recipe. 'N' will return to the "
                                "main menu.")
                    if confirm == 'Y':
                        removed = self.recipes.pop(index - 1)
                        self.save_recipes()
                        print(f"You deleted '{removed.name}' successfully.\n")
                    elif confirm == 'N':
                        manager.main_menu()
                    else:
                        print("Invalid response. Please type 'Y' or 'N'.\n")
                else:
                    print(f"Please enter a valid number between 1 and {len(self.recipes)} .\n")
            else:
                print("Please enter a number or 'menu'.")


if __name__ == "__main__":
    recipe_loop()                   # Show Welcome screen first
    manager = RecipeManager()       # Initialize RecipeManager
    manager.main_menu()             # Show main menu after user starts
