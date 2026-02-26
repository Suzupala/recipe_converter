import sys


from recipe_parser import CrudeLineItem, printing_recipe, parsing_pasted_recipe, load_ingredients
from constants_editor import add_ingredient_to_ingredients, add_density_to_density_constants
from recipe_storage import load_recipe, save_recipe, find_recipe

def read_pasted_recipe():
    print("Paste the recipe and press Ctrl+D (or Ctrl+Z on Windows) when done:")
    text_block = sys.stdin.read()
    items = parsing_pasted_recipe(text_block)
    printing_recipe(items)
    return items

def edit_line_item(items):
    happy= False
    print("Which line item would you like to see differently represented?")
    while not happy:
        line_item = input("Input line number, 0 if no corrections:")
        try:
            choice = int(line_item)
            if choice > len(items) or choice < 0:
                print("Requested line out of bounds")
            elif choice != 0:
                request = input("input d for density-edit or i for ingredient-edit:")
                if request == "i":
                    add_ingredient_to_ingredients("constants/ingredients.txt",items,choice-1)
                elif request == "d":
                    add_density_to_density_constants("constants/density_constants.txt",items,choice-1)
                else:
                    print("invalid input for edit request")
            else:
                happy = True
        

        except ValueError:
            print("Not a valid line number!")


def main():
    running = True
    items = []
    load_ingredients()
    while running:
        
        command = input("Commands: 'f'find saved recipe, 'n'input new recipe, 's'save current recipe, 'e'edit current recipe, 'q'quit: ")

        if command == 'q':
            running = False
            break
        elif command == 'f':
            items = find_recipe()
            printing_recipe(items)
        elif command == 'n':
            items = read_pasted_recipe()
        elif command == 's':
            if items:
                save_recipe(items)
            else:
                print("No current recipe")
        elif command == 'e':
            if items:
                edit_line_item(items)
            else:
                print("No current recipe")
        else:
            print("invalid command")
main()
