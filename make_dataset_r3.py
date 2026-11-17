"""Round 3 (extension): korean_natural = the same 70 narratives rewritten by a native Korean speaker (variants_r3.txt).
Same prompt, categories and gold labels as round 1.  usage: python make_dataset_r3.py  -> dataset_osha_r3.jsonl (70 rows)"""
import csv, json
from collections import Counter
from make_dataset_osha import PROMPT, LETTER, NAMES

def build():
    base = list(csv.DictReader(open('base_70.csv', encoding='utf-8')))
    kor = {}
    for ln in open('variants_r3.txt', encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'): continue
        bid, kind, text = ln.rstrip('\n').split('|', 2)
        assert kind == 'korean_natural', ln
        assert text.strip() and '|' not in text, ln
        kor[bid] = text.strip()
    missing = [b['bid'] for b in base if b['bid'] not in kor]
    assert not missing, f'missing: {missing}'
    rows = []
    for b in base:
        gold = LETTER[b['div']]; t = kor[b['bid']]
        rows.append(dict(id=f"{b['bid']}_korean_natural", bid=b['bid'], qtype='event_class', cond='korean_natural', size=0, seed=0,
                         prompt=PROMPT.format(report=t), gold=gold, gold_en=gold, gold_name=NAMES[gold], metric='label', report=t))
    with open('dataset_osha_r3.jsonl', 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(rows), 'prompts;', Counter(r['cond'] for r in rows))
if __name__ == '__main__': build()
