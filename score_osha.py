"""Score results.jsonl for the OSHA event-class benchmark.
usage: python score_osha.py [dataset_osha.jsonl] [results.jsonl]
Writes scored_osha.csv and prints: accuracy by model x condition (with 95% Wilson CI), paired change vs. original text,
accuracy by class x condition, and confusion matrices per model."""
import json, re, sys, math
import pandas as pd
LET = 'ABCDEFG'
def final_letter(reply):
    m = re.findall(r'FINAL ANSWER:\s*\**\s*\(?([A-Ga-g])\b', reply or '', flags=re.I)
    return m[-1].upper() if m else None
def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d
def main(data='dataset_osha.jsonl', res='results.jsonl'):
    gold = {r['id']: r for r in map(json.loads, open(data, encoding='utf-8'))}
    out = []
    for r in map(json.loads, open(res, encoding='utf-8')):
        g = gold[r['id']]; pred = final_letter(r['reply'])
        out.append(dict(model=r['model'], id=r['id'], bid=g['bid'], cond=g['cond'], gold=g['gold'], pred=pred or 'NONE',
                        correct=int(pred == g['gold'])))
    df = pd.DataFrame(out); df.to_csv('scored_osha.csv', index=False)
    pd.set_option('display.width', 180); pd.set_option('display.max_columns', 30)
    order = ['orig', 'symbols', 'mixed', 'plain', 'jargon']
    print('== accuracy by model x condition  [acc (95% CI), n per cell]')
    for m, g in df.groupby('model'):
        print(f'\n{m}')
        for c in order:
            x = g[g.cond == c]
            if len(x): lo, hi = wilson(x.correct.sum(), len(x)); print(f'  {c:8s} {x.correct.mean():.3f}  ({lo:.2f}-{hi:.2f})  n={len(x)}')
        print(f'  no-answer rate: {(g.pred == "NONE").mean():.3f}')
    print('\n== paired change vs. original text (same narrative; + = fixed, - = broken)')
    for m, g in df.groupby('model'):
        p = g.pivot(index='bid', columns='cond', values='correct')
        if 'orig' not in p: continue
        for c in order[1:]:
            if c in p:
                d = p[c] - p['orig']; print(f'  {m:28s} {c:8s} mean diff {d.mean():+.3f}  (broken {int((d<0).sum())}, fixed {int((d>0).sum())})')
    print('\n== accuracy by true class x condition')
    print(df.groupby(['model', 'gold', 'cond']).correct.mean().unstack('cond').reindex(columns=order).round(2))
    for m, g in df.groupby('model'):
        print(f'\n== confusion matrix (rows=gold, cols=pred), all conditions: {m}')
        print(pd.crosstab(g.gold, g.pred).reindex(index=list(LET), columns=list(LET) + ['NONE'], fill_value=0))
if __name__ == '__main__': main(*sys.argv[1:])
