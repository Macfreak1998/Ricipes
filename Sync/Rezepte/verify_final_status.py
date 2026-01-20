#!/usr/bin/env python3
"""
Verify the final status of ingredient linking after all fixes.
"""

import os
import re
from pathlib import Path
from collections import Counter

def get_all_ingredient_files():
    """Get all ingredient files from Zutaten directory."""
    base_path = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Zutaten')
    ingredients = set()

    for subdir in ['Spirituosen', 'Säfte', 'Sirups', 'Filler']:
        dir_path = base_path / subdir
        if dir_path.exists():
            for file in dir_path.glob('*.md'):
                ingredients.add(file.stem)

    return ingredients

def extract_ingredients_from_file(file_path):
    """Extract all ingredient links from a cocktail file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all [[ingredient]] links
    ingredients = re.findall(r'\[\[([^\]]+)\]\]', content)
    return ingredients

def analyze_cocktails():
    """Analyze all cocktail files for missing ingredients."""
    cocktails_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Cocktails')
    available_ingredients = get_all_ingredient_files()

    files_with_issues = []
    files_without_issues = []
    all_missing = Counter()

    for file_path in cocktails_dir.glob('*.md'):
        ingredients = extract_ingredients_from_file(file_path)
        missing = [ing for ing in ingredients if ing not in available_ingredients]

        # Filter out non-ingredient links (techniques, glassware, etc.)
        missing = [ing for ing in missing if not is_non_ingredient(ing)]

        if missing:
            files_with_issues.append((file_path.name, missing))
            for ing in missing:
                all_missing[ing] += 1
        else:
            files_without_issues.append(file_path.name)

    return files_with_issues, files_without_issues, all_missing

def is_non_ingredient(name):
    """Check if a link is not an ingredient."""
    # Techniques
    techniques = {
        'Shake', 'Stir', 'Build', 'Strain', 'Double Strain', 'Dry Shake',
        'Muddled', 'Shaken', 'Stirred', 'Built', 'Blended', 'Muddle',
        'Top', 'Float', 'Layer', 'Roll', 'Rinse', 'Express', 'Whip Shake',
        'Blend', 'Dump', 'Im Glas', 'stir', 'whip Shake', 'strain', 'shake', 'muddle'
    }

    # Glassware
    glassware = {
        'Coupe', 'Highball', 'Collins', 'Rocks', 'Martini Glas', 'Cocktailglas',
        'Tumbler', 'Tiki', 'Sektglas', 'Aperitifglas', 'Sherry Glas',
        'Champagne Flute', 'Cocktail Glass', 'Highball Glass', 'Rocks Glass',
        'Coupe Glass', 'Old Fashioned Glas', 'Aperitif Glas', 'Mixingglas',
        'Nick and Nora', 'Hurricane Glass', 'Tiki Mug', 'Sour Glas',
        'Old Fashioned Glass', 'Martini Glass', 'Wine Glass', 'Shot Glass',
        'Copper Mug', 'Goblet', 'Julep Cup'
    }

    # Ice types
    ice = {
        'Eiswürfel', 'Crushed Ice', 'Würfel', 'Straight', 'Cracked Ice',
        'Cube', 'Crushed', 'None', 'Ice Cubes', 'Large Ice Cube', 'Cubed Ice',
        'Slush', 'Fresh Ice', 'Pebble Ice'
    }

    # Categories - these are wiki-links in the Kategorien section
    categories = {
        'Standard ABV', 'Summer', 'Fruity', 'Rum-Based', 'Modern Classics',
        'Citrus-Forward', 'Fruity Cocktails', 'Sour', 'Tiki-Tropical',
        'Rum Cocktails', 'Sweet', 'High ABV', 'Tiki-Polynesian', 'Mixed-Spirit',
        'Caribbean-Latin', 'Bitter', 'Classic Cocktails', 'American Classic',
        'Low ABV', 'Aperitif', 'Digestif', 'Winter', 'Fall', 'Spring',
        'Gin-Based', 'Vodka-Based', 'Whiskey-Based', 'Tequila-Based',
        'European Classic', 'Refreshing', 'Bitter Cocktails', 'Gin Cocktails',
        'Mezcal Cocktails', 'Brandy Cocktails', 'Bourbon Cocktails',
        'Whiskey Cocktails', 'Martini-Style', 'Dessert Cocktails',
        'Creamy Cocktails', 'Vodka Cocktails', 'Tequila Cocktails',
        'Brunch Cocktails', 'After-Dinner', 'Savory Cocktails'
    }

    # Garnishes that are in Deko section
    garnishes = {
        'Zitronenzeste', 'Limettenzeste', 'Orangenzeste', 'Twist',
        'Cherry', 'Lemon', 'Lime', 'Orange', 'Mint Sprig', 'Nutmeg',
        'Pineapple', 'Maraschino Kirsche', 'Limette', 'Lemon Wedge',
        'Lime Wedge', 'Orange Peel', 'Lemon Peel', 'Lime Peel',
        'Pineapple Wedge', 'Pineapple Leaves', 'Cocktail Cherry',
        'Zitronenscheibe', 'Zitrone', 'Lemon Twist', 'Muskat',
        'Cucumber Slice', 'mint', 'Orangenscheibe', 'Minzblatt',
        'cucumber, mint', 'Salt Rim', 'Cinnamon Stick', 'Star Anise',
        'Brandied Cherry', 'Orange Twist', 'Lime Twist', 'Grapefruit Twist'
    }

    # Equipment/Tools
    equipment = {
        'Cocktail Shaker', 'Blender', 'Muddler', 'Strainer', 'Jigger',
        'Bar Spoon', 'Mixing Glass', 'Hawthorne Strainer', 'Fine Strainer'
    }

    return (name in techniques or name in glassware or name in ice or
            name in categories or name in garnishes or name in equipment)

def main():
    print("Analyzing cocktail recipes...")

    files_with_issues, files_without_issues, all_missing = analyze_cocktails()

    total_files = len(files_with_issues) + len(files_without_issues)
    success_rate = (len(files_without_issues) / total_files) * 100

    # Generate report
    report_path = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/FINAL_STATUS_REPORT.md')

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Final Ingredient Linking Status Report\n\n")
        f.write(f"**Date:** {Path(__file__).stat().st_mtime}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- **Total cocktail files:** {total_files}\n")
        f.write(f"- **Files without issues:** {len(files_without_issues)} ({success_rate:.1f}%)\n")
        f.write(f"- **Files with issues:** {len(files_with_issues)} ({100-success_rate:.1f}%)\n")
        f.write(f"- **Unique missing ingredients:** {len(all_missing)}\n\n")

        f.write("## Improvement\n\n")
        f.write("- **Previous success rate:** 72.1%\n")
        f.write(f"- **Current success rate:** {success_rate:.1f}%\n")
        f.write(f"- **Improvement:** +{success_rate - 72.1:.1f} percentage points\n\n")

        f.write("## Top Missing Ingredients\n\n")
        f.write("Most common missing ingredients (used in 2+ recipes):\n\n")
        for ing, count in all_missing.most_common(30):
            if count >= 2:
                f.write(f"- **{ing}** (used in {count} recipes)\n")

        f.write("\n## All Missing Ingredients\n\n")
        f.write(f"Total unique missing ingredients: {len(all_missing)}\n\n")
        for ing, count in sorted(all_missing.items(), key=lambda x: (-x[1], x[0])):
            f.write(f"- {ing} ({count})\n")

    print(f"\n✓ Analysis complete!")
    print(f"✓ Total files: {total_files}")
    print(f"✓ Success rate: {success_rate:.1f}%")
    print(f"✓ Improvement: +{success_rate - 72.1:.1f} percentage points")
    print(f"✓ Unique missing ingredients: {len(all_missing)}")
    print(f"✓ Report saved to: {report_path}")

if __name__ == '__main__':
    main()
