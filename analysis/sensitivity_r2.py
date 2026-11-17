"""Sensitivity check: redo accuracy / 95% Wilson CI / broken-fixed vs orig / exact McNemar p
after dropping narratives where pred is NONE in round-1 orig OR in the condition being compared, per model.
Does not modify score_r2.py, score_osha.py, or any scored/results file.
Reads scored_r2.csv (written by score_r2.py). Usage: python analysis/sensitivity_r2.py
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pandas as pd
from score_osha import wilson
from score_r2 import mcnemar_exact, ORDER

CONDS = [c for c in ORDER if c != 'orig']

df = pd.read_csv('scored_r2.csv')
models = sorted(df.model.unique())

rows = []
for m in models:
    g = df[df.model == m]
    pred = g.pivot(index='bid', columns='cond', values='pred')
    corr = g.pivot(index='bid', columns='cond', values='correct')
    if 'orig' not in pred.columns:
        continue
    for c in CONDS:
        if c not in pred.columns:
            continue
        mask = (pred['orig'] != 'NONE') & (pred[c] != 'NONE')
        sub = corr.loc[mask, ['orig', c]].dropna()
        n = len(sub)
        if n:
            k = int(sub[c].sum())
            acc = k / n
            lo, hi = wilson(k, n)
            b = int(((sub['orig'] == 1) & (sub[c] == 0)).sum())
            f = int(((sub['orig'] == 0) & (sub[c] == 1)).sum())
            p = mcnemar_exact(b, f)
        else:
            k = 0; acc = float('nan'); lo = hi = float('nan'); b = f = 0; p = float('nan')
        rows.append(dict(model=m, cond=c, n=n, n_excluded=len(pred) - n, k=k, acc=acc, ci_lo=lo, ci_hi=hi,
                          broken=b, fixed=f, mcnemar_p=p))

out = pd.DataFrame(rows)
out.to_csv('analysis/sensitivity_r2.csv', index=False)

lines = ['# sensitivity_r2\n',
         '모델×조건별로, round-1 orig 또는 해당 조건에서 pred=NONE인 문항(같은 bid)을 제외한 뒤 재계산.\n']
for m in models:
    gm = out[out.model == m]
    if gm.empty:
        continue
    lines.append(f'\n## {m}\n')
    lines.append('| 조건 | n(제외 후) | 제외된 문항 수 | 정확도 | 95% CI | broken | fixed | McNemar p |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for c in CONDS:
        r = gm[gm.cond == c]
        if r.empty:
            continue
        r = r.iloc[0]
        if r['n'] == 0:
            lines.append(f'| {c} | 0 | {int(r["n_excluded"])} | - | - | - | - | - |')
        else:
            lines.append(f'| {c} | {int(r["n"])} | {int(r["n_excluded"])} | {r["acc"]:.3f} | {r["ci_lo"]:.2f}-{r["ci_hi"]:.2f} | '
                          f'{int(r["broken"])} | {int(r["fixed"])} | {r["mcnemar_p"]:.4f} |')

open('analysis/sensitivity_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/sensitivity_r2.md and analysis/sensitivity_r2.csv')
