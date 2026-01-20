#!/usr/bin/env python3
"""
Generate collection files for cocktails grouped by spirit base.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_base_spirit(content: str, filename: str) -> str:
    """Extract base spirit from Kategorien section or first ingredient."""
    # First try Kategorien
    kategorien = re.search(r'# Kategorien\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if kategorien:
        base_match = re.search(r'-\s*Base:\s*\[\[(.*?)\]\]', kategorien.group(1))
        if base_match:
            base = base_match.group(1)
            # Normalize
            if 'Gin' in base:
                return 'Gin'
            elif 'Vodka' in base:
                return 'Vodka'
            elif 'Rum' in base:
                return 'Rum'
            elif 'Whiskey' in base or 'Bourbon' in base or 'Rye' in base:
                return 'Whiskey'
            elif 'Tequila' in base or 'Mezcal' in base:
                return 'Tequila & Mezcal'
            elif 'Brandy' in base or 'Cognac' in base:
                return 'Brandy & Cognac'
            return base

    # Fallback: try first ingredient
    zutaten_match = re.search(r'# Zutaten\s*\n\n-\s*[\d\.]+\s*\[\[(.*?)\]\]', content)
    if zutaten_match:
        spirit = zutaten_match.group(1).strip()
        spirit_map = {
            'Gin': 'Gin',
            'Vodka': 'Vodka',
            'White Rum': 'Rum',
            'Dark Rum': 'Rum',
            'Aged Rum': 'Rum',
            'Light Rum': 'Rum',
            'Rum': 'Rum',
            'Bourbon': 'Whiskey',
            'Rye Whiskey': 'Whiskey',
            'Scotch': 'Whiskey',
            'Irish Whiskey': 'Whiskey',
            'Tequila Blanco': 'Tequila & Mezcal',
            'Reposado Tequila': 'Tequila & Mezcal',
            'Mezcal': 'Tequila & Mezcal',
            'Cognac': 'Brandy & Cognac',
            'Brandy': 'Brandy & Cognac',
            'Calvados': 'Brandy & Cognac',
        }
        if spirit in spirit_map:
            return spirit_map[spirit]

    return 'Other Spirits'

def extract_flavor_profiles(content: str) -> list:
    """Extract flavor profiles from Kategorien."""
    flavors = []
    kategorien = re.search(r'# Kategorien\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if kategorien:
        flavor_matches = re.findall(r'-\s*Flavor:\s*\[\[(.*?)\]\]', kategorien.group(1))
        flavors.extend(flavor_matches)
    return flavors

def extract_occasion(content: str) -> list:
    """Extract occasions from Kategorien."""
    occasions = []
    kategorien = re.search(r'# Kategorien\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if kategorien:
        occasion_matches = re.findall(r'-\s*Occasion:\s*\[\[(.*?)\]\]', kategorien.group(1))
        occasions.extend(occasion_matches)
    return occasions

def extract_technique(content: str) -> str:
    """Extract technique from Kategorien or Zubereitung."""
    kategorien = re.search(r'# Kategorien\s*\n(.*?)(?=\n#|\Z)', content, re.DOTALL)
    if kategorien:
        tech_match = re.search(r'-\s*Technique:\s*\[\[(.*?)\]\]', kategorien.group(1))
        if tech_match:
            return tech_match.group(1)

    # Fallback
    if '[[Shake]]' in content or '[[Shaken]]' in content:
        return 'Shaken'
    elif '[[Stir]]' in content or '[[Stirred]]' in content:
        return 'Stirred'
    elif '[[Build]]' in content or '[[Built]]' in content:
        return 'Built'
    return 'Built'

def get_one_liner(content: str) -> str:
    """Try to extract a one-line description from History."""
    history = re.search(r'# History\s*\n(.*?)(?=\n\n|\n#)', content, re.DOTALL)
    if history:
        first_sentence = history.group(1).strip().split('.')[0] + '.'
        # Clean up
        first_sentence = re.sub(r'\*\*', '', first_sentence)
        first_sentence = re.sub(r'\n', ' ', first_sentence)
        if len(first_sentence) < 200:
            return first_sentence
    return ""

def main():
    """Generate collection files."""
    cocktails_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Cocktails')
    collections_dir = Path('/Users/jan/Documents/Obsidian Vault/Sync/Rezepte/Kategorien/Collections')

    collections = defaultdict(list)
    flavor_collections = defaultdict(list)
    occasion_collections = defaultdict(list)
    technique_collections = defaultdict(list)

    print("📚 Generating Collection Files")
    print("=" * 60)
    print()

    # Scan all cocktail files
    for filepath in sorted(cocktails_dir.glob('*.md')):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            name = filepath.stem
            spirit = extract_base_spirit(content, name)
            flavors = extract_flavor_profiles(content)
            occasions = extract_occasion(content)
            technique = extract_technique(content)
            one_liner = get_one_liner(content)

            # Add to spirit collection
            collections[spirit].append((name, one_liner))

            # Add to flavor collections
            for flavor in flavors:
                flavor_collections[flavor].append(name)

            # Add to occasion collections
            for occasion in occasions:
                occasion_collections[occasion].append(name)

            # Add to technique collection
            technique_collections[technique].append(name)

        except Exception as e:
            print(f"⚠️  Error reading {filepath.name}: {e}")

    # Create spirit-based collections
    print("\n📖 Creating Spirit Collections:")
    for spirit, cocktails in sorted(collections.items()):
        if len(cocktails) < 3:  # Skip spirits with very few cocktails
            continue

        filename = collections_dir / f"{spirit.replace(' & ', '-').replace(' ', '-')}-Cocktails.md"

        content_lines = [f"# {spirit} Cocktails"]
        content_lines.append("")
        content_lines.append(f"Collection of {len(cocktails)} cocktails featuring {spirit} as the base spirit.")
        content_lines.append("")
        content_lines.append("## Cocktails")
        content_lines.append("")

        for name, one_liner in sorted(cocktails, key=lambda x: x[0]):
            if one_liner:
                content_lines.append(f"- [[{name}]] - {one_liner[:120]}")
            else:
                content_lines.append(f"- [[{name}]]")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        print(f"  ✅ {filename.name} ({len(cocktails)} cocktails)")

    # Create technique collections
    print("\n🔧 Creating Technique Collections:")
    for technique, cocktails in sorted(technique_collections.items()):
        if len(cocktails) < 10:
            continue

        filename = collections_dir / f"{technique}-Cocktails.md"

        content_lines = [f"# {technique} Cocktails"]
        content_lines.append("")
        content_lines.append(f"Collection of {len(cocktails)} cocktails using the {technique.lower()} technique.")
        content_lines.append("")
        content_lines.append("## Cocktails")
        content_lines.append("")

        for name in sorted(cocktails):
            content_lines.append(f"- [[{name}]]")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        print(f"  ✅ {filename.name} ({len(cocktails)} cocktails)")

    # Create flavor collections (top flavors only)
    print("\n🎨 Creating Flavor Collections:")
    top_flavors = sorted(flavor_collections.items(), key=lambda x: len(x[1]), reverse=True)[:10]

    for flavor, cocktails in top_flavors:
        if len(cocktails) < 10:
            continue

        filename = collections_dir / f"{flavor.replace(' ', '-')}-Cocktails.md"

        content_lines = [f"# {flavor} Cocktails"]
        content_lines.append("")
        content_lines.append(f"Collection of {len(cocktails)} cocktails with {flavor.lower()} flavor profile.")
        content_lines.append("")
        content_lines.append("## Cocktails")
        content_lines.append("")

        for name in sorted(cocktails):
            content_lines.append(f"- [[{name}]]")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        print(f"  ✅ {filename.name} ({len(cocktails)} cocktails)")

    # Create occasion collections
    print("\n🎉 Creating Occasion Collections:")
    for occasion, cocktails in sorted(occasion_collections.items()):
        if len(cocktails) < 10:
            continue

        filename = collections_dir / f"{occasion.replace(' ', '-')}-Cocktails.md"

        content_lines = [f"# {occasion} Cocktails"]
        content_lines.append("")
        content_lines.append(f"Collection of {len(cocktails)} cocktails perfect for {occasion.lower()} occasions.")
        content_lines.append("")
        content_lines.append("## Cocktails")
        content_lines.append("")

        for name in sorted(cocktails):
            content_lines.append(f"- [[{name}]]")

        with open(filename, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content_lines))

        print(f"  ✅ {filename.name} ({len(cocktails)} cocktails)")

    # Summary
    print()
    print("=" * 60)
    print("📊 Summary:")
    print(f"  Spirit collections: {len([c for c in collections.values() if len(c) >= 3])}")
    print(f"  Technique collections: {len([c for c in technique_collections.values() if len(c) >= 10])}")
    print(f"  Flavor collections: {len([c for c in flavor_collections.values() if len(c) >= 10])}")
    print(f"  Occasion collections: {len([c for c in occasion_collections.values() if len(c) >= 10])}")
    print()
    print(f"📁 Collections saved to: {collections_dir}")

if __name__ == '__main__':
    main()
