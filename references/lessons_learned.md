# Lessons learned (check these at every stage)

These are pitfalls found during real runs of this workflow.

## Extraction
- **Damaged text layers.** Some PDFs have text layers with missing letters or whole missing words, often on only some pages. Always compare the text layer with the page image. Where they differ, transcribe from the image and cross-check with OCR.
- **Symbols that are in the text layer but not on the page** (or the reverse): ×, °, −, arrows. Flag them for checking against the printed book.
- **Lookalike features next to eligible sections.** Boxes such as "Think about it", "Did you know?", history or fun-fact boxes and reflection prompts often sit beside or inside the eligible sections and look like questions. Use the section structure to decide, and list what was left out in the report.
- **Different books use different headings and layouts** for the same item type. One book may number its items while another uses bullets. Never assume the second book matches the first; ask for or confirm its headings.
- **Group instructions** ("For Questions 4–6, choose the correct answer") belong to no single item, but they can change the task. Always ask the researcher whether to include them (see intake), and handle every book the same way.
- **Empty answer tables** printed for students to fill in: copy the headers only, and note this.
- **The section label may be missing** on a continuation page. Rely on the section's structure, and flag the item.

## Coding
- **Items that depend on figures** fall on a range. Most can be coded from what the task asks for. A few can't, because the figure is the task (e.g. "Label the parts shown in Fig. X"). Leave only those blank and recommend excluding them.
- **Coding by command words is the most common mistake.** "Explain" can be recall, and "List" can need analysis. Always ask what a student at this grade would actually have to do.
- **Recall formats** (fill in the blanks, true/false, factual multiple choice, matching, crosswords, single-term answers) are usually the framework's lowest recall category. Decide this once and apply it everywhere.
- **Activities that only ask students to observe or record** are usually descriptive. Don't assume that an activity involves higher-order thinking.
- **Items that fit no category** occur in most textbooks. Decide how to treat them once, list them, and judge only against the framework's own definitions.
- **Rules drift between books.** Coding the second book without re-reading the first book's rules leads to inconsistent coding. Always read `conventions.md` first.
- **Framework conventions versus research design:** some frameworks assign each assessment item to one category (TIMSS does this for its own test items). Multi-label coding is a legitimate research choice, but the methods section should state it as one.

## Analysis
- **Heatmap colour scale:** a 0–100% scale makes most cells look the same when prevalences are low. Cap the scale just above the highest value, and use the same scale across heatmaps.
- **Small groups:** activity or project groups are often small (around 50 items or fewer). Say this whenever you report differences.
- **Exclusions must reach every number.** Assert the group sizes in the script so an excluded item can't slip back in.
- **Fonts and colour packages** may not be installed. Check before plotting (e.g. `cmcrameri`; Helvetica Neue isn't available on every operating system), fall back cleanly, and tell the researcher.
