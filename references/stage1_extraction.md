# Stage 1: Text extraction

{FOR EACH BOOK}

Please perform a text extraction on the PDF "[BOOK_n_PDF]" ([BOOK_n_NAME]). Extract all eligible items accurately and verbatim, and organise them into an Excel spreadsheet (.xlsx). This is strictly a text extraction task. Do not analyse, interpret, summarise, rewrite or classify the educational content.

## Which sections to extract
Extract content ONLY from the following sections:
{FOR EACH ITEM TYPE}
- "[BOOK_n_SECTION_<TYPE>]": extract every item in this section as a [ITEM_TYPE]. For this project, a [ITEM_TYPE] is [ITEM_TYPE_DEFINITION].
{END}

Do not extract any content from any other section of the textbook. In particular:
- Ignore chapter summaries, introductions, explanations, worked examples, discussions, keyword lists, learning objectives and other supplementary material.
- Ignore questions, experiments, activities or projects that appear outside the sections listed above, even if they look similar.
- Ignore unrelated text above, below or beside these sections, even when it is on the same PDF page. [BOOK_n_EXCLUDE_NOTES]
- If a page contains both other content (such as a summary) and the start of a listed section, extract only the content that belongs to the listed section.
- If a page contains the end of one listed section and the start of an unrelated section, stop at the section boundary.
- If a listed section continues onto the next page, keep extracting until the section ends, even if the heading is not repeated.
- Use the actual section headings and boundaries to decide what to include. Do not rely only on numbering, bullet points or position on the page.
- If a section boundary is unclear, flag it rather than making an assumption.

In short: a page that contains eligible content does not make all the text on that page eligible. Include only the text that belongs to the listed sections.

## What counts as one item
Treat each main item as one row. If it contains subquestions such as (a), (b), (c), or (i), (ii), (iii), or smaller bullet points beneath the main item, keep them together with the parent item in the same cell. Do not split or merge items. Multi-step activities and projects stay together as one item.

## Columns
- **Item_ID**: sequential identifiers, [BOOK_n_CODE]_<letter>001, [BOOK_n_CODE]_<letter>002, …, where <letter> is the item type's ID letter. Each item type has its own numbering sequence.
- **Item_Type**: [ITEM_TYPES]
- **Original_Number**: the number printed in the PDF, if there is one. Leave it blank for unnumbered items.
- **Extracted_Text**: the full item, verbatim, including all subparts
- **PDF_Page**: the page number in the PDF file where the item begins
- **Extraction_Status**: Complete or Needs Review
- **Extraction_Notes**: a brief explanation of any missing text, unclear section boundary, missing visual context or other issue

## Accuracy
Accuracy is the highest priority. Transcribe spelling, punctuation, numbers, units, symbols, mathematical expressions and subject terminology exactly. Do not correct errors (including the book's own typos), simplify or paraphrase.

This project uses text-based analysis only. Do not extract, reproduce, describe or interpret images, illustrations, graphs or diagrams in the items. Record any missing visual context in Extraction_Notes instead, and mark the item Needs Review if the missing visual could matter.

## Formatting conventions
Apply these to every book and record them in a Read_Me sheet in the workbook and in `skill_run/conventions.md`. If a convention already exists in `conventions.md` from an earlier book, reuse it.
- Put the main number only in Original_Number. Don't repeat it at the start of Extracted_Text.
- Keep line breaks between subquestions, numbered steps and subparts. Put each subpart or option on its own line, even when the book prints several on one line.
- Write blanks printed as drawn lines as 10 underscores (`__________`) and note this.
- Write tables as text with " | " between columns, one row per line. Write match-the-columns tables as Column A, then Column B.
- Unnumbered (bulleted) items: leave Original_Number blank, and give the item's position in Extraction_Notes (e.g. "3rd bullet in the section").
- Shared instructions that apply to a group of items (e.g. "For Questions 4–6, choose the correct answer"):
  {IF GROUP_INSTRUCTIONS = include} Copy the instruction into each item it applies to, as the first line, marked `[Shared instruction] …`, and note this in Extraction_Notes. {END}
  {IF GROUP_INSTRUCTIONS = leave out} Leave it out, quote it in Extraction_Notes for each affected item, and mark those items Needs Review. {END}
- Leave out lists of links or further-reading references placed after the items, figure captions, labels inside figures, and puzzle grids. Flag the affected item.
- Write special characters correctly (×, °, →, ≤, subscripts and superscripts where Unicode has them). If there's no clean character for something, use a clear notation, note it, and mark the item Needs Review.
- Bold and italics are not kept.
- Set column widths and row heights (wrapped text) so every cell can be read without resizing.

## Method
- Extract from the PDF's text layer (e.g. `pdftotext -layout`), and also look at the rendered image of every page. The text layer gives exact characters; the page images show section boundaries, layout, blanks and symbols.
- If the text layer is damaged (letters, words or options missing, or garbled text), transcribe from the page image. Cross-check it word by word against an independent OCR pass (e.g. tesseract), mark the item Needs Review, and explain this in the notes.
- Watch for symbols that are in the text layer but don't appear on the rendered page, or the other way round (×, °, arrows, minus signs). Flag these.
- Check `references/lessons_learned.md` for other pitfalls.

## Self-check (always run, then fix and run again)
As a final check, look at every page of the PDF again and confirm that all of the instructions above were followed.
- All eligible items have been extracted, in their original order.
- No eligible item has been left out or repeated. Numbering has no gaps within each chapter or section, and any break in numbering is explained.
- Multi-part and multi-step items are each kept together in one row.
- Every line of every item has been compared, by a script, against the text layer (or the OCR for damaged pages). Any remaining differences are listed and explained.
- Nothing has been rewritten. The extracted text matches the PDF exactly.
- Text that couldn't be transcribed with confidence is flagged, not guessed. Every uncertainty is marked for review, not left unmentioned.
- The counts in the report match the spreadsheet: total, per item type and per chapter.

## Pause
Report the counts, the number of items marked Complete and Needs Review, the reasons items need review (grouped), and any new conventions. Suggest that the researcher check the Needs Review items against the printed book, plus a random sample of Complete items, before Stage 2. Stage 3 assumes the extraction has been checked by hand.

{END}
