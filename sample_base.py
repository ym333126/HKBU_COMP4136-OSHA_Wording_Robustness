"""Stratified sample of OSHA Severe Injury Reports narratives -> base_70.csv
usage: python -I sample_base.py <SIR csv> """
import sys, pandas as pd
SEED, PER_CLASS = 2026, 10
LABELS = {  # OIICS event/exposure divisions (first digit of the Event code)
    '1': 'Violence and other injuries by persons or animals',
    '2': 'Transportation incident',
    '3': 'Fire or explosion',
    '4': 'Fall, slip or trip',
    '5': 'Exposure to harmful substance or environment',
    '6': 'Contact with object or equipment',
    '7': 'Overexertion or bodily reaction'}
df = pd.read_csv(sys.argv[1], encoding='latin-1', low_memory=False)
df['div'] = df['Event'].astype(str).str.strip().str[0]
df['text'] = df['Final Narrative'].astype(str).str.strip()
ok = df[df['div'].isin(LABELS) & df['text'].str.len().between(80, 230) & df['text'].map(str.isascii)
        & ~df['text'].str.contains(r'\d{3,}|Mr\.|Ms\.|Mrs\.')]
print('eligible per class:', ok['div'].value_counts().sort_index().to_dict())
parts = [g.sample(PER_CLASS, random_state=SEED) for _, g in ok.groupby('div')]
base = pd.concat(parts).reset_index(drop=True)
base.insert(0, 'bid', [f'B{i+1:02d}' for i in range(len(base))])
base[['bid', 'ID', 'div', 'EventTitle', 'text']].to_csv('base_70.csv', index=False)
for _, r in base.iterrows(): print(r.bid, r['div'], '|', r.text)
