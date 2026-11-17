# Wording Robustness of Low-Cost LLMs on Injury Reports

This is a mini-project for COMP4136 Natural Language Processing and Large Language Models at Hong Kong Baptist University. It tests whether four low-cost LLMs (`gemini-3.1-flash-lite`, `gemini-3.5-flash-lite`, `gpt-4o-mini`, `gpt-6-luna`) give the same event label (A-G, OIICS event division) when the same OSHA severe-injury narrative is worded differently.

## Data

70 narratives sampled (10 per class, seed 2026) from the public OSHA Severe Injury Reports (federal jurisdiction, 2015-2025): https://www.osha.gov/severeinjury

## Wording conditions

- Round 1: `orig`, `symbols`, `mixed`, `plain`, `jargon`
- Round 2: `orig2`, `korean`, `typos`, `heavy`
- Round 3 (post hoc): `korean_natural`

## How to run

Set API keys as environment variables before running anything; never commit them.

```
GEMINI_API_KEY, OPENAI_API_KEY, DASHSCOPE_API_KEY, DEEPSEEK_API_KEY
```

1. Build the base sample and datasets:
   - `sample_base.py` draws the stratified 70-narrative sample into `base_70.csv`.
   - `make_dataset_osha.py` builds `dataset_osha.jsonl` (round 1: adds the rule-based `symbols` condition, reads `variants.txt` for `mixed`/`plain`/`jargon`).
   - `make_dataset_r2.py` builds `dataset_osha_r2.jsonl` (round 2: `orig2`, `typos`, `heavy` are rule-based; `korean` comes from `variants_r2.txt`).
   - `make_dataset_r3.py` builds `dataset_osha_r3.jsonl` (round 3: `korean_natural` comes from `variants_r3.txt`).
2. Check API keys/model names before a full run: `python check_keys.py --models gemini:<model>,openai:<model>,qwen:<model>` (one tiny call per model; also reports token usage so far with `--usage results.jsonl`).
3. Send prompts to the models with `run_eval.py` (resumable; append-only output):
   ```
   python run_eval.py --data dataset_osha.jsonl    --out results.jsonl    --models <provider:model> --sleep 5
   python run_eval.py --data dataset_osha_r2.jsonl --out results_r2.jsonl --models <provider:model> --sleep 5
   python run_eval.py --data dataset_osha_r3.jsonl --out results_r3.jsonl --models <provider:model> --sleep 5
   ```
4. Score the results:
   - `score_osha.py` scores round 1 only.
   - `score_r2.py` scores round 1 + round 2 together (reference = each model's round-1 `orig` answer).
   - `score_r3.py` scores round 1 + round 2 + round 3 together.
5. `analysis/*.py` scripts (run after scoring; each reads the `scored_*.csv`/`results*.jsonl` files and writes its own `.md`/`.csv`/`.png` output into `analysis/`) produce the detailed tables used to write up the results: per-model/per-condition accuracy with Wilson confidence intervals, paired broken/fixed counts, exact McNemar tests, bootstrap pooled effect sizes, per-class breakdowns, a lenient-scoring variant, and no-answer/case-list follow-ups.

Note: the raw per-prompt model replies (`results*.jsonl`) and the generated chart images (`analysis/*.png`) are not included in this repository; re-running the steps above regenerates them.

## Files

- `sample_base.py`, `base_70.csv` - stratified sample of 70 OSHA narratives.
- `make_dataset_osha.py`, `variants.txt`, `dataset_osha.jsonl` - round-1 dataset (5 conditions, 350 prompts).
- `make_dataset_r2.py`, `variants_r2.txt`, `dataset_osha_r2.jsonl` - round-2 dataset (4 conditions, 280 prompts).
- `make_dataset_r3.py`, `variants_r3.txt`, `dataset_osha_r3.jsonl` - round-3 dataset (1 condition, 70 prompts).
- `run_eval.py`, `check_keys.py` - model calls and key/model/usage checks.
- `score_osha.py`, `score_r2.py`, `score_r3.py` - scoring and summary CSVs (`scored_osha.csv`, `scored_r2.csv`, `scored_r3.csv`, `r2_summary.csv`, `r3_summary.csv`).
- `analysis/` - follow-up tables and figures built from the scored data (accuracy/CI tables, confusion matrices, pooled bootstrap effect sizes, per-class breakdown, lenient scoring, case lists).
- `README_r2.md` - notes specific to the round-2 add-on.

## Results

Accuracy changes from rewording were small (pooled mean change between -1.8 and +1.4 points, n=70, not proof of robustness); differences between models and event types were larger.

## Notes

This repository is for coursework. OSHA data is public.
