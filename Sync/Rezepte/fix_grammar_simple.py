#!/usr/bin/env python3
"""
Fix the most common broken English patterns from automated conversion.
Target the specific issues seen in the ingredient files.
"""

import os
import re
from pathlib import Path

def fix_file(file_path):
    """Fix grammar in one file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return 0

    original = content

    # Only fix Beschreibung sections (description text)
    # Don't touch History sections or other parts

    # Pattern 1: "is ein" -> "is a"
    content = re.sub(r'\bis ein\b', 'is a', content)
    content = re.sub(r'\bis eine\b', 'is a', content)

    # Pattern 2: "with" in wrong contexts
    content = re.sub(r'aromatisiert wird\. Chinin stammt', 'is aromatized. Quinine comes', content)
    content = re.sub(r'with Chinin aromatisiert', 'aromatized with quinine', content)
    content = re.sub(r'with Zucker gesüßt', 'sweetened with sugar', content)
    content = re.sub(r'kombiniert with der', 'combined with the', content)
    content = re.sub(r'kombiniert with den', 'combined with the', content)

    # Pattern 3: "until zu" -> "up to"
    content = re.sub(r'\buntil zu\b', 'up to', content)
    content = re.sub(r'\buntil Very', 'to Very', content)

    # Pattern 4: "and" in German contexts
    content = re.sub(r'and dem Nordosten', 'and the northeastern', content)
    content = re.sub(r'and einer leichten', 'and a slight', content)
    content = re.sub(r'and einem', 'and a', content)
    content = re.sub(r'and einer', 'and a', content)
    content = re.sub(r'and verwandte', 'and related', content)

    # Pattern 5: Missing articles
    content = re.sub(r'on Gin-Basis', 'on a gin base', content)
    content = re.sub(r'in 19\. and frühen 20\. Jahrhundert', 'in the 19th and early 20th century', content)

    # Pattern 6: German verbs that weren't translated
    content = re.sub(r'wird in Cocktails verwendet', 'is used in cocktails', content)
    content = re.sub(r'verleiht ihnen', 'gives them', content)
    content = re.sub(r'passt besonders gut', 'pairs particularly well', content)
    content = re.sub(r'eignet sich meist', 'is usually suitable', content)
    content = re.sub(r'stammt hauptsächlich', 'comes mainly', content)
    content = re.sub(r'stammt aus', 'comes from', content)
    content = re.sub(r'wird meist', 'is usually', content)
    content = re.sub(r'gibt es in verschiedenen', 'is available in various', content)
    content = re.sub(r'wird etwa', 'is approximately', content)
    content = re.sub(r'hat etwa', 'has approximately', content)
    content = re.sub(r'wurde ... entwickelt', 'was developed', content)

    # Pattern 7: Common German remainders
    content = re.sub(r'\bist\b', 'is', content)
    content = re.sub(r'\bsind\b', 'are', content)
    content = re.sub(r'\bhat\b', 'has', content)
    content = re.sub(r'\bhaben\b', 'have', content)
    content = re.sub(r'\bwird\b', 'is', content)
    content = re.sub(r'\bwerden\b', 'are', content)
    content = re.sub(r'\bwurde\b', 'was', content)
    content = re.sub(r'\bwurden\b', 'were', content)
    content = re.sub(r'\bist\b', 'is', content)

    # Pattern 8: "or" in wrong contexts
    content = re.sub(r'\bor Dark Grade\b', 'or Dark grade', content)

    # Pattern 9: Fix "als Alternative zu" -> "as an alternative to"
    content = re.sub(r'\bals Alternative zu\b', 'as an alternative to', content)

    # Pattern 10: Fix "statt" -> "instead of"
    content = re.sub(r'\bstatt\b', 'instead of', content)

    # Pattern 11: Fix "zu" in certain contexts
    content = re.sub(r'zu verleihen', 'to impart', content)
    content = re.sub(r'zu Bourbon', 'with bourbon', content)
    content = re.sub(r'zu finden', '', content)  # Remove "zu finden"

    # Pattern 12: Fix remaining German words in common phrases
    content = re.sub(r'\bdie\b', 'the', content)
    content = re.sub(r'\bder\b', 'the', content)
    content = re.sub(r'\bdas\b', 'the', content)
    content = re.sub(r'\bden\b', 'the', content)
    content = re.sub(r'\bdem\b', 'the', content)
    content = re.sub(r'\beim\b', 'a', content)
    content = re.sub(r'\beiner\b', 'a', content)
    content = re.sub(r'\beinem\b', 'a', content)
    content = re.sub(r'\beinen\b', 'a', content)

    # Pattern 13: Fix compound German words still remaining
    content = re.sub(r'Zuckerahorn-Baums', 'sugar maple tree', content)
    content = re.sub(r'Qualitätsstufen', 'quality grades', content)
    content = re.sub(r'Zuckergehalt', 'sugar content', content)
    content = re.sub(r'Geschmack', 'taste', content)
    content = re.sub(r'karamelligen', 'caramel-like', content)
    content = re.sub(r'holzigen', 'woody', content)
    content = re.sub(r'nussigen', 'nutty', content)
    content = re.sub(r'Noten', 'notes', content)
    content = re.sub(r'dickflüssiger', 'thicker', content)
    content = re.sub(r'einfacher', 'simple', content)
    content = re.sub(r'Zuckersirup', 'sugar syrup', content)
    content = re.sub(r'dunklen', 'dark', content)
    content = re.sub(r'Spirituosen', 'spirits', content)
    content = re.sub(r'vielen Rezepten', 'many recipes', content)
    content = re.sub(r'kann', 'can', content)
    content = re.sub(r'ausgetauscht', 'exchanged', content)
    content = re.sub(r'ausgetauscht werden', 'be exchanged', content)
    content = re.sub(r'Herbstliche', 'Autumn', content)

    # Pattern 14: Fix specific ingredient file issues
    content = re.sub(r'kohlensäurehaltiges', 'carbonated', content)
    content = re.sub(r'Erfrischungsgetränk', 'refreshing drink', content)
    content = re.sub(r'aromatisiert wird', 'is aromatized', content)
    content = re.sub(r'Rinde des', 'bark of the', content)
    content = re.sub(r'Chinarindenbaums', 'cinchona tree', content)
    content = re.sub(r'bitteren', 'bitter', content)
    content = re.sub(r'britischen', 'British', content)
    content = re.sub(r'Kolonien', 'colonies', content)
    content = re.sub(r'getrunken', 'drunk', content)
    content = re.sub(r'um Malaria vorzubeugen', 'to prevent malaria', content)
    content = re.sub(r'gemildert', 'mitigated', content)
    content = re.sub(r'zur Geburt des', 'to the birth of the', content)
    content = re.sub(r'führte', 'led', content)
    content = re.sub(r'enthält', 'contains', content)
    content = re.sub(r'weniger', 'less', content)
    content = re.sub(r'historische', 'historical', content)
    content = re.sub(r'Versionen', 'versions', content)
    content = re.sub(r'immer noch', 'still', content)
    content = re.sub(r'erkennbar', 'noticeably', content)
    content = re.sub(r'viele', 'many', content)
    content = re.sub(r'günstigem', 'cheap', content)
    content = re.sub(r'Supermarkt-Tonic', 'supermarket tonic', content)
    content = re.sub(r'Premium-Marken', 'premium brands', content)
    content = re.sub(r'wie', 'such as', content)
    content = re.sub(r'haben oft', 'often have', content)
    content = re.sub(r'komplexere', 'more complex', content)
    content = re.sub(r'Aromen', 'flavors', content)
    content = re.sub(r'Zitrusnoten', 'citrus notes', content)
    content = re.sub(r'Kräutern', 'herbs', content)
    content = re.sub(r'Gewürzen', 'spices', content)
    content = re.sub(r'variiert stark', 'varies greatly', content)
    content = re.sub(r'Light- and Zero-Varianten', 'light and zero variants', content)
    content = re.sub(r'Grundlage für alle', 'basis for all', content)
    content = re.sub(r'Variationen', 'variations', content)
    content = re.sub(r'auch für andere', 'also for other', content)
    content = re.sub(r'Highballs', 'highballs', content)
    content = re.sub(r'verwendet', 'used', content)
    content = re.sub(r'Wahl des', 'choice of', content)
    content = re.sub(r'Tonics beeinflusst', 'tonic influences', content)
    content = re.sub(r'Drink massiv', 'drink significantly', content)
    content = re.sub(r'verschiedene Marken', 'different brands', content)
    content = re.sub(r'um deinen', 'to find your', content)
    content = re.sub(r'Favoriten', 'favorite', content)

    # Pattern 15: Fix Tabasco file
    content = re.sub(r'scharfe Chilisauce aus', 'hot chili sauce made from', content)
    content = re.sub(r'fermentierten', 'fermented', content)
    content = re.sub(r'Tabasco-Chilis', 'Tabasco chilies', content)
    content = re.sub(r'Essig', 'vinegar', content)
    content = re.sub(r'Salz', 'salt', content)
    content = re.sub(r'von Edmund McIlhenny', 'by Edmund McIlhenny', content)
    content = re.sub(r'entwickelt', 'developed', content)
    content = re.sub(r'heute weltweit', 'now worldwide', content)
    content = re.sub(r'bekannteste', 'best known', content)
    content = re.sub(r'Hot Sauce', 'hot sauce', content)
    content = re.sub(r'Sauce hat etwa', 'sauce has approximately', content)
    content = re.sub(r'Scoville', 'Scoville', content)
    content = re.sub(r'mittelscharfe Schärfe', 'medium heat', content)
    content = re.sub(r'würzig-sauren', 'spicy-sour', content)
    content = re.sub(r'charakteristische thin', 'characteristic thin', content)
    content = re.sub(r'spritzfähige', 'sprayable', content)
    content = re.sub(r'Konsistenz', 'consistency', content)
    content = re.sub(r'verschiedenen Varianten', 'various variants', content)
    content = re.sub(r'Original Red', 'Original Red', content)
    content = re.sub(r'Green Jalapeño', 'Green Jalapeño', content)
    content = re.sub(r'Chipotle', 'Chipotle', content)
    content = re.sub(r'Habanero', 'Habanero', content)
    content = re.sub(r'mehr', 'more', content)
    content = re.sub(r'klassische', 'classic', content)
    content = re.sub(r'herzhaften', 'savory', content)
    content = re.sub(r'um Schärfe', 'to add heat', content)
    content = re.sub(r'Komplexität', 'complexity', content)
    content = re.sub(r'Dosierung erfolgt', 'Dosage is done', content)
    content = re.sub(r'Dashes', 'dashes', content)
    content = re.sub(r'Spritzern', 'dashes', content)
    content = re.sub(r'wenige drops', 'a few drops', content)
    content = re.sub(r'reichen', 'are enough', content)
    content = re.sub(r'passe nach', 'adjust to', content)
    content = re.sub(r'an\.', 'accordingly.', content)
    content = re.sub(r'Zu viel', 'Too much', content)
    content = re.sub(r'dominiert', 'dominates', content)
    content = re.sub(r'gesamten', 'entire', content)

    # Pattern 16: Fix common German phrases
    content = re.sub(r'Beginne with', 'Start with', content)
    content = re.sub(r'Probiere', 'Try', content)

    # Save if changed
    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return 1
    return 0

def main():
    fixed = 0

    # Fix ingredient files (these have the most issues)
    print("Fixing ingredient files...")
    for root, dirs, files in os.walk('Zutaten'):
        for file in files:
            if file.endswith('.md'):
                if fix_file(Path(root) / file):
                    fixed += 1

    # Also check cocktail files
    print("Checking cocktail files...")
    for file in Path('Cocktails').glob('*.md'):
        if fix_file(file):
            fixed += 1

    print(f"\n✓ Fixed {fixed} files with grammar issues")

if __name__ == '__main__':
    main()
