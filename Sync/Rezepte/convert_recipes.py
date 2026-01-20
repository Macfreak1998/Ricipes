#!/usr/bin/env python3
"""
Convert cocktail recipes from Rezepte 1 format to standard vault format.
"""

import os
import re
from pathlib import Path

# Ingredient translations
INGREDIENT_TRANSLATIONS = {
    'Sekt': 'Prosecco',
    'Wodka': 'Vodka',
    'Sahne': 'Heavy Cream',
    'Schlagsahne': 'Heavy Cream',
    'Zitronensaft': 'Lemon Juice',
    'Limettensaft': 'Lime Juice',
    'Orangensaft': 'Orange Juice',
    'Ananassaft': 'Pineapple Juice',
    'Cranberrysaft': 'Cranberry Juice',
    'Grapefrui​tsaft': 'Grapefruit Juice',
    'Zuckersirup': 'Simple Syrup',
    'Soda': 'Soda Water',
    'Tonic Water': 'Tonic Water',
    'Ginger Ale': 'Ginger Ale',
    'Ginger Beer': 'Ginger Beer',
}

# Technique translations
TECHNIQUE_TRANSLATIONS = {
    'im Glas': 'Build',
    'geshaked': 'Shake',
    'shaken': 'Shake',
    'double strained': 'Double Strain',
    'reverse dry shaked': 'Reverse Dry Shake',
    'geshakt': 'Shake',
}

def clean_ingredient_link(ingredient):
    """Clean up wiki-links in ingredients."""
    # Fix broken links like [[Lemondrive/Zutaten/Säfte/Zitronensaft|...]]
    if '|' in ingredient:
        # Extract the display text after |
        match = re.search(r'\[\[.*?\|(.*?)\]\]', ingredient)
        if match:
            display_text = match.group(1).strip()
            # Translate if needed
            for de, en in INGREDIENT_TRANSLATIONS.items():
                if de.lower() in display_text.lower():
                    return f'[[{en}]]'
            return f'[[{display_text}]]'

    # Handle normal wiki-links
    if '[[' in ingredient and ']]' in ingredient:
        match = re.search(r'\[\[(.*?)\]\]', ingredient)
        if match:
            ing_name = match.group(1)
            # Translate if in our dictionary
            if ing_name in INGREDIENT_TRANSLATIONS:
                return f'[[{INGREDIENT_TRANSLATIONS[ing_name]}]]'
            return f'[[{ing_name}]]'

    # No wiki-link, check if it needs translation
    for de, en in INGREDIENT_TRANSLATIONS.items():
        if ingredient.strip().lower() == de.lower():
            return f'[[{en}]]'

    return ingredient

def add_wiki_link_if_needed(ingredient):
    """Add wiki-link to ingredient if it doesn't have one."""
    ingredient = ingredient.strip()

    # Already has wiki-link
    if '[[' in ingredient and ']]' in ingredient:
        return ingredient

    # List of common ingredients that should be wiki-linked
    common_ingredients = [
        'Vodka', 'Gin', 'Rum', 'Whiskey', 'Tequila', 'Bourbon', 'Cognac', 'Brandy',
        'Aperol', 'Campari', 'Cointreau', 'Triple Sec', 'Prosecco',
        'Lemon Juice', 'Lime Juice', 'Orange Juice', 'Pineapple Juice', 'Cranberry Juice',
        'Simple Syrup', 'Grenadine', 'Soda Water', 'Tonic Water', 'Ginger Beer', 'Ginger Ale',
        'Espresso', 'Coffee Liqueur', 'Amaretto', 'Kahlua', 'Baileys',
        'Angostura Bitters', 'Orange Bitters', 'Peychaud\'s Bitters',
        'Egg White', 'Heavy Cream', 'Coconut Cream', 'Cream of Coconut',
        'Vermouth', 'Sweet Vermouth', 'Dry Vermouth',
    ]

    # Check if ingredient matches any common ingredient (case-insensitive)
    for common in common_ingredients:
        if ingredient.lower() == common.lower():
            return f'[[{common}]]'

    # Check for partial matches (e.g., "Likör 43" should become "[[Likör 43]]")
    # If it's a capitalized word or phrase, wiki-link it
    if ingredient and ingredient[0].isupper() and len(ingredient) > 2:
        return f'[[{ingredient}]]'

    return ingredient

def parse_quantity(ingredient_line):
    """Extract quantity and ingredient from a line."""
    ingredient_line = ingredient_line.strip().lstrip('-*').strip()

    # Match patterns like "5 cl", "1,5 oz", "3/4 oz", etc.
    # Remove "cl" and "oz" but keep the number
    quantity_match = re.match(r'([\d,/.]+)\s*(cl|oz|ml)?\s+(.*)', ingredient_line)
    if quantity_match:
        quantity = quantity_match.group(1).replace(',', '.')  # Convert comma to dot
        ingredient = quantity_match.group(3)
        ingredient = clean_ingredient_link(ingredient)
        ingredient = add_wiki_link_if_needed(ingredient)
        return f'{quantity} {ingredient}'

    # No quantity found, just clean the ingredient
    cleaned = clean_ingredient_link(ingredient_line)
    return add_wiki_link_if_needed(cleaned)

def extract_techniques(zubereitung_line):
    """Extract techniques from Zubereitung line."""
    techniques = []
    # Split by comma
    parts = zubereitung_line.split(',')
    for part in parts:
        part = part.strip()
        # Extract wiki-links
        match = re.search(r'\[\[(.*?)\]\]', part)
        if match:
            technique = match.group(1)
            # Translate if needed
            if technique in TECHNIQUE_TRANSLATIONS:
                techniques.append(TECHNIQUE_TRANSLATIONS[technique])
            elif technique.lower() != 'free pour':  # Skip "free pour"
                techniques.append(technique)
        else:
            # Check for non-linked techniques
            for de, en in TECHNIQUE_TRANSLATIONS.items():
                if de in part:
                    techniques.append(en)
                    break

    return techniques

def convert_recipe(content, filename):
    """Convert a recipe from old format to new format."""
    lines = content.split('\n')

    # Parse the old format
    glas = ''
    zubereitung_techniques = []
    preis = ''
    zutaten = []
    zubereitungshinweise = []
    eis = '[[Eiswürfel]]'  # Default
    deko = ''

    current_section = None

    for line in lines:
        line = line.strip()

        if line.startswith('#### Glas:'):
            glas = line.replace('#### Glas:', '').strip()
            current_section = None
        elif line.startswith('#### Zubereitung:'):
            zubereitung_line = line.replace('#### Zubereitung:', '').strip()
            zubereitung_techniques = extract_techniques(zubereitung_line)
            current_section = None
        elif line.startswith('#### Preis:'):
            preis = line.replace('#### Preis:', '').strip()
            current_section = None
        elif line.startswith('#### Zutaten:'):
            current_section = 'zutaten'
        elif line.startswith('#### Zubereitungshinweise:'):
            current_section = 'zubereitungshinweise'
        elif current_section == 'zutaten' and line and not line.startswith('####'):
            if line.startswith('-') or line.startswith('*'):
                zutaten.append(line)
        elif current_section == 'zubereitungshinweise' and line and not line.startswith('####'):
            if line.startswith('-') or line.startswith('*'):
                zubereitungshinweise.append(line.lstrip('-*').strip())
            elif line:
                zubereitungshinweise.append(line)

    # If no technique was specified in Zubereitung line, infer from hints
    if not zubereitung_techniques:
        for hint in zubereitungshinweise:
            hint_lower = hint.lower()
            if 'shake' in hint_lower or 'schütteln' in hint_lower:
                if 'dry shake' in hint_lower:
                    zubereitung_techniques.append('Dry Shake')
                elif 'reverse' in hint_lower:
                    zubereitung_techniques.append('Reverse Dry Shake')
                else:
                    zubereitung_techniques.append('Shake')
                break
            elif 'stir' in hint_lower or 'rühren' in hint_lower:
                zubereitung_techniques.append('Stir')
                break
            elif 'blend' in hint_lower:
                zubereitung_techniques.append('Blend')
                break
            elif 'build' in hint_lower or 'im glas' in hint_lower:
                zubereitung_techniques.append('Build')
                break

    # Process ingredients
    processed_ingredients = []
    ingredient_names = []  # For technique line

    for ing in zutaten:
        if 'Verhältnis' in ing or '*Verhältnis' in ing:
            continue  # Skip ratio notes

        parsed = parse_quantity(ing)
        if parsed:
            processed_ingredients.append(f'- {parsed}')
            # Extract ingredient name for technique line
            match = re.search(r'\[\[(.*?)\]\]', parsed)
            if match:
                ingredient_names.append(match.group(1))

    # Extract decoration/garnish from Zubereitungshinweise
    garnish_keywords = ['garnieren', 'garnish', 'Deko', 'decoration']
    for hint in zubereitungshinweise[:]:
        for keyword in garnish_keywords:
            if keyword.lower() in hint.lower():
                # Try to extract garnish
                if 'Zitronenzeste' in hint or 'lemon zest' in hint.lower():
                    deko = '[[Zitronenzeste]]'
                elif 'Limettenzeste' in hint or 'lime zest' in hint.lower():
                    deko = '[[Limettenzeste]]'
                elif 'Orange' in hint:
                    deko = '[[Orangenscheibe]]'
                elif 'Kirsche' in hint or 'cherry' in hint.lower():
                    deko = '[[Cocktailkirsche]]'
                elif 'Minz' in hint or 'mint' in hint.lower():
                    deko = '[[Minzblatt]]'
                zubereitungshinweise.remove(hint)
                break

    # Check ingredients for garnish items
    for ing in zutaten:
        if 'Orangenscheibe' in ing:
            deko = '[[Orangenscheibe]]'
        elif 'Zitronenscheibe' in ing:
            deko = '[[Zitronenscheibe]]'
        elif 'Limettenscheibe' in ing:
            deko = '[[Limettenscheibe]]'

    # Check for ice mentions in Zubereitungshinweise
    for hint in zubereitungshinweise:
        if 'crushed' in hint.lower() or 'Crushed' in hint:
            eis = '[[Crushed Ice]]'
            break
        elif 'kein Eis' in hint.lower() or 'ohne Eis' in hint.lower():
            eis = ''
            break

    # Build the new format
    new_content = '# Zutaten\n'
    for ing in processed_ingredients:
        new_content += f'{ing}\n'

    new_content += '\n# Zubereitung\n'

    # Add technique line
    if zubereitung_techniques and ingredient_names:
        technique_str = ', '.join([f'[[{t}]]' for t in zubereitung_techniques])
        ingredients_str = ', '.join(ingredient_names)
        new_content += f'{technique_str}: {ingredients_str}\n'
    elif zubereitung_techniques:
        technique_str = ', '.join([f'[[{t}]]' for t in zubereitung_techniques])
        new_content += f'{technique_str}\n'

    # Add preparation hints
    for hint in zubereitungshinweise:
        new_content += f'{hint}\n'

    new_content += '\n# Served\n'
    new_content += f'* Glas: {glas}\n'
    if eis:
        new_content += f'* Eis: {eis}\n'
    new_content += f'* Deko: {deko}\n'

    new_content += '\n# Kategorien\n'

    return new_content

def main():
    base_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Cocktails')
    rezepte_1_dir = base_dir / 'Rezepte 1'
    target_dir = base_dir

    # Read the list of files to convert
    list_file = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/missing_recipes_list.txt')

    if not list_file.exists():
        print(f"Error: {list_file} not found")
        return

    with open(list_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Extract file paths (skip header lines)
    files_to_convert = []
    for line in lines:
        line = line.strip()
        if line and line.startswith('Cocktails/Rezepte 1/'):
            # Convert relative path to absolute
            rel_path = line.replace('Cocktails/Rezepte 1/', '')
            files_to_convert.append(rel_path)

    print(f"Found {len(files_to_convert)} recipes to convert\n")

    converted = []
    failed = []

    for rel_path in files_to_convert:
        source_file = rezepte_1_dir / rel_path

        if not source_file.exists():
            print(f"⚠️  File not found: {source_file}")
            failed.append((rel_path, "File not found"))
            continue

        try:
            # Read the original file
            with open(source_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Convert the recipe
            new_content = convert_recipe(content, source_file.name)

            # Write to target directory (just the filename, not the subdirectory structure)
            target_file = target_dir / source_file.name

            with open(target_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            print(f"✓ Converted: {source_file.name}")
            converted.append(source_file.name)

        except Exception as e:
            print(f"✗ Failed: {source_file.name} - {str(e)}")
            failed.append((rel_path, str(e)))

    # Print summary
    print("\n" + "="*80)
    print(f"CONVERSION SUMMARY")
    print("="*80)
    print(f"Total recipes to convert: {len(files_to_convert)}")
    print(f"Successfully converted: {len(converted)}")
    print(f"Failed: {len(failed)}")

    if failed:
        print("\n❌ Failed conversions:")
        for path, error in failed:
            print(f"  - {path}: {error}")

    print("\n✅ Conversion complete!")

if __name__ == '__main__':
    main()
