from rapidfuzz import process
from fractions import Fraction

class CrudeLineItem:
    def __init__(self, text="", amount=""):
        self.text = text.lower()
        self.amount = amount
        self.amount_decimal = self._fraction_to_decimal()
        self.unit = self._extract_unit()
        self.ingredient = ""

    def __repr__(self):
        return f"{self.amount_decimal:.2f} {self.unit:<15} of {self.ingredient:<20} '{self.text}'"

    def _fraction_to_decimal(self):
        if not self.amount:
            return None
        try:
            parts = self.amount.split()
            total = 0

            for part in parts:
                if '/' in part:
                    total += float(Fraction(part))
                else:
                    total += float(part)
            return total
        except:
            return None


    def _extract_unit(self):
        words = self.text.split()
        for i, word in enumerate(words):
            clean_word = word.strip(',.;()')
            for standard_unit, variants in UNIT_VARIANTS.items():
                if clean_word in variants:
                    words.pop(i)
                    self.text = " ".join(words)
                    return standard_unit
        return ""


    def _extract_ingredient(self):
        fuzzy_ingredient = self.text
        fuzzy_ingredient = fuzzy_ingredient.strip(' ,;:.')
        if not fuzzy_ingredient:
            return ""
        best_match = process.extractOne(fuzzy_ingredient, ALL_VARIANTS)
        if best_match and best_match[1] > 70:
            return VARIANT_TO_KEY[best_match[0]]
        return "" 


UNIT_VARIANTS = {}
with open('constants/unit_variants.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line and '=' in line:
            unit, variants = line.split('=')
            UNIT_VARIANTS[unit.strip()] = [variant.strip() for variant in variants.split(',')]

INGREDIENTS = {}
with open('constants/ingredients.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line and '=' in line:
            ingredient, variants = line.split('=')
            INGREDIENTS[ingredient.strip()] = [variant.strip() for variant in variants.split(',')]


ALL_VARIANTS = []
VARIANT_TO_KEY = {}
for key, variants in INGREDIENTS.items():
    for variant in variants:
        ALL_VARIANTS.append(variant)
        VARIANT_TO_KEY[variant] = key


def printing_recipe(text_block):
    items = parsing_pasted_recipes(text_block)
    print ("\n\n ---RECIPE IN GRAMS--- \n")
    for i, item in enumerate(items):
        print(f"{i+1}. {item}")
    return items

def parsing_pasted_recipes(unparsed_recipe):

    lines = unparsed_recipe.splitlines()

    all_items = []

    for line in lines:
        item_list = parsing_line(line)
        all_items.extend(item_list)

    return all_items


def parsing_line(line):
    split_by_space = line.split(" ")
    line_items = []
    words = []
    numbers = []
    for string in split_by_space:
        if any(char.isdigit() for char in string):
            if words and numbers:
                line_items.append(CrudeLineItem(text=" ".join(words),amount=" ".join(numbers)))
                words = []
                numbers = []
                numbers.append(string)

            else:
                numbers.append(string)
        else:
            if string.strip():
                words.append(string.strip(' '))
    line_items.append(CrudeLineItem(text=" ".join(words),amount=" ".join(numbers)))

    texts_joined = ""
    for item in line_items:
        texts_joined += " " + item.text
    for item in line_items:
        item.text = texts_joined.strip()
        item.ingredient = item._extract_ingredient()

    line_items = [item for item in line_items if item.amount or item.unit or item.ingredient]

    return line_items


