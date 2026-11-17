"""Lenient scoring: a reply whose entire content (stripped of leading/trailing whitespace) is a
single letter A-G is accepted as that letter. Everything else uses score_osha.py's own
final_letter (the 'FINAL ANSWER: <letter>' regex). All other scoring rules (gold, Wilson CI,
McNemar exact, broken/fixed, answer-changed, no-answer) match score_osha.py / score_r2.py.
Does not modify score_osha.py or score_r2.py (only imports from them).
Usage: python analysis/lenient_r2.py (run from the osha_kit folder)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import json
import pandas as pd
from score_osha import final_letter, wilson
from score_r2 import mcnemar_exact

ORDER = ['orig', 'orig2', 'symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']
LETTERS = set('ABCDEFG')


def is_single_letter(reply):
    s = (reply or '').strip()
    return len(s) == 1 and s.upper() in LETTERS


def lenient_letter(reply):
    if is_single_letter(reply):
        return reply.strip().upper()
    return final_letter(reply)


gold = {}
for fn in ('dataset_osha.jsonl', 'dataset_osha_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        gold[r['id']] = r

rows = []
for fn in ('results.jsonl', 'results_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        g = gold[r['id']]
        pred = lenient_letter(r['reply'])
        rows.append(dict(model=r['model'], id=r['id'], bid=g['bid'], cond=g['cond'], gold=g['gold'],
                          pred=pred or 'NONE', correct=int(pred == g['gold']), single=is_single_letter(r['reply']),
                          single_correct=(is_single_letter(r['reply']) and r['reply'].strip().upper() == g['gold'])))

df = pd.DataFrame(rows)
models = sorted(df.model.unique())

lines = ['# lenient_r2\n',
         "관대한 채점: 응답 전체(앞뒤 공백 제외)가 A-G 한 글자면 그 글자로 인정. 그 외는 score_osha.py의 "
         "'FINAL ANSWER: <letter>' 규칙과 동일. score_osha.py, score_r2.py는 수정하지 않고 import만 함.\n"]

# ---- table 1: single-letter-only replies, count + match rate, per model x cond ----
lines.append('## 글자 하나만 있는 응답 (모델 x 조건)\n')
lines.append('| 모델 | 조건 | 전체 n | 글자 하나만 응답한 건수 | 그 글자가 정답과 일치한 비율 |')
lines.append('|---|---|---|---|---|')
for m in models:
    g = df[df.model == m]
    for c in ORDER:
        x = g[g.cond == c]
        if len(x) == 0:
            continue
        n_single = int(x['single'].sum())
        rate = (x.loc[x['single'], 'single_correct'].mean() if n_single else float('nan'))
        rate_s = f'{rate:.3f}' if n_single else '-'
        lines.append(f'| {m} | {c} | {len(x)} | {n_single} | {rate_s} |')

# ---- table 2: results_tables_r2.md-equivalent, lenient scoring ----
lines.append('\n## 모델 x 9개 조건, 관대한 채점 기준\n')
for m in models:
    g = df[df.model == m]
    p = g.pivot(index='bid', columns='cond', values='correct')
    pr = g.pivot(index='bid', columns='cond', values='pred')
    if 'orig' not in p.columns:
        continue
    lines.append(f'\n### {m}\n')
    lines.append('| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|')
    for c in ORDER:
        if c not in p.columns:
            continue
        x = g[g.cond == c]
        n = len(x); k = int(x.correct.sum()); acc = k / n; lo, hi = wilson(k, n)
        na = (x.pred == 'NONE').mean()
        if c == 'orig':
            lines.append(f'| {c} | {n} | {acc:.3f} | {lo:.2f}-{hi:.2f} | - | - | - | - | - | {na:.3f} |')
        else:
            both = p[['orig', c]].dropna()
            b = int(((both['orig'] == 1) & (both[c] == 0)).sum())
            f = int(((both['orig'] == 0) & (both[c] == 1)).sum())
            mp = mcnemar_exact(b, f)
            pp = pr[['orig', c]].dropna()
            ch = int((pp['orig'] != pp[c]).sum())
            lines.append(f'| {c} | {n} | {acc:.3f} | {lo:.2f}-{hi:.2f} | {b} | {f} | {mp:.4f} | {ch} | {ch/len(pp):.3f} | {na:.3f} |')

open('analysis/lenient_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/lenient_r2.md')
