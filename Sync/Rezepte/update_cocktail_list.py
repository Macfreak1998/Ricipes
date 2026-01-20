#!/usr/bin/env python3
"""
Update Cocktail-Liste.md with all current cocktails from Cocktails directory.
"""

from pathlib import Path

def main():
    cocktails_dir = Path('Cocktails')

    # Get all .md files from Cocktails directory
    cocktail_files = sorted([f.stem for f in cocktails_dir.glob('*.md')])

    total_cocktails = len(cocktail_files)

    # Generate the list
    content = f"""# Cocktail Liste

Diese Liste enthält alle Cocktails, die derzeit in dieser Sammlung enthalten sind.

## Vollständige Liste ({total_cocktails} Cocktails)

"""

    for i, cocktail in enumerate(cocktail_files, 1):
        content += f"{i}. [[{cocktail}]]\n"

    # Write the updated list
    list_path = Path('Cocktail-Liste.md')
    with open(list_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✓ Updated Cocktail-Liste.md")
    print(f"✓ Total cocktails: {total_cocktails}")
    print(f"✓ List saved to: {list_path}")

if __name__ == '__main__':
    main()
