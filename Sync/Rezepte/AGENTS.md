# Repository Guidelines

## Project Structure & Module Organization
The vault is organized as an Obsidian knowledge base. `Cocktails/` holds one Markdown file per drink, while supporting entities live in `Zutaten/`, `Deko/`, `Eis/`, `Gläser/`, `Techniken/`, and `Tools/` so every `[[Link]]` resolves to a glossary entry. `Cocktail-Liste.md`, `Cocktails.csv`, and `Cocktails.numbers` provide overview lists, and `Vorlage.md` is the canonical template for new recipes. Keep files in their existing folders; ingredients that do not yet exist should be added under the closest matching subfolder inside `Zutaten/`.

## Build, Test, and Development Commands
No compilation is needed, but a few commands keep the vault consistent:
- `rg -n "# Zutaten" Cocktails` quickly surfaces files missing required sections.
- `markdownlint Cocktails/**/*.md Zutaten/**/*.md` (if available) enforces basic Markdown hygiene.
- `open -a Obsidian "/Users/jan/Documents/Obsidian Vault/Sync/Rezepte"` launches the vault for visual verification.

## Coding Style & Naming Conventions
Each cocktail file must contain the ordered headings `# Zutaten`, `# Zubereitung`, `# Served`, and `# Kategorien`. Use unordered lists for ingredients (`* 1 [[Gin]]`) and keep preparation steps as short imperative sentences. Prefer existing entity names and wrap every reference in double brackets to maintain backlink graphs. File names stay human-readable (`Negroni.md`, `King's Breakfast.md`) and should mirror the title case used inside the document. Avoid trailing whitespace and keep indentation to two spaces for nested lists when needed.

## Testing Guidelines
Because this is content-driven, “tests” are manual checks: confirm that every ingredient, tool, and technique links to a file, opened in Obsidian’s graph view or via `rg -l "\[\[Falernum\]\]"`. Scan rendered previews to ensure bullet alignment and that the Served block specifies glass, ice, and garnish. When editing shared assets like `Cocktails.csv`, open the file in a spreadsheet viewer to confirm delimiters remain intact. Aim for full coverage of new recipes; partial drafts should be saved as `WIP - Name.md` outside `Cocktails/` until complete.

## Commit & Pull Request Guidelines
Recent history uses timestamped messages such as `vault backup: 2025-04-08 09:17:54`; follow the same `vault backup: YYYY-MM-DD HH:MM:SS` convention unless coordinating a feature branch. Pull requests or handoffs should summarize which recipes or glossary entries changed, note any new supporting files, and include screenshots of noteworthy Obsidian previews when layout shifts. Link related issues or tasks and call out unresolved questions so the next agent can continue without repeating verification steps.
