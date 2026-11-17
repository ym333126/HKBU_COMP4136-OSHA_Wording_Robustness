"""Score rounds 1+2+3 together (round 3 = korean_natural). Reference = round-1 orig answer of the same model.
usage: python score_r3.py   (needs dataset_osha.jsonl/results.jsonl, dataset_osha_r2.jsonl/results_r2.jsonl, dataset_osha_r3.jsonl/results_r3.jsonl)
Writes scored_r3.csv and r3_summary.csv. score_osha.py and score_r2.py are only imported, never changed."""
import sys, pandas as pd
import score_r2
from score_r2 import load, mcnemar_exact
from score_osha import wilson
ORDER = ['orig', 'orig2', 'symbols', 'mixed', 'plain', 'jargon', 'korean', 'korean_natural', 'typos', 'heavy']
def main():
    df = pd.DataFrame(load('dataset_osha.jsonl', 'results.jsonl') + load('dataset_osha_r2.jsonl', 'results_r2.jsonl')
                      + load('dataset_osha_r3.jsonl', 'results_r3.jsonl'))
    dup = df.duplicated(['model', 'id']).sum()
    if dup: sys.exit(f'STOP: {dup} duplicated (model, id) rows')
    df.to_csv('scored_r3.csv', index=False); summary = []
    for m, g in df.groupby('model'):
        acc = g.pivot(index='bid', columns='cond', values='correct'); prd = g.pivot(index='bid', columns='cond', values='pred')
        print(f'\n=== {m}')
        for c in [c for c in ORDER if c in acc]:
            x = acc[c].dropna(); k, n = int(x.sum()), len(x); lo, hi = wilson(k, n)
            row = dict(model=m, cond=c, n=n, acc=round(k / n, 3), ci_lo=round(lo, 3), ci_hi=round(hi, 3),
                       no_answer=round(float((prd[c].dropna() == 'NONE').mean()), 3))
            line = f'  {c:15s} {k / n:.3f} ({lo:.2f}-{hi:.2f}) n={n}'
            if c != 'orig':
                both = acc[['orig', c]].dropna()
                b = int(((both['orig'] == 1) & (both[c] == 0)).sum()); f = int(((both['orig'] == 0) & (both[c] == 1)).sum())
                pp = prd[['orig', c]].dropna(); ch = int((pp['orig'] != pp[c]).sum())
                row.update(broken=b, fixed=f, mcnemar_p=round(mcnemar_exact(b, f), 4), answer_changed=ch, answer_changed_rate=round(ch / len(pp), 3))
                line += f'  broken={b} fixed={f} p={mcnemar_exact(b, f):.3f} changed={ch}/{len(pp)}={ch / len(pp):.3f}'
            print(line + f'  no-answer={row["no_answer"]:.3f}'); summary.append(row)
    pd.DataFrame(summary).to_csv('r3_summary.csv', index=False); print('\nwrote scored_r3.csv and r3_summary.csv')
if __name__ == '__main__': main()
