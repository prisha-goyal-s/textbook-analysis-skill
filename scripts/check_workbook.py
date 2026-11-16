#!/usr/bin/env python3
"""Checks reused across stages of textbook-analysis-skill.

Usage:
    python check_workbook.py ORIGINAL.xlsx NEW.xlsx --config skill_run/config.json --stage setup|coded

  --stage setup : after Stage 2. The category columns must all be blank.
  --stage coded : after Stage 3. Every row is fully coded with 0/1, except the excluded rows (which must be blank).

What it checks:
  1. Every sheet in ORIGINAL is still in NEW, in the same order.
  2. On every sheet, each cell that existed in ORIGINAL has the same value in NEW (new rows such as Read_Me notes are allowed).
  3. On the item sheet: same row count, Item_IDs unique, category headers exactly match config and come right after the original columns.
  4. Category values: numbers 0/1 only (not text); Path B: exactly one 1 per coded row.
  5. Data validation covers the category columns (a warning only, not a failure).
Exits with code 1 if any check fails.
"""
import argparse, json, os, re, sys
from openpyxl import load_workbook
from openpyxl.utils import get_column_letter

ap = argparse.ArgumentParser()
ap.add_argument('original'); ap.add_argument('new')
ap.add_argument('--config', required=True)
ap.add_argument('--stage', choices=['setup', 'coded'], required=True)
a = ap.parse_args()
cfg = json.load(open(a.config)); FW = cfg['framework']
CATS = FW['categories']; MODE = FW['coding_mode'].strip().upper()[0]
EXCL = set(cfg.get('exclusions') or [])
ex_md = os.path.join(os.path.dirname(os.path.abspath(a.config)), 'exclusions.md')
if os.path.exists(ex_md):
    for line in open(ex_md):
        m = re.match(r'\s*\|\s*`?([A-Za-z0-9]+_[A-Za-z]\d+)`?\s*\|', line)
        if m: EXCL.add(m.group(1))

results = []
def check(name, ok, detail=''):
    results.append((name, ok, detail))

wo = load_workbook(a.original); wn = load_workbook(a.new)
check('Original sheets kept, same order', wn.sheetnames[:len(wo.sheetnames)] == wo.sheetnames,
      f'original {wo.sheetnames}, new {wn.sheetnames}')

def item_sheet(wb):
    for ws in wb.worksheets:
        if 'Item_ID' in [c.value for c in ws[1]]: return ws
    return None

for so in wo.worksheets:
    if so.title not in wn.sheetnames: continue
    sn = wn[so.title]; diffs = []
    for row in so.iter_rows():
        for c in row:
            if c.value is not None and sn[c.coordinate].value != c.value:
                diffs.append(c.coordinate)
    check(f'Sheet "{so.title}": original cells unchanged', not diffs, f'{len(diffs)} changed, e.g. {diffs[:5]}' if diffs else '')

io_, in_ = item_sheet(wo), item_sheet(wn)
if io_ is None or in_ is None:
    check('Item sheet found (header row contains Item_ID)', False)
else:
    ho = [c.value for c in io_[1] if c.value is not None]
    hn = [c.value for c in in_[1] if c.value is not None]
    n_orig = len([h for h in ho if h not in CATS])           # columns before the categories
    check('Same number of item rows', io_.max_row == in_.max_row, f'original {io_.max_row - 1}, new {in_.max_row - 1}')
    check('Category headers exact and in order, right after original columns', hn[n_orig:n_orig + len(CATS)] == CATS,
          f'found {hn[n_orig:n_orig + len(CATS)]}')
    idcol = hn.index('Item_ID') + 1
    ids = [in_.cell(r, idcol).value for r in range(2, in_.max_row + 1)]
    ids = [i for i in ids if i is not None]
    check('Item_IDs unique', len(ids) == len(set(ids)), f'{len(ids) - len(set(ids))} duplicates')
    c0 = n_orig + 1; bad_type, bad_val, blank_rows, filled_rows, multi, zero = [], [], [], [], [], []
    for r in range(2, in_.max_row + 1):
        iid = in_.cell(r, idcol).value
        if iid is None: continue
        vals = [in_.cell(r, c0 + k).value for k in range(len(CATS))]
        if all(v is None for v in vals): blank_rows.append(iid); continue
        if any(v is not None for v in vals): filled_rows.append(iid)
        for v in vals:
            if isinstance(v, str): bad_type.append(iid); break
            if v not in (0, 1, None): bad_val.append(iid); break
        if any(v is None for v in vals): bad_val.append(f'{iid} (partly blank)')
        s = sum(v for v in vals if isinstance(v, (int, float)))
        if MODE == 'B' and s > 1: multi.append(iid)
        if s == 0: zero.append(iid)
    if a.stage == 'setup':
        check('All category cells blank', not filled_rows, f'filled: {filled_rows[:10]}')
    else:
        unexpected = [i for i in blank_rows if i not in EXCL]
        check('Every non-excluded row is coded', not unexpected, f'blank but not excluded: {unexpected}')
        check('Excluded rows are blank', all(i in blank_rows for i in EXCL if i in ids),
              f'excluded but coded: {[i for i in EXCL if i in ids and i not in blank_rows]}')
        check('Values are numbers, not text', not bad_type, f'{bad_type[:10]}')
        check('Values are only 0 or 1, no partly blank rows', not bad_val, f'{bad_val[:10]}')
        if MODE == 'B': check('Path B: at most one 1 per row', not multi, f'{multi[:10]}')
        if zero: print(f'NOTE: {len(zero)} rows are all 0 (deliberate "outside framework" items?): {zero}')
    # data validation (warning)
    rng = f'{get_column_letter(c0)}2:{get_column_letter(c0 + len(CATS) - 1)}{in_.max_row}'
    covered = any(get_column_letter(c0) in str(dv.sqref) for dv in in_.data_validations.dataValidation)
    if not covered: print(f'WARNING: no data validation found on the category columns ({rng}).')

w = max(len(n) for n, _, _ in results)
for n, ok, d in results:
    print(f'{"PASS" if ok else "FAIL"}  {n.ljust(w)}  {d if not ok else ""}')
fails = sum(not ok for _, ok, _ in results)
print(f'\n{len(results) - fails}/{len(results)} checks passed.')
sys.exit(1 if fails else 0)
