# Round 2 add-on (extract these files INTO the existing osha_kit folder; nothing from round 1 is overwritten)

Round 1 found no statistically detectable accuracy change (McNemar p > 0.05, 2-9 discordant pairs per model).
Round 2 was added AFTER seeing that result. It asks two things on the same 70 narratives and the same prompt:
1. Do stronger wording changes move the answers?  (korean, typos, heavy)
2. How much do answers move when nothing changes? (orig2 = the original prompt asked again; noise baseline)

| file | what it is |
|---|---|
| variants_r2.txt | 70 hand-written full-Korean translations |
| make_dataset_r2.py | builds dataset_osha_r2.jsonl (typos and heavy are rule-based and deterministic) |
| dataset_osha_r2.jsonl | 280 prompts = 70 narratives x (orig2, korean, typos, heavy) |
| score_r2.py | scores round 1 + round 2 together; reference = round-1 orig answer of the same model |

Run (one model at a time, same models as round 1):
    python run_eval.py --data dataset_osha_r2.jsonl --out results_r2.jsonl --models <provider:model> --sleep 5
    python score_r2.py
Do not edit results.jsonl, dataset_osha.jsonl or the prompt. Round-2 rows go to results_r2.jsonl only.
Note: orig2 is run on a later day than orig, so its answer-change rate includes any day-to-day model drift.
