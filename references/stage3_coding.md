# Stage 3: Code the items against the framework

You are helping with an academic research project [RESEARCH_PURPOSE]. Use two files for each textbook: `[BOOK_n_CODE]_[FRAMEWORK_SHORT]_Coding.xlsx` and [FRAMEWORK_DOC]. The spreadsheet has already been checked by hand for extraction accuracy. It contains one blank column for each [FRAMEWORK_NAME] category. Your task is to read every item carefully, work out which cognitive processes students are meaningfully required to perform, and fill in the category columns following the rules below.

Code [BOOK_1_NAME] first. Then code each later book using exactly the same rules (see "Consistency").

## 1. Use the official framework
Use the definitions, explanations and examples in [FRAMEWORK_DOC] as the authoritative classification criteria. Read the whole framework document before you start coding.

The categories are:
[CATEGORY_LIST]

{IF CATEGORY_GROUPS} The categories belong to these broader groups: [CATEGORY_GROUPS]. Do not code the groups separately. They will be calculated later from the category values. {END}

[EXTRA_CODING_RULES]

## 2. Understand each item before you classify it
For each item:
- Read the complete item, including all subquestions, instructions and steps.
- Work out what a [GRADE_LEVEL] student would actually need to do to complete the task satisfactorily.
- Identify the cognitive processes that the task directly and meaningfully requires.
- Compare those processes with the official framework definitions.
- Assign the classification.

Consider the nature of the task, the expected student response, the information provided and the [SUBJECT] thinking required. Interpret each item in the context of the knowledge a [GRADE_LEVEL] student can reasonably be expected to have. Do not classify an item only by its command words. Focus on the actual cognitive demands, not on surface wording.

## 3. Classification rules
{PATH A}
For each category, assign 1 if the item directly and meaningfully requires that cognitive process, or 0 if it does not. Multiple labels are allowed.
- An item may have a 1 in more than one category when those processes are genuinely required.
- Do not assign a category just because the process might be involved incidentally. Do not code every prerequisite mental step.
- Every 1 must be justified on its own by a meaningful requirement of the task.
- Be selective, but do not artificially limit the number of categories. Some items need only one process; others genuinely need several. Do not set a fixed maximum number of 1s.
{PATH B}
Assign each item exactly one category: the one that best describes the central cognitive demand of the task as a whole. Put 1 in that column and 0 in every other column.
- Choose the category that the task as a whole requires students to reach, not the category of its easiest or most incidental part.
- {IF LEVEL_ORDER} When an item falls between two levels, choose the higher level only if a substantive part of the task actually requires it. Do not raise the level just because the item is long or has many parts. {END}
- If no category fits, see "Items outside the framework" below. Do not force the nearest category.
{END}

## 4. Separate primary demands from incidental skills
Only the cognitive processes that are central to completing the task count. Do not count background knowledge, routine reading, ordinary comprehension or incidental thinking as separate demands unless they independently meet a framework definition.
- Do not assume that a longer item is more cognitively demanding.
- Do not assume that activities or projects automatically involve higher-order thinking.
- Do not assume that a short item is cognitively simple.

## 5. Multi-part items
Each row is one complete item. Some items have subquestions such as (a), (b), (c); some activities have several instructions or stages.
- Read and consider the whole item, and weigh the meaningful demands of all its parts.
{PATH A}
- Assign 1 to each category that at least one substantive part genuinely requires. The codes apply to the item as a whole.
{PATH B}
- Assign the one category that best describes the item as a whole, taking every substantive part into account.
{END}

## 6. Missing context and ambiguity
Some items refer to diagrams, graphs, tables or images that are not in the text-only dataset.
- Classify the item if its cognitive demand can be determined reliably from the text available. Do not exclude an item automatically just because it refers to a visual.
- Do not invent or infer the contents of missing images.
- If missing context prevents a reliable classification, flag the item instead of guessing. Do not force an uncertain classification into 0 or 1.
- If classification is genuinely impossible because essential information is missing (for example, the figure itself defines the task), leave all of that item's category cells blank and record it in the review report. Recommend excluding it from analysis and ask the researcher. If they agree, follow "Exclusions" below.
- Sort flagged items into two groups: **coded, check the figure** (the type of demand is clear but the answer depends on the image) and **cannot be coded** (left blank).

## 7. Items outside the framework
Some items may not require any cognitive process covered by the framework's definitions.
{PATH A} Code them as all 0 on purpose, so no cell is left blank, and list them in the review report as deliberate all-0 items. {END}
{PATH B} Leave the category cells all 0, note "Outside framework" in the review report, and ask the researcher whether to exclude them from the analysis. {END}

## 8. Keep the original workbook data unchanged
The existing data has been checked by hand and must stay exactly as it is.
- Do not change Item_ID or Item_Type values.
- Do not modify, rewrite, correct, shorten or reorder Extracted_Text.
- Do not change the original numbering, page references, extraction statuses or notes.
- Do not add or remove items, and do not split or merge rows.
- Keep the existing worksheet names and column order.
- Fill in only the existing category columns.

## 9. Consistency across items and books
- Some judgement calls will come up again and again, e.g. "fill-in-the-blank, true/false and factual multiple-choice items → [the recall category]" or "one-step calculations → [the category for applying a model or procedure]". Write each one as a rule in `skill_run/conventions.md`, with an example item ID.
- Apply each rule the same way to every similar item, in every book.
- When coding a later book, read `conventions.md` first. If it needs a new rule, add it, mark it as new, and report it.

## 10. Exclusions
When the researcher agrees to exclude an item:
- Shade the whole row in light red and put the Item_ID in bold, dark red.
- Add a comment to the Item_ID cell giving the reason.
- Add an "Excluded items" note to the Read_Me sheet. Do not write in the original columns.
- Record the item in `skill_run/exclusions.md` with its ID, the reason and the date.
- Report the analysis base after exclusions: the number of items per book and item type.

## Outputs
For each book:
1. `[BOOK_n_CODE]_[FRAMEWORK_SHORT]_Coding_[FRAMEWORK_SHORT]_Classified.xlsx`: the original workbook with only the category columns filled in. Do not overwrite the uncoded workbook.
2. `[BOOK_n_CODE]_[FRAMEWORK_SHORT]_Review_Report.xlsx`, a separate report with:
   - an **Item codes** sheet: the Item_ID, the categories coded 1, a one-line reason for each item, and a flag column, with flagged rows highlighted
   - a **Summary** sheet: counts of flagged items by reason, deliberate all-0 or outside-framework items, exclusions, and the coding rules applied (copied from `conventions.md`)

## Self-check (always run, then fix and run again)
After coding, check:
- Every eligible item has been processed.
- Every coded row has exactly [number of categories] values, and each value is a number, 0 or 1 (not text).
- No category column has been skipped, shifted or mismatched. The 1s in each row are in the intended columns, checked against the review report's reasons.
- {PATH A} Rows with several 1s are justified by the stated reasons. {END}
- {PATH B} Every coded row has exactly one 1. {END}
- Similar items have been coded the same way. Group items by format and wording pattern, and check each group for codes that don't fit.
- All original workbook data is unchanged: run `scripts/check_workbook.py` to compare the original columns, sheet names, column order, row count and validation against the uncoded workbook.
- The only blank rows are the ones in the review report's "cannot be coded" list.

## Pause
Report:
- the number of labels per item (Path A) or the distribution of levels (Path B)
- the most and least used categories
- the flagged items, grouped
- the deliberate all-0 items
- the judgement calls the researcher may want to change, listed as rules with example IDs

Suggest that a second coder independently code a random sample (about 20–25%) so inter-rater agreement can be reported, and that the researcher check the "check the figure" items against the printed book.
