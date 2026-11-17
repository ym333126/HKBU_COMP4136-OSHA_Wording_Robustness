"""Send every prompt in dataset_osha.jsonl to each model and store raw replies (resumable).
Usage:  python run_eval.py --models gemini:<model>,openai:<model>,qwen:<model> --sleep 4
Keys (env): GEMINI_API_KEY, OPENAI_API_KEY, DASHSCOPE_API_KEY, DEEPSEEK_API_KEY
Model names must be copied from each provider's console/docs (they change often).
Each result row also stores total_tokens, so you can track a free quota. Failed calls are NOT written
(a failure stops the run with a message); rerun the same command to resume where it stopped."""
import argparse, json, os, time, sys
ENDPOINTS = {  # all expose OpenAI-compatible chat endpoints
    'gemini':   ('https://generativelanguage.googleapis.com/v1beta/openai/', 'GEMINI_API_KEY'),
    'openai':   ('https://api.openai.com/v1', 'OPENAI_API_KEY'),
    'deepseek': ('https://api.deepseek.com', 'DEEPSEEK_API_KEY'),
    'qwen':     ('https://dashscope-intl.aliyuncs.com/compatible-mode/v1', 'DASHSCOPE_API_KEY'),
}
# errors that retrying cannot fix: stop at once instead of waiting through 6 retries
FATAL = ('insufficient_quota', 'invalid_api_key', 'Incorrect API key', 'AllocationQuota', 'model_not_found',
         'does not exist', 'Error code: 401', 'Error code: 403', 'Error code: 404')
def ask(provider, model, prompt, row):
    """returns (reply_text, total_tokens)"""
    if provider == 'mock':
        return f"FINAL ANSWER: {row['gold'] if model == 'oracle' else 'wrong'}", 0
    from openai import OpenAI
    base, keyenv = ENDPOINTS[provider]
    if keyenv not in os.environ: sys.exit(f'STOP: environment variable {keyenv} is not set')
    client = OpenAI(base_url=base, api_key=os.environ[keyenv])
    kw = dict(model=model, messages=[{'role': 'user', 'content': prompt}])
    kw['max_completion_tokens' if provider == 'openai' else 'max_tokens'] = 8192
    use_temp = True
    for attempt in range(6):
        if use_temp: kw['temperature'] = 0
        else: kw.pop('temperature', None)
        try:
            r = client.chat.completions.create(**kw)
            return r.choices[0].message.content or '', (r.usage.total_tokens if r.usage else 0)
        except Exception as e:
            msg = str(e)
            if provider == 'openai' and use_temp and 'temperature' in msg:
                use_temp = False; continue          # some OpenAI models accept only the default temperature
            if any(k in msg for k in FATAL): sys.exit(f'STOP (not retrying): {msg[:400]}')
            wait = 10 * (attempt + 1); print(f'  retry in {wait}s: {msg[:120]}', file=sys.stderr); time.sleep(wait)
    sys.exit('STOP: too many failures in a row; rerun the same command to resume')
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--data', default='dataset_osha.jsonl'); ap.add_argument('--out', default='results.jsonl')
    ap.add_argument('--models', required=True); ap.add_argument('--sleep', type=float, default=0)
    ap.add_argument('--limit', type=int, default=0, help='only first N prompts (smoke test)')
    a = ap.parse_args()
    rows = [json.loads(l) for l in open(a.data, encoding='utf-8')]
    if a.limit: rows = rows[:a.limit]
    done = set()
    if os.path.exists(a.out):
        done = {(r['id'], r['model']) for r in map(json.loads, open(a.out, encoding='utf-8'))}
    with open(a.out, 'a', encoding='utf-8') as f:
        for spec in a.models.split(','):
            provider, model = spec.split(':', 1); tag = f'{provider}:{model}'; used = 0
            for i, row in enumerate(rows):
                if (row['id'], tag) in done: continue
                t0 = time.time(); reply, tok = ask(provider, model, row['prompt'], row); used += tok
                f.write(json.dumps({'id': row['id'], 'model': tag, 'reply': reply, 'tokens': tok, 'sec': round(time.time() - t0, 1)}, ensure_ascii=False) + '\n'); f.flush()
                print(f'{tag} {i+1}/{len(rows)} {row["id"]}  tokens so far this run: {used}'); time.sleep(a.sleep)
if __name__ == '__main__': main()
