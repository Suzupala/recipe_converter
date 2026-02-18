from constants import volume_constants, density_constants


def volume_to_milliliters(unit, amount):
    return getattr(volume_constants, unit) * amount

def milliliters_to_grams(item, amount):
    return getattr(density_constants, item) * amount

def volume_to_grams(item, volume_unit, amount):
    print (f"{item}")
    print(f"{volume_unit}")
    print(f"{amount}")
    return getattr(density_constants, item) * getattr(volume_constants, volume_unit) * amount

