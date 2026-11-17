"""Build dataset_osha.jsonl: 70 base OSHA narratives x 5 conditions = 350 classification prompts.
Conditions: orig | symbols (rule-based abbreviations) | mixed (Korean-English) | plain | jargon  (last three hand-written in variants.txt)
usage: python make_dataset_osha.py            (needs base_70.csv and variants.txt next to it)"""
import csv, json, re
from collections import Counter

LETTER = {'1': 'A', '2': 'B', '3': 'C', '4': 'D', '5': 'E', '6': 'F', '7': 'G'}
NAMES = {'A': 'Violence and other injuries by persons or animals', 'B': 'Transportation incident',
         'C': 'Fire or explosion', 'D': 'Fall, slip or trip', 'E': 'Exposure to harmful substance or environment',
         'F': 'Contact with object or equipment', 'G': 'Overexertion or bodily reaction'}
CONDS = ['orig', 'symbols', 'mixed', 'plain', 'jargon']

PROMPT = """You are classifying workplace injury reports. Read the report and choose the ONE category that best describes the type of event that caused the injury.

Categories:
A. Violence and other injuries by persons or animals (assaults, hitting, kicking, animal or insect bites and stings)
B. Transportation incident (vehicles of any kind, including forklifts, ATVs, golf carts and construction vehicles; pedestrians struck by vehicles)
C. Fire or explosion (burns or injuries caused by a fire, flash fire, ignition or explosion)
D. Fall, slip or trip (falls to the same level or to a lower level)
E. Exposure to harmful substance or environment (electricity, arc flash, steam or hot liquids, chemicals, extreme heat, diving or pressure, lightning, medication reactions)
F. Contact with object or equipment (struck by or against objects, caught in or between machinery or objects, cuts, punctures, amputations)
G. Overexertion or bodily reaction (lifting, pushing, pulling, carrying, twisting, awkward posture, strain)

Report:
{report}

Answer with one letter. End your reply with exactly one line in this form:
FINAL ANSWER: <letter>"""

# ---- rule-based "symbols and abbreviations" variant (deterministic, no LLM) ----
RULES = [
    (r'\b(?:An?|The) (?:temporary|temp) employee\b', 'temp EE'), (r'\b(?:An?|The) employee\b', 'EE'),
    (r'\btemporary employee\b', 'temp EE'), (r"\bemployee's\b", "EE's"), (r'\bemployees\b', 'EEs'), (r'\bemployee\b', 'EE'),
    (r'\bsecond[- ]degree\b', '2nd deg'), (r'\bfirst[- ]degree\b', '1st deg'),
    (r'\bhospitalization\b', 'hosp.'), (r'\bhospitalized\b', "hosp'd"), (r'\bhospital\b', 'hosp.'),
    (r'\b(?:fractured|fracturing|fractures|fracture|broken|breaking|broke)\b', 'fx'),
    (r'\bamputated\b', 'amp.'), (r'\bamputating\b', 'amp.'), (r'\bamputation\b', 'amp.'),
    (r'\bsurgery\b', 'sx'), (r'\bright\b', 'R'), (r'\bleft\b', 'L'),
    (r'\bemergency room\b', 'ER'), (r'\bpatient\b', 'pt'), (r'\bapproximately\b', '~'), (r'\babout (?=\d)', '~'),
    (r'\b(\d+) (?:feet|foot)\b', r'\1 ft'), (r'\b(\d+)-pound\b', r'\1 lb'),
    (r'\bresulting in\b', '->'), (r'\bcausing\b', '->'), (r'\bwith\b', 'w/'), (r'\bwithout\b', 'w/o'),
    (r'\bbetween\b', 'btwn'), (r'\bmaintenance\b', 'maint.'), (r'\bequipment\b', 'equip.'),
    (r'\binjuries\b', 'inj.'), (r'\binjury\b', 'inj.'), (r'\brequiring\b', 'req.'), (r'\brequired\b', 'req.'),
    (r'\band\b', '&'), (r'\b(?:a|an|the|The|A|An)\b ', ''),
]
def symbols(text):
    for pat, rep in RULES: text = re.sub(pat, rep, text)
    return re.sub(r'\s{2,}', ' ', text).strip()

def build():
    base = list(csv.DictReader(open('base_70.csv', encoding='utf-8')))
    var = {}
    for ln in open('variants.txt', encoding='utf-8'):
        if not ln.strip() or ln.startswith('#'): continue
        bid, kind, text = ln.rstrip('\n').split('|', 2); var[(bid, kind)] = text.strip()
    rows = []
    for b in base:
        gold = LETTER[b['div']]
        texts = {'orig': b['text'], 'symbols': symbols(b['text'])}
        for k in ('mixed', 'plain', 'jargon'): texts[k] = var[(b['bid'], k)]   # KeyError = a variant is missing
        for c in CONDS:
            rows.append(dict(id=f"{b['bid']}_{c}", bid=b['bid'], qtype='event_class', cond=c, size=0, seed=0,
                             prompt=PROMPT.format(report=texts[c]), gold=gold, gold_en=gold,
                             gold_name=NAMES[gold], metric='label', report=texts[c]))
    with open('dataset_osha.jsonl', 'w', encoding='utf-8') as f:
        for r in rows: f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(len(rows), 'prompts;', Counter(r['gold'] for r in rows if r['cond'] == 'orig'))
if __name__ == '__main__': build()
