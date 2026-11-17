# results_tables

OSHA Event-class benchmark. 모델 4개(Gemini 2, OpenAI 2), 조건 5개(orig/symbols/mixed/plain/jargon), 조건당 n=70.

라벨은 OSHA 담당자가 붙인 코드이며 일부 항목(needlestick, golf cart, hot plastic 등)은 원래 경계가 애매할 수 있음. mixed 조건은 한국어에 영어 용어를 섞은 코드믹스로, 완전한 한국어 문장이 아님.

## 1. 모델 x 조건 정확도 (95% Wilson CI)

| 모델 | 조건 | n | 정확도 | 95% CI | no-answer |
|---|---|---|---|---|---|
| gemini:gemini-3.1-flash-lite | orig | 70 | 0.929 | 0.84-0.97 | 0.000 |
| gemini:gemini-3.1-flash-lite | symbols | 70 | 0.957 | 0.88-0.99 | 0.000 |
| gemini:gemini-3.1-flash-lite | mixed | 70 | 0.900 | 0.81-0.95 | 0.000 |
| gemini:gemini-3.1-flash-lite | plain | 70 | 0.971 | 0.90-0.99 | 0.000 |
| gemini:gemini-3.1-flash-lite | jargon | 70 | 0.943 | 0.86-0.98 | 0.000 |
| gemini:gemini-3.5-flash-lite | orig | 70 | 0.943 | 0.86-0.98 | 0.000 |
| gemini:gemini-3.5-flash-lite | symbols | 70 | 0.914 | 0.83-0.96 | 0.000 |
| gemini:gemini-3.5-flash-lite | mixed | 70 | 0.914 | 0.83-0.96 | 0.000 |
| gemini:gemini-3.5-flash-lite | plain | 70 | 0.929 | 0.84-0.97 | 0.000 |
| gemini:gemini-3.5-flash-lite | jargon | 70 | 0.957 | 0.88-0.99 | 0.000 |
| openai:gpt-4o-mini | orig | 70 | 0.829 | 0.72-0.90 | 0.057 |
| openai:gpt-4o-mini | symbols | 70 | 0.843 | 0.74-0.91 | 0.029 |
| openai:gpt-4o-mini | mixed | 70 | 0.786 | 0.68-0.87 | 0.086 |
| openai:gpt-4o-mini | plain | 70 | 0.843 | 0.74-0.91 | 0.029 |
| openai:gpt-4o-mini | jargon | 70 | 0.914 | 0.83-0.96 | 0.014 |
| openai:gpt-6-luna | orig | 70 | 0.986 | 0.92-1.00 | 0.000 |
| openai:gpt-6-luna | symbols | 70 | 0.957 | 0.88-0.99 | 0.000 |
| openai:gpt-6-luna | mixed | 70 | 0.957 | 0.88-0.99 | 0.000 |
| openai:gpt-6-luna | plain | 70 | 0.971 | 0.90-0.99 | 0.000 |
| openai:gpt-6-luna | jargon | 70 | 0.971 | 0.90-0.99 | 0.000 |

## 2. no-answer 비율 (전체 조건, 모델별)

| 모델 | no-answer 비율 |
|---|---|
| gemini:gemini-3.1-flash-lite | 0.000 |
| gemini:gemini-3.5-flash-lite | 0.000 |
| openai:gpt-4o-mini | 0.043 |
| openai:gpt-6-luna | 0.000 |

## 3. orig 대비 짝지은 변화 (같은 사고, + = 고쳐짐, - = 깨짐)

| 모델 | 조건 | mean diff | broken(orig맞음→틀림) | fixed(orig틀림→맞음) |
|---|---|---|---|---|
| gemini:gemini-3.1-flash-lite | symbols | +0.029 | 0 | 2 |
| gemini:gemini-3.1-flash-lite | mixed | -0.029 | 2 | 0 |
| gemini:gemini-3.1-flash-lite | plain | +0.043 | 0 | 3 |
| gemini:gemini-3.1-flash-lite | jargon | +0.014 | 1 | 2 |
| gemini:gemini-3.5-flash-lite | symbols | -0.029 | 3 | 1 |
| gemini:gemini-3.5-flash-lite | mixed | -0.029 | 4 | 2 |
| gemini:gemini-3.5-flash-lite | plain | -0.014 | 4 | 3 |
| gemini:gemini-3.5-flash-lite | jargon | +0.014 | 1 | 2 |
| openai:gpt-4o-mini | symbols | +0.014 | 2 | 3 |
| openai:gpt-4o-mini | mixed | -0.043 | 6 | 3 |
| openai:gpt-4o-mini | plain | +0.014 | 2 | 3 |
| openai:gpt-4o-mini | jargon | +0.086 | 1 | 7 |
| openai:gpt-6-luna | symbols | -0.029 | 2 | 0 |
| openai:gpt-6-luna | mixed | -0.029 | 2 | 0 |
| openai:gpt-6-luna | plain | -0.014 | 1 | 0 |
| openai:gpt-6-luna | jargon | -0.014 | 1 | 0 |

## 4. 분류(A-G) x 조건 정확도


### gemini:gemini-3.1-flash-lite

| gold | orig | symbols | mixed | plain | jargon |
|---|---|---|---|---|---|
| A (Violence and other injuries by persons or animals) | 0.90 | 0.90 | 0.90 | 0.90 | 1.00 |
| B (Transportation incident) | 0.70 | 0.90 | 0.70 | 1.00 | 0.80 |
| C (Fire or explosion) | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 |
| D (Fall, slip or trip) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| E (Exposure to harmful substance or environment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| F (Contact with object or equipment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| G (Overexertion or bodily reaction) | 1.00 | 1.00 | 0.80 | 1.00 | 0.90 |

### gemini:gemini-3.5-flash-lite

| gold | orig | symbols | mixed | plain | jargon |
|---|---|---|---|---|---|
| A (Violence and other injuries by persons or animals) | 0.90 | 1.00 | 1.00 | 1.00 | 1.00 |
| B (Transportation incident) | 0.90 | 0.60 | 0.70 | 0.70 | 0.80 |
| C (Fire or explosion) | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 |
| D (Fall, slip or trip) | 0.90 | 0.90 | 1.00 | 1.00 | 1.00 |
| E (Exposure to harmful substance or environment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| F (Contact with object or equipment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| G (Overexertion or bodily reaction) | 1.00 | 1.00 | 0.80 | 0.90 | 1.00 |

### openai:gpt-4o-mini

| gold | orig | symbols | mixed | plain | jargon |
|---|---|---|---|---|---|
| A (Violence and other injuries by persons or animals) | 0.80 | 0.70 | 0.90 | 0.90 | 0.90 |
| B (Transportation incident) | 0.40 | 0.50 | 0.40 | 0.50 | 0.60 |
| C (Fire or explosion) | 0.90 | 1.00 | 0.80 | 0.90 | 1.00 |
| D (Fall, slip or trip) | 1.00 | 1.00 | 0.90 | 1.00 | 1.00 |
| E (Exposure to harmful substance or environment) | 0.80 | 0.80 | 0.60 | 0.70 | 0.90 |
| F (Contact with object or equipment) | 1.00 | 0.90 | 1.00 | 1.00 | 1.00 |
| G (Overexertion or bodily reaction) | 0.90 | 1.00 | 0.90 | 0.90 | 1.00 |

### openai:gpt-6-luna

| gold | orig | symbols | mixed | plain | jargon |
|---|---|---|---|---|---|
| A (Violence and other injuries by persons or animals) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| B (Transportation incident) | 1.00 | 0.80 | 0.90 | 1.00 | 1.00 |
| C (Fire or explosion) | 0.90 | 0.90 | 0.90 | 0.90 | 0.90 |
| D (Fall, slip or trip) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| E (Exposure to harmful substance or environment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| F (Contact with object or equipment) | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 |
| G (Overexertion or bodily reaction) | 1.00 | 1.00 | 0.90 | 0.90 | 0.90 |

## 5. McNemar 정확 검정 (조건 vs orig, 같은 사고 짝지음)

이항검정 기반 정확 McNemar (discordant pairs b,c; 통계량=min(b,c), n=b+c). 조건당 표본 70개라 discordant count 자체가 작아 검정력이 낮음 — p값이 크게 나와도 "차이 없음"을 증명하지는 못함.

| 모델 | 조건 | b(orig only) | c(cond only) | n=b+c | p-value (two-sided exact) |
|---|---|---|---|---|---|
| gemini:gemini-3.1-flash-lite | symbols | 0 | 2 | 2 | 0.500 |
| gemini:gemini-3.1-flash-lite | mixed | 2 | 0 | 2 | 0.500 |
| gemini:gemini-3.1-flash-lite | plain | 0 | 3 | 3 | 0.250 |
| gemini:gemini-3.1-flash-lite | jargon | 1 | 2 | 3 | 1.000 |
| gemini:gemini-3.5-flash-lite | symbols | 3 | 1 | 4 | 0.625 |
| gemini:gemini-3.5-flash-lite | mixed | 4 | 2 | 6 | 0.688 |
| gemini:gemini-3.5-flash-lite | plain | 4 | 3 | 7 | 1.000 |
| gemini:gemini-3.5-flash-lite | jargon | 1 | 2 | 3 | 1.000 |
| openai:gpt-4o-mini | symbols | 2 | 3 | 5 | 1.000 |
| openai:gpt-4o-mini | mixed | 6 | 3 | 9 | 0.508 |
| openai:gpt-4o-mini | plain | 2 | 3 | 5 | 1.000 |
| openai:gpt-4o-mini | jargon | 1 | 7 | 8 | 0.070 |
| openai:gpt-6-luna | symbols | 2 | 0 | 2 | 0.500 |
| openai:gpt-6-luna | mixed | 2 | 0 | 2 | 0.500 |
| openai:gpt-6-luna | plain | 1 | 0 | 1 | 1.000 |
| openai:gpt-6-luna | jargon | 1 | 0 | 1 | 1.000 |
