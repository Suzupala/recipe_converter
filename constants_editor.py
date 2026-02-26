from recipe_parser import CrudeLineItem, printing_recipe, load_ingredients


def add_ingredient_to_ingredients(ingredients_list,items,index):
    
    print (f"\n\nediting ingredient list to correctly identify {items[index].text}:\n")
    
    standardized_ingredient = input("input standardized unit in the form of 'NEW_INGREDIENT':").upper().strip("'").strip()
    common_spellings = input("common spellings found in recipes in the form of 'spellingone, spellintwo'").lower().strip("'").strip()
    with open(ingredients_list, 'a') as file:
        file.write(f"\n{standardized_ingredient}={common_spellings}")
    
    load_ingredients()
    items[index].ingredient = items[index]._extract_ingredient()
    print(f"added '{standardized_ingredient}={common_spellings}' to ingredients.txt")
    print("Updated redipe:")
    printing_recipe(items)
    

def add_variant_to_ingredient(ingredients_list,items,index):

    with open(ingredients_list, 'r') as file:
        lines = file.readlines()

    with open(ingredients_list, 'w') as file:
        found = False
        for line in lines:
            if line.startswith(items[index].ingredient + "="):
                new_variant = input(f"add spelling variant to {items[index].ingredient}:").strip()
                line = line.strip() + f", {new_variant}\n"
                print(f"added {new_variant} to {items[index].ingredient}")
                found = True
            file.write(line)
        if not found:
            print(f"{items[index].ingredient} not found")



def add_density_to_density_constants(density_constants,items,index):
    if items[index].ingredient:
        print(f"{items[index].ingredient} density missing from data")
        while True:
            try:
                density = input ("enter density (kg/liter) as a decimal, or q to quit:")
                if density == "q":
                    break
                density = float(density)
                with open(density_constants, 'a') as file:
                    file.write(f"\n{items[index].ingredient}={density}")
                break
            except ValueError:
                print("not a valid number entry, try again")
    else:
        print("items[index].ingredient not found")



