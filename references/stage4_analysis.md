# Stage 4: Descriptive analysis and figures

Use the classified spreadsheets for [BOOK_1_NAME]{FOR EACH LATER BOOK}, [BOOK_n_NAME]{END}. Leave out every item in `skill_run/exclusions.md`, and any row whose category cells are blank. Report how many items were left out and why.

## Groups
Analyse each textbook × item type combination as its own group (e.g. [BOOK_1_NAME] – [ITEM_TYPE_1], [BOOK_2_NAME] – [ITEM_TYPE_1], …). Do not combine item types in the main analysis. The textbooks may contain different numbers of each item type, so use proportions and percentages rather than raw counts for the main comparisons. Always report the size of each group (N) next to its percentages.

## Analyses
{PATH A}
**Analysis 1: Category prevalence.** For each category in each group, calculate:
- the number of items coded 1
- the total number of eligible, fully coded items in the group
- the prevalence: (items coded 1 ÷ eligible items) × 100

Because items can have several 1s, the percentages across categories may add up to more than 100%. Say so in the table notes and figure captions. Figure: a grouped horizontal bar chart of the categories, one bar per book, with one figure for each item type.

**Analysis 2: Prevalence heatmap.** Show the prevalence of every category (rows) for each book (columns), with one heatmap per item type. Add a panel showing the difference in percentage points ([COMPARISON]). Use the same colour scale for every heatmap so they can be compared. Set its maximum to the highest prevalence rounded up to the next 10%, not 100%, so the differences stay visible, and state the scale in the caption.

**Analysis 3: Group prevalence** (skip if no [CATEGORY_GROUPS]). Calculate the groups from the category values. An item belongs to a group if at least one category in that group is 1. For example, [first group] = 1 if [its categories joined with OR] = 1. An item with several 1s in the same group counts only once for that group. Calculate the number and percentage of items involving each group; these can add up to more than 100%. Figure: a grouped bar chart of the groups by book, separately for each item type.

**Analysis 4: Number of categories per item.** For each item, the number of positive labels is the sum of its category values. Group the items as 0, 1, 2, 3 and 4 or more labels. For each book and item type, calculate the number and percentage of items in each group, plus the mean and median. Figure: a grouped bar chart by book, separately for each item type.
{PATH B}
**Analysis 1: Level distribution.** For each group, calculate the number and percentage of items assigned to each category. These add up to 100%. Figure: a grouped bar chart by book, separately for each item type. {IF LEVEL_ORDER} Also make a 100% stacked bar per group, with the levels in order. {END}

**Analysis 2: Heatmap.** Category (rows) × book (columns), one heatmap per item type, with a difference panel ([COMPARISON]) and a shared colour scale (see the Path A heatmap rule).

**Analysis 3: Group distribution** (skip if no [CATEGORY_GROUPS]). Each item belongs to exactly one group, the group of its category. Calculate the number and percentage per group (they add up to 100%), shown as a grouped bar chart.

**Analysis 4: Ordinal summary** (skip if no [LEVEL_ORDER]). For each group: the median and mean level, with the level number taken from its position in [LEVEL_ORDER], and the percentage at or above [HIGHER_DEMAND_THRESHOLD]. Figure: a grouped bar chart of the higher-demand percentage by book.
{END}

## Figure style
- Colours: [PALETTE]. Give each book one fixed colour, used in every figure, and pick colours far enough apart to tell apart in greyscale. For heatmaps, use the sequential version of the palette.
- Font: [FONT], with clean axes (no top or right spines), percentages labelled on or next to the bars, and N for each group in the legend or subtitle.
- Use consistent file names: `Fig<number><a|b>_<Analysis>_<ItemType>`, e.g. `Fig1a_Category_Prevalence_Questions`.
- Formats: [FIGURE_FORMATS]. Embed the fonts in PDFs (TrueType).

## Outputs (in [OUTPUT_DIR]/Analysis/)
- `[FRAMEWORK_SHORT]_Prevalence_Analysis.xlsx`, with:
  - a **Method** sheet: sources, groups, Ns, exclusions, formulas, the category-group rule (if used) and the coding mode
  - one sheet per analysis, in long format
  - a wide comparison sheet with the differences
  - an item-level sheet of derived values (category groups, number of labels)
- a `figures/` folder
- the analysis script, copied into the project so the researcher can rerun it: `scripts/analyze.py --config skill_run/config.json`

## Self-check (always run)
- Each group's N matches the classified workbook minus the exclusions, checked with an assertion in the script.
- Every category value used is 0 or 1. No blank rows are counted.
- {PATH A} The label-count groups add up to N for each group. Group counts are no greater than N. {END}
- {PATH B} The level percentages add up to 100% (±0.1 for rounding) for each group. {END}
- Recalculate two or three numbers by hand from the raw spreadsheet and confirm that they match the tables.
- Open every figure and check that labels aren't cut off, legends don't cover data, colours match the books and the right font is used.

## Reporting
Report:
- a table of N per group
- the main differences, in percentage points, for each item type
- a small table of group results, if groups are used
- where the files are saved

Always add these caveats:
- With small groups, one item changes a percentage by about 100/N points, so small differences should be read with caution.
- These are descriptive results only. No significance tests have been run.
- Anything that needs installing to rerun the script, e.g. `pip install cmcrameri` for Batlow.
