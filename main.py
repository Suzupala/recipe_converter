import sys

from converter import volume_to_grams
from recipe_parser import CrudeLineItem, printing_recipe
from constants_editor import add_ingredient_to_ingredients, add_density_to_density_constants


#def display_recipe(items):
    #table = Table(show_header=False, show_lines= False, box=None)
    #table.add_column



def main():

    print("Paste the recipe and press Ctrl+D (or Ctrl+Z on Windows) when done:")

    text_block = sys.stdin.read()
    items = printing_recipe(text_block)


    happy = False

    
    print("Which line item would you like to see differently represented?")
    while not happy:
        line_item = input("Input line number, 0 if no corrections")
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


main()
