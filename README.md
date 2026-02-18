Recipe converter (in progress)

The converter accepts a pasted recipe with any sorts of measurements and converts it into grams.

recipe_parser.py opens a .txt file, breaks it down line by line, and identifies amount, unit, and ingredient.
converter.py converts amount into grams using density_constants.txt and unit_constants.txt
