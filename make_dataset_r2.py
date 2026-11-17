"""Round 2: build dataset_osha_r2.jsonl = the same 70 OSHA narratives x 4 new conditions = 280 prompts.
Conditions:
  orig2  : the original text again, identical prompt to round-1 'orig' (run-to-run noise baseline)
  korean : full Korean translation (hand-written in variants_r2.txt)
  typos  : rule-based spelling errors (deterministic, seeded per narrative)
  heavy  : heavy shorthand = round-1 'symbols' rules + interior vowels dropped from words of 5+ letters
The prompt text, categories and gold labels are exactly those of round 1 (imported from make_dataset_osha.py).
usage: python make_dataset_r2.py      (needs base_70.csv, variants_r2.txt, make_dataset_osha.py next to it)"""
import csv, json, random, re
from collections import Counter
from make_dataset_osha import PROMPT, LETTER, NAMES, symbols

CONDS_R2 = ['orig2', 'korean', 'typos', 'heavy']
NEAR = {'a': 's', 'b': 'v', 'c': 'x', 'd': 'f', 'e': 'r', 'f': 'g', 'g': 'h', 'h': 'j', 'i': 'o', 'j': 'k', 'k': 'l', 'l': 'k',
        'm': 'n', 'n': 'm', 'o': 'p', 'p': 'o', 'q': 'w', 'r': 't', 's': 'd', 't': 'y', 'u': 'i', 'v': 'b', 'w': 'e', 'x': 'c',
        'y': 'u', 'z': 'x'}
TYPO_RATE = 0.4   # share of eligible words (4+ letters, all lowercase letters) that get one spelling error

def typo_word(w, rng):
    i = rng.randrange(1, len(w) - 1)              # never touch the first or last letter
    op = rng.choice(['swap', 'drop', 'double', 'near'])
    if op == 'swap' and i + 1 < len(w) - 1 and w[i] != w[i + 1]: return w[:i] + w[i + 1] + w[i] + w[i + 2:]
    if op == 'drop': return w[:i] + w[i + 1:]
    if op == 'double': return w[:i] + w[i] + w[i:]
    return w[:i] + NEAR.get(w[i], w[i]) + w[i + 1:]

def typos(text, bid):
    rng = random.Random('typos-' + bid)            # str seed: same output on every machine
    def sub(m):
        w = m.group(0)
        return typo_word(w, rng) if rng.random() < TYPO_RATE else w
    return re.sub(r'\b[a-z]{4,}\b', sub, text)

def heavy(text):
    def squeeze(m):
        w = m.group(0)
        return w[0] + re.sub(r'[aeiou]', '', w[1:-1]) + w[-1]
    return re.sub(r'\b[A-Za-z]{5,}\b', squeeze, symbols(text))

def build():
    base = list(csv.DictReader(open('base_70.csv', encoding='utf-8')))
    kor = {}
    for ln in open('variants_r2.txt', encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'): continue
        bid, kind, text = ln.rstrip('\n').split('|', 2)
        assert kind == 'korean', ln
        kor[bid] = text.strip()
    rows = []
    for b in base:
        gold = LETTER[b['div']]
        texts = {'orig2': b['text'], 'korean': kor[b['bid']], 'typos': typos(b['text'], b['bid']), 'heavy': heavy(b['text'])}
        for c in CONDS_R2:
            rows.append(dict(id=f"{b['bid']}_{c}", bid=b['bid'], qtype='event_class', cond=c, size=0, seed=0,
                             prompt=PROMPT.format(report=texts[c]), gold=gold, gold_en=gold,
                             gold_name=NAMES[gold], metric='label', report=texts[c]))
    with open('dataset_osha_r2.jsonl', 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(rows), 'prompts;', Counter(r['cond'] for r in rows))
if __name__ == '__main__': build()
