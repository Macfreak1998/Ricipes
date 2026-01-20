#!/usr/bin/env python3
"""
Fix broken English from automated German->English conversion.
The automated conversion did word-by-word replacement, creating grammatically incorrect English.
"""

import os
import re
from pathlib import Path

# Grammar fixes for common broken patterns
GRAMMAR_FIXES = [
    # "is ein" -> "is a"
    (r'\bis ein\b', 'is a'),
    (r'\bis eine\b', 'is a'),
    (r'\bis der\b', 'is the'),
    (r'\bis die\b', 'is the'),
    (r'\bis das\b', 'is the'),

    # "hat ein" -> "has a"
    (r'\bhat ein\b', 'has a'),
    (r'\bhat eine\b', 'has a'),
    (r'\bhat einen\b', 'has a'),

    # "wird in" -> "is used in" / "is added in"
    (r'\bwird in\b', 'is used in'),
    (r'\bwird mit\b', 'is mixed with'),
    (r'\bwird durch\b', 'is made by'),

    # "with Zucker" -> "with sugar"
    (r'\bwith Zucker\b', 'with sugar'),
    (r'\bwith Salz\b', 'with salt'),
    (r'\bwith Essig\b', 'with vinegar'),

    # "and einem" -> "and a"
    (r'\band einem\b', 'and a'),
    (r'\band einer\b', 'and a'),
    (r'\band einen\b', 'and a'),
    (r'\band dem\b', 'and the'),
    (r'\band der\b', 'and the'),

    # "until zu" -> "up to"
    (r'\buntil zu\b', 'up to'),
    (r'\buntil Very\b', 'to Very'),

    # "or Dark" -> "or Dark"  (already correct)
    # "on Gin-Basis" -> "on a gin base"
    (r'\bon ([\w-]+)-Basis\b', r'on a \1 base'),

    # "in 19." -> "in the 19th"
    (r'\bin (\d+)\.\b', r'in the \1th'),

    # "als Alternative zu" -> "as an alternative to"
    (r'\bals Alternative zu\b', 'as an alternative to'),
    (r'\bals\b(?! an| a)', 'as'),

    # "nach Geschmack" -> "to taste"
    (r'\bnach Geschmack\b', 'to taste'),

    # "zu viel" -> "too much"
    (r'\bzu viel\b', 'too much'),

    # "etwa" -> "about" / "approximately"
    (r'\betwa\b', 'approximately'),

    # "meist" -> "usually" / "mostly"
    (r'\bmeist\b', 'usually'),

    # "auch" -> "also"
    (r'\bauch\b', 'also'),

    # "nur" -> "only"
    (r'\bnur\b', 'only'),

    # "sehr" -> "very"
    (r'\bsehr\b', 'very'),

    # "weniger" -> "less"
    (r'\bweniger\b', 'less'),

    # "mehr" -> "more"
    (r'\bmehr\b', 'more'),

    # "über" -> "over"
    (r'\büber\b', 'over'),

    # "für" -> "for"
    (r'\bfür\b', 'for'),

    # "aus" -> "from"
    (r'\baus\b', 'from'),

    # "von" -> "from" / "of"
    (r'\bvon\b', 'from'),

    # "bei" -> "at" / "with"
    (r'\bbei\b', 'at'),

    # "da sie" -> "as they" / "since they"
    (r'\bda sie\b', 'as they'),
    (r'\bda er\b', 'as it'),

    # "wenn" -> "when" / "if"
    (r'\bwenn\b', 'when'),

    # "alle" -> "all"
    (r'\balle\b', 'all'),

    # "beiden" -> "both"
    (r'\bbeeiden\b', 'both'),

    # "anderen" -> "other"
    (r'\banderen\b', 'other'),

    # "verschiedenen" -> "various"
    (r'\bverschiedenen\b', 'various'),

    # "können" -> "can"
    (r'\bkönnen\b', 'can'),

    # "werden" -> "are" / "become"
    (r'\bwerden\b', 'are'),

    # "wurde" -> "was"
    (r'\bwurde\b', 'was'),

    # "wurden" -> "were"
    (r'\bwurden\b', 'were'),

    # "gibt es" -> "there are"
    (r'\bgibt es\b', 'there are'),

    # "es gibt" -> "there are"
    (r'\bes gibt\b', 'there are'),

    # "enthält" -> "contains"
    (r'\benthält\b', 'contains'),

    # "verleiht" -> "gives" / "imparts"
    (r'\bverleiht\b', 'gives'),

    # "eignet sich" -> "is suitable"
    (r'\beignet sich\b', 'is suitable'),

    # "passt" -> "fits" / "goes well"
    (r'\bpasst besonders gut\b', 'goes particularly well'),
    (r'\bpasst\b', 'pairs'),

    # "stammt" -> "comes from"
    (r'\bstammt hauptsächlich\b', 'comes mainly'),
    (r'\bstammt\b', 'comes from'),

    # "can Maple Syrup" -> "Maple Syrup can"
    (r'\bcan ([\w\s]+) ausgetauscht werden\b', r'\1 can be exchanged'),

    # "passe...an" -> "adjust to"
    (r'\bpasse\b', 'adjust'),
    (r'\ban\.\b', 'accordingly.'),

    # "Beginne with" -> "Start with"
    (r'\bBeginne with\b', 'Start with'),

    # "Probiere" -> "Try"
    (r'\bProbiere\b', 'Try'),

    # "um deinen" -> "to find your"
    (r'\bum deinen\b', 'to find your'),

    # "zu finden" -> (already handled)
    (r'\bzu finden\b', ''),

    # "beeinflusst den" -> "influences the"
    (r'\bbeeinflusst den\b', 'influences the'),

    # "massiv" -> "significantly"
    (r'\bmassiv\b', 'significantly'),

    # "entwickelt" -> "develops"
    (r'\bentwickelt\b', 'develops'),

    # "reicht" -> "is sufficient"
    (r'\breicht meist\b', 'is usually sufficient'),

    # "zwischen" -> "between"
    (r'\bzwischen\b', 'between'),

    # "während" -> "during"
    (r'\bwährend\b', 'during'),

    # "langsam" -> "slowly"
    (r'\blangsam\b', 'slowly'),

    # "deutlich" -> "significantly"
    (r'\bdeutlich\b', 'significantly'),

    # "stark" -> "strongly"
    (r'\bstark\b', 'strongly'),

    # "variiert" -> "varies"
    (r'\bvariiert\b', 'varies'),

    # "verwendet werden" -> "be used"
    (r'\bverwendet werden\b', 'be used'),

    # "verwendet" -> "used"
    (r'\bverwendet\b', 'used'),

    # "beliebter" -> "popular"
    (r'\bbeliebter\b', 'popular'),

    # "unverzichtbar" -> "indispensable"
    (r'\bunverzichtbar\b', 'indispensable'),

    # "authentische" -> "authentic"
    (r'\bauthentische\b', 'authentic'),

    # "klassische" -> "classic"
    (r'\bklassische\b', 'classic'),

    # "klassischen" -> "classic"
    (r'\bklassischen\b', 'classic'),

    # "häufiger" -> "more frequently"
    (r'\bhäufiger\b', 'more frequently'),

    # "seltener" -> "less frequently"
    (r'\bseltener\b', 'less frequently'),

    # "weltweit" -> "worldwide"
    (r'\bweltweit\b', 'worldwide'),

    # "bekannteste" -> "most well-known"
    (r'\bbekannteste\b', 'most well-known'),

    # "hervorragend" -> "excellent"
    (r'\bhervorragend\b', 'excellent'),

    # "perfekte" -> "perfect"
    (r'\bperfekte\b', 'perfect'),

    # "derselben" -> "the same"
    (r'\bderselben\b', 'the same'),

    # "harmonisch" -> "harmoniously"
    (r'\bharmonisch\b', 'harmoniously'),

    # "ergänzt" -> "complements"
    (r'\bergänzt\b', 'complements'),

    # "gewonnen wird" -> "is obtained"
    (r'\bgewonnen wird\b', 'is obtained'),

    # "eingeteil" -> "divided"
    (r'\beingeteilt\b', 'divided'),

    # "eingekochten" -> "boiled down"
    (r'\beingekochten\b', 'boiled down'),

    # "Saft" remaining -> "sap" / "juice"
    (r'\bSaft des\b', 'sap from'),

    # Fix remaining German compound words
    (r'\bZuckerahorn-Baums\b', 'sugar maple tree'),
    (r'\bZuckergehalt\b', 'sugar content'),
    (r'\bZuckersirup\b', 'sugar syrup'),
    (r'\bQualitätsstufen\b', 'quality grades'),
    (r'\bGeschmack\b', 'taste'),
    (r'\bSchlüsselzutat\b', 'key ingredient'),
    (r'\bKomplexität\b', 'complexity'),
    (r'\bTiefe\b', 'depth'),
    (r'\bWürze\b', 'spice'),
    (r'\bWahl\b', 'choice'),
    (r'\bRezepten\b', 'recipes'),
    (r'\bDosierung\b', 'Dosage'),
    (r'\bSpritzern\b', 'dashes'),
    (r'\bKonsistenz\b', 'consistency'),
    (r'\bGrundlage\b', 'basis'),
    (r'\bVariationen\b', 'variations'),
    (r'\bVarianten\b', 'variants'),
    (r'\bMischung\b', 'mixture'),
    (r'\bGewürzen\b', 'spices'),
    (r'\bZwiebeln\b', 'onions'),
    (r'\bEichenfässern\b', 'oak barrels'),
    (r'\bfermentiert\b', 'fermented'),
    (r'\bFruchtlikör\b', 'fruit liqueur'),
    (r'\bSchlehenbeeren\b', 'sloe berries'),
    (r'\bEinlegen\b', 'infusion'),
    (r'\beingelegt\b', 'infused'),
    (r'\bgesüßt\b', 'sweetened'),
    (r'\bNoten\b', 'notes'),
    (r'\bMandel\b', 'almond'),
    (r'\bKirsche\b', 'cherry'),
    (r'\bPflaume\b', 'plum'),
    (r'\bWacholder-Würze\b', 'juniper spice'),
    (r'\btiefrote\b', 'deep red'),
    (r'\bFarbe\b', 'color'),
    (r'\bMarken\b', 'brands'),
    (r'\bCraft Cocktail Szene\b', 'craft cocktail scene'),
    (r'\bErsatz\b', 'substitute'),
    (r'\bErgänzung\b', 'addition'),
    (r'\bfruchtig-süße\b', 'fruity-sweet'),
    (r'\bhinzuzufügen\b', 'to add'),
    (r'\bHaupttypen\b', 'main types'),
    (r'\bPfirsichbrand\b', 'peach brandy'),
    (r'\bPfirsichen\b', 'peaches'),
    (r'\bfermentierten\b', 'fermented'),
    (r'\bdestilliert\b', 'distilled'),
    (r'\bNeutralalkohol\b', 'neutral alcohol'),
    (r'\bPfirsichextrakt\b', 'peach extract'),
    (r'\btrocken\b', 'dry'),
    (r'\bintensiv pfirsichig\b', 'intensely peachy'),
    (r'\bproduziert\b', 'produced'),
    (r'\bsüßer\b', 'sweeter'),
    (r'\bangereichert\b', 'enriched'),
    (r'\bVersion\b', 'version'),
    (r'\bCocktailrezepten\b', 'cocktail recipes'),
    (r'\baromatisch-fruchtig\b', 'aromatic-fruity'),
    (r'\breifen\b', 'ripe'),
    (r'\bPfirsichnoten\b', 'peach notes'),
    (r'\bmanchmal\b', 'sometimes'),
    (r'\bMandeltönen\b', 'almond tones'),
    (r'\bPfirsichkernen\b', 'peach pits'),
    (r'\bGängige\b', 'Common'),
    (r'\bBestandteil\b', 'component'),
    (r'\bklassischer Ära\b', 'classic era'),
    (r'\bersetzt\b', 'replaced'),
    (r'\bHinweis\b', 'Note'),
    (r'\bmodernen\b', 'modern'),
    (r'\bfunktionieren ähnlich\b', 'function similarly'),
    (r'\bteil\b', 'part'),
    (r'\bHühnereis\b', 'chicken egg'),
    (r'\bCocktailswird\b', 'In cocktails, it is'),
    (r'\breichhaltige\b', 'rich'),
    (r'\bcremige\b', 'creamy'),
    (r'\bTextur\b', 'texture'),
    (r'\bweichen\b', 'soft'),
    (r'\bsamtigen\b', 'velvety'),
    (r'\bMundgefühl\b', 'mouthfeel'),
    (r'\bzu erzeugen\b', 'to create'),
    (r'\bAnders\b', 'Unlike'),
    (r'\bEiweiß\b', 'egg white'),
    (r'\bSchaum\b', 'foam'),
    (r'\bsorgt\b', 'provides'),
    (r'\bKörper\b', 'body'),
    (r'\bRückhaltigkeit\b', 'richness'),
    (r'\bseidige\b', 'silky'),
    (r'\bLecithin\b', 'lecithin'),
    (r'\bnatürlicher\b', 'natural'),
    (r'\bEmulgator\b', 'emulsifier'),
    (r'\bwirkt\b', 'acts'),
    (r'\bmilden\b', 'mild'),
    (r'\bleicht süßlichen\b', 'slightly sweet'),
    (r'\bdominiert\b', 'dominates'),
    (r'\bcremig-dick\b', 'creamy-thick'),
    (r'\bähnlich\b', 'similar'),
    (r'\bSicherheit\b', 'Safety'),
    (r'\bVerwende\b', 'Use'),
    (r'\bfrisch\b', 'fresh'),
    (r'\bguter Qualität\b', 'good quality'),
    (r'\bBedenken\b', 'concerns'),
    (r'\bwegen\b', 'about'),
    (r'\brohem\b', 'raw'),
    (r'\bkannst du\b', 'you can'),
    (r'\bpasteurisiertes\b', 'pasteurized'),
    (r'\bverwenden\b', 'use'),
    (r'\bklassisch\b', 'classically'),
    (r'\bFlips\b', 'flips'),
    (r'\bNogs\b', 'nogs'),
    (r'\breichhaltigen\b', 'rich'),
    (r'\bDessert-Cocktails\b', 'dessert cocktails'),
    (r'\bTechnik\b', 'Technique'),
    (r'\bDas\b', 'The'),
    (r'\bmit den\b', 'with the'),
    (r'\bZutaten\b', 'ingredients'),
    (r'\bkräftig\b', 'vigorously'),
    (r'\bgeshakt\b', 'shaken'),
    (r'\bempfohlen\b', 'recommended'),
    (r'\bvollständig\b', 'completely'),
    (r'\bzu emulgieren\b', 'to emulsify'),
]

def fix_grammar_in_file(file_path):
    """Fix broken English grammar in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='latin-1') as f:
                content = f.read()
        except:
            return 0

    original_content = content
    fixes_made = 0

    # Apply all grammar fixes
    for pattern, replacement in GRAMMAR_FIXES:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            fixes_made += content.count(pattern)
            content = new_content

    # Write back if changed
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return fixes_made

    return 0

def main():
    # Fix cocktails
    cocktails_dir = Path('Cocktails')
    ingredients_dir = Path('Zutaten')

    total_fixes = 0
    files_fixed = 0

    print("Fixing broken English in cocktail recipes...")
    for file_path in cocktails_dir.glob('*.md'):
        fixes = fix_grammar_in_file(file_path)
        if fixes > 0:
            files_fixed += 1
            total_fixes += fixes

    print("Fixing broken English in ingredient files...")
    for root, dirs, files in os.walk(ingredients_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = Path(root) / file
                fixes = fix_grammar_in_file(file_path)
                if fixes > 0:
                    files_fixed += 1
                    total_fixes += fixes

    print(f"\n✓ Grammar fixes complete!")
    print(f"✓ Files modified: {files_fixed}")
    print(f"✓ Total fixes applied: {total_fixes}")

if __name__ == '__main__':
    main()
