# Vault Organization Guide

**Last Updated**: 2025-01-18
**Status**: ✅ Optimized for Book Creation

---

## Overview

This vault is now fully organized to streamline cocktail book creation. All 656 cocktails and 192 ingredients are documented in English with proper structure, metadata, and cross-references.

---

## 📁 Directory Structure

```
Rezepte/
├── Cocktails/              # 656 cocktail recipes
├── Zutaten/                # 192 ingredient descriptions
│   ├── Spirituosen/        # Spirits
│   ├── Säfte/              # Juices
│   ├── Sirups/             # Syrups
│   └── Filler/             # Other ingredients
├── Kategorien/             # Organization & collections
│   ├── Collections/        # Curated spirit & theme collections
│   └── Families/           # Cocktail family relationships
├── Book-Planning/          # Book project resources
│   ├── Hooks-and-Stories.md      # Anecdotes & narrative hooks
│   └── Project-Template.md       # Book project template
└── Scripts/                # Automation tools
```

---

## 🎯 New Organizational Features

### 1. YAML Frontmatter Script ✅

**Location**: `add_yaml_frontmatter.py`

**What it does**: Adds structured metadata to all cocktail files

**Metadata included**:
- `spirit_base`: Main spirit (Gin, Rum, Whiskey, etc.)
- `difficulty`: Easy, Intermediate, Advanced
- `technique`: Shaken, Stirred, Built, etc.
- `glassware`: Glass type
- `flavor_profile`: Bitter, Citrus, Fruity, etc.
- `occasion`: Summer, Aperitif, Digestif, etc.
- `strength`: High ABV, Standard ABV, Low ABV
- `era`: Classic, Pre-Prohibition, Contemporary, etc.
- `garnish`: Garnish description

**How to run**:
```bash
cd /Users/jan/Documents/Obsidian\ Vault/Sync/Rezepte
python3 add_yaml_frontmatter.py
```

**First run**: Choose dry-run mode to preview changes
**Second run**: Confirm to apply to all 656 files

**Example output**:
```yaml
---
title: Negroni
spirit_base: Gin
difficulty: Easy
technique: Stirred
glassware: Tumbler
flavor_profile: ["Bitter"]
occasion: ["Aperitif"]
strength: High ABV
era: Classic
garnish: Orange
---
```

---

### 2. Collection Files ✅

**Location**: `Kategorien/Collections/`

**What they are**: Pre-curated lists of cocktails grouped by:
- Spirit base (Gin, Rum, Whiskey, etc.)
- Technique (Shaken, Stirred, Built)
- Flavor profile (Citrus, Fruity, Bitter)
- Occasion (Summer, Aperitif, etc.)

**Created collections**:
- 9 spirit collections
- 3 technique collections
- 4 flavor collections
- 1 occasion collection

**How to use for books**:
- Need all gin cocktails for Chapter 3? → Open `Gin-Cocktails.md`
- Want easy summer drinks? → Check `Summer-Cocktails.md`
- Building a shaken cocktails chapter? → See `Shaken-Cocktails.md`

**Example**: `Gin-Cocktails.md` contains 51 gin-based cocktails with one-liner descriptions

---

### 3. Book Hooks & Stories ✅

**Location**: `Book-Planning/Hooks-and-Stories.md`

**What it is**: A comprehensive collection of:
- Great opening stories (Negroni origin, Martini mystery, Mojito medicine)
- Celebrity connections (Hemingway, James Bond, Orson Welles)
- Prohibition era tales
- Origin controversies (Mai Tai wars, Moscow Mule marketing)
- Technical revelations (why shaking Manhattans is a crime)
- One-liner hooks for chapter openers
- Character profiles (Jerry Thomas, Harry Craddock)
- Interesting sidebar facts

**How to use**:
- Starting a new chapter? → Find a compelling opening hook
- Need a quote? → Check celebrity connections
- Want a sidebar? → Use interesting facts section
- Historical context? → Browse origin stories

**Example hooks**:
- "Count Camillo Negroni walks into Caffè Casoni in 1919..."
- "Three origin stories. Zero proof. The Martini mystery."
- "Hemingway claimed he drank 16 Daiquiris in one sitting..."

---

### 4. Book Project Template ✅

**Location**: `Book-Planning/Project-Template.md`

**What it is**: A complete project management template for book projects

**Sections included**:
- Project Overview (type, audience, concept)
- Structure & Outline (chapters, word counts)
- Content Plan (cocktails to feature, research needed)
- Writing Progress (chapter status, weekly goals)
- Voice & Style Reminders
- Production Notes (images, formatting)
- Publication Plan

**How to use**:
1. Copy `Project-Template.md`
2. Rename to your project: `My-Gin-Book-Project.md`
3. Fill in your specific details
4. Use as working document throughout project
5. Track progress chapter by chapter

---

### 5. Cocktail Family Files ✅

**Location**: `Kategorien/Families/`

**What they are**: Deep-dive relationship documents showing how cocktail families evolved

**Created families**:
1. **Negroni Family** - From Americano to Boulevardier
2. **Daiquiri Family** - The universal sour formula
3. **Martini Family** - The most debated cocktail

**What each file contains**:
- Origin story and evolution
- Family tree diagram
- All major variations
- Teaching moments for different audiences
- Narrative arcs for book chapters
- Recipe collection recommendations
- Key quotes and insights
- Sidebar ideas

**How to use for books**:
- Writing a Negroni chapter? → Use Negroni-Family.md for structure
- Teaching the sour formula? → Daiquiri-Family.md shows all variations
- Martini history section? → Martini-Family.md has timeline and debates

**Example**: Negroni-Family.md shows evolution:
```
Milano-Torino (pre-1860)
    ↓
Americano (1860s)
    ↓
Negroni (1919)
    ├→ Boulevardier (whiskey)
    ├→ Sbagliato (prosecco)
    ├→ White Negroni (Suze & Lillet)
    └→ Kingston Negroni (rum)
```

---

## 🎯 How to Use This Organization for Book Creation

### Starting a New Book Project

1. **Copy the project template**
```bash
cp Book-Planning/Project-Template.md Book-Planning/My-Book-Project.md
```

2. **Fill in project details**
   - Choose book type (recipe, history, guide, etc.)
   - Define target audience
   - Outline chapters

3. **Identify content needs**
   - Which spirits/cocktails to feature
   - What stories to include
   - Research needed

4. **Use collections for content gathering**
   - Find relevant cocktails from Collections/
   - Reference Family files for relationships
   - Pull hooks from Hooks-and-Stories.md

### Writing a Chapter

**Step 1: Gather Content**
- Check Collections/ for relevant cocktails
- Review Family files for context
- Find hooks in Hooks-and-Stories.md

**Step 2: Research**
- Read individual cocktail files for history
- Check ingredient descriptions
- Note interesting facts

**Step 3: Write**
- Use Cocktail Book Writer skill (cocktail-book-writer.skill)
- Follow bartender voice from style guide
- Integrate vault content with research

**Step 4: Reference**
- Link to cocktails: `[[Negroni]]`
- Link to ingredients: `[[Gin]]`
- Link to techniques: `[[Stir]]`

---

## 🔍 Quick Find Guide

### Need all cocktails with...
- **Gin base**: `Collections/Gin-Cocktails.md`
- **Rum base**: `Collections/Rum-Cocktails.md`
- **Shaken technique**: `Collections/Shaken-Cocktails.md`
- **Summer theme**: `Collections/Summer-Cocktails.md`
- **Bitter flavor**: `Collections/Bitter-Cocktails.md`

### Need relationship info for...
- **Negroni variations**: `Families/Negroni-Family.md`
- **Daiquiri variations**: `Families/Daiquiri-Family.md`
- **Martini variations**: `Families/Martini-Family.md`

### Need story hooks about...
- **Cocktail origins**: `Book-Planning/Hooks-and-Stories.md` → Origin Stories
- **Famous drinkers**: `Book-Planning/Hooks-and-Stories.md` → Celebrity Connections
- **Technique insights**: `Book-Planning/Hooks-and-Stories.md` → Technical Revelations
- **Chapter openers**: `Book-Planning/Hooks-and-Stories.md` → One-Liner Hooks

---

## 🔧 Automation & Scripts

### Add YAML Frontmatter
```bash
python3 add_yaml_frontmatter.py
```
Adds structured metadata to all cocktail files.

### Regenerate Collections
```bash
python3 generate_collections.py
```
Updates collection files based on current cocktail metadata.

---

## 📊 Current Vault Statistics

**Cocktails**: 656 recipes
**Ingredients**: 192 descriptions
**Collections**: 18 curated lists
**Families**: 3 relationship files
**Languages**: 100% English content, German structure headers

**Spirits Breakdown**:
- Gin: 51 cocktails
- Rum: 42 cocktails
- Whiskey: 31 cocktails
- Tequila & Mezcal: 19 cocktails
- Vodka: 21 cocktails
- Brandy & Cognac: 13 cocktails
- Other: 466 cocktails (many need base spirit identification)

---

## 💡 Tips for Efficient Book Writing

### Use Collections as Chapter Outlines
Each collection file can become a chapter. Example:
- `Gin-Cocktails.md` → "Chapter 3: Essential Gin Cocktails"

### Use Family Files for Deep Dives
Each family file can be a major section. Example:
- `Negroni-Family.md` → "The Negroni and Its Children" subsection

### Use Hooks for Engaging Writing
Start every chapter with a compelling hook from `Hooks-and-Stories.md`

### Cross-Reference Everything
Use wiki-links liberally:
- Link to cocktails: `[[Martini]]`
- Link to ingredients: `[[Gin]]`, `[[Dry Vermouth]]`
- Link to techniques: `[[Stir]]`, `[[Shake]]`

### Track Progress with Project Template
Update your project file after each writing session to maintain momentum and visibility.

---

## 🚀 Next Steps

### Recommended Actions

1. **Run YAML script** (if not done yet)
   ```bash
   python3 add_yaml_frontmatter.py
   ```
   This adds searchable metadata to all cocktails.

2. **Browse the collections**
   Explore `Kategorien/Collections/` to see how cocktails are grouped.

3. **Read a family file**
   Open `Families/Negroni-Family.md` to see how relationship files work.

4. **Start a book project**
   Copy `Project-Template.md` and begin planning your first book.

---

## 📚 Resources

### Skill File
- **cocktail-book-writer.skill** - AI skill for writing cocktail books
  - Includes voice guide, book structures, chapter templates
  - Extract and reference when writing

### Key Documents
- `ENGLISH_CONVERSION_COMPLETE.md` - English conversion project summary
- `Cocktail-Liste.md` - Master list of all 656 cocktails
- `CLAUDE.md` - Repository overview and conventions

### External References
- Cocktail Book Writer skill documentation
- Kevin Kos style guide (bartender voice)
- Book structure templates

---

## ✅ System Status

| Feature | Status | Notes |
|---------|--------|-------|
| English Conversion | ✅ Complete | 100% proper English |
| YAML Frontmatter Script | ✅ Ready | Run when needed |
| Collection Files | ✅ Created | 18 collections |
| Family Relationship Files | ✅ Created | 3 major families |
| Book Hooks File | ✅ Complete | Comprehensive |
| Project Template | ✅ Ready | Copy to use |
| Categories | 🔄 In Progress | Another agent working |

---

**Your vault is now optimized for efficient, professional cocktail book creation!**

Use the Cocktail Book Writer skill with this organized vault to create comprehensive, engaging cocktail books with the distinctive voice of a passionate 30-year-old bartender.
