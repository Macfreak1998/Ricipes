#!/usr/bin/env python3
"""
Find all German text in cocktail recipes and ingredient files.
"""

import os
import re
from pathlib import Path
from collections import Counter

# Common German words/patterns to look for
GERMAN_PATTERNS = {
    # Ingredients
    'Zitrone': 'Lemon',
    'Limette': 'Lime',
    'Orange': 'Orange',
    'Minze': 'Mint',
    'Sahne': 'Heavy Cream',
    'Ananassaft': 'Pineapple Juice',
    'Orangensaft': 'Orange Juice',
    'Grapefruitsaft': 'Grapefruit Juice',
    'Cranberrysaft': 'Cranberry Juice',
    'Limettensaft': 'Lime Juice',
    'Zitronensaft': 'Lemon Juice',
    'Maracujasaft': 'Passion Fruit Juice',

    # Common words
    'mit': 'with',
    'und': 'and',
    'oder': 'or',
    'auf': 'on',
    'im': 'in',
    'Glas': 'Glass',
    'Eis': 'Ice',
    'garnieren': 'garnish',
    'auffüllen': 'top up',
    'shaken': 'shake',
    'rühren': 'stir',
    'mixen': 'mix',

    # Glass types
    'Weinglas': 'Wine Glass',
    'Sektglas': 'Champagne Flute',
    'Tumbler': 'Tumbler',
    'Highball': 'Highball Glass',

    # Garnishes
    'Zitronenscheibe': 'Lemon Slice',
    'Limettenscheibe': 'Lime Slice',
    'Orangenscheibe': 'Orange Slice',
    'Zitronenzeste': 'Lemon Twist',
    'Limettenzeste': 'Lime Twist',
    'Orangenzeste': 'Orange Twist',
    'Minzblatt': 'Mint Leaf',
    'Gurkenscheibe': 'Cucumber Slice',
    'Maraschino Kirsche': 'Maraschino Cherry',

    # Techniques
    'im Glas': 'Build',
    'geshaked': 'Shake',
    'gerührt': 'Stir',

    # Misc
    'Schluck': 'splash',
    'Spritzer': 'dash',
    'Tropfen': 'drops',
    'frisch gepresst': 'freshly squeezed',
    'frischer': 'fresh',
    'halbvoll': 'half full',
    'voll': 'full',
}

def find_german_in_file(file_path):
    """Find German text in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            return [('ERROR', f'Could not read file: {file_path}')]

    found = []
    for german, english in GERMAN_PATTERNS.items():
        # Case-insensitive search for the German word
        if re.search(r'\b' + re.escape(german) + r'\b', content, re.IGNORECASE):
            found.append((german, english))

    # Also check for common German patterns
    # Look for umlaut characters
    if re.search(r'[äöüÄÖÜß]', content):
        found.append(('UMLAUT_DETECTED', 'Contains German umlauts'))

    return found

def main():
    cocktails_dir = Path('Cocktails')
    ingredients_dir = Path('Zutaten')

    german_in_cocktails = {}
    german_in_ingredients = {}

    # Scan cocktails
    print("Scanning cocktail recipes...")
    for file_path in cocktails_dir.glob('*.md'):
        found = find_german_in_file(file_path)
        if found:
            german_in_cocktails[file_path.name] = found

    # Scan ingredients
    print("Scanning ingredient files...")
    for root, dirs, files in os.walk(ingredients_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                found = find_german_in_file(file_path)
                if found:
                    german_in_ingredients[str(file_path)] = found

    # Generate report
    print(f"\n{'='*80}")
    print("GERMAN TEXT DETECTION REPORT")
    print(f"{'='*80}\n")

    print(f"Cocktail recipes with German text: {len(german_in_cocktails)}")
    print(f"Ingredient files with German text: {len(german_in_ingredients)}\n")

    # Count occurrences
    german_word_count = Counter()
    for findings in german_in_cocktails.values():
        for german, _ in findings:
            german_word_count[german] += 1

    print("Most common German words in cocktails:")
    for word, count in german_word_count.most_common(20):
        print(f"  {word}: {count} files")

    # Write detailed report
    with open('german_text_report.txt', 'w', encoding='utf-8') as f:
        f.write("GERMAN TEXT DETECTION REPORT\n")
        f.write("="*80 + "\n\n")

        f.write(f"Total cocktail files with German: {len(german_in_cocktails)}\n")
        f.write(f"Total ingredient files with German: {len(german_in_ingredients)}\n\n")

        f.write("COCKTAIL RECIPES WITH GERMAN TEXT:\n")
        f.write("-"*80 + "\n")
        for filename, findings in sorted(german_in_cocktails.items()):
            f.write(f"\n{filename}:\n")
            for german, english in findings:
                f.write(f"  - {german} → {english}\n")

        f.write("\n\nINGREDIENT FILES WITH GERMAN TEXT:\n")
        f.write("-"*80 + "\n")
        for filepath, findings in sorted(german_in_ingredients.items()):
            f.write(f"\n{filepath}:\n")
            for german, english in findings:
                f.write(f"  - {german} → {english}\n")

    print(f"\n✓ Detailed report saved to: german_text_report.txt")
    print(f"✓ Found German text in {len(german_in_cocktails)} cocktails")
    print(f"✓ Found German text in {len(german_in_ingredients)} ingredient files")

if __name__ == '__main__':
    main()
