"""Check that each API key works (one tiny call per model) and summarise token usage so far.
Usage:
  python check_keys.py --models gemini:<MODEL>,openai:<MODEL>,qwen:<MODEL>
  python check_keys.py --usage results.jsonl            # tokens used per model in a results file
Keys come from environment variables (see run_eval.py). The remaining balance / free quota CANNOT be read
through these APIs; what this script can tell you is: key valid, model name valid, has quota or credit right now,
rate-limit headers (when the provider sends them), and how many tokens you already used in results.jsonl."""
import argparse, json, os, sys
from collections import defaultdict
from run_eval import ENDPOINTS

QWEN_FREE_TOKENS = 1_000_000   # per model, 90 days (Alibaba Model Studio new-user quota; check the console for your model)

def diagnose(msg):
    if 'insufficient_quota' in msg: return 'NO CREDIT: key is valid but the account has no balance/quota (add credit or wait for the free quota)'
    if 'AllocationQuota' in msg:   return 'FREE QUOTA USED UP (Free Quota Only is on, so calls are blocked and not billed)'
    if 'invalid_api_key' in msg or 'Incorrect API key' in msg or 'Error code: 401' in msg: return 'BAD KEY: the key is invalid or belongs to another service'
    if 'model_not_found' in msg or 'does not exist' in msg or 'Error code: 404' in msg: return 'BAD MODEL NAME: copy the current name from the provider console'
    if 'Error code: 403' in msg: return 'FORBIDDEN: key has no access to this model/region'
    if 'Error code: 429' in msg: return 'RATE LIMITED: key works but too many requests right now, wait and retry'
    return 'ERROR: ' + msg[:200]

def check(spec):
    provider, model = spec.split(':', 1)
    base, keyenv = ENDPOINTS[provider]
    if keyenv not in os.environ: return f'{spec:34s} {keyenv} is not set'
    from openai import OpenAI
    client = OpenAI(base_url=base, api_key=os.environ[keyenv], max_retries=0)
    kw = dict(model=model, messages=[{'role': 'user', 'content': 'Reply with the single word OK.'}])
    kw['max_completion_tokens' if provider == 'openai' else 'max_tokens'] = 64
    try:
        raw = client.chat.completions.with_raw_response.create(**kw)
        r = raw.parse()
        lim = {k: v for k, v in raw.headers.items() if k.lower().startswith('x-ratelimit')}
        extra = ('  | ' + ', '.join(f'{k}={v}' for k, v in lim.items())) if lim else ''
        return f'{spec:34s} OK  (used {r.usage.total_tokens if r.usage else "?"} tokens){extra}'
    except Exception as e:
        return f'{spec:34s} {diagnose(str(e))}'

def usage(path):
    tok, n = defaultdict(int), defaultdict(int)
    for line in open(path, encoding='utf-8'):
        r = json.loads(line); tok[r['model']] += r.get('tokens', 0); n[r['model']] += 1
    for m in sorted(tok):
        note = ''
        if m.startswith('qwen:'): note = f'  ({tok[m] / QWEN_FREE_TOKENS:.0%} of a {QWEN_FREE_TOKENS:,}-token free quota)'
        print(f'{m:34s} {n[m]:4d} calls, {tok[m]:>9,} tokens{note}')

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--models'); ap.add_argument('--usage')
    a = ap.parse_args()
    if not (a.models or a.usage): ap.error('give --models and/or --usage')
    if a.models:
        for spec in a.models.split(','): print(check(spec))
    if a.usage: usage(a.usage)
