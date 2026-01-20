#!/usr/bin/env python3
"""
Second pass conversion - catches German text not in wiki-links
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path("/Users/jan/Documents/Obsidian Vault/Sync/Rezepte")

# Additional replacements for second pass
REPLACEMENTS = {
    # German words not in wiki-links
    r'\bGrüner Apfelsaft\b': 'Green Apple Juice',
    r'\bApfelsaft\b': 'Apple Juice',
    r'\bApfelscheibe\b': 'Apple Slice',
    r'\bLimettenscheibe\b': 'Lime Slice',
    r'\bZitronenscheibe\b': 'Lemon Slice',
    r'\bOrangenscheibe\b': 'Orange Slice',
    r'\bMaracujasirup\b': 'Passion Fruit Syrup',
    r'\bMaracujasaft\b': 'Passion Fruit Juice',
    r'\bAnanassaft\b': 'Pineapple Juice',
    r'\bCocktailglas\b': 'Cocktail Glass',
    r'\bWeinglas\b': 'Wine Glass',
    r'\bSektglas\b': 'Champagne Flute',
    r'\bSekt\b': 'Sparkling Wine',
    r'\bGlas\b(?! Skull)': 'Glass',  # Avoid "Glas Skull" edge case
    r'\bhalf full with Eis\b': 'half full with ice',
    r'\bins Glas geben\b': 'add to glass',
    r'\bSoda drauf\b': 'top with soda',

    # More garnish terms
    r'\[\[Apfelscheibe\]\]': '[[Apple Slice]]',
    r'\[\[Gurkenscheibe\]\]': '[[Cucumber Slice]]',

    # More juice terms
    r'\[\[Ananassaft\]\]': '[[Pineapple Juice]]',
    r'\[\[Maracujasaft\]\]': '[[Passion Fruit Juice]]',

    # Common preparation words
    r'\bdazu\b': 'add',
    r'\bdrauf\b': 'on top',
    r'\bEis\b(?!-)': 'ice',  # Avoid "Eis-" compound words
}

# Statistics tracking
stats = {
    'files_processed': 0,
    'files_modified': 0,
    'total_replacements': 0,
    'replacements_by_pattern': defaultdict(int),
}

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
        return False

    # Track if file was modified
    original_content = content

    # Apply all replacements
    for pattern, replacement in REPLACEMENTS.items():
        matches = len(re.findall(pattern, content))
        if matches > 0:
            content = re.sub(pattern, replacement, content)
            stats['total_replacements'] += matches
            stats['replacements_by_pattern'][pattern] += matches

    # Write back if modified
    if content != original_content:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            stats['files_modified'] += 1
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {e}")
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

    return modified

def main():
    print("=" * 80)
    print("GERMAN TO ENGLISH CONVERSION - SECOND PASS")
    print("=" * 80)
    print()

    # Process all directories
    for subdir in ['Cocktails', 'Zutaten', 'Deko', 'Gläser', 'Eis', 'Techniken', 'Tools']:
        dir_path = BASE_DIR / subdir
        if dir_path.exists():
            process_directory(dir_path)

    print()
    print("=" * 80)
    print("SECOND PASS COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {stats['files_processed']}")
    print(f"Total files modified: {stats['files_modified']}")
    print(f"Total replacements made: {stats['total_replacements']}")
    print()

    if stats['replacements_by_pattern']:
        print("Top replacements made:")
        print("-" * 80)
        for pattern, count in sorted(stats['replacements_by_pattern'].items(), key=lambda x: x[1], reverse=True)[:20]:
            print(f"  {pattern[:60]:<60} {count:>6}")

    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
