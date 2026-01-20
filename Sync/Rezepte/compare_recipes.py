#!/usr/bin/env python3
"""
Compare recipes in Rezepte 1 with main Cocktails directory.
Find missing recipes and list them.
"""

import os
from pathlib import Path

def get_recipe_names(directory):
    """Get all .md recipe names from a directory."""
    recipes = set()
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                # Use just the filename without extension for comparison
                recipes.add(file)
    return recipes

def main():
    rezepte_1_dir = Path('Cocktails/Rezepte 1')
    cocktails_dir = Path('Cocktails')

    # Get all recipes from both locations
    rezepte_1_recipes = get_recipe_names(rezepte_1_dir)
    existing_recipes = set()

    # Get existing recipes (excluding Rezepte 1 subdirectory)
    for file in cocktails_dir.glob('*.md'):
        existing_recipes.add(file.name)

    # Find missing recipes
    missing_recipes = rezepte_1_recipes - existing_recipes

    print(f"Total recipes in Rezepte 1: {len(rezepte_1_recipes)}")
    print(f"Total recipes in main Cocktails: {len(existing_recipes)}")
    print(f"Missing recipes: {len(missing_recipes)}")
    print("\nMissing recipe files:")
    print("=" * 80)

    # Find the full paths of missing recipes
    missing_paths = []
    for root, dirs, files in os.walk(rezepte_1_dir):
        for file in files:
            if file in missing_recipes:
                full_path = os.path.join(root, file)
                missing_paths.append(full_path)
                print(f"{file:<50} -> {full_path}")

    # Write to file
    with open('missing_recipes_list.txt', 'w', encoding='utf-8') as f:
        f.write(f"Missing recipes: {len(missing_recipes)}\n")
        f.write("=" * 80 + "\n\n")
        for path in sorted(missing_paths):
            f.write(f"{path}\n")

    print(f"\n✓ Report saved to missing_recipes_list.txt")

    # Also list duplicates (recipes that exist in both)
    duplicates = rezepte_1_recipes & existing_recipes
    print(f"\n✓ Duplicate recipes (exist in both): {len(duplicates)}")

if __name__ == '__main__':
    main()
