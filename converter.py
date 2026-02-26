
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



def volume_to_milliliters(unit, amount):
    if unit in VOLUME_CONSTANTS:
        return VOLUME_CONSTANTS[unit] * amount
    else:
        return "n/a"

def milliliters_to_grams(ingredient):
    if ingredient in DENSITY_CONSTANTS:
        return DENSITY_CONSTANTS[ingredient]
    

