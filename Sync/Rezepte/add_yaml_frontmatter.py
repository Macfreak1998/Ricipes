#!/usr/bin/env python3
"""
Add YAML frontmatter to cocktail files based on existing content.
Extracts metadata from Kategorien section and standardizes it.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Optional

def extract_base_spirit(content: str) -> Optional[str]:
    """Extract base spirit from first ingredient."""
    zutaten_match = re.search(r'# Zutaten\s*\n\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if zutaten_match:
        first_ingredient = re.search(r'-\s*[\d\.]+\s*\[\[(.*?)\]\]', zutaten_match.group(1))
        if first_ingredient:
            spirit = first_ingredient.group(1).strip()
            # Map to standard categories
            spirit_map = {
                'Gin': 'Gin',
                'Vodka': 'Vodka',
                'White Rum': 'Rum',
                'Dark Rum': 'Rum',
                'Aged Rum': 'Rum',
                'Light Rum': 'Rum',
                'Bourbon': 'Whiskey',
                'Rye Whiskey': 'Whiskey',
                'Scotch': 'Whiskey',
                'Irish Whiskey': 'Whiskey',
                'Tequila Blanco': 'Tequila',
                'Reposado Tequila': 'Tequila',
                'Añejo Tequila': 'Tequila',
                'Mezcal': 'Mezcal',
                'Cognac': 'Brandy',
                'Brandy': 'Brandy',
                'Calvados': 'Brandy',
                'Rum': 'Rum',
                'Campari': 'Liqueur',
                'Aperol': 'Liqueur',
            }
            return spirit_map.get(spirit, spirit)
    return None

def extract_technique(content: str) -> Optional[str]:
    """Extract primary technique from Zubereitung."""
    zubereitung = re.search(r'# Zubereitung\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if zubereitung:
        text = zubereitung.group(1)
        if '[[Shake]]' in text or '[[Shaken]]' in text:
            return 'Shaken'
        elif '[[Stir]]' in text or '[[Stirred]]' in text:
            return 'Stirred'
        elif '[[Build]]' in text or '[[Built]]' in text:
            return 'Built'
        elif '[[Muddle]]' in text:
            return 'Muddled'
        elif '[[Blend]]' in text:
            return 'Blended'
    return 'Built'

def extract_kategorien(content: str) -> Dict[str, List[str]]:
    """Extract all categories from Kategorien section."""
    kategorien = {}
    kat_section = re.search(r'# Kategorien\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)

    if kat_section:
        lines = kat_section.group(1).strip().split('\n')
        for line in lines:
            match = re.match(r'-\s*(\w+):\s*\[\[(.*?)\]\]', line)
            if match:
                key = match.group(1)
                value = match.group(2)
                if key not in kategorien:
                    kategorien[key] = []
                kategorien[key].append(value)

    return kategorien

def extract_glass_and_garnish(content: str) -> tuple:
    """Extract glassware and garnish from Served section."""
    served = re.search(r'# Served\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    glass = None
    garnish = None

    if served:
        text = served.group(1)
        glass_match = re.search(r'\*\s*Glass:\s*\[\[(.*?)\]\]', text)
        if glass_match:
            glass = glass_match.group(1)

        garnish_match = re.search(r'\*\s*Garnish:\s*(.+?)(?=\n|\Z)', text)
        if garnish_match:
            garnish = garnish_match.group(1).strip()
            # Clean up wiki links in garnish
            garnish = re.sub(r'\[\[(.*?)\]\]', r'\1', garnish)

    return glass, garnish

def count_ingredients(content: str) -> int:
    """Count number of ingredients."""
    zutaten = re.search(r'# Zutaten\s*\n\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if zutaten:
        return len(re.findall(r'-\s*[\d\.]+', zutaten.group(1)))
    return 0

def determine_difficulty(content: str) -> str:
    """Determine difficulty based on ingredients and techniques."""
    num_ingredients = count_ingredients(content)
    technique = extract_technique(content)

    # Check for complex techniques
    complex_keywords = ['Double Strain', 'Dry Shake', 'Fat Wash', 'Infusion',
                       'Muddle', 'Layer', 'Flame', 'Reverse Dry Shake']
    is_complex = any(keyword in content for keyword in complex_keywords)

    if num_ingredients <= 3 and technique in ['Built', 'Stirred'] and not is_complex:
        return 'Easy'
    elif num_ingredients > 6 or is_complex:
        return 'Advanced'
    else:
        return 'Intermediate'

def extract_era(content: str) -> Optional[str]:
    """Try to determine era from history section."""
    if 'History' not in content:
        return None

    history = re.search(r'# History\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if not history:
        return None

    text = history.group(1)

    # Look for date ranges
    if any(year in text for year in ['1800s', '1850', '1860', '1870', '1880', '1890']):
        return 'Pre-Prohibition'
    elif any(year in text for year in ['1920', '1930', '1940', '1950', '1960']):
        if 'Prohibition' in text or '1920' in text or '1933' in text:
            return 'Prohibition Era'
        else:
            return 'Golden Age'
    elif any(year in text for year in ['1970', '1980', '1990']):
        return 'Modern Classic'
    elif any(year in text for year in ['2000', '2010', '2020', 'contemporary', 'modern']):
        return 'Contemporary'

    return 'Classic'

def create_yaml_frontmatter(content: str, filename: str) -> Dict:
    """Create YAML frontmatter dictionary from cocktail content."""
    kategorien = extract_kategorien(content)
    glass, garnish = extract_glass_and_garnish(content)

    frontmatter = {
        'title': filename.replace('.md', '').replace('-', ' '),
        'spirit_base': extract_base_spirit(content) or 'Unknown',
        'difficulty': determine_difficulty(content),
        'technique': extract_technique(content),
        'glassware': glass or 'Unknown',
    }

    # Add flavor profiles
    if 'Flavor' in kategorien:
        frontmatter['flavor_profile'] = kategorien['Flavor']

    # Add occasions
    if 'Occasion' in kategorien:
        frontmatter['occasion'] = kategorien['Occasion']

    # Add strength
    if 'Strength' in kategorien:
        strength = kategorien['Strength'][0] if kategorien['Strength'] else 'Standard ABV'
        frontmatter['strength'] = strength

    # Add era
    era = extract_era(content)
    if era:
        frontmatter['era'] = era

    # Add style/family
    if 'Family' in kategorien:
        frontmatter['style'] = kategorien['Family'][0] if kategorien['Family'] else None

    # Add garnish if exists
    if garnish:
        frontmatter['garnish'] = garnish

    return frontmatter

def format_yaml_value(value) -> str:
    """Format a value for YAML output."""
    if isinstance(value, list):
        if len(value) == 1:
            return f'"{value[0]}"'
        return '[' + ', '.join(f'"{v}"' for v in value) + ']'
    elif isinstance(value, str):
        # Escape quotes in strings
        if '"' in value or "'" in value or ':' in value:
            value = value.replace('"', '\\"')
            return f'"{value}"'
        return value
    return str(value)

def add_frontmatter_to_file(filepath: Path, dry_run: bool = False) -> bool:
    """Add YAML frontmatter to a cocktail file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Skip if already has frontmatter
        if content.startswith('---'):
            print(f"  ⏭️  Already has frontmatter: {filepath.name}")
            return False

        # Create frontmatter
        frontmatter = create_yaml_frontmatter(content, filepath.name)

        # Build YAML string
        yaml_lines = ['---']
        for key, value in frontmatter.items():
            if value is not None:
                yaml_lines.append(f'{key}: {format_yaml_value(value)}')
        yaml_lines.append('---')
        yaml_lines.append('')

        # Combine with original content
        new_content = '\n'.join(yaml_lines) + content

        if dry_run:
            print(f"  📝 Would add to: {filepath.name}")
            print(f"     Base: {frontmatter.get('spirit_base')}, "
                  f"Difficulty: {frontmatter.get('difficulty')}, "
                  f"Technique: {frontmatter.get('technique')}")
            return True
        else:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"  ✅ Updated: {filepath.name}")
            return True

    except Exception as e:
        print(f"  ❌ Error processing {filepath.name}: {e}")
        return False

def main():
    """Main function to process all cocktail files."""
    cocktails_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Cocktails')

    if not cocktails_dir.exists():
        print(f"❌ Cocktails directory not found: {cocktails_dir}")
        return

    print("🍸 Cocktail YAML Frontmatter Generator")
    print("=" * 60)
    print()

    # Get all markdown files
    cocktail_files = sorted(cocktails_dir.glob('*.md'))
    total = len(cocktail_files)

    print(f"Found {total} cocktail files\n")

    # Ask for dry run
    response = input("Run in DRY RUN mode first? (y/n): ").strip().lower()
    dry_run = response == 'y'

    if dry_run:
        print("\n🔍 DRY RUN MODE - No files will be modified\n")
    else:
        confirm = input("\n⚠️  This will modify all cocktail files. Continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            return
        print()

    # Process files
    updated = 0
    skipped = 0
    errors = 0

    for filepath in cocktail_files:
        result = add_frontmatter_to_file(filepath, dry_run)
        if result:
            updated += 1
        elif result is False:
            skipped += 1
        else:
            errors += 1

    # Summary
    print()
    print("=" * 60)
    print("📊 Summary:")
    print(f"  Total files: {total}")
    print(f"  {'Would update' if dry_run else 'Updated'}: {updated}")
    print(f"  Skipped (already have frontmatter): {skipped}")
    if errors > 0:
        print(f"  Errors: {errors}")

    if dry_run:
        print("\n💡 Run again without dry run to apply changes")

if __name__ == '__main__':
    main()
