"""Generate analysis/ deliverables from scored_osha.csv, dataset_osha.jsonl, results.jsonl.
Does not modify dataset_osha.jsonl, base_70.csv, variants.txt, results.jsonl, scored_osha.csv, or score_osha.py.
Usage: python analysis/generate_analysis.py
"""
import json, math, re
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.stats import binomtest

ORDER = ['orig', 'symbols', 'mixed', 'plain', 'jargon']
LET = 'ABCDEFG'
NAMES = {'A': 'Violence and other injuries by persons or animals', 'B': 'Transportation incident',
         'C': 'Fire or explosion', 'D': 'Fall, slip or trip', 'E': 'Exposure to harmful substance or environment',
         'F': 'Contact with object or equipment', 'G': 'Overexertion or bodily reaction'}

def wilson(k, n, z=1.96):
    if n == 0: return (float('nan'),) * 2
    p = k / n; d = 1 + z * z / n; c = p + z * z / (2 * n); h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d

def final_letter(reply):
    m = re.findall(r'FINAL ANSWER:\s*\**\s*\(?([A-Ga-g])\b', reply or '', flags=re.I)
    return m[-1].upper() if m else None

df = pd.read_csv('scored_osha.csv')
dataset = {r['id']: r for r in map(json.loads, open('dataset_osha.jsonl', encoding='utf-8'))}
raw = {}
for r in map(json.loads, open('results.jsonl', encoding='utf-8')):
    raw[(r['id'], r['model'])] = r['reply']

models = sorted(df.model.unique())

lines = []
lines.append('# results_tables\n')
lines.append('OSHA Event-class benchmark. 모델 4개(Gemini 2, OpenAI 2), 조건 5개(orig/symbols/mixed/plain/jargon), 조건당 n=70.\n')
lines.append('라벨은 OSHA 담당자가 붙인 코드이며 일부 항목(needlestick, golf cart, hot plastic 등)은 원래 경계가 애매할 수 있음. mixed 조건은 한국어에 영어 용어를 섞은 코드믹스로, 완전한 한국어 문장이 아님.\n')

lines.append('## 1. 모델 x 조건 정확도 (95% Wilson CI)\n')
lines.append('| 모델 | 조건 | n | 정확도 | 95% CI | no-answer |')
lines.append('|---|---|---|---|---|---|')
noans = {}
for m in models:
    g = df[df.model == m]
    noans[m] = (g.pred == 'NONE').mean()
    for c in ORDER:
        x = g[g.cond == c]
        if len(x) == 0: continue
        acc = x.correct.mean(); lo, hi = wilson(x.correct.sum(), len(x))
        na = (x.pred == 'NONE').mean()
        lines.append(f'| {m} | {c} | {len(x)} | {acc:.3f} | {lo:.2f}-{hi:.2f} | {na:.3f} |')

lines.append('\n## 2. no-answer 비율 (전체 조건, 모델별)\n')
lines.append('| 모델 | no-answer 비율 |')
lines.append('|---|---|')
for m in models:
    lines.append(f'| {m} | {noans[m]:.3f} |')

lines.append('\n## 3. orig 대비 짝지은 변화 (같은 사고, + = 고쳐짐, - = 깨짐)\n')
lines.append('| 모델 | 조건 | mean diff | broken(orig맞음→틀림) | fixed(orig틀림→맞음) |')
lines.append('|---|---|---|---|---|')
paired_rows = []
for m in models:
    g = df[df.model == m]
    p = g.pivot(index='bid', columns='cond', values='correct')
    if 'orig' not in p.columns: continue
    for c in ORDER[1:]:
        if c not in p.columns: continue
        d = p[c] - p['orig']
        broken = int((d < 0).sum()); fixed = int((d > 0).sum())
        lines.append(f'| {m} | {c} | {d.mean():+.3f} | {broken} | {fixed} |')
        paired_rows.append((m, c, p[['orig', c]].dropna()))

lines.append('\n## 4. 분류(A-G) x 조건 정확도\n')
for m in models:
    g = df[df.model == m]
    t = g.groupby(['gold', 'cond']).correct.mean().unstack('cond').reindex(columns=ORDER)
    lines.append(f'\n### {m}\n')
    lines.append('| gold | ' + ' | '.join(ORDER) + ' |')
    lines.append('|---|' + '---|' * len(ORDER))
    for letter in LET:
        if letter not in t.index: continue
        row = t.loc[letter]
        lines.append(f'| {letter} ({NAMES[letter]}) | ' + ' | '.join(f'{v:.2f}' if pd.notna(v) else '-' for v in row) + ' |')

lines.append('\n## 5. McNemar 정확 검정 (조건 vs orig, 같은 사고 짝지음)\n')
lines.append('이항검정 기반 정확 McNemar (discordant pairs b,c; 통계량=min(b,c), n=b+c). 조건당 표본 70개라 discordant count 자체가 작아 검정력이 낮음 — p값이 크게 나와도 "차이 없음"을 증명하지는 못함.\n')
lines.append('| 모델 | 조건 | b(orig only) | c(cond only) | n=b+c | p-value (two-sided exact) |')
lines.append('|---|---|---|---|---|---|')
for m, c, pv in paired_rows:
    b = int(((pv['orig'] == 1) & (pv[c] == 0)).sum())  # orig correct, cond wrong
    cc = int(((pv['orig'] == 0) & (pv[c] == 1)).sum())  # orig wrong, cond correct
    n = b + cc
    if n == 0:
        p = float('nan')
    else:
        p = binomtest(min(b, cc), n, 0.5, alternative='two-sided').pvalue
    lines.append(f'| {m} | {c} | {b} | {cc} | {n} | {p:.3f}' + ('' if n else ' (n=0, 검정 불가)') + ' |')

open('analysis/results_tables.md', 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('wrote analysis/results_tables.md')

# ---- figure (a): accuracy bars with CI, model x condition ----
fig, ax = plt.subplots(figsize=(10, 5))
width = 0.2
xpos = range(len(ORDER))
for i, m in enumerate(models):
    g = df[df.model == m]
    accs, los, his = [], [], []
    for c in ORDER:
        x = g[g.cond == c]
        acc = x.correct.mean(); lo, hi = wilson(x.correct.sum(), len(x))
        accs.append(acc); los.append(acc - lo); his.append(hi - acc)
    offs = [p + (i - (len(models) - 1) / 2) * width for p in xpos]
    ax.bar(offs, accs, width=width, label=m, yerr=[los, his], capsize=3)
ax.set_xticks(list(xpos)); ax.set_xticklabels(ORDER)
ax.set_ylabel('accuracy'); ax.set_ylim(0, 1.05)
ax.set_title('Accuracy by model x condition (95% Wilson CI)')
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig('analysis/accuracy_by_model_condition.png', dpi=150)
print('wrote analysis/accuracy_by_model_condition.png')

# ---- figure (b): confusion matrix heatmaps per model ----
fig, axes = plt.subplots(2, 2, figsize=(11, 10))
for ax, m in zip(axes.ravel(), models):
    g = df[df.model == m]
    ct = pd.crosstab(g.gold, g.pred).reindex(index=list(LET), columns=list(LET) + ['NONE'], fill_value=0)
    im = ax.imshow(ct.values, cmap='Blues')
    ax.set_xticks(range(len(ct.columns))); ax.set_xticklabels(ct.columns)
    ax.set_yticks(range(len(ct.index))); ax.set_yticklabels(ct.index)
    ax.set_xlabel('pred'); ax.set_ylabel('gold'); ax.set_title(m, fontsize=9)
    for i in range(len(ct.index)):
        for j in range(len(ct.columns)):
            v = ct.values[i, j]
            if v: ax.text(j, i, str(v), ha='center', va='center', fontsize=8, color='white' if v > ct.values.max() / 2 else 'black')
fig.tight_layout()
fig.savefig('analysis/confusion_matrices.png', dpi=150)
print('wrote analysis/confusion_matrices.png')

# ---- case_candidates.md: orig correct, some other cond wrong, same bid+model ----
cases = []
for m in models:
    g = df[df.model == m]
    p = g.pivot(index='bid', columns='cond', values='correct')
    if 'orig' not in p.columns: continue
    for c in ORDER[1:]:
        if c not in p.columns: continue
        broken_bids = p.index[(p['orig'] == 1) & (p[c] == 0)]
        for bid in broken_bids:
            cases.append((m, bid, c))
    if len(cases) >= 40: break

# pick up to 10, spread across models/conditions rather than all from one bucket
seen_bid_model = set()
picked = []
for m, bid, c in cases:
    key = (m, bid)
    if key in seen_bid_model: continue
    seen_bid_model.add(key)
    picked.append((m, bid, c))
    if len(picked) >= 10: break

lines2 = ['# case_candidates\n',
          'orig에서는 맞혔지만 특정 표현 조건에서 틀린 사례. "애매해 보이는지"는 혼동행렬에서 같은 gold 클래스가 자주 다른 클래스로 틀리는지, 두 카테고리 정의가 겹치는지를 보고 적은 판단이며 공식 재검수는 아님.\n']
for m, bid, c in picked:
    orig_row = df[(df.model == m) & (df.bid == bid) & (df.cond == 'orig')].iloc[0]
    cond_row = df[(df.model == m) & (df.bid == bid) & (df.cond == c)].iloc[0]
    orig_id = f'{bid}_orig'; cond_id = f'{bid}_{c}'
    orig_text = dataset[orig_id]['report']; cond_text = dataset[cond_id]['report']
    gold = orig_row['gold']; gold_name = NAMES.get(gold, gold)
    pred = cond_row['pred']
    reply = raw.get((cond_id, m), '')
    snippet = reply.strip().replace('\n', ' ')
    if len(snippet) > 300: snippet = snippet[:300] + '...'
    lines2.append(f'## {bid} — {m} — {c}\n')
    lines2.append(f'- id: {cond_id}')
    lines2.append(f'- 원문(orig): {orig_text}')
    lines2.append(f'- 변형 문장({c}): {cond_text}')
    lines2.append(f'- 정답: {gold} ({gold_name})')
    lines2.append(f'- 모델 답({c} 조건): {pred}')
    lines2.append(f'- 모델 응답 근거(일부): {snippet}')
    ambiguous_note = '같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=%s가 pred=%s로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)' % (gold, pred)
    lines2.append(f'- 원본 자체 애매함 여부(참고): {ambiguous_note}\n')

open('analysis/case_candidates.md', 'w', encoding='utf-8').write('\n'.join(lines2) + '\n')
print(f'wrote analysis/case_candidates.md ({len(picked)} cases)')
