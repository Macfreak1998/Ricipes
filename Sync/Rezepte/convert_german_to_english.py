#!/usr/bin/env python3
"""
Systematic conversion of German text to English in cocktail vault.
Handles all recipe files and ingredient files with comprehensive replacements.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
import sys

# Base directory
BASE_DIR = Path("/Users/jan/Documents/Obsidian Vault/Sync/Rezepte")

# Comprehensive replacement dictionary
REPLACEMENTS = {
    # Section labels (most critical - 619+ files affected)
    r'\* Glas:': '* Glass:',
    r'\* Eis:': '* Ice:',
    r'\* Deko:': '* Garnish:',

    # German juice names (very common)
    r'\[\[Zitronensaft\]\]': '[[Lemon Juice]]',
    r'\[\[Limettensaft\]\]': '[[Lime Juice]]',
    r'\[\[Orangensaft\]\]': '[[Orange Juice]]',
    r'\[\[Grapefruitsaft\]\]': '[[Grapefruit Juice]]',
    r'\[\[Ananassaft\]\]': '[[Pineapple Juice]]',
    r'\[\[Cranberrysaft\]\]': '[[Cranberry Juice]]',
    r'\[\[Maracujasaft\]\]': '[[Passion Fruit Juice]]',

    # Garnish names
    r'\[\[Zitronenscheibe\]\]': '[[Lemon Slice]]',
    r'\[\[Limettenscheibe\]\]': '[[Lime Slice]]',
    r'\[\[Orangenscheibe\]\]': '[[Orange Slice]]',
    r'\[\[Zitronenzeste\]\]': '[[Lemon Twist]]',
    r'\[\[Limettenzeste\]\]': '[[Lime Twist]]',
    r'\[\[Orangenzeste\]\]': '[[Orange Twist]]',
    r'\[\[Minzblatt\]\]': '[[Mint Leaf]]',
    r'\[\[Gurkenscheibe\]\]': '[[Cucumber Slice]]',
    r'\[\[Maraschino Kirsche\]\]': '[[Maraschino Cherry]]',
    r'\[\[Kirsche\]\]': '[[Cherry]]',
    r'\[\[Salzrand\]\]': '[[Salt Rim]]',
    r'\[\[Zuckerrand\]\]': '[[Sugar Rim]]',

    # Glass types
    r'\[\[Weinglas\]\]': '[[Wine Glass]]',
    r'\[\[Sektglas\]\]': '[[Champagne Flute]]',
    r'\[\[Cocktailglas\]\]': '[[Cocktail Glass]]',
    r'\[\[Martini Glas\]\]': '[[Martini Glass]]',
    r'\[\[Highball\]\]': '[[Highball Glass]]',

    # Ice types
    r'\[\[Eiswürfel\]\]': '[[Ice Cubes]]',
    r'\[\[Würfel\]\]': '[[Cubes]]',

    # Technique names
    r'\[\[im Glas\]\]': '[[Build]]',
    r'\[\[geshaked\]\]': '[[Shake]]',
    r'\[\[gerührt\]\]': '[[Stir]]',

    # Common German words in preparation
    r'\bmit\b': 'with',
    r'\bund\b': 'and',
    r'\boder\b': 'or',
    r'\bauf\b': 'on',
    r'\bim\b': 'in',
    r'\bgarnieren\b': 'garnish',
    r'\bauffüllen\b': 'top up',
    r'\bSchluck\b': 'splash',
    r'\bfrisch gepresst\b': 'freshly squeezed',
    r'\bfrischer\b': 'fresh',
    r'\bfrische\b': 'fresh',
    r'\bfrisches\b': 'fresh',
    r'\bhalbvoll\b': 'half full',

    # Ingredient names
    r'\[\[Zitrone\]\]': '[[Lemon]]',
    r'\[\[Limette\]\]': '[[Lime]]',
    r'\[\[Orange\]\]': '[[Orange]]',
    r'\[\[Minze\]\]': '[[Mint]]',
    r'\[\[Sahne\]\]': '[[Heavy Cream]]',
    r'\[\[Gurke\]\]': '[[Cucumber]]',
    r'\[\[Zucker\]\]': '[[Sugar]]',
    r'\[\[Salz\]\]': '[[Salt]]',

    # Other common terms
    r'\bZitronensaft\b': 'Lemon Juice',
    r'\bLimettensaft\b': 'Lime Juice',
    r'\bOrangensaft\b': 'Orange Juice',
    r'\bGrapefruitsaft\b': 'Grapefruit Juice',
    r'\bAnanassaft\b': 'Pineapple Juice',
    r'\bCranberrysaft\b': 'Cranberry Juice',
    r'\bMaracujasaft\b': 'Passion Fruit Juice',
    r'\bZitronenzeste\b': 'Lemon Twist',
    r'\bLimettenzeste\b': 'Lime Twist',
    r'\bOrangenzeste\b': 'Orange Twist',
    r'\bMinzblatt\b': 'Mint Leaf',
    r'\bGurkenscheibe\b': 'Cucumber Slice',
    r'\bEiswürfel\b': 'Ice Cubes',
    r'\bWürfel\b': 'Cubes',
}

# Statistics tracking
stats = {
    'files_processed': 0,
    'files_modified': 0,
    'total_replacements': 0,
    'replacements_by_type': defaultdict(int),
    'encoding_issues': [],
    'errors': []
}

def categorize_replacement(pattern):
    """Categorize replacement for statistics"""
    if 'Glas:' in pattern or 'Eis:' in pattern or 'Deko:' in pattern:
        return 'Section Labels'
    elif 'saft' in pattern.lower():
        return 'Juice Names'
    elif 'zeste' in pattern.lower() or 'scheibe' in pattern.lower() or 'blatt' in pattern.lower():
        return 'Garnish Names'
    elif 'glas' in pattern.lower():
        return 'Glass Types'
    elif 'würfel' in pattern.lower() or 'Crushed' in pattern:
        return 'Ice Types'
    elif r'\b' in pattern and not r'\[\[' in pattern:
        return 'Common Words'
    else:
        return 'Other'

def process_file(file_path):
    """Process a single file and apply all replacements"""
    global stats

    stats['files_processed'] += 1

    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'iso-8859-1']
    content = None
    encoding_used = None

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            encoding_used = encoding
            break
        except UnicodeDecodeError:
            continue

    if content is None:
        stats['encoding_issues'].append(str(file_path))
        return False

    # Track if file was modified
    original_content = content
    file_replacements = 0

    # Apply all replacements
    for pattern, replacement in REPLACEMENTS.items():
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            file_replacements += matches
            stats['total_replacements'] += matches
            category = categorize_replacement(pattern)
            stats['replacements_by_type'][category] += matches

    # Write back if modified
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            return True
        except Exception as e:
            stats['errors'].append(f"{file_path}: {str(e)}")
            return False

    return False

def process_directory(directory, pattern="**/*.md"):
    """Process all markdown files in directory"""
    files = list(Path(directory).glob(pattern))
    print(f"Processing {len(files)} files in {directory}...")

    modified = 0
    for file_path in files:
        if process_file(file_path):
            modified += 1
            if modified % 50 == 0:
                print(f"  Modified {modified} files so far...")

    return modified

def main():
    print("=" * 80)
    print("GERMAN TO ENGLISH CONVERSION - COCKTAIL VAULT")
    print("=" * 80)
    print()

    # Process cocktail recipes
    print("Phase 1: Processing Cocktail Recipes")
    print("-" * 80)
    cocktails_dir = BASE_DIR / "Cocktails"
    process_directory(cocktails_dir)

    print()
    print("Phase 2: Processing Ingredient Files")
    print("-" * 80)

    # Process all ingredient subdirectories
    zutaten_dir = BASE_DIR / "Zutaten"
    if zutaten_dir.exists():
        process_directory(zutaten_dir)

    # Process other directories (Deko, Gläser, Eis, etc.)
    for subdir in ['Deko', 'Gläser', 'Eis', 'Techniken', 'Tools']:
        dir_path = BASE_DIR / subdir
        if dir_path.exists():
            process_directory(dir_path)

    print()
    print("=" * 80)
    print("CONVERSION COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {stats['files_processed']}")
    print(f"Total files modified: {stats['files_modified']}")
    print(f"Total replacements made: {stats['total_replacements']}")
    print()

    print("Replacements by category:")
    print("-" * 80)
    for category, count in sorted(stats['replacements_by_type'].items(), key=lambda x: x[1], reverse=True):
        print(f"  {category:.<40} {count:>6}")

    if stats['encoding_issues']:
        print()
        print(f"Encoding issues encountered: {len(stats['encoding_issues'])}")
        for file in stats['encoding_issues'][:10]:
            print(f"  - {file}")
        if len(stats['encoding_issues']) > 10:
            print(f"  ... and {len(stats['encoding_issues']) - 10} more")

    if stats['errors']:
        print()
        print(f"Errors encountered: {len(stats['errors'])}")
        for error in stats['errors'][:10]:
            print(f"  - {error}")
        if len(stats['errors']) > 10:
            print(f"  ... and {len(stats['errors']) - 10} more")

    print()
    print("=" * 80)

    # Write detailed report
    report_file = BASE_DIR / "conversion_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("GERMAN TO ENGLISH CONVERSION REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Date: {Path(__file__).stat().st_mtime}\n")
        f.write(f"Total files processed: {stats['files_processed']}\n")
        f.write(f"Total files modified: {stats['files_modified']}\n")
        f.write(f"Total replacements made: {stats['total_replacements']}\n\n")

        f.write("Replacements by category:\n")
        f.write("-" * 80 + "\n")
        for category, count in sorted(stats['replacements_by_type'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"{category}: {count}\n")

        if stats['encoding_issues']:
            f.write(f"\n\nEncoding issues ({len(stats['encoding_issues'])}):\n")
            for file in stats['encoding_issues']:
                f.write(f"  {file}\n")

        if stats['errors']:
            f.write(f"\n\nErrors ({len(stats['errors'])}):\n")
            for error in stats['errors']:
                f.write(f"  {error}\n")

    print(f"Detailed report saved to: {report_file}")

if __name__ == "__main__":
    main()
