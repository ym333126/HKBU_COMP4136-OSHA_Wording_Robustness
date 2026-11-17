"""Per gold-class (A-G) x model: accuracy pooled over all 9 round-1+round-2 conditions (original
scoring, no-answer=wrong) with 95% Wilson CI; accuracy on orig only with its own CI; top-3
gold->pred mismatch pairs. Does not modify any existing file.
Usage: python analysis/per_class_r2.py (run from the osha_kit folder)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from collections import Counter
import pandas as pd
from score_osha import wilson

LET = 'ABCDEFG'

df = pd.read_csv('scored_r2.csv')
models = sorted(df.model.unique())

lines = ['# per_class_r2\n',
         '모델 x 유형(A-G): 1차+2차 9개 조건을 합친 정확도(원본 채점, no-answer=오답)와 orig 조건만의 정확도, '
         '95% Wilson CI, 가장 많이 틀린 (정답->오답) 상위 3개.\n']

for m in models:
    g = df[df.model == m]
    lines.append(f'\n## {m}\n')
    lines.append('| 유형 | 전체(9조건) n | 전체 정확도 | 95% CI | orig n | orig 정확도 | 95% CI | 가장 많이 틀린 정답->오답 top3 |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for letter in LET:
        gc = g[g.gold == letter]
        if len(gc) == 0:
            continue
        n_all = len(gc); k_all = int(gc.correct.sum()); acc_all = k_all / n_all
        lo_all, hi_all = wilson(k_all, n_all)

        go = gc[gc.cond == 'orig']
        n_o = len(go); k_o = int(go.correct.sum())
        if n_o:
            acc_o = k_o / n_o; lo_o, hi_o = wilson(k_o, n_o)
            orig_cell = f'{n_o} | {acc_o:.3f} | {lo_o:.2f}-{hi_o:.2f}'
        else:
            orig_cell = '0 | - | -'

        wrong = gc[gc.correct == 0]
        cnt = Counter(wrong.pred)
        top3 = cnt.most_common(3)
        top3_s = ', '.join(f'{letter}->{p} ({c})' for p, c in top3) if top3 else '(없음)'

        lines.append(f'| {letter} | {n_all} | {acc_all:.3f} | {lo_all:.2f}-{hi_all:.2f} | {orig_cell} | {top3_s} |')

open('analysis/per_class_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/per_class_r2.md')
