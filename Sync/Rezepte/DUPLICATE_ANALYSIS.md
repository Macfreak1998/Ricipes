# Ingredient Files - Duplicate and Error Analysis

**Total Files:** 289
**Date:** 2025-11-10

---

## 1. FILES STARTING WITH MEASUREMENTS (Should be removed or renamed)

These files contain measurements in the filename and should reference the actual ingredient instead:

### Bitters/Drops
- `Dashes  Bogart's Bitters.md` → Should use `[[Bitters]]` with quantity in recipe
- `Dashes Angostura Bitters.md` → Should use `[[Angostura Bitters]]`
- `dashes Angostura Aromatic Bitters.md` → Should use `[[Angostura Bitters]]`
- `Dashes of Angostura Bitters.md` → Should use `[[Angostura Bitters]]`
- `Dashes Angustrora Bitters.md` → TYPO + measurement → `[[Angostura Bitters]]`
- `Dashes Bitters.md` → Should use `[[Bitters]]`
- `Dashes Chocolate Bitters.md` → Create `[[Chocolate Bitters]]`
- `Dashes Orange Bitters.md` → Should use `[[Orange Bitters]]`
- `Drops Absinthe.md` → Should use `[[Absinthe]]`
- `drops of Pernod.md` → Create `[[Pernod]]`
- `Drops Saline Solution.md` → Create `[[Saline Solution]]`
- `Drops Saline.md` → Create `[[Saline Solution]]`
- `Heavy Top Angostura Bitters.md` → Should use `[[Angostura Bitters]]`

### Quantity-based Names
- `bar spoons cold soda water.md` → Should use `[[Soda Water]]`
- `Layer 1.5 Dark Rum.md` → Should use `[[Dark Rum]]`
- `of Benedictine.md` → Should use `[[Benedictine]]`
- `soda water Approx. 2oz.md` → Should use `[[Soda Water]]`
- `Tsp Simple Syrup.md` → Should use `[[Simple Syrup]]`
- `tsp Gold's Horseradish.md` → Create `[[Horseradish]]`
- `tsp Hot Sauce.md` → Create `[[Hot Sauce]]`
- `tsp Spice Mix.md` → Should use `[[Spice Mix]]`

### Portioning Words
- `Part Cayenne Pepper.md` → Create `[[Cayenne Pepper]]`
- `Part Paprika.md` → Create `[[Paprika]]`
- `Parts Garlic Powder.md` → Create `[[Garlic Powder]]`
- `Parts Garlic Salt.md` → Create `[[Garlic Salt]]`
- `Slices Cucumber.md` → Create `[[Cucumber]]`
- `Quartered Limes.md` → Should use `[[Lime]]`
- `Lime Quartered.md` → Should use `[[Lime]]`
- `Lime Quarters.md` → Should use `[[Lime]]`
- `Lemon wedges.md` → Should use `[[Lemon]]`
- `Lemon,Lime and Orange Wedge.md` → Delete (use individual ingredients)

### Preparation States
- `Crushed Eis.md` → Move to `Eis/` folder as ice type
- `Cucumber Slices.md` → Should use `[[Cucumber]]`
- `Garnish 3 Brandied Cherries.md` → Create `[[Brandied Cherries]]` in Deko folder
- `mint leaves.md` → Create proper `[[Mint]]` or `[[Fresh Mint]]`
- `thin slices of red chilli.md` → Create `[[Red Chilli]]`
- `Small Stick of Rosmary.md` → Create `[[Rosemary]]` (note spelling)

### Special Cases
- `with Prosecco.md` → Should use `[[Prosecco]]`

---

## 2. TYPOS AND SPELLING ERRORS

| Current (Wrong) | Correct | Action |
|----------------|---------|---------|
| `Angustora Bitters.md` | `Angostura Bitters.md` | Rename/merge |
| `Apricot Liqor.md` | `Apricot Liqueur.md` | Rename/merge |
| `Champage.md` | `Champagne.md` | Rename/merge |
| `Cognag.md` | `Cognac.md` | Rename/merge |
| `Cramberry Juice.md` | `Cranberry Juice.md` | Rename/merge |
| `Dark RUm.md` | Should be `Dark Rum.md` | Fix capitalization |
| `Demarara Rum.md` | `Demerara Rum.md` | Rename/merge |
| `Green Chartruse.md` | `Green Chartreuse.md` | Rename/merge |
| `Grendaine.md` | `Grenadine.md` | Rename/merge |
| `Lime Juce.md` | `Lime Juice.md` | Rename/merge |
| `Luxado Cherrys.md` | `Luxardo Cherries.md` | Rename/merge |
| `Passion Fruit Syup.md` | `Passion Fruit Syrup.md` | Rename/merge |
| `Peach Purre.md` | `Peach Puree.md` | Rename |
| `Represado Tequila.md` | `Reposado Tequila.md` | Rename/merge |
| `Rhum Agricol.md` | `Rhum Agricole.md` | Rename/merge |
| `Tequilla.md` | `Tequila.md` | Rename/merge |
| `Tripple Sec.md` | `Triple Sec.md` | Rename/merge |
| `Vosdka.md` | `Vodka.md` | Rename/merge |
| `Wallnut Liquor.md` | `Walnut Liqueur.md` | Rename (liqueur not liquor) |
| `Eiweiss.md` | Keep as German OR use `Egg White.md` | Decide language |

---

## 3. DUPLICATE INGREDIENTS (Consolidation Needed)

### Absinthe Family
**Files:** `Absinth.md`, `Absinthe.md`, `Absinth Spray.md`, `Absinthe Spray.md`, `Absinthe Rinse.md`
**Recommendation:**
- Keep: `Absinthe.md` (English standard)
- Delete: `Absinth.md` (German variant)
- Merge spray/rinse into: `Absinthe.md` (these are just preparation methods)

### Agave Syrup
**Files:** `Agave Sirup.md`, `Agave Syrup.md`, `Agavensirup.md`
**Recommendation:** Keep `Agave Syrup.md`, delete others

### Angostura Bitters
**Files:** `Angostura.md`, `Angostura Bitters.md`, `Angustora Bitters.md`, plus 5 measurement-based files
**Recommendation:** Keep only `Angostura Bitters.md`

### Apricot Liqueur
**Files:** `Apricot Brandy.md`, `Apricot Liqor.md`, `Apricot Liqueur.md`
**Recommendation:** Keep `Apricot Liqueur.md` (modern standard)

### Benedictine
**Files:** `Benedictine.md`, `DOM Benedictine.md`
**Recommendation:** Keep `Benedictine.md` (DOM is just the label)

### Bourbon
**Files:** `Bourbon.md`, `Bourbon Whiskey.md`, `Bonded Bourbon.md`
**Recommendation:**
- Keep: `Bourbon.md` (general)
- Keep: `Bonded Bourbon.md` (specific type - 100 proof, different flavor)
- Delete: `Bourbon Whiskey.md` (redundant)

### Cachaça
**Files:** `Cachaca.md`
**Recommendation:** Rename to `Cachaça.md` (proper Portuguese spelling with cedilla)

### Champagne
**Files:** `Champage.md`, `Champagne.md`
**Recommendation:** Keep `Champagne.md`, delete typo

### Coconut Products
**Files:** `Coconut Cream.md`, `Coconut Creme.md`, `Cream of Coconut.md`, `Coconut Milk.md`
**Recommendation:**
- Keep: `Coconut Cream.md` (thick, for piña coladas)
- Keep: `Coconut Milk.md` (thinner, different product)
- Delete: `Coconut Creme.md` (spelling variant)
- Note: "Cream of Coconut" is sweetened (Coco López), different from coconut cream

### Coffee Liqueur
**Files:** `Coffee Liqueur.md`, `Coffee Liquor.md`
**Recommendation:** Keep `Coffee Liqueur.md` (correct spelling)

### Cognac
**Files:** `Cognac.md`, `Cognac VSOP.md`, `Cognag.md`
**Recommendation:**
- Keep: `Cognac.md`
- Keep: `Cognac VSOP.md` (specific age designation)
- Delete: `Cognag.md` (typo)

### Cranberry Juice
**Files:** `Cramberry Juice.md`, `Cranberry Juice.md`
**Recommendation:** Keep `Cranberry Juice.md`, delete typo

### Cream
**Files:** `Cream.md`, `Heavy Cream.md`, `Cold Heavy Cream.md`
**Recommendation:** Keep `Heavy Cream.md`, delete others (temperature is preparation)

### Crème de Cacao
**Files:** `Creme de Cacao White.md`, also exists: `Creme de Menthe White.md`
**Note:** These are correct - white/green are different products

### Curaçao
**Files:** `Curacao.md`, `Dry Curacao.md`, `Orange Curacao.md`, `Blue Curacao.md`
**Recommendation:** Keep all (different types with different flavors/colors)

### Dark Jamaican Rum
**Files:** `Dark Jamaica Rum.md`, `Dark Jamaican Rum.md`, `Jamaican Dark Rum.md`, `Jamaica Rum.md`, `Jamaican Rum.md`
**Recommendation:**
- Keep: `Jamaican Rum.md` (general)
- Keep: `Dark Jamaican Rum.md` (specific type)
- Delete others

### Demerara Rum
**Files:** `Demarara Rum.md`, `Demerara Rum.md`, `Demerara Rum 151 75,5 %.md`
**Recommendation:**
- Keep: `Demerara Rum.md`
- Keep: `Demerara Rum 151.md` (rename, specific high-proof)
- Delete: `Demarara Rum.md` (typo)

### Fernet
**Files:** `Fernet.md`, `Fernet Branca.md`
**Recommendation:** Keep both (Fernet-Branca is the most common but Fernet is the category)

### Galliano
**Files:** `Galliano.md`, `Galliano Liqueur.md`
**Recommendation:** Keep `Galliano.md`, delete redundant

### Gin Types
**Files:** `Gin.md`, `Dry Gin.md`, `Gin London Dry.md`, `Old Tom Gin.md`, `Cucumber Forward Gin.md`
**Recommendation:**
- Keep: `Gin.md` (general London Dry)
- Keep: `Old Tom Gin.md` (different style)
- Delete: `Dry Gin.md`, `Gin London Dry.md` (use `Gin.md`)
- Delete: `Cucumber Forward Gin.md` (too specific, use `Gin.md`)

### Grapefruit Juice
**Files:** `Fresh Grapefruit.md`, `Fresh Grapefruit Juice.md`, `Grapefruit Juice.md`, `white grapefruit juice.md`
**Recommendation:** Keep `Grapefruit Juice.md`, delete others

### Grenadine
**Files:** `Grenadine.md`, `Grenadine Syrup.md`, `Grendaine.md`
**Recommendation:** Keep `Grenadine.md`, delete others

### Havana Club
**Files:** `Havana.md`, `Havana Club 3 Years old.md`
**Recommendation:** Keep `Havana Club 3 Years old.md`, delete `Havana.md`

### Honey Syrup
**Files:** `Honey Sirup.md`, `Honey Syrup.md`, `Honigsirup.md`
**Recommendation:** Keep `Honey Syrup.md` (English), keep `Honigsirup.md` (German) OR consolidate

### Lemon Juice
**Files:** `Fresh Lemon Juice.md`, `Lemon Juice.md`
**Recommendation:** Keep `Lemon Juice.md` (fresh is implied)

### Lime Juice
**Files:** `Fresh Lime Juice.md`, `Lime Juice.md`, `Lime Juice Cordial.md`, `Limettensaft.md`, `frischer Limettensaft.md`, `frisch gepresster Limettensaft.md`
**Recommendation:**
- Keep: `Lime Juice.md` (fresh)
- Keep: `Lime Juice Cordial.md` (different product - Rose's)
- Keep: `Limettensaft.md` (German) OR consolidate to English only
- Delete: All "frischer" variants

### Lillet
**Files:** `Kina Lillet.md`, `Lillet.md`, `Lillet Blanc.md`
**Recommendation:**
- Keep: `Lillet Blanc.md` (current product)
- Keep: `Kina Lillet.md` (historical, different formula)
- Delete: `Lillet.md`

### Maraschino
**Files:** `Maraschino Likör.md`, `Maraschino Liqueur.md`, `Maraschino Liquor.md`, `Luxardo Maraschino.md`
**Recommendation:** Keep `Maraschino Liqueur.md`, delete others

### Orange Juice
**Files:** `Fresh Orange Juice.md`, `Orange Juice.md`
**Recommendation:** Keep `Orange Juice.md`

### Overproof Rum
**Files:** `Overproof Jamaica Rum.md`, `Overproof Jamaican Rum.md`, `Overproof Rum.md`, `Weißen Overproof Jamaika Rum.md`
**Recommendation:**
- Keep: `Overproof Rum.md` (general)
- Keep: `Overproof Jamaican Rum.md` (specific)
- Delete: Others

### Puerto Rican Rum
**Files:** `Puerto Rican Rum.md`, `Puerto Rican White Rum.md`, `Rican Rum.md`
**Recommendation:** Keep `Puerto Rican Rum.md`, delete others

### Reposado Tequila
**Files:** `Reposado Tequila.md`, `Represado Tequila.md`
**Recommendation:** Keep `Reposado Tequila.md`, delete typo

### Rhum Agricole
**Files:** `Agricole rhum.md`, `Rhum Agricol.md`, `Rhum Agricole Blanc.md`
**Recommendation:**
- Keep: `Rhum Agricole.md` (general, rename if needed)
- Keep: `Rhum Agricole Blanc.md` (specific white agricole)
- Delete: Others

### Rum Types
**Files:** `Rum.md`, `Light Rum.md`, `White Rum.md`, `Heller Rum.md`, `Dark Rum.md`, `Aged Rum.md`, `Gold Rum.md`
**Recommendation:**
- Keep: `White Rum.md` (standard light rum)
- Keep: `Dark Rum.md`
- Keep: `Aged Rum.md`
- Keep: `Gold Rum.md`
- Delete: `Rum.md`, `Light Rum.md`, `Heller Rum.md`

### Rye Whiskey
**Files:** `Rye.md`, `Rye Whiskey.md`, `Rye, Scotch or Bourbon.md`
**Recommendation:** Keep `Rye Whiskey.md`, delete others

### Simple Syrup
**Files:** `Simple Sirup.md`, `Simple Syrup.md`, `Simply Syrup.md`
**Recommendation:** Keep `Simple Syrup.md`, delete others

### Soda Water
**Files:** `Soda.md`, `Soda Water.md`
**Recommendation:** Keep `Soda Water.md`, delete `Soda.md`

### St-Germain
**Files:** `St Germain.md`, also `St. Germain.md` (in untracked)
**Recommendation:** Use `St-Germain.md` (official brand spelling with hyphen)

### Tequila
**Files:** `Tequila.md`, `Tequila Blanco.md`, `Blanco Tequila.md`, `Tequilla.md`, `Reposado Tequila.md`, `añejo tequila.md`
**Recommendation:**
- Keep: `Tequila Blanco.md`
- Keep: `Reposado Tequila.md`
- Keep: `Añejo Tequila.md` (fix lowercase)
- Delete: `Tequila.md`, `Blanco Tequila.md`, `Tequilla.md`

### Triple Sec
**Files:** `Triple Sec.md`, `Tripple Sec.md`
**Recommendation:** Keep `Triple Sec.md`, delete typo

### Vanilla Syrup
**Files:** `Vanilla Syrup.md`, `Vanille Syrup.md`
**Recommendation:** Keep `Vanilla Syrup.md` (English), delete German OR consolidate

### Vodka
**Files:** `Vodka.md`, `Vosdka.md`, `Vanilla Vodka.md`
**Recommendation:**
- Keep: `Vodka.md`
- Keep: `Vanilla Vodka.md` (flavored, different)
- Delete: `Vosdka.md` (typo)

### Whiskey
**Files:** `Whiskey.md`, `Bourbon Whiskey.md`, `Rye Whiskey.md`, `Irish Whiskey.md`
**Recommendation:** Keep all specific types, delete general `Whiskey.md`

---

## 4. MISSING ACCENTS / SPECIAL CHARACTERS

| Current | Should Be |
|---------|-----------|
| `Cachaca.md` | `Cachaça.md` |
| `Jagermeister.md` | `Jägermeister.md` |
| `Curacao.md` | `Curaçao.md` |
| `Eiweiss.md` | `Eiweiss.md` or `Eiweiß.md` |

---

## 5. LANGUAGE INCONSISTENCY (German vs English)

Consider standardizing to English OR creating clear German alternatives:

| German | English |
|--------|---------|
| `Absinth` | `Absinthe` |
| `Agavensirup` | `Agave Syrup` |
| `Eiweiss` | `Egg White` |
| `Heller Rum` | `White Rum` / `Light Rum` |
| `Honigsirup` | `Honey Syrup` |
| `Limettensaft` | `Lime Juice` |
| `Maraschino Likör` | `Maraschino Liqueur` |
| `Vanille Syrup` | `Vanilla Syrup` |
| `Zitronensaft` | `Lemon Juice` |
| `Zuckersirup` | `Simple Syrup` |

---

## 6. ORPHANED/INCOMPLETE ENTRIES TO REVIEW

- `Optional Grated Nutmeg.md` → Move to Deko folder
- `Rye, Scotch or Bourbon.md` → Delete (use individual spirits)
- `Strawberry Jam.md` → Keep if used, otherwise delete
- `Wildberry.md` → Be more specific (which berries?)
- `woodruff Syrup.md` → Keep (Waldmeister, specific ingredient)

---

## RECOMMENDED ACTIONS SUMMARY

1. **Delete 80+ files** that start with measurements
2. **Merge ~50 duplicate files** with typos/variants
3. **Rename ~20 files** with spelling errors
4. **Standardize language** (recommend English for spirits, mixed for syrups/juices)
5. **Add missing accent marks** to 4 files
6. **Create proper files** for garnishes/fillers currently mislabeled

**Estimated final count:** ~150-180 ingredient files (from 289)

