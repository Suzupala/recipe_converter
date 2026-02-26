import unicodedata
from rapidfuzz import process
from fractions import Fraction


class CrudeLineItem:
    def __init__(self, text="", amount=""):
        self.text = text.lower()
        self.amount = amount
        self.amount_decimal = self._fraction_to_decimal()
        self.unit = self._extract_unit()
        self.ingredient = ""
        self.weight = ""


    def __repr__(self):
        if isinstance(self.weight, (int, float)):
            weight_repr = f"{self.weight:>14.1f}"
        else:
            weight_repr = f"{self.weight:>14}"
        
        return f"{weight_repr} grams {self.amount_decimal:.2f} {self.unit:<15} of {self.ingredient:<20} '{self.text}'"

    def _fraction_to_decimal(self):
        if not self.amount:
            return None
        try:
            parts = self.amount.split()
            total = 0

            for part in parts:
                if '/' in part:
                    total += float(Fraction(part))
                elif any(unicodedata.category(c) == 'No' for c in part):
                    total += parse_unicode_fraction(part)
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

    def _to_grams(self):
        load_densities()
        load_volumes()
        if not self.amount_decimal:
            return "No amount"
        elif not self.ingredient:
            return "No Ingredient"
        elif not self.unit:
            return "No unit"
        elif self.ingredient not in DENSITY_CONSTANTS:
            return "Density N/A"
        elif self.unit not in VOLUME_CONSTANTS:
            return "Volume N/A"
        else:
            return self.amount_decimal * DENSITY_CONSTANTS[self.ingredient] * VOLUME_CONSTANTS[self.unit]

UNIT_VARIANTS = {}
with open('constants/unit_variants.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if line and '=' in line:
            unit, variants = line.split('=')
            UNIT_VARIANTS[unit.strip()] = [variant.strip() for variant in variants.split(',')]


INGREDIENTS = {}
ALL_VARIANTS = []
VARIANT_TO_KEY = {}
def load_ingredients():
    INGREDIENTS.clear()
    ALL_VARIANTS.clear()
    VARIANT_TO_KEY.clear()

    with open('constants/ingredients.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                ingredient, variants = line.split('=')
                INGREDIENTS[ingredient.strip()] = [variant.strip() for variant in variants.split(',')]

    for key, variants in INGREDIENTS.items():
        for variant in variants:
            ALL_VARIANTS.append(variant)
            VARIANT_TO_KEY[variant] = key


VOLUME_CONSTANTS = {}
def load_volumes():
    with open('constants/volume_constants.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                unit, conversion = line.split('=')
                VOLUME_CONSTANTS[unit.strip()] = float(conversion.strip())


DENSITY_CONSTANTS = {}
def load_densities():
    with open('constants/density_constants.txt', 'r') as file:
        for line in file:
            line = line.strip()
            if line and '=' in line:
                ingredient, density = line.split('=')
                DENSITY_CONSTANTS[ingredient.strip()] = float(density.strip())


def printing_recipe(items):
    print ("\n\n ---RECIPE IN GRAMS--- \n")
    for i, item in enumerate(items):
        print(f"{i+1:2}. {item}")
    

def parsing_pasted_recipe(unparsed_recipe):
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
        if any(char.isdigit() for char in string) or any(unicodedata.category(char) == 'No' for char in string):
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
        item.weight = item._to_grams()

    line_items = [item for item in line_items if item.amount or item.unit or item.ingredient]

    return line_items

def parse_unicode_fraction(part):
    total = 0
    for char in part:
        total += unicodedata.numeric(char)
    return total

