"""Two follow-up tables, no interpretation. Does not modify any existing file.
1) analysis/mixed_cases_r2.md  - bids where orig was correct and mixed was wrong, per model; bids broken in >=2 models shown together with both texts.
2) analysis/noanswer_cases_r2.md - gpt-4o-mini NONE replies under mixed/korean/heavy (id, cond, first 150 chars, has-Hangul), plus NONE counts for orig/orig2/typos.
Usage: python analysis/generate_followup_r2.py  (run from the osha_kit folder)
"""
import json, re
import pandas as pd

df = pd.read_csv('scored_r2.csv')
models = sorted(df.model.unique())

dataset = {}
for fn in ('dataset_osha.jsonl', 'dataset_osha_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        dataset[r['id']] = r

raw = {}
for fn in ('results.jsonl', 'results_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        raw[(r['id'], r['model'])] = r['reply']

HANGUL = re.compile(r'[가-힣]')

# ---------------- 1) mixed_cases_r2.md ----------------
per_model_broken = {}
pivots = {}
for m in models:
    g = df[df.model == m]
    pred = g.pivot(index='bid', columns='cond', values='pred')
    corr = g.pivot(index='bid', columns='cond', values='correct')
    pivots[m] = (pred, corr)
    if 'orig' not in corr.columns or 'mixed' not in corr.columns:
        per_model_broken[m] = []
        continue
    bids = corr.index[(corr['orig'] == 1) & (corr['mixed'] == 0)].tolist()
    per_model_broken[m] = bids

lines = ['# mixed_cases_r2\n', "orig는 맞았고 mixed는 틀린 문항(bid), 모델별.\n"]
for m in models:
    bids = per_model_broken[m]
    lines.append(f'\n## {m} (n={len(bids)})\n')
    if not bids:
        lines.append('(없음)\n')
        continue
    lines.append('| bid | orig pred | mixed pred | gold |')
    lines.append('|---|---|---|---|')
    pred, _ = pivots[m]
    for bid in bids:
        gold = dataset[f'{bid}_orig']['gold']
        lines.append(f'| {bid} | {pred.loc[bid, "orig"]} | {pred.loc[bid, "mixed"]} | {gold} |')

bid_to_models = {}
for m, bids in per_model_broken.items():
    for bid in bids:
        bid_to_models.setdefault(bid, []).append(m)
shared = {bid: ms for bid, ms in bid_to_models.items() if len(ms) >= 2}

lines.append('\n## 2개 이상 모델에서 orig->mixed로 깨진 bid\n')
if not shared:
    lines.append('(없음)\n')
else:
    for bid, ms in sorted(shared.items()):
        gold = dataset[f'{bid}_orig']['gold']
        orig_text = dataset[f'{bid}_orig']['report']
        mixed_text = dataset[f'{bid}_mixed']['report']
        lines.append(f'\n### {bid} (깨진 모델: {", ".join(ms)})\n')
        lines.append(f'- 원문(orig): {orig_text}')
        lines.append(f'- 변형 문장(mixed): {mixed_text}')
        lines.append(f'- 정답: {gold}\n')
        lines.append('| 모델 | orig pred | mixed pred |')
        lines.append('|---|---|---|')
        for m in models:
            pred, _ = pivots[m]
            if bid in pred.index and 'orig' in pred.columns and 'mixed' in pred.columns:
                lines.append(f'| {m} | {pred.loc[bid, "orig"]} | {pred.loc[bid, "mixed"]} |')

open('analysis/mixed_cases_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/mixed_cases_r2.md')

# ---------------- 2) noanswer_cases_r2.md ----------------
TARGET_MODEL = 'openai:gpt-4o-mini'
LIST_CONDS = ['mixed', 'korean', 'heavy']
COUNT_CONDS = ['orig', 'orig2', 'typos']

g = df[df.model == TARGET_MODEL]

lines2 = ['# noanswer_cases_r2\n', f'모델: {TARGET_MODEL}\n']
lines2.append(f'\n## {"/".join(LIST_CONDS)} 조건의 NONE 응답 전체\n')
lines2.append('| id | 조건 | reply 앞 150자 | 한글 포함 |')
lines2.append('|---|---|---|---|')
none_rows = g[(g.cond.isin(LIST_CONDS)) & (g.pred == 'NONE')].sort_values(['cond', 'id'])
for _, r in none_rows.iterrows():
    reply = raw.get((r['id'], TARGET_MODEL), '')
    snippet = reply[:150].replace('\n', ' ').replace('|', '\\|')
    has_kr = 'Y' if HANGUL.search(reply) else 'N'
    lines2.append(f'| {r["id"]} | {r["cond"]} | {snippet} | {has_kr} |')

lines2.append(f'\n## {", ".join(COUNT_CONDS)} 조건의 NONE 개수\n')
lines2.append('| 조건 | NONE 개수 | 전체 n |')
lines2.append('|---|---|---|')
for c in COUNT_CONDS:
    gc = g[g.cond == c]
    lines2.append(f'| {c} | {(gc.pred == "NONE").sum()} | {len(gc)} |')

open('analysis/noanswer_cases_r2.md', 'w', encoding='utf-8').write('\n'.join(lines2) + '\n')
print('wrote analysis/noanswer_cases_r2.md')
