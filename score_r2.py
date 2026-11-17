"""Score round 2 together with round 1.
usage: python score_r2.py            (needs dataset_osha.jsonl, results.jsonl, dataset_osha_r2.jsonl, results_r2.jsonl)
Reference for every comparison = the round-1 'orig' answer of the same model on the same narrative.
Prints and writes (scored_r2.csv, r2_summary.csv):
  1. accuracy by model x condition with 95% Wilson CI (round 1 and round 2 conditions side by side)
  2. paired change vs. round-1 orig: broken / fixed counts and the exact McNemar p-value
  3. answer-change rate: share of the 70 narratives whose chosen letter differs from the round-1 orig letter.
     'orig2' is the SAME prompt asked again, so its answer-change rate is the noise baseline: a wording condition
     only shows a wording effect if its rate is clearly above the orig2 rate.
  4. no-answer rate per model x condition"""
import json, math, sys
import pandas as pd
from score_osha import final_letter, wilson

ORDER = ['orig', 'orig2', 'symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']

def mcnemar_exact(b, c):
    n = b + c
    if n == 0: return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)

def load(data, res):
    gold = {r['id']: r for r in map(json.loads, open(data, encoding='utf-8'))}
    out = []
    for r in map(json.loads, open(res, encoding='utf-8')):
        g = gold[r['id']]; pred = final_letter(r['reply'])
        out.append(dict(model=r['model'], id=r['id'], bid=g['bid'], cond=g['cond'], gold=g['gold'], pred=pred or 'NONE',
                        correct=int(pred == g['gold'])))
    return out

def main(d1='dataset_osha.jsonl', r1='results.jsonl', d2='dataset_osha_r2.jsonl', r2='results_r2.jsonl'):
    df = pd.DataFrame(load(d1, r1) + load(d2, r2))
    dup = df.duplicated(['model', 'id']).sum()
    if dup: sys.exit(f'STOP: {dup} duplicated (model, id) rows in the results files')
    df.to_csv('scored_r2.csv', index=False)
    summary = []
    for m, g in df.groupby('model'):
        acc = g.pivot(index='bid', columns='cond', values='correct')
        prd = g.pivot(index='bid', columns='cond', values='pred')
        if 'orig' not in acc: print(f'\n{m}: no round-1 orig results, skipped'); continue
        print(f'\n=== {m}')
        print('  cond      acc    95% CI        n   vs orig: broken fixed  McNemar p   answer changed vs orig   no-answer')
        for c in [c for c in ORDER if c in acc]:
            x = acc[c].dropna(); k, n = int(x.sum()), len(x); lo, hi = wilson(k, n)
            row = dict(model=m, cond=c, n=n, acc=round(k / n, 3), ci_lo=round(lo, 3), ci_hi=round(hi, 3),
                       no_answer=round(float((prd[c].dropna() == 'NONE').mean()), 3))
            line = f'  {c:8s} {k / n:.3f}  ({lo:.2f}-{hi:.2f})  {n:3d}'
            if c != 'orig':
                both = acc[['orig', c]].dropna()
                b = int(((both['orig'] == 1) & (both[c] == 0)).sum()); f = int(((both['orig'] == 0) & (both[c] == 1)).sum())
                p = mcnemar_exact(b, f)
                pp = prd[['orig', c]].dropna(); ch = int((pp['orig'] != pp[c]).sum())
                row.update(broken=b, fixed=f, mcnemar_p=round(p, 4), answer_changed=ch, answer_changed_rate=round(ch / len(pp), 3))
                line += f'            {b:3d}   {f:3d}    {p:.3f}       {ch:3d}/{len(pp)} = {ch / len(pp):.3f}'
            else:
                line += ' ' * 58
            print(line + f'        {row["no_answer"]:.3f}')
            summary.append(row)
    pd.DataFrame(summary).to_csv('r2_summary.csv', index=False)
    print('\nwrote scored_r2.csv and r2_summary.csv')
    print("Read 'answer changed vs orig' for orig2 as the noise baseline (same prompt, asked again).")
if __name__ == '__main__': main(*sys.argv[1:])
