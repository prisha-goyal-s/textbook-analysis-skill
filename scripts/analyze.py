#!/usr/bin/env python3
"""Stage 4 descriptive analysis for textbook-analysis-skill.

Usage:
    python analyze.py --config skill_run/config.json [--out OUTPUT_FOLDER]

Everything project-specific (books, item types, categories, groups, coding mode,
exclusions, palette, font) comes from config.json. See config_example.json.
Path A = multi-label 0/1; Path B = exactly one category per item.
"""
import argparse, json, math, os, re, sys, warnings
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ------------------------------------------------------------------ config
ap = argparse.ArgumentParser()
ap.add_argument('--config', required=True)
ap.add_argument('--out', help='output folder (default: <output_dir>/Analysis)')
args = ap.parse_args()
CFG_PATH = os.path.abspath(args.config)
cfg = json.load(open(CFG_PATH))
# project root = folder that contains skill_run/ (or the config's own folder)
cfg_dir = os.path.dirname(CFG_PATH)
ROOT = os.path.dirname(cfg_dir) if os.path.basename(cfg_dir) == 'skill_run' else cfg_dir
def resolve(p): return p if os.path.isabs(os.path.expanduser(p)) else os.path.join(ROOT, p)
OUTDIR = os.path.expanduser(cfg.get('output_dir') or ROOT)
OUT = os.path.abspath(args.out) if args.out else os.path.join(resolve(OUTDIR), 'Analysis')
FIG = os.path.join(OUT, 'figures'); os.makedirs(FIG, exist_ok=True)

FW = cfg['framework']; MODE = FW['coding_mode'].strip().upper()[0]   # 'A' or 'B'
assert MODE in 'AB', 'framework.coding_mode must be "A" or "B"'
SHORTFW = FW['short']
CATS = list(FW['categories'])
GROUPS = {g: list(c) for g, c in (FW.get('category_groups') or {}).items()}
for g, cs in GROUPS.items():
    missing = [c for c in cs if c not in CATS]
    assert not missing, f'category_groups[{g}] lists unknown categories: {missing}'
LEVELS = FW.get('level_order') or []           # Path B only, optional
THRESH = FW.get('higher_demand_threshold')
BOOKS = [b['code'] for b in cfg['books']]; BNAME = {b['code']: b['name'] for b in cfg['books']}
TYPES = [t['name'] for t in cfg['item_types']]
PL = {t['name']: t.get('plural') or (t['name'] + 's' if not t['name'].endswith('y') else t['name'][:-1] + 'ies') for t in cfg['item_types']}
AN = cfg.get('analysis', {})
REF = (AN.get('comparison') or {}).get('reference', BOOKS[0])
CMP = (AN.get('comparison') or {}).get('compare', [b for b in BOOKS if b != REF])
CMP = [CMP] if isinstance(CMP, str) else list(CMP)
FORMATS = AN.get('figure_formats') or ['png', 'pdf']; DPI = AN.get('dpi', 300)

# ------------------------------------------------------------------ style
def pick_font(wanted):
    have = {f.name for f in fm.fontManager.ttflist}
    for f in [wanted, 'Helvetica Neue', 'Helvetica', 'Arial', 'Liberation Sans', 'DejaVu Sans']:
        if f and f in have: return f
    return 'sans-serif'
FONT = pick_font(AN.get('font', 'Helvetica Neue'))
if FONT != AN.get('font', 'Helvetica Neue'): print(f'NOTE: font "{AN.get("font","Helvetica Neue")}" not found; using "{FONT}".')
plt.rcParams.update({'font.family': FONT, 'font.size': 10, 'axes.titlesize': 12, 'axes.titleweight': 'bold',
    'axes.labelsize': 10, 'axes.spines.top': False, 'axes.spines.right': False, 'axes.edgecolor': '#444',
    'axes.linewidth': 0.8, 'xtick.color': '#333', 'ytick.color': '#333', 'pdf.fonttype': 42,
    'svg.fonttype': 'none', 'savefig.dpi': DPI})

def get_cmap(name):
    name = (name or 'batlow').strip()
    try:
        import cmcrameri.cm as cmc
        if hasattr(cmc, name.lower()): return getattr(cmc, name.lower())
    except ImportError:
        if name.lower() in ('batlow', 'crameri batlow', "crameri's batlow"):
            print('NOTE: cmcrameri not installed (pip install cmcrameri); falling back to viridis.')
            return plt.get_cmap('viridis')
    try: return plt.get_cmap(name)
    except ValueError:
        print(f'NOTE: palette "{name}" not recognised; using viridis.'); return plt.get_cmap('viridis')
CMAP = get_cmap(re.sub(r"(?i)crameri'?s?\s*", '', AN.get('palette', 'batlow')))
pos = [0.18, 0.68] if len(BOOKS) == 2 else list(np.linspace(0.1, 0.85, len(BOOKS)))
COL = {b: CMAP(p) for b, p in zip(BOOKS, pos)}

# ------------------------------------------------------------------ data
def exclusion_ids():
    ids = set(cfg.get('exclusions') or [])
    p = os.path.join(ROOT, 'skill_run', 'exclusions.md')
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r'\s*\|\s*`?([A-Za-z0-9]+_[A-Za-z]\d+)`?\s*\|', line)
            if m: ids.add(m.group(1))
    return ids
EXCL = exclusion_ids()

def load_book(b):
    f = resolve(b['classified_file'])
    x = pd.ExcelFile(f)
    sheet = b.get('sheet') or next(s for s in x.sheet_names if 'Item_ID' in pd.read_excel(x, s, nrows=0).columns)
    df = pd.read_excel(x, sheet)
    miss = [c for c in CATS if c not in df.columns]
    assert not miss, f'{f}: missing category columns {miss}'
    df['Book'] = b['code']; return df

frames, dropped = [], []
for b in cfg['books']:
    df = load_book(b)
    ex = df[df.Item_ID.isin(EXCL)]
    blank = df[~df.Item_ID.isin(EXCL) & df[CATS].isna().any(axis=1)]
    for _, r in ex.iterrows(): dropped.append((r.Item_ID, 'listed in exclusions'))
    for _, r in blank.iterrows(): dropped.append((r.Item_ID, 'blank category cells (NOT in exclusions list: check this)'))
    df = df.drop(ex.index.union(blank.index))
    bad = ~df[CATS].isin([0, 1])
    assert not bad.any().any(), f'{b["code"]}: non-0/1 values in rows {list(df.Item_ID[bad.any(axis=1)])}'
    frames.append(df)
D = pd.concat(frames, ignore_index=True); D[CATS] = D[CATS].astype(int)
unknown_types = set(D.Item_Type) - set(TYPES)
assert not unknown_types, f'Item_Type values not in config item_types: {unknown_types}'
if MODE == 'B':
    multi = D[D[CATS].sum(axis=1) > 1]
    assert multi.empty, f'Path B but these items have more than one 1: {list(multi.Item_ID)}'
N = {(b, t): int(((D.Book == b) & (D.Item_Type == t)).sum()) for b in BOOKS for t in TYPES}
TYPES = [t for t in TYPES if any(N[(b, t)] for b in BOOKS)]
for (b, t), n in N.items():
    if t in TYPES and n == 0: print(f'NOTE: {BNAME[b]} has no {PL[t]}.')
def grp(b, t): return D[(D.Book == b) & (D.Item_Type == t)]
def pct(k, n): return round(100 * k / n, 1) if n else float('nan')
group_of = {c: g for g, cs in GROUPS.items() for c in cs}
def short(c):
    g = group_of.get(c)
    return c[len(g) + 3:] if g and c.startswith(g + ' - ') else c
SHORT = [short(c) for c in CATS]
print('N per group:', {f'{BNAME[b]} {PL[t]}': N[(b, t)] for b in BOOKS for t in TYPES})
print('Left out:', dropped or 'none')

# ------------------------------------------------------------------ tables
T = {}   # sheet name -> DataFrame
rows = []
for t in TYPES:
    for b in BOOKS:
        g = grp(b, t)
        for c in CATS:
            k = int(g[c].sum())
            rows.append(dict(Item_Type=PL[t], Textbook=BNAME[b], Group=group_of.get(c, ''), Category=short(c),
                             Items_Coded_1=k, Eligible_Items=len(g), Percent=pct(k, len(g))))
        if MODE == 'B':
            k = int((g[CATS].sum(axis=1) == 0).sum())
            if k: rows.append(dict(Item_Type=PL[t], Textbook=BNAME[b], Group='', Category='No category (outside framework)',
                                   Items_Coded_1=k, Eligible_Items=len(g), Percent=pct(k, len(g))))
T1 = pd.DataFrame(rows)
if not GROUPS: T1 = T1.drop(columns='Group')
T['1_Category_Prevalence' if MODE == 'A' else '1_Level_Distribution'] = T1

W = T1.pivot_table(index='Category', columns=['Item_Type', 'Textbook'], values='Percent', sort=False)
W = W.fillna(0.0)   # a book with no items in a row (e.g. 'No category') counts as 0%
for t in TYPES:
    for c in CMP:
        W[(PL[t], f'Difference ({BNAME[c]} − {BNAME[REF]}, pp)')] = (W[(PL[t], BNAME[c])] - W[(PL[t], BNAME[REF])]).round(1)
W = W[[col for t in TYPES for col in W.columns if col[0] == PL[t]]]
T['2_Heatmap_Matrix'] = W

for g, cs in GROUPS.items(): D['GRP_' + g] = (D[cs].sum(axis=1) > 0).astype(int)
if GROUPS:
    rows = []
    for t in TYPES:
        for b in BOOKS:
            gg = grp(b, t)
            for g in GROUPS:
                k = int(gg['GRP_' + g].sum())
                rows.append(dict(Item_Type=PL[t], Textbook=BNAME[b], Category_Group=g, Items_In_Group=k,
                                 Eligible_Items=len(gg), Percent=pct(k, len(gg))))
    T3 = pd.DataFrame(rows); T['3_Group_Prevalence' if MODE == 'A' else '3_Group_Distribution'] = T3

D['n_labels'] = D[CATS].sum(axis=1)
BINS = ['0', '1', '2', '3', '4+']
D['label_bin'] = D.n_labels.map(lambda x: '4+' if x >= 4 else str(x))
if MODE == 'A':
    rows = []
    for t in TYPES:
        for b in BOOKS:
            g = grp(b, t)
            for bn in BINS:
                k = int((g.label_bin == bn).sum())
                rows.append(dict(Item_Type=PL[t], Textbook=BNAME[b], Positive_Labels=bn, Items=k, Eligible_Items=len(g), Percent=pct(k, len(g))))
    T4 = pd.DataFrame(rows); T['4_Labels_per_Item'] = T4
    T['4b_Labels_Summary'] = pd.DataFrame([dict(Item_Type=PL[t], Textbook=BNAME[b], Eligible_Items=len(grp(b, t)),
        Mean_Labels=round(grp(b, t).n_labels.mean(), 2), Median_Labels=grp(b, t).n_labels.median(),
        Max_Labels=int(grp(b, t).n_labels.max()) if len(grp(b, t)) else np.nan) for t in TYPES for b in BOOKS])
    for t in TYPES:
        for b in BOOKS:
            assert T4[(T4.Item_Type == PL[t]) & (T4.Textbook == BNAME[b])].Items.sum() == N[(b, t)]
else:
    for t in TYPES:
        for b in BOOKS:
            s = T1[(T1.Item_Type == PL[t]) & (T1.Textbook == BNAME[b])].Items_Coded_1.sum()
            assert s == N[(b, t)], f'{b} {t}: level counts {s} != N {N[(b,t)]}'
    if LEVELS:
        assert sorted(LEVELS) == sorted(CATS), 'level_order must list every category exactly once'
        D['level'] = D[LEVELS].values.argmax(axis=1) + 1
        D.loc[D[CATS].sum(axis=1) == 0, 'level'] = np.nan
        thr = LEVELS.index(THRESH) + 1 if THRESH else None
        rows = []
        for t in TYPES:
            for b in BOOKS:
                g = grp(b, t); lv = g.level.dropna()
                r = dict(Item_Type=PL[t], Textbook=BNAME[b], Items_With_Level=len(lv),
                         Mean_Level=round(lv.mean(), 2), Median_Level=lv.median())
                if thr:
                    k = int((lv >= thr).sum()); r.update({f'Items_at_or_above_{THRESH}': k, 'Percent_Higher_Demand': pct(k, len(lv))})
                rows.append(r)
        T4 = pd.DataFrame(rows); T['4_Ordinal_Summary'] = T4

# ------------------------------------------------------------------ workbook
groups_txt = '; '.join(f'{BNAME[b]} {PL[t]}: {N[(b,t)]}' for t in TYPES for b in BOOKS)
method = [
    ('Framework', f'{FW.get("name", SHORTFW)} ({FW.get("doc", "")})'),
    ('Coding mode', 'Path A: multi-label 0/1 (an item can have several categories)' if MODE == 'A'
                    else 'Path B: single level (exactly one category per item)'),
    ('Sources', '; '.join(os.path.basename(b['classified_file']) for b in cfg['books'])),
    ('Groups', 'Each textbook × item type is analysed separately; item types are never combined.'),
    ('Eligible items (N)', groups_txt),
    ('Left out', '; '.join(f'{i}: {r}' for i, r in dropped) or 'none'),
    ('Percent formula', 'Percent = items coded 1 ÷ eligible items in the group × 100' +
        ('. Items can have several labels, so category percentages can add up to more than 100%.' if MODE == 'A'
         else '. Each item has one category, so percentages add up to 100%.')),
]
if GROUPS: method.append(('Category groups', '; '.join(f'{g} = 1 if any of: {", ".join(short(c) for c in cs)}' for g, cs in GROUPS.items())
                          + ('. An item counts once per group.' if MODE == 'A' else '')))
if MODE == 'A': method.append(('Labels per item', f'Sum of the {len(CATS)} binary values per item, grouped 0, 1, 2, 3, 4+.'))
if MODE == 'B' and LEVELS: method.append(('Level order', ' < '.join(LEVELS) + (f'; higher demand = {THRESH} and above' if THRESH else '')))
if len(BOOKS) > 1: method.append(('Differences', ', '.join(f'{BNAME[c]} − {BNAME[REF]}' for c in CMP) + ', in percentage points'))
method.append(('Note', 'Descriptive statistics only; no significance tests. Percentages rounded to 1 decimal place.'))
derived = ['Book', 'Item_ID', 'Item_Type'] + ['GRP_' + g for g in GROUPS] + (['n_labels'] if MODE == 'A' else []) + (['level'] if MODE == 'B' and LEVELS else [])
XLSX = os.path.join(OUT, f'{SHORTFW}_Prevalence_Analysis.xlsx')
with pd.ExcelWriter(XLSX) as xw:
    pd.DataFrame(method, columns=['Item', 'Detail']).to_excel(xw, sheet_name='Method', index=False)
    for name, df in T.items(): df.to_excel(xw, sheet_name=name[:31], index=(name == '2_Heatmap_Matrix'))
    D[derived].rename(columns=lambda c: c[4:] if c.startswith('GRP_') else c).to_excel(xw, sheet_name='Item_Level_Derived', index=False)

# ------------------------------------------------------------------ figures
def save(fig, name):
    for ext in FORMATS:
        fig.savefig(os.path.join(FIG, f'{name}.{ext}'), bbox_inches='tight', facecolor='white')
    plt.close(fig)
def legend(ax, t, **kw):
    ax.legend([plt.Rectangle((0, 0), 1, 1, color=COL[b]) for b in BOOKS], [f'{BNAME[b]} (n = {N[(b, t)]})' for b in BOOKS], frameon=False, **kw)
AB = 'abcdefghijklmnopqrstuvwxyz'
def vals(df, t, b, col='Percent', key='Category', order=None):
    s = df[(df.Item_Type == PL[t]) & (df.Textbook == BNAME[b])].set_index(key)[col]
    return s.reindex(order).fillna(0).values if order is not None else s.values

ROWLAB = list(T1.Category.drop_duplicates())        # categories (+ "No category" in Path B if any)
# contiguous group bands for figure separators
bands = []
if GROUPS:
    labs = [group_of.get(c, '') for c in CATS]
    start = 0
    for i in range(1, len(labs) + 1):
        if i == len(labs) or labs[i] != labs[start]:
            bands.append((labs[start], start, i - 1)); start = i
    if len({b[0] for b in bands}) != len(bands): bands = []   # groups not contiguous: skip bands
nb = len(BOOKS)

# Figure 1: horizontal grouped bars per category
for i, t in enumerate(TYPES):
    n = len(ROWLAB); fig, ax = plt.subplots(figsize=(7.6, max(3.2, 0.32 * n * max(nb, 2) / 2 + 2.6)))
    y = np.arange(n); h = 0.76 / nb
    for j, b in enumerate(BOOKS):
        v = vals(T1, t, b, order=ROWLAB)
        ax.barh(y + (j - (nb - 1) / 2) * h, v, height=h, color=COL[b], edgecolor='white', linewidth=0.5)
        for yy, vv in zip(y + (j - (nb - 1) / 2) * h, v): ax.text(vv + 0.8, yy, f'{vv:.1f}', va='center', fontsize=7.5, color='#333')
    ax.set_yticks(y); ax.set_yticklabels(ROWLAB); ax.invert_yaxis()
    xmax = max(60, np.ceil((T1[T1.Item_Type == PL[t]].Percent.max() + 12) / 10) * 10); ax.set_xlim(0, xmax)
    for gname, a, z in bands:
        if z < n - 1: ax.axhline(z + 0.5, color='#999', lw=0.7, ls=(0, (3, 3)))
        ax.text(xmax * 0.99, (a + z) / 2, gname.upper(), ha='right', va='center', fontsize=8.5, fontweight='bold', color='#777')
    ax.set_xlabel('Items involving the category (%)' if MODE == 'A' else 'Items at this level (%)')
    ax.xaxis.grid(True, color='#e6e6e6', lw=0.6); ax.set_axisbelow(True)
    ax.set_title(f'{SHORTFW} {"category prevalence" if MODE == "A" else "level distribution"}: {PL[t]}', loc='left')
    legend(ax, t, loc='lower right')
    ax.text(0.0, -0.6 / fig.get_size_inches()[1] - 0.04,
            'Items can have several labels, so percentages add up to more than 100%.' if MODE == 'A'
            else 'Each item has one category, so percentages add up to 100%.', fontsize=7.5, color='#666', transform=ax.transAxes)
    save(fig, f'Fig1{AB[i]}_{"Category_Prevalence" if MODE == "A" else "Level_Distribution"}_{PL[t]}')

# Figure 1 (Path B, ordered): 100% stacked bars
if MODE == 'B' and LEVELS:
    for i, t in enumerate(TYPES):
        fig, ax = plt.subplots(figsize=(7.2, 1.2 + 0.55 * nb))
        for j, b in enumerate(BOOKS):
            left = 0
            for k, lv in enumerate(LEVELS):
                v = vals(T1, t, b, order=[short(lv)])[0]; c = CMAP(0.08 + 0.7 * k / max(len(LEVELS) - 1, 1))
                ax.barh(j, v, left=left, color=c, edgecolor='white', height=0.6, label=short(lv) if j == 0 else None)
                rgb = c[:3]; lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
                if v >= 6: ax.text(left + v / 2, j, f'{v:.0f}%', ha='center', va='center', fontsize=7.5, color='black' if lum > 0.55 else 'white')
                left += v
            rest = vals(T1, t, b, order=['No category (outside framework)'])[0]
            if rest > 0:
                ax.barh(j, rest, left=left, color='#bdbdbd', edgecolor='white', height=0.6, label='No category' if 'No category' not in [h.get_label() for h in ax.patches] else None)
        ax.set_yticks(range(nb)); ax.set_yticklabels([f'{BNAME[b]} (n = {N[(b,t)]})' for b in BOOKS]); ax.invert_yaxis()
        ax.set_xlim(0, 100); ax.set_xlabel('Items (%)'); ax.set_title(f'{SHORTFW} levels, lower to higher: {PL[t]}', loc='left')
        ax.legend(ncol=len(LEVELS) + 1, frameon=False, loc='upper center', bbox_to_anchor=(0.5, -0.32), fontsize=8)
        save(fig, f'Fig1{AB[i]}2_Level_Stacked_{PL[t]}')

# Figure 2: heatmap (shared scale across item types) + difference panel
VMAX = max(10, math.ceil(T1.Percent.max() / 10) * 10)
for i, t in enumerate(TYPES):
    M = np.array([[vals(T1, t, b, order=[r])[0] for b in BOOKS] for r in ROWLAB]); n = len(ROWLAB)
    diffpanel = len(BOOKS) > 1 and CMP
    if diffpanel:
        fig, (ax, axd) = plt.subplots(1, 2, figsize=(4.2 + 1.1 * nb, 1.6 + 0.4 * n), gridspec_kw=dict(width_ratios=[nb, 1], wspace=0.06))
    else:
        fig, ax = plt.subplots(figsize=(3.4 + 1.1 * nb, 1.6 + 0.4 * n)); axd = None
    im = ax.imshow(M, cmap=CMAP, vmin=0, vmax=VMAX, aspect='auto')
    for r in range(n):
        for c in range(nb):
            rgb = CMAP(min(M[r, c] / VMAX, 1))[:3]; lum = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]
            ax.text(c, r, f'{M[r, c]:.1f}%', ha='center', va='center', fontsize=8.5, color='black' if lum > 0.55 else 'white')
    ax.set_xticks(range(nb)); ax.set_xticklabels([f'{BNAME[b]}\n(n = {N[(b, t)]})' for b in BOOKS]); ax.xaxis.tick_top()
    ax.set_yticks(range(n)); ax.set_yticklabels(ROWLAB); ax.tick_params(length=0)
    for sp in ax.spines.values(): sp.set_visible(False)
    for _, a, z in bands:
        if z < n - 1:
            ax.axhline(z + 0.5, color='white', lw=2.5)
            if axd is not None: axd.axhline(z + 0.5, color='#bbb', lw=0.8)
    if axd is not None:
        c0 = CMP[0]; diff = M[:, BOOKS.index(c0)] - M[:, BOOKS.index(REF)]; lim = max(abs(diff).max(), 1)
        axd.barh(range(n), diff, color=[COL[c0] if d > 0 else COL[REF] for d in diff], height=0.62)
        for r, d in enumerate(diff):
            axd.text(d + (lim * 0.04 if d >= 0 else -lim * 0.04), r, ('0.0' if abs(d) < 0.05 else f'{d:+.1f}'.replace('-', '−')),
                     va='center', ha='left' if d >= 0 else 'right', fontsize=7.5, color='#333')
        axd.set_ylim(n - 0.5, -0.5); axd.set_xlim(-lim * 1.55, lim * 1.55); axd.axvline(0, color='#444', lw=0.8)
        axd.set_yticks([]); axd.spines['left'].set_visible(False); axd.tick_params(axis='x', labelsize=7.5)
        axd.set_xlabel(f'{BNAME[c0]} − {BNAME[REF]}\n(percentage points)', fontsize=8.5); axd.xaxis.set_label_position('top'); axd.xaxis.tick_top()
        axd.spines['bottom'].set_visible(False); axd.spines['top'].set_visible(True)
    cb = fig.colorbar(im, ax=[ax, axd] if axd is not None else ax, orientation='horizontal', fraction=0.035, pad=0.03, aspect=40)
    cb.set_label(f'Percent of items; scale capped at {VMAX}%, the same for every item type', fontsize=8.5)
    cb.outline.set_visible(False); cb.ax.tick_params(labelsize=7.5)
    fig.suptitle(f'{SHORTFW} {"category prevalence" if MODE == "A" else "level distribution"} heatmap: {PL[t]}', x=0.02, ha='left', fontsize=12, y=0.99)
    save(fig, f'Fig2{AB[i]}_Heatmap_{PL[t]}')

def grouped(cats, v, k, t, title, xlabel, ylabel, name, ylim=None, note=None):
    fig, ax = plt.subplots(figsize=(max(6.6, 1.1 * len(cats) * nb / 2 + 2.2), 4.4)); x = np.arange(len(cats)); w = 0.76 / nb
    for j, b in enumerate(BOOKS):
        xs = x + (j - (nb - 1) / 2) * w
        ax.bar(xs, v[b], width=w, color=COL[b], edgecolor='white', linewidth=0.5)
        for xx, vv, kk in zip(xs, v[b], k[b]): ax.text(xx, vv + 1.2, f'{vv:.1f}%\n({kk})', ha='center', va='bottom', fontsize=7.5, color='#333', linespacing=1.1)
    ax.set_xticks(x); ax.set_xticklabels(cats); ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_ylim(0, ylim or 100); ax.set_yticks(np.arange(0, min(ylim or 100, 100) + 1, 10 if (ylim or 100) <= 80 else 20))
    ax.yaxis.grid(True, color='#e6e6e6', lw=0.6); ax.set_axisbelow(True)
    ax.set_title(title, loc='left'); legend(ax, t, loc='upper right')
    if note: ax.text(0, -0.18, note, va='top', transform=ax.transAxes, fontsize=7.5, color='#666')
    save(fig, name)

# Figure 3: category groups
if GROUPS:
    for i, t in enumerate(TYPES):
        s = T3[T3.Item_Type == PL[t]]
        grouped(list(GROUPS), {b: s[s.Textbook == BNAME[b]].Percent.values for b in BOOKS},
                {b: s[s.Textbook == BNAME[b]].Items_In_Group.values for b in BOOKS}, t,
                f'{SHORTFW} category groups: {PL[t]}', 'Category group', 'Items in the group (%)',
                f'Fig3{AB[i]}_Group_{"Prevalence" if MODE == "A" else "Distribution"}_{PL[t]}', ylim=110,
                note=("An item counts once per group if any of that group's categories = 1.\n"
                      "Items can be in several groups, so percentages add up to more than 100%.") if MODE == 'A'
                     else 'Each item is in exactly one group (the group of its category).')

# Figure 4: labels per item (A) or higher-demand share (B, ordered)
if MODE == 'A':
    for i, t in enumerate(TYPES):
        s = T4[T4.Item_Type == PL[t]]; top = s.Percent.max()
        grouped(BINS, {b: s[s.Textbook == BNAME[b]].Percent.values for b in BOOKS}, {b: s[s.Textbook == BNAME[b]].Items.values for b in BOOKS},
                t, f'Number of {SHORTFW} categories per item: {PL[t]}', f'Positive labels per item (of {len(CATS)})', 'Items (%)',
                f'Fig4{AB[i]}_Labels_per_Item_{PL[t]}', ylim=min(100, np.ceil((top + 14) / 10) * 10),
                note=f'Labels per item = the sum of its {len(CATS)} binary values. Bar labels show % (n).')
elif LEVELS and THRESH:
    for i, t in enumerate(TYPES):
        s = T4[T4.Item_Type == PL[t]]
        grouped([f'{THRESH} and above'], {b: s[s.Textbook == BNAME[b]].Percent_Higher_Demand.values for b in BOOKS},
                {b: s[s.Textbook == BNAME[b]][f'Items_at_or_above_{THRESH}'].values for b in BOOKS}, t,
                f'Higher-demand items ({THRESH}+): {PL[t]}', '', 'Items (%)', f'Fig4{AB[i]}_Higher_Demand_{PL[t]}', ylim=110,
                note='Mean and median levels are in the 4_Ordinal_Summary sheet.')

print(f'\nWrote {XLSX}\nFigures in {FIG}')
for name, df in T.items():
    print(f'\n== {name}'); print(df.to_string())
