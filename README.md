# textbook-analysis-skill: a Claude Code skill

Extract, code and compare the cognitive demand of textbook questions and activities against a framework you choose.

## Install
Copy this folder to `~/.claude/skills/textbook-analysis-skill/` (just for you) or to `<your project>/.claude/skills/textbook-analysis-skill/` (shared with everyone working on that project). Then, in Claude Code, type `/textbook-analysis-skill` or describe the task in plain words.

## Files to put in your project folder first
- The textbook PDFs (one per book, ideally merged to just the relevant chapters)
- The official framework document (PDF or text)

## The blanks you will fill in
When the skill starts, Claude asks you for these, a few at a time, and fills your answers into the instructions for each stage. It only asks for the blanks the stages you run need. It's quicker if you prepare them beforehand.

**About your project**
| Blank | What to give | Example |
|---|---|---|
| `[RESEARCH_PURPOSE]` | One sentence on what the study investigates | "the cognitive demands of practice questions and investigations in two Grade 6 mathematics textbooks" |
| `[SUBJECT]` | The subject of the textbooks | Science |
| `[GRADE_LEVEL]` | The grade or age group the books are written for. Coding judges what a student at this level must do. | Grade 6 |
| `[CURRICULUM]` | The curriculum, publisher or series (optional) | a national curriculum or publisher series |
| `[OUTPUT_DIR]` | Where to save the outputs (default: the current folder) | `~/Research/TextbookStudy` |

**About each textbook** (repeated for Book 1, Book 2, …)
| Blank | What to give | Example |
|---|---|---|
| `[BOOK_n_NAME]` | The textbook's full name | Number Journeys |
| `[BOOK_n_CODE]` | A short code of 2–5 capital letters, used in item IDs and file names. Each book needs a different one. | NJY |
| `[BOOK_n_PDF]` | The PDF file name in your project folder | `Number_Journeys_Ch1-10.pdf` |
| `[BOOK_n_SECTION_<TYPE>]` | The exact heading(s), as printed, of the section each item type comes from. Different books often use different headings. | Questions: "Practice Set"; Activities: "Let's Investigate" |
| `[BOOK_n_EXCLUDE_NOTES]` | Optional: boxes or features beside those sections that must **not** be extracted | "Ignore the 'Did you know?' boxes" |

**About the items**
| Blank | What to give | Example |
|---|---|---|
| `[ITEM_TYPES]` | The kinds of item to analyse, each with a one-letter ID. Default: Question (Q), Activity (A). | Question (Q), Activity (A), Project (P) |
| `[ITEM_TYPE_DEFINITION]` | What counts as one item of each type. Default: each main numbered or listed item, with its sub-parts grouped under it. | "Each numbered exercise, including its (a), (b), (c) parts" |
| `[GROUP_INSTRUCTIONS]` | How to handle instructions printed once for several items (e.g. "For Questions 4–6, choose the correct answer"): **include** them in each item they apply to, or **leave them out and flag** the items | Include |

**About the framework**
| Blank | What to give | Example |
|---|---|---|
| `[FRAMEWORK_NAME]` | The framework's full name | Webb's Depth of Knowledge |
| `[FRAMEWORK_SHORT]` | A short tag used in file names | DOK |
| `[FRAMEWORK_DOC]` | The framework document's file name. It is the authority for all coding. | `DOK_Guide.pdf` |
| `[CODING_MODE]` | **A: multi-label** (each item gets 0/1 for every category and can have several 1s) or **B: single level** (each item gets exactly one category). Claude explains both and can recommend one. | B |
| `[CATEGORY_LIST]` | The exact category names, in order, as you want them as column headers. Use whatever level and naming you prefer. Claude can draft this from the framework document. | DOK 1, DOK 2, DOK 3, DOK 4 |
| `[CATEGORY_GROUPS]` | Optional: broader groups you also want results for, and which categories belong to each | Lower = DOK 1, DOK 2; Higher = DOK 3, DOK 4 |
| `[LEVEL_ORDER]` | Path B only, optional: the order of the categories from lower to higher demand, if they have one | DOK 1 < DOK 2 < DOK 3 < DOK 4 |
| `[HIGHER_DEMAND_THRESHOLD]` | Path B, ordered only, optional: the level and above that count as "higher demand" | DOK 3 |
| `[EXTRA_CODING_RULES]` | Optional: your own decision rules or an existing codebook to follow | "Code multiple-choice recall items as DOK 1" |

**About the analysis and figures**
| Blank | What to give | Example |
|---|---|---|
| `[COMPARISON]` | Which book is the reference and which is compared against it (differences are shown as Book 2 − Book 1) | Book 1 = Maths Explorer, Book 2 = Number Journeys |
| `[PALETTE]` | The figure colours. Default: Crameri's Batlow (readable for colour-blind viewers). | Batlow |
| `[FONT]` | The figure font. Default: Helvetica Neue. | Arial |
| `[FIGURE_FORMATS]` | The file formats for figures. Default: PNG at 300 dpi plus PDF. | PNG, PDF |

At the end of setup, Claude shows all your answers in one table to confirm, and saves them to `skill_run/config.json`. To change one later, tell Claude or edit that file.

`config_example.json` in this folder shows a complete config for a made-up two-textbook study (Webb's DOK, single level), so you can see the format.

## What you get
- verified extraction spreadsheets
- coded spreadsheets, plus a review report giving a reason for every code
- results tables and figures
- a `skill_run/` folder recording every setting and rule, for your methods section

## Requirements
Python 3 with pandas, openpyxl and matplotlib, plus cmcrameri for the default palette. poppler (`pdftotext`) and tesseract are needed for extraction.

## Not included
Significance testing and inter-rater reliability statistics. The skill suggests a second-coder sample but doesn't calculate agreement.
