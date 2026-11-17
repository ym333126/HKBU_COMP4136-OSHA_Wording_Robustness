"""Pooled effect size per model: mean of (acc(cond) - acc(orig)) across the 7 wording conditions
(symbols, mixed, plain, jargon, korean, typos, heavy), plus the same for orig2 (noise baseline).
Bootstrap: resample the 70 bids with replacement, 10,000 times, seed 2026; 95% percentile CI.
Default criterion: no-answer counted as wrong (score_r2.py's own 'correct' column, unchanged).
A second line repeats the same calculation excluding narratives where orig or the compared
condition returned no-answer (pred == 'NONE').
Does not modify any existing file. Usage: python analysis/pooled_r2.py (run from the osha_kit folder)
"""
import numpy as np
import pandas as pd

SEED = 2026
N_BOOT = 10000
CONDS7 = ['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']

df = pd.read_csv('scored_r2.csv')
models = sorted(df.model.unique())


def boot_diff_shared(cond_arrs, orig_arr, n_boot, seed):
    """Shared bid-resample across all conds in cond_arrs (list of arrays, same length as orig_arr).
    Returns the bootstrap array of the mean-over-conds diff (n_boot,)."""
    n = len(orig_arr)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    orig_boot = orig_arr[idx].mean(axis=1)
    per_cond = [c[idx].mean(axis=1) - orig_boot for c in cond_arrs]
    return np.mean(per_cond, axis=0) * 100


def boot_diff_single(cond_arr, orig_arr, n_boot, seed):
    n = len(orig_arr)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, n, size=(n_boot, n))
    return (cond_arr[idx].mean(axis=1) - orig_arr[idx].mean(axis=1)) * 100


def boot_diff_indep(cond_arrs_valid, orig_arrs_valid, n_boot, seed):
    """Each cond has its own valid-subset arrays (possibly different n); resample each
    independently (seeded from the same base seed + offset) and average the n_boot draws elementwise."""
    per_cond = []
    for i, (c, o) in enumerate(zip(cond_arrs_valid, orig_arrs_valid)):
        n = len(o)
        if n == 0:
            per_cond.append(np.full(n_boot, np.nan))
            continue
        rng = np.random.default_rng(seed + i + 1)
        idx = rng.integers(0, n, size=(n_boot, n))
        per_cond.append((c[idx].mean(axis=1) - o[idx].mean(axis=1)) * 100)
    return np.nanmean(per_cond, axis=0)


lines = ['# pooled_r2\n',
         'seed=2026, bootstrap 10,000회, bid 단위 복원추출, 95% 백분위 신뢰구간. '
         'no-answer=오답 기준이 원본 채점(score_r2.py)의 기본값이고, 각 모델마다 no-answer 제외 기준 줄을 하나 더 추가함.\n']

for m in models:
    g = df[df.model == m]
    pred = g.pivot(index='bid', columns='cond', values='pred')
    corr = g.pivot(index='bid', columns='cond', values='correct')
    bids = sorted(corr.index)
    pred = pred.loc[bids]; corr = corr.loc[bids]
    n_bid = len(bids)

    orig_c = corr['orig'].values.astype(float)
    orig_p = pred['orig'].values
    cond_arrs = [corr[c].values.astype(float) for c in CONDS7]

    # ---- pooled-7, NONE=wrong (default) ----
    point = np.mean([(c.mean() - orig_c.mean()) * 100 for c in cond_arrs])
    boot = boot_diff_shared(cond_arrs, orig_c, N_BOOT, SEED)
    lo, hi = np.percentile(boot, [2.5, 97.5])

    # ---- pooled-7, NONE excluded ----
    valid_cond_arrs, valid_orig_arrs, ns = [], [], []
    for c, carr in zip(CONDS7, cond_arrs):
        valid = (orig_p != 'NONE') & (pred[c].values != 'NONE')
        valid_cond_arrs.append(carr[valid]); valid_orig_arrs.append(orig_c[valid]); ns.append(int(valid.sum()))
    point_ex = np.nanmean([(c.mean() - o.mean()) * 100 if len(o) else np.nan
                            for c, o in zip(valid_cond_arrs, valid_orig_arrs)])
    boot_ex = boot_diff_indep(valid_cond_arrs, valid_orig_arrs, N_BOOT, SEED)
    lo_ex, hi_ex = np.nanpercentile(boot_ex, [2.5, 97.5])

    # ---- orig2 (noise baseline), NONE=wrong ----
    orig2_c = corr['orig2'].values.astype(float)
    point_o2 = (orig2_c.mean() - orig_c.mean()) * 100
    boot_o2 = boot_diff_single(orig2_c, orig_c, N_BOOT, SEED)
    lo_o2, hi_o2 = np.percentile(boot_o2, [2.5, 97.5])

    # ---- orig2, NONE excluded ----
    valid_o2 = (orig_p != 'NONE') & (pred['orig2'].values != 'NONE')
    vo2_orig = orig_c[valid_o2]; vo2_cond = orig2_c[valid_o2]; n_o2 = int(valid_o2.sum())
    point_o2_ex = (vo2_cond.mean() - vo2_orig.mean()) * 100 if n_o2 else float('nan')
    if n_o2:
        boot_o2_ex = boot_diff_single(vo2_cond, vo2_orig, N_BOOT, SEED)
        lo_o2_ex, hi_o2_ex = np.percentile(boot_o2_ex, [2.5, 97.5])
    else:
        lo_o2_ex = hi_o2_ex = float('nan')

    lines.append(f'\n## {m}\n')
    lines.append('| 계산 | 평균 diff (%p) | 95% bootstrap CI | n |')
    lines.append('|---|---|---|---|')
    lines.append(f'| 7개 조건 평균, NONE=오답 | {point:+.2f} | {lo:+.2f} ~ {hi:+.2f} | {n_bid} (조건당) |')
    lines.append(f'| 7개 조건 평균, NONE 제외 | {point_ex:+.2f} | {lo_ex:+.2f} ~ {hi_ex:+.2f} | {ns} (조건별 n, 순서={CONDS7}) |')
    lines.append(f'| orig2 vs orig, NONE=오답 | {point_o2:+.2f} | {lo_o2:+.2f} ~ {hi_o2:+.2f} | {n_bid} |')
    lines.append(f'| orig2 vs orig, NONE 제외 | {point_o2_ex:+.2f} | {lo_o2_ex:+.2f} ~ {hi_o2_ex:+.2f} | {n_o2} |')

open('analysis/pooled_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/pooled_r2.md')
