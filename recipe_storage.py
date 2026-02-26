import os
import json
from rapidfuzz import process 


from recipe_parser import CrudeLineItem

def load_recipe(name):
    with open(f'saved_recipes/{name}.json', 'r') as f:
        recipe_data = json.load(f)
        items = [CrudeLineItem(**item_dict) for item_dict in recipe_data["ingredients"]]
        return items

def save_recipe(items):
    recipe_files = os.listdir('saved_recipes')
    existing = [f.replace('.json','') for f in recipe_files if f.endswith('.json')]

    while True:
        name = input("Enter desired recipe_name:").lower().replace(' ','_')
        if name not in existing:
            break
        print (f'"{name}" already in use. Choose another one.')
    recipe_data = {
            "name":name,
            "ingredients":[item.__dict__ for item in items]
            }
    with open(f'saved_recipes/{name}.json', 'w') as f:
        json.dump(recipe_data, f, indent = 2)

def find_recipe():
    recipe_files = os.listdir('saved_recipes')
    recipe_names = [f.replace('.json','') for f in recipe_files if f.endswith('.json')]

    searching = True
    while searching:
        query = input("Enter keyword/keywords:")
        matches = process.extract(query, recipe_names, limit = 10)
        print("The 10 closest matches:")
        for i, match in enumerate(matches,1):
            print (f"{i}. {match[0]}")
        choice = input("Select recipe number, or 'f' to search again, or 'q' to quit search:")
        if choice == 'f':
            continue
        elif choice == 'q':
            searching = False
            break
        else:
            try:
                selected = matches[int(choice)-1][0]
                return selected
            except (ValueError,IndexError):
                print("Invalid choice. Please enter a valid number")
        
