# pooled_r2

seed=2026, bootstrap 10,000회, bid 단위 복원추출, 95% 백분위 신뢰구간. no-answer=오답 기준이 원본 채점(score_r2.py)의 기본값이고, 각 모델마다 no-answer 제외 기준 줄을 하나 더 추가함.


## gemini:gemini-3.1-flash-lite

| 계산 | 평균 diff (%p) | 95% bootstrap CI | n |
|---|---|---|---|
| 7개 조건 평균, NONE=오답 | +1.43 | -1.63 ~ +4.90 | 70 (조건당) |
| 7개 조건 평균, NONE 제외 | +1.43 | -0.20 ~ +3.06 | [70, 70, 70, 70, 70, 70, 70] (조건별 n, 순서=['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']) |
| orig2 vs orig, NONE=오답 | +0.00 | +0.00 ~ +0.00 | 70 |
| orig2 vs orig, NONE 제외 | +0.00 | +0.00 ~ +0.00 | 70 |

## gemini:gemini-3.5-flash-lite

| 계산 | 평균 diff (%p) | 95% bootstrap CI | n |
|---|---|---|---|
| 7개 조건 평균, NONE=오답 | -1.43 | -6.53 ~ +3.27 | 70 (조건당) |
| 7개 조건 평균, NONE 제외 | -1.43 | -3.67 ~ +0.82 | [70, 70, 70, 70, 70, 70, 70] (조건별 n, 순서=['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']) |
| orig2 vs orig, NONE=오답 | -1.43 | -7.14 ~ +2.86 | 70 |
| orig2 vs orig, NONE 제외 | -1.43 | -7.14 ~ +2.86 | 70 |

## openai:gpt-4o-mini

| 계산 | 평균 diff (%p) | 95% bootstrap CI | n |
|---|---|---|---|
| 7개 조건 평균, NONE=오답 | +1.22 | -3.27 ~ +6.33 | 70 (조건당) |
| 7개 조건 평균, NONE 제외 | -0.06 | -2.04 ~ +1.94 | [65, 62, 64, 65, 61, 66, 64] (조건별 n, 순서=['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']) |
| orig2 vs orig, NONE=오답 | +2.86 | +0.00 ~ +7.14 | 70 |
| orig2 vs orig, NONE 제외 | +0.00 | +0.00 ~ +0.00 | 66 |

## openai:gpt-6-luna

| 계산 | 평균 diff (%p) | 95% bootstrap CI | n |
|---|---|---|---|
| 7개 조건 평균, NONE=오답 | -1.84 | -4.29 ~ -0.20 | 70 (조건당) |
| 7개 조건 평균, NONE 제외 | -1.84 | -3.06 ~ -0.82 | [70, 70, 70, 70, 70, 70, 70] (조건별 n, 순서=['symbols', 'mixed', 'plain', 'jargon', 'korean', 'typos', 'heavy']) |
| orig2 vs orig, NONE=오답 | -1.43 | -4.29 ~ +0.00 | 70 |
| orig2 vs orig, NONE 제외 | -1.43 | -4.29 ~ +0.00 | 70 |
