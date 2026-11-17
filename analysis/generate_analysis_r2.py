"""Generate round-2 analysis/ deliverables from r2_summary.csv, scored_r2.csv, results.jsonl, results_r2.jsonl.
Does not modify any round-1 or round-2 source/scoring files.
Usage: python analysis/generate_analysis_r2.py
"""
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ORDER = ['orig', 'orig2', 'symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']
CHANGE_CONDS = ['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']  # non-orig, orig2 drawn separately as baseline
R2_NEW_CONDS = ['orig2', 'korean', 'typos', 'heavy']

summary = pd.read_csv('r2_summary.csv')
scored = pd.read_csv('scored_r2.csv')
models = sorted(summary.model.unique())

dataset = {}
for fn in ('dataset_osha.jsonl', 'dataset_osha_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        dataset[r['id']] = r
raw = {}
for fn in ('results.jsonl', 'results_r2.jsonl'):
    for r in map(json.loads, open(fn, encoding='utf-8')):
        raw[(r['id'], r['model'])] = r['reply']

# ---- 1. results_tables_r2.md ----
lines = ['# results_tables_r2\n',
         'Round 2: 같은 70개 사고 서술을 orig2(동일 프롬프트 재실행, 노이즈 기준선), korean(완전 한국어 번역), typos(규칙 기반 오타), '
         'heavy(symbols + 모음 제거) 4개 조건으로 추가. 기준(reference)은 각 모델의 1차 orig 답.\n',
         'McNemar는 정확 이항검정(round 1과 동일 방식). orig2의 "answer changed" 비율이 노이즈 기준선이며, '
         '다른 조건의 비율이 이보다 뚜렷이 높을 때만 표현 효과로 볼 수 있음.\n']
for m in models:
    g = summary[summary.model == m].set_index('cond').reindex(ORDER)
    lines.append(f'\n## {m}\n')
    lines.append('| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |')
    lines.append('|---|---|---|---|---|---|---|---|---|---|')
    for c in ORDER:
        if c not in g.index or pd.isna(g.loc[c, 'n']): continue
        row = g.loc[c]
        n = int(row['n']); acc = row['acc']; lo = row['ci_lo']; hi = row['ci_hi']; na = row['no_answer']
        if c == 'orig':
            lines.append(f'| {c} | {n} | {acc:.3f} | {lo:.2f}-{hi:.2f} | - | - | - | - | - | {na:.3f} |')
        else:
            b = int(row['broken']); f = int(row['fixed']); p = row['mcnemar_p']
            ch = int(row['answer_changed']); chr_ = row['answer_changed_rate']
            lines.append(f'| {c} | {n} | {acc:.3f} | {lo:.2f}-{hi:.2f} | {b} | {f} | {p:.4f} | {ch} | {chr_:.3f} | {na:.3f} |')

open('analysis/results_tables_r2.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/results_tables_r2.md')

# ---- 2. answer_change_rate.png: bars for CHANGE_CONDS, orig2 as a dashed baseline per model ----
fig, ax = plt.subplots(figsize=(11, 5))
width = 0.8 / len(models)
xpos = range(len(CHANGE_CONDS))
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
for i, m in enumerate(models):
    g = summary[(summary.model == m)].set_index('cond')
    rates = [g.loc[c, 'answer_changed_rate'] if c in g.index else float('nan') for c in CHANGE_CONDS]
    offs = [p + (i - (len(models) - 1) / 2) * width for p in xpos]
    ax.bar(offs, rates, width=width, label=m, color=colors[i % len(colors)])
    baseline = g.loc['orig2', 'answer_changed_rate'] if 'orig2' in g.index else float('nan')
    ax.hlines(baseline, -0.5, len(CHANGE_CONDS) - 0.5, colors=colors[i % len(colors)], linestyles='dashed', linewidth=1)
ax.set_xticks(list(xpos)); ax.set_xticklabels(CHANGE_CONDS)
ax.set_ylabel('answer changed vs round-1 orig (rate)')
ax.set_title('Answer-change rate by condition (dashed line = that model\'s orig2 noise baseline)')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('analysis/answer_change_rate.png', dpi=150)
print('wrote analysis/answer_change_rate.png')

# ---- 3. accuracy_r1_r2.png: model x 9 conditions, accuracy + 95% CI ----
fig, ax = plt.subplots(figsize=(13, 5))
width = 0.8 / len(models)
xpos = range(len(ORDER))
for i, m in enumerate(models):
    g = summary[summary.model == m].set_index('cond').reindex(ORDER)
    accs = g['acc'].tolist()
    los = [a - lo for a, lo in zip(accs, g['ci_lo'])]
    his = [hi - a for a, hi in zip(accs, g['ci_hi'])]
    offs = [p + (i - (len(models) - 1) / 2) * width for p in xpos]
    ax.bar(offs, accs, width=width, label=m, yerr=[los, his], capsize=2, color=colors[i % len(colors)])
ax.set_xticks(list(xpos)); ax.set_xticklabels(ORDER)
ax.set_ylabel('accuracy'); ax.set_ylim(0, 1.05)
ax.set_title('Accuracy by model x condition, round 1 + round 2 (95% Wilson CI)')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('analysis/accuracy_r1_r2.png', dpi=150)
print('wrote analysis/accuracy_r1_r2.png')

# ---- 4. case_candidates_r2.md: round-2 conditions where pred != round-1 orig pred ----
orig_pred = {}
for _, r in scored[scored.cond == 'orig'].iterrows():
    orig_pred[(r['model'], r['bid'])] = r['pred']

cases_by_model = {m: [] for m in models}
for m in models:
    g = scored[(scored.model == m) & (scored.cond.isin(R2_NEW_CONDS))]
    for _, r in g.iterrows():
        op = orig_pred.get((m, r['bid']))
        if op is not None and op != r['pred']:
            cases_by_model[m].append((m, r['bid'], r['cond'], op, r['pred'], r['gold'], r['id']))

# round-robin across models so the ~10 cases aren't dominated by one model
picked = []
idx = {m: 0 for m in models}
while len(picked) < 12 and any(idx[m] < len(cases_by_model[m]) for m in models):
    for m in models:
        if idx[m] < len(cases_by_model[m]):
            picked.append(cases_by_model[m][idx[m]]); idx[m] += 1
        if len(picked) >= 12: break

lines2 = ['# case_candidates_r2\n',
          '2차 조건(orig2/korean/typos/heavy)에서 같은 모델·같은 사고의 1차 orig 답과 달라진 사례.\n']
for m, bid, cond, op, pred, gold, cid in picked:
    text = dataset[cid]['report']
    lines2.append(f'## {bid} — {m} — {cond}\n')
    lines2.append(f'- id: {cid}')
    lines2.append(f'- 1차 orig 답: {op}')
    lines2.append(f'- 바뀐 답({cond}): {pred}')
    lines2.append(f'- 정답: {gold}')
    lines2.append(f'- 바뀐 서술문({cond}): {text}\n')

open('analysis/case_candidates_r2.md', 'w', encoding='utf-8').write('\n'.join(lines2) + '\n')
print(f'wrote analysis/case_candidates_r2.md ({len(picked)} cases)')
