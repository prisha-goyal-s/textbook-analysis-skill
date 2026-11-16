# Intake

Ask these questions in rounds. Skip any round the requested stages don't need. Offer the default if there is one. Don't move on until each answer is clear.

## Round 1: The project
- Which stages do you want to run? (All four, or start from a later stage with files you already have.)
- `[RESEARCH_PURPOSE]`: In one sentence, what is the study about? (e.g. "investigating the cognitive demands of practice questions and investigations in two Grade 6 mathematics textbooks")
- `[SUBJECT]`: the subject (e.g. Science, Mathematics, English)
- `[GRADE_LEVEL]`: the grade or age group (e.g. Grade 6)
- `[CURRICULUM]`: the curriculum, publisher or series, if relevant (e.g. a national curriculum, Common Core, a publisher series)
- `[OUTPUT_DIR]`: where to save the outputs. Default: the current project folder.

## Round 2: The textbooks (repeat for each book)
- `[BOOK_n_NAME]`: the full name of the textbook
- `[BOOK_n_CODE]`: a short code of 2 to 5 capital letters, used in item IDs (e.g. MEX). Every book needs a different code.
- `[BOOK_n_PDF]`: the PDF file, i.e. its path or name in the project folder

Then ask about item types for the whole project:
- `[ITEM_TYPES]`: which kinds of items will be analysed, and the one-letter ID for each. Default: Question (Q) and Activity (A).
- `[ITEM_TYPE_DEFINITION]`: for each item type, what counts as one item. Default: "any main numbered or separately listed item in the section; sub-parts belong to their parent item".

Then, for each book and each item type:
- `[BOOK_n_SECTION_<TYPE>]`: the exact heading or headings of the section(s) this item type comes from, as printed (e.g. "Exercises"). Different books often use different headings for the same item type. Ask for each book separately.
- `[BOOK_n_EXCLUDE_NOTES]` (optional): any boxes or features sitting next to these sections that must not be included.

### Shared group instructions, `[GROUP_INSTRUCTIONS]`
Show the researcher this explanation and ask them to choose before Stage 1 runs:

> Textbooks sometimes print one instruction that applies to several items, for example "For Questions 4–6, choose the correct answer" or "Answer Questions 3–5 using Table 2.1". It isn't part of any single numbered item, but it can change what a student has to do. For example, it can turn an open question into multiple choice. How should these be handled?
> - **(a) Include:** copy the shared instruction into each item it applies to, on its own first line and marked `[Shared instruction] …`, and note this in Extraction_Notes. This is recommended if you will code cognitive demand, because the coder sees the full task.
> - **(b) Leave out and flag:** don't copy the instruction into the items. Quote it in Extraction_Notes for each affected item, and mark those items Needs Review.

Record the choice in `config.json` and `conventions.md`.

## Round 3: The framework
- `[FRAMEWORK_NAME]`: the full name, e.g. "Webb's Depth of Knowledge"
- `[FRAMEWORK_SHORT]`: a short tag used in file names, e.g. TIMSS, DOK, Bloom
- `[FRAMEWORK_DOC]`: the official framework document (PDF or text) in the project folder. It is the authority for every coding decision, so ask the researcher to supply it if they haven't.

### Choosing the coding mode, `[CODING_MODE]`
Show the researcher this explanation as written, and ask them to choose:

> **Path A: Multi-label (independent yes/no categories).** Each item gets a 1 or a 0 for every category in the framework, and it can have several 1s when it really requires several processes. Percentages across categories can add up to more than 100%. This suits frameworks that list processes or practices which can occur together. Examples: the TIMSS cognitive subcategories, NGSS science and engineering practices, PISA competencies, and Bloom's taxonomy when you want to record every process an item requires.
>
> **Path B: Single level (one category per item).** Each item is assigned exactly one category, the one that best describes its central demand. The categories are often ordered from lower to higher demand. Percentages across categories add up to 100%. This suits frameworks built as levels or a ladder. Examples: Webb's Depth of Knowledge (DOK 1–4), Smith & Stein's levels of cognitive demand, Barrett's taxonomy, and Bloom's taxonomy coded at the highest level an item reaches.
>
> **Not sure?** I can read your framework document and recommend one. Some frameworks have an official rule. For example, the TIMSS assessments themselves assign each test item to a single domain, but researchers often code textbook items with several labels. Whichever you choose, state it in your methods as a design decision.

If the researcher is unsure: read `[FRAMEWORK_DOC]`, recommend a path with a two-sentence reason, and ask them to confirm.

### Categories
- `[CATEGORY_LIST]`: the exact category names, in order. These become the column names. Use whatever level of the framework the researcher wants to code, named however they like: e.g. "Remember, Understand, Apply…", "DOK 1, DOK 2…", or "Knowing - Recognize, Knowing - Describe…". Offer to draft the list from `[FRAMEWORK_DOC]`, then ask the researcher to confirm or edit it.
- `[CATEGORY_GROUPS]` (optional, default: none): ask "Do you also want results summarised for broader groups of these categories?" (e.g. TIMSS Knowing / Applying / Reasoning, Smith & Stein lower / higher demand, PIRLS's two process pairs). If yes, ask which categories belong to each group. If no, skip the group analysis.
- `[LEVEL_ORDER]` (Path B only, optional): whether the categories run from lower to higher demand, and in what order. If they are unordered, analyses that rely on order are skipped.
- `[HIGHER_DEMAND_THRESHOLD]` (Path B, ordered only, optional): the level and above that count as "higher demand" (e.g. DOK 3+).
- `[EXTRA_CODING_RULES]` (optional): any rules the researcher wants applied, e.g. their own decision rules or a codebook from a previous study.

## Round 4: The analysis and figures
- `[COMPARISON]`: which textbook to treat as the reference (Book 1) and which as the comparison (Book 2), used for difference panels as "Book 2 − Book 1". With 3 or more books, ask which comparisons to make. With 1 book, there are no difference panels.
- `[PALETTE]`: the figure colours. Default: Crameri's Batlow, which is perceptually uniform and readable for colour-blind viewers.
- `[FONT]`: the figure font. Default: Helvetica Neue, falling back to Arial and then any sans-serif font.
- `[FIGURE_FORMATS]`: Default: PNG at 300 dpi and PDF.

## Confirm
Show every answer in one table, Blank | Value, and ask "Is everything correct?" Write `skill_run/config.json` only after the researcher confirms. Follow the structure of `config_example.json` exactly, because `scripts/analyze.py` and `scripts/check_workbook.py` read it.
