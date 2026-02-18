import sys
from converter import volume_to_grams
from recipe_parser import CrudeLineItem, parsing_pasted_recipes


def main():

    items = parsing_pasted_recipes("test_input.txt")

    for item in items:
        print(item)


main()
