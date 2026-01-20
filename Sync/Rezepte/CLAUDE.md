# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an Obsidian vault containing a German-language cocktail recipe collection. The vault uses Obsidian's wiki-link syntax (`[[link]]`) to create interconnected notes for recipes, ingredients, techniques, and serving details.

## Directory Structure

```
Rezepte/
├── Cocktails/          # Individual cocktail recipes (~165+ recipes)
├── Zutaten/            # Ingredients (organized by type)
│   ├── Spirituosen/    # Spirits (Gin, Vodka, Rum, etc.)
│   ├── Säfte/          # Juices (Limettensaft, Zitronensaft, etc.)
│   ├── Sirups/         # Syrups (Zuckersirup, etc.)
│   └── Filler/         # Fillers (Soda, etc.)
├── Techniken/          # Preparation techniques (Shake, Stir, Double Strain, etc.)
├── Gläser/             # Glassware types (Coupe, Tumbler, Highball)
├── Eis/                # Ice types (Straight, Crushed Ice, Würfel)
├── Deko/               # Garnishes (Zitronenzeste, Minzblatt, Limettenrad)
├── Tools/              # Bar tools
└── Vorlage.md          # Template for new recipes
```

## Recipe Structure

All cocktail recipes follow a standardized format defined in `Vorlage.md`:

```markdown
# Zutaten
- [quantity] [[ingredient_name]]

# Zubereitung
[[technique]]: ingredient1, ingredient2, ...
[[technique2]]

# Served
* Glas: [[glass_type]]
* Eis: [[ice_type]]
* Deko: [[garnish]]

# Kategorien
```

### Key Points:
- Ingredients use wiki-links: `[[Gin]]`, `[[Limettensaft]]`
- Quantities are in oz (standard cocktail measurements)
- Techniques are wiki-linked and comma-separated: `[[Shake]]: Gin, Zitronensaft, ...`
- All structural elements (glass, ice, garnishes) use wiki-links
- Language is German with some English cocktail names

## Common Operations

### Adding a New Cocktail Recipe
1. Create a new `.md` file in `Cocktails/` with the cocktail name
2. Copy the structure from `Vorlage.md`
3. Fill in ingredients with wiki-links: `[[ingredient_name]]`
4. Add preparation steps using technique wiki-links
5. Specify glass, ice, and decoration

### Adding a New Ingredient
1. Determine the correct subdirectory in `Zutaten/`:
   - Spirits → `Zutaten/Spirituosen/`
   - Juices → `Zutaten/Säfte/`
   - Syrups → `Zutaten/Sirups/`
   - Fillers → `Zutaten/Filler/`
2. Create a new `.md` file (most ingredient files are empty/placeholders)

### Git Operations
This vault uses automatic git backups with commit messages like "vault backup: YYYY-MM-DD HH:MM:SS". When making manual changes:
- Stage all changes: `git add .`
- Commit with descriptive message matching the pattern
- The main branch is `main`

## Obsidian-Specific Conventions

- **Wiki-links**: Use `[[Page Name]]` syntax for all cross-references
- **No aliases**: Links use exact file names without extensions
- **Flat hierarchies**: Most category folders contain simple placeholder files
- **Measurements**: Quantities are in oz (e.g., `2 [[Gin]]` = 2 oz of gin)

## German-English Terminology

- Zutaten = Ingredients
- Zubereitung = Preparation
- Served = Serving details
- Glas = Glass
- Eis = Ice
- Deko = Decoration/Garnish
- Spirituosen = Spirits
- Säfte = Juices
- Sirups = Syrups

## Notes for AI Assistants

- Maintain the wiki-link structure when editing recipes
- Preserve the exact section headers from `Vorlage.md`
- Most technique, ingredient, and glass files are empty placeholders—this is intentional
- When creating new recipes, ensure all ingredients and techniques exist as files or create them
- Keep cocktail names in their original language (often English even in this German vault)
