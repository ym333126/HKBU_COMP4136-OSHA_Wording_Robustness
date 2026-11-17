# mixed_cases_r2

orig는 맞았고 mixed는 틀린 문항(bid), 모델별.


## gemini:gemini-3.1-flash-lite (n=2)

| bid | orig pred | mixed pred | gold |
|---|---|---|---|
| B61 | G | D | G |
| B65 | G | F | G |

## gemini:gemini-3.5-flash-lite (n=4)

| bid | orig pred | mixed pred | gold |
|---|---|---|---|
| B16 | B | D | B |
| B17 | B | F | B |
| B61 | G | D | G |
| B65 | G | F | G |

## openai:gpt-4o-mini (n=6)

| bid | orig pred | mixed pred | gold |
|---|---|---|---|
| B13 | B | D | B |
| B24 | C | NONE | C |
| B36 | D | NONE | D |
| B47 | E | C | E |
| B48 | E | NONE | E |
| B65 | G | F | G |

## openai:gpt-6-luna (n=2)

| bid | orig pred | mixed pred | gold |
|---|---|---|---|
| B16 | B | F | B |
| B61 | G | D | G |

## 2개 이상 모델에서 orig->mixed로 깨진 bid


### B16 (깨진 모델: gemini:gemini-3.5-flash-lite, openai:gpt-6-luna)

- 원문(orig): An employee stepped onto the track of a bulldozer to speak to the operator. The dozer moved forward, and the employee fell between the track and the blade. They sustained injuries to their pelvis and legs.
- 변형 문장(mixed): bulldozer의 track 위로 올라가 operator에게 말하려는데 dozer가 앞으로 움직여서 track과 blade 사이로 떨어졌고 pelvis와 legs를 다침.
- 정답: B

| 모델 | orig pred | mixed pred |
|---|---|---|
| gemini:gemini-3.1-flash-lite | F | F |
| gemini:gemini-3.5-flash-lite | B | D |
| openai:gpt-4o-mini | D | D |
| openai:gpt-6-luna | B | F |

### B61 (깨진 모델: gemini:gemini-3.1-flash-lite, gemini:gemini-3.5-flash-lite, openai:gpt-6-luna)

- 원문(orig): While getting out of his truck, an employee misstepped and re-injured a previous hernia in his left lower abdomen.
- 변형 문장(mixed): truck에서 내리다가 misstep 하여 이전에 있던 hernia를 left lower abdomen에 re-injure 함.
- 정답: G

| 모델 | orig pred | mixed pred |
|---|---|---|
| gemini:gemini-3.1-flash-lite | G | D |
| gemini:gemini-3.5-flash-lite | G | D |
| openai:gpt-4o-mini | D | G |
| openai:gpt-6-luna | G | D |

### B65 (깨진 모델: gemini:gemini-3.1-flash-lite, gemini:gemini-3.5-flash-lite, openai:gpt-4o-mini)

- 원문(orig): An employee was using a pipe wrench to loosen a part in a vise. When the wrench moved, the employee's thigh muscles were torn at both knees. The employee was hospitalized, requiring surgery.
- 변형 문장(mixed): vise에 물린 part를 pipe wrench로 풀다가 wrench가 움직이면서 양쪽 knee 위 thigh muscle이 torn 되어 hospitalized 후 surgery가 필요했음.
- 정답: G

| 모델 | orig pred | mixed pred |
|---|---|---|
| gemini:gemini-3.1-flash-lite | G | F |
| gemini:gemini-3.5-flash-lite | G | F |
| openai:gpt-4o-mini | G | F |
| openai:gpt-6-luna | G | G |
