# lenient_r2

관대한 채점: 응답 전체(앞뒤 공백 제외)가 A-G 한 글자면 그 글자로 인정. 그 외는 score_osha.py의 'FINAL ANSWER: <letter>' 규칙과 동일. score_osha.py, score_r2.py는 수정하지 않고 import만 함.

## 글자 하나만 있는 응답 (모델 x 조건)

| 모델 | 조건 | 전체 n | 글자 하나만 응답한 건수 | 그 글자가 정답과 일치한 비율 |
|---|---|---|---|---|
| gemini:gemini-3.1-flash-lite | orig | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | orig2 | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | symbols | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | mixed | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | plain | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | jargon | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | korean | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | typos | 70 | 0 | - |
| gemini:gemini-3.1-flash-lite | heavy | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | orig | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | orig2 | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | symbols | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | mixed | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | plain | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | jargon | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | korean | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | typos | 70 | 0 | - |
| gemini:gemini-3.5-flash-lite | heavy | 70 | 0 | - |
| openai:gpt-4o-mini | orig | 70 | 4 | 1.000 |
| openai:gpt-4o-mini | orig2 | 70 | 2 | 1.000 |
| openai:gpt-4o-mini | symbols | 70 | 2 | 1.000 |
| openai:gpt-4o-mini | mixed | 70 | 6 | 0.833 |
| openai:gpt-4o-mini | plain | 70 | 2 | 1.000 |
| openai:gpt-4o-mini | jargon | 70 | 1 | 1.000 |
| openai:gpt-4o-mini | korean | 70 | 7 | 0.857 |
| openai:gpt-4o-mini | typos | 70 | 1 | 1.000 |
| openai:gpt-4o-mini | heavy | 70 | 4 | 1.000 |
| openai:gpt-6-luna | orig | 70 | 0 | - |
| openai:gpt-6-luna | orig2 | 70 | 0 | - |
| openai:gpt-6-luna | symbols | 70 | 0 | - |
| openai:gpt-6-luna | mixed | 70 | 0 | - |
| openai:gpt-6-luna | plain | 70 | 0 | - |
| openai:gpt-6-luna | jargon | 70 | 0 | - |
| openai:gpt-6-luna | korean | 70 | 0 | - |
| openai:gpt-6-luna | typos | 70 | 0 | - |
| openai:gpt-6-luna | heavy | 70 | 0 | - |

## 모델 x 9개 조건, 관대한 채점 기준


### gemini:gemini-3.1-flash-lite

| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |
|---|---|---|---|---|---|---|---|---|---|
| orig | 70 | 0.929 | 0.84-0.97 | - | - | - | - | - | 0.000 |
| orig2 | 70 | 0.929 | 0.84-0.97 | 0 | 0 | 1.0000 | 0 | 0.000 | 0.000 |
| symbols | 70 | 0.957 | 0.88-0.99 | 0 | 2 | 0.5000 | 2 | 0.029 | 0.000 |
| mixed | 70 | 0.900 | 0.81-0.95 | 2 | 0 | 0.5000 | 2 | 0.029 | 0.000 |
| plain | 70 | 0.971 | 0.90-0.99 | 0 | 3 | 0.2500 | 3 | 0.043 | 0.000 |
| jargon | 70 | 0.943 | 0.86-0.98 | 1 | 2 | 1.0000 | 3 | 0.043 | 0.000 |
| korean | 70 | 0.929 | 0.84-0.97 | 2 | 2 | 1.0000 | 4 | 0.057 | 0.000 |
| typos | 70 | 0.971 | 0.90-0.99 | 0 | 3 | 0.2500 | 3 | 0.043 | 0.000 |
| heavy | 70 | 0.929 | 0.84-0.97 | 1 | 1 | 1.0000 | 2 | 0.029 | 0.000 |

### gemini:gemini-3.5-flash-lite

| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |
|---|---|---|---|---|---|---|---|---|---|
| orig | 70 | 0.943 | 0.86-0.98 | - | - | - | - | - | 0.000 |
| orig2 | 70 | 0.929 | 0.84-0.97 | 2 | 1 | 1.0000 | 3 | 0.043 | 0.000 |
| symbols | 70 | 0.914 | 0.83-0.96 | 3 | 1 | 0.6250 | 4 | 0.057 | 0.000 |
| mixed | 70 | 0.914 | 0.83-0.96 | 4 | 2 | 0.6875 | 6 | 0.086 | 0.000 |
| plain | 70 | 0.929 | 0.84-0.97 | 4 | 3 | 1.0000 | 7 | 0.100 | 0.000 |
| jargon | 70 | 0.957 | 0.88-0.99 | 1 | 2 | 1.0000 | 3 | 0.043 | 0.000 |
| korean | 70 | 0.929 | 0.84-0.97 | 3 | 2 | 1.0000 | 5 | 0.071 | 0.000 |
| typos | 70 | 0.914 | 0.83-0.96 | 2 | 0 | 0.5000 | 2 | 0.029 | 0.000 |
| heavy | 70 | 0.943 | 0.86-0.98 | 2 | 2 | 1.0000 | 4 | 0.057 | 0.000 |

### openai:gpt-4o-mini

| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |
|---|---|---|---|---|---|---|---|---|---|
| orig | 70 | 0.886 | 0.79-0.94 | - | - | - | - | - | 0.000 |
| orig2 | 70 | 0.886 | 0.79-0.94 | 0 | 0 | 1.0000 | 0 | 0.000 | 0.000 |
| symbols | 70 | 0.871 | 0.77-0.93 | 2 | 1 | 1.0000 | 3 | 0.043 | 0.000 |
| mixed | 70 | 0.857 | 0.76-0.92 | 3 | 1 | 0.6250 | 4 | 0.057 | 0.000 |
| plain | 70 | 0.871 | 0.77-0.93 | 2 | 1 | 1.0000 | 3 | 0.043 | 0.000 |
| jargon | 70 | 0.929 | 0.84-0.97 | 0 | 3 | 0.2500 | 3 | 0.043 | 0.000 |
| korean | 70 | 0.886 | 0.79-0.94 | 2 | 2 | 1.0000 | 4 | 0.057 | 0.000 |
| typos | 70 | 0.929 | 0.84-0.97 | 0 | 3 | 0.2500 | 3 | 0.043 | 0.000 |
| heavy | 70 | 0.843 | 0.74-0.91 | 4 | 1 | 0.3750 | 5 | 0.071 | 0.000 |

### openai:gpt-6-luna

| 조건 | n | 정확도 | 95% CI | vs orig broken | vs orig fixed | McNemar p | answer changed | changed rate | no-answer |
|---|---|---|---|---|---|---|---|---|---|
| orig | 70 | 0.986 | 0.92-1.00 | - | - | - | - | - | 0.000 |
| orig2 | 70 | 0.971 | 0.90-0.99 | 1 | 0 | 1.0000 | 1 | 0.014 | 0.000 |
| symbols | 70 | 0.957 | 0.88-0.99 | 2 | 0 | 0.5000 | 2 | 0.029 | 0.000 |
| mixed | 70 | 0.957 | 0.88-0.99 | 2 | 0 | 0.5000 | 2 | 0.029 | 0.000 |
| plain | 70 | 0.971 | 0.90-0.99 | 1 | 0 | 1.0000 | 1 | 0.014 | 0.000 |
| jargon | 70 | 0.971 | 0.90-0.99 | 1 | 0 | 1.0000 | 1 | 0.014 | 0.000 |
| korean | 70 | 0.957 | 0.88-0.99 | 2 | 0 | 0.5000 | 2 | 0.029 | 0.000 |
| typos | 70 | 0.986 | 0.92-1.00 | 0 | 0 | 1.0000 | 0 | 0.000 | 0.000 |
| heavy | 70 | 0.971 | 0.90-0.99 | 1 | 0 | 1.0000 | 1 | 0.014 | 0.000 |
