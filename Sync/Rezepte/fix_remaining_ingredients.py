#!/usr/bin/env python3
"""
Fix remaining ingredient linking issues:
1. Fix typos
2. Map German ingredients to English
3. Map brand names to generics
"""

import os
import re
from pathlib import Path

# Define mappings
TYPO_FIXES = {
    'Simply Syrup': 'Simple Syrup',
    'Tripple Sec': 'Triple Sec',
    'Coffee Liquor': 'Coffee Liqueur',
    'Champage': 'Champagne',
    'Ramazotti': 'Ramazzotti',
    'Simple Sirup': 'Simple Syrup',
    'Rhum Agricolee': 'Rhum Agricole',
    'Curacao': 'Curaçao',
    'Dashes Angustrora Bitters': 'Angostura Bitters',
    'Kahlúa': 'Coffee Liqueur',
    'Orgeat Syrup': 'Orgeat',
}

PREFIX_REMOVALS = {
    'Barspoon Velvet Falernum': 'Velvet Falernum',
    'Barspoon Grendaine': 'Grenadine',
    '1 Soda Water': 'Soda Water',
    '1/2 Blue Curacao': 'Blue Curaçao',
    'bar Spoon Maraschino Liqueur': 'Maraschino Liqueur',
    'Dash Angostura': 'Angostura Bitters',
    '1/4 Green Chartreuse lit on fire': 'Green Chartreuse',
    'Dashes of Angostura Bitters': 'Angostura Bitters',
    'Barspoon Vanilla Syrup': 'Vanilla Syrup',
    'Drops Absinthe': 'Absinthe',
    'Dash Orange Bitters': 'Orange Bitters',
    'dashes Angostura Bitters': 'Angostura Bitters',
    'Spoon Brown Sugar': 'Brown Sugar',
    'Top Angostura Bitters': 'Angostura Bitters',
    'Dash Bitters': 'Bitters',
    'Bar Spoon Orange Marmalade': 'Orange Marmalade',
    '1/4 Red Wine': 'Red Wine',
    '1/4oz (37.5ml) Irish Whiskey': 'Irish Whiskey',
    '(7.5ml) Cinnamon Syrup': 'Cinnamon Syrup',
    '4-5oz (120-150ml) Hot Coffee': 'Hot Coffee',
    '1/4 mezcal': 'Mezcal',
    'Bar Spoon Maraschino Liqueur': 'Maraschino Liqueur',
    'Dash Absinthe': 'Absinthe',
    'Dash Peychaud\'s Bitters': 'Peychaud\'s Bitters',
    'Dashes Angostura bitters': 'Angostura Bitters',
    '1/2 Creme de Mure': 'Creme de Mure',
    'of Benedictine': 'Benedictine',
    'drops of Pernod': 'Pernod',
}

GERMAN_TO_ENGLISH = {
    'Salzlösung': 'Saline Solution',
    'ganzes Ei': 'Whole Egg',
    'Ingwersirup': 'Ginger Syrup',
    'Bananenlikör': 'Banana Liqueur',
    'Waldmeistersirup': 'Woodruff Syrup',
    'Himbeersirup': 'Raspberry Syrup',
    'Roter Portwein': 'Red Port Wine',
    'Vanillesirup': 'Vanilla Syrup',
    'Kaffeelikör': 'Coffee Liqueur',
    'rote Chilli': 'Red Chilli',
    'Rosmarin': 'Rosemary',
    'Agavendicksaft': 'Agave Syrup',
    'Orangenblütenwasser': 'Orange Flower Water',
    'Kokosrum': 'coconut rum',
    'Basilikum Blätter': 'Basil',
    'Kokosnusscreme': 'Coconut Cream',
    'schwarzer Himbeerlikör': 'Black Raspberry Liqueur',
    'Kokossirup': 'Coconut Syrup',
    'Pfirsichlikör': 'Peach Liquor',
    'frischer Lime Juice': 'Lime Juice',
    'Vanille Vodka': 'Vanilla Vodka',
    'Limettenzeste': 'Lime',
    'Heidelbeersirup': 'Raspberry Syrup',
    'Maracujalikör': 'Passion Fruit Liquor',
}

BRAND_TO_GENERIC = {
    'Chambord': 'Black Raspberry Liqueur',
    'Ricard': 'Pernod',
    'Noilly Prat Dry Vermouth': 'Dry Vermouth',
    'Rose\'s Lime Cordial': 'Lime Juice',
    'Bacardi Rum': 'White Rum',
    'Grey Goose': 'Vodka',
    'Aviation Gin': 'Gin',
    'Roku Gin': 'Gin',
    'St-Germain': 'Elderflower Liqueur',
    'Galliano L\'Autentico': 'Galliano',
    'Appleton Estate Signature': 'Jamaican Rum',
    'Banks 7 Rum': 'Gold Rum',
    'Cruzan Blackstrap Rum': 'Dark Rum',
    'Smith and Cross Jamaican Rum': 'Jamaican Rum',
    'Havana': 'White Rum',
    'Puerto Rican White Rum': 'White Rum',
    'Moët & Chandon Imperial Brut': 'Champagne',
    'Brut Champagne': 'Champagne',
    'Hard Truth Toasted Coconut Rum': 'coconut rum',
}

# Combine all mappings
ALL_MAPPINGS = {**TYPO_FIXES, **PREFIX_REMOVALS, **GERMAN_TO_ENGLISH, **BRAND_TO_GENERIC}

def fix_ingredients_in_file(file_path):
    """Fix ingredient links in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    fixes_made = []

    # Apply all mappings
    for old_name, new_name in ALL_MAPPINGS.items():
        # Look for [[old_name]] pattern
        old_pattern = f'[[{old_name}]]'
        new_pattern = f'[[{new_name}]]'

        if old_pattern in content:
            content = content.replace(old_pattern, new_pattern)
            fixes_made.append(f'{old_name} → {new_name}')

    # Write back if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes_made

    return []

def main():
    cocktails_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Cocktails')

    total_files_modified = 0
    total_fixes = 0
    all_fixes = []

    for file_path in cocktails_dir.glob('*.md'):
        fixes = fix_ingredients_in_file(file_path)
        if fixes:
            total_files_modified += 1
            total_fixes += len(fixes)
            all_fixes.append(f"\n{file_path.name}:")
            for fix in fixes:
                all_fixes.append(f"  - {fix}")

    # Write report
    report_path = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/ingredient_cleanup_report.txt')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"INGREDIENT CLEANUP REPORT\n")
        f.write(f"=" * 80 + "\n\n")
        f.write(f"Files modified: {total_files_modified}\n")
        f.write(f"Total fixes applied: {total_fixes}\n\n")
        f.write(f"DETAILS:\n")
        f.write("\n".join(all_fixes))

    print(f"✓ Fixed {total_fixes} ingredients across {total_files_modified} files")
    print(f"✓ Report saved to: {report_path}")

if __name__ == '__main__':
    main()
