#!/usr/bin/env python3
"""
Sixth pass conversion - final comprehensive cleanup of all remaining German
"""

import os
import re
from pathlib import Path
from collections import defaultdict

# Base directory
BASE_DIR = Path("/Users/jan/Documents/Obsidian Vault/Sync/Rezepte")

# Additional replacements for sixth pass - comprehensive cleanup
REPLACEMENTS = {
    # More specific German words
    r'\bPfirsichlikör\b': 'Peach Liqueur',
    r'\bBarlöffel\b': 'bar spoon',
    r'\bvorsichtig\b': 'carefully',
    r'\boben\b': 'on top',
    r'\baufgießen\b': 'pour',
    r'\bdann\b': 'then',
    r'\bdrei\b': 'three',
    r'\beinzelne\b': 'individual',
    r'\bhinein\b': 'into',
    r'\btropfen\b': 'drip',
    r'\beinem\b': 'a',

    r'\bWodka\b': 'Vodka',
    r'\bShotglas\b': 'shot glass',
    r'\bfüllen\b': 'fill',
    r'\bhalbe\b': 'half',
    r'\bZitrone-\b': 'lemon',
    r'\bOrangenschreibe\b': 'orange slice',
    r'\bdas Glass\b': 'the glass',
    r'\blegen\b': 'place',
    r'\bZuckerwürfel\b': 'sugar cube',
    r'\bdie Scheibe\b': 'the slice',
    r'\bbeträufeln\b': 'drizzle',
    r'\bkurz\b': 'briefly',
    r'\bwarten\b': 'wait',
    r'\bbis\b': 'until',
    r'\bgetränkt\b': 'soaked',
    r'\bist\b': 'is',
    r'\banzünden\b': 'ignite',

    r'\bdünne\b': 'thin',
    r'\bScheiben\b': 'slices',
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

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
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
            return False

    return False

def process_directory(directory, pattern="**/*.md"):
    """Process all markdown files in directory"""
    files = list(Path(directory).glob(pattern))

    modified = 0
    for file_path in files:
        if process_file(file_path):
            modified += 1

    return modified

def main():
    print("=" * 80)
    print("GERMAN TO ENGLISH CONVERSION - SIXTH PASS (FINAL COMPREHENSIVE)")
    print("=" * 80)
    print()

    # Process all directories
    for subdir in ['Cocktails', 'Zutaten']:
        dir_path = BASE_DIR / subdir
        if dir_path.exists():
            modified = process_directory(dir_path)
            print(f"Processed {subdir}: {modified} files modified")

    print()
    print("=" * 80)
    print("SIXTH PASS COMPLETE - SUMMARY")
    print("=" * 80)
    print(f"Total files processed: {stats['files_processed']}")
    print(f"Total files modified: {stats['files_modified']}")
    print(f"Total replacements made: {stats['total_replacements']}")

    if stats['replacements_by_pattern']:
        print()
        print("Replacements made:")
        print("-" * 80)
        for pattern, count in sorted(stats['replacements_by_pattern'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {pattern[:60]:<60} {count:>6}")

    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
