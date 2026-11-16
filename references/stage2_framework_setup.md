# Stage 2: Add the framework columns

Create new spreadsheets for the next stage of the research by adding the [FRAMEWORK_NAME] categories as new columns.

{FOR EACH BOOK}
Make a copy of the extraction spreadsheet for [BOOK_n_NAME]. Name the copy `[BOOK_n_CODE]_[FRAMEWORK_SHORT]_Coding.xlsx`. Do not modify the original.
{END}

Keep all existing rows and columns unchanged. Add one column for each category to the right of the existing columns, using these exact column names in this exact order:

[CATEGORY_LIST]

These columns will hold a binary classification:
{PATH A}
- 1 = the item meaningfully requires this cognitive process.
- 0 = the item does not meaningfully require this cognitive process.
- An item may have a 1 in more than one column.
{PATH B}
- 1 = this is the single category that best describes the item's central demand.
- 0 = all other categories.
- Each item has exactly one 1.
{END}

For now, leave every cell in the new columns blank.

## Make the columns easy to code
- Add data validation so the new cells accept only 0, 1 or blank, with an error message that explains the coding rule above.
- If [CATEGORY_GROUPS] are defined, colour the headers by group with a light tint for each group.
- Freeze the header row and the ID and text columns, so the item text stays visible while scrolling.
- Extend the filter to cover the new columns.
- Add a line to the Read_Me sheet explaining the coding rule and the framework source ([FRAMEWORK_DOC]).

## Self-check (always run, two independent ways)
Check 1, with a spreadsheet library, and Check 2, by reading the raw file contents directly:
- Every original header and data cell is identical to the source spreadsheet.
- The new headers match [CATEGORY_LIST] exactly and are in the same order.
- Row counts and counts per item type match the source. All Item_IDs are unique.
- Every cell in the new columns is empty, and the 0/1 validation covers every data row.
- The source spreadsheets have not been changed (their modification time is from before this stage).

## Pause
Report the new files, where the columns were added (which columns, by letter) and the results of both checks.
