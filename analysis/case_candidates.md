# case_candidates

orig에서는 맞혔지만 특정 표현 조건에서 틀린 사례. "애매해 보이는지"는 혼동행렬에서 같은 gold 클래스가 자주 다른 클래스로 틀리는지, 두 카테고리 정의가 겹치는지를 보고 적은 판단이며 공식 재검수는 아님.

## B61 — gemini:gemini-3.1-flash-lite — mixed

- id: B61_mixed
- 원문(orig): While getting out of his truck, an employee misstepped and re-injured a previous hernia in his left lower abdomen.
- 변형 문장(mixed): truck에서 내리다가 misstep 하여 이전에 있던 hernia를 left lower abdomen에 re-injure 함.
- 정답: G (Overexertion or bodily reaction)
- 모델 답(mixed 조건): D
- 모델 응답 근거(일부): The report describes an injury that occurred while stepping down from a truck, resulting in a misstep and subsequent injury. This is classified as a fall or slip event.  FINAL ANSWER: D
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=G가 pred=D로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B65 — gemini:gemini-3.1-flash-lite — mixed

- id: B65_mixed
- 원문(orig): An employee was using a pipe wrench to loosen a part in a vise. When the wrench moved, the employee's thigh muscles were torn at both knees. The employee was hospitalized, requiring surgery.
- 변형 문장(mixed): vise에 물린 part를 pipe wrench로 풀다가 wrench가 움직이면서 양쪽 knee 위 thigh muscle이 torn 되어 hospitalized 후 surgery가 필요했음.
- 정답: G (Overexertion or bodily reaction)
- 모델 답(mixed 조건): F
- 모델 응답 근거(일부): The report describes an injury caused by a tool (pipe wrench) slipping and striking the worker's thighs, which falls under the category of being struck by an object.  FINAL ANSWER: F
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=G가 pred=F로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B15 — gemini:gemini-3.5-flash-lite — symbols

- id: B15_symbols
- 원문(orig): A temporary employee was standing on a golf cart when it made a turn and she lost balance and fell to the ground. The employee sustained a concussion.
- 변형 문장(symbols): temp EE was standing on golf cart when it made turn & she lost balance & fell to ground. EE sustained concussion.
- 정답: B (Transportation incident)
- 모델 답(symbols 조건): D
- 모델 응답 근거(일부): To determine the correct category for the workplace injury report, let's analyze the incident described:  - The temporary employee was standing on a golf cart when it made a turn. - She lost her balance and **fell to the ground**. - This resulted in a concussion.  Looking at the categories: - **B. T...
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=B가 pred=D로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B16 — gemini:gemini-3.5-flash-lite — symbols

- id: B16_symbols
- 원문(orig): An employee stepped onto the track of a bulldozer to speak to the operator. The dozer moved forward, and the employee fell between the track and the blade. They sustained injuries to their pelvis and legs.
- 변형 문장(symbols): EE stepped onto track of bulldozer to speak to operator. dozer moved forward, & EE fell btwn track & blade. They sustained inj. to their pelvis & legs.
- 정답: B (Transportation incident)
- 모델 답(symbols 조건): F
- 모델 응답 근거(일부): To determine the correct category for this injury report, we look at the primary event that caused the injury. The employee stepped onto the track of a moving bulldozer, fell between the track and the blade, and was struck or caught by the heavy machinery while it was in motion.   While a vehicle (b...
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=B가 pred=F로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B17 — gemini:gemini-3.5-flash-lite — symbols

- id: B17_symbols
- 원문(orig): An employee was attempting to make a U-turn on a forklift when her foot was caught and fractured between the forklift and a pallet rack.
- 변형 문장(symbols): EE was attempting to make U-turn on forklift when her foot was caught & fx btwn forklift & pallet rack.
- 정답: B (Transportation incident)
- 모델 답(symbols 조건): F
- 모델 응답 근거(일부): To determine the correct category for this injury report, let's analyze the event described:  The employee was operating a forklift (a vehicle) and her foot became caught and fractured between the forklift and a pallet rack (an object/structure) while making a U-turn.   Although a forklift is involv...
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=B가 pred=F로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B61 — gemini:gemini-3.5-flash-lite — mixed

- id: B61_mixed
- 원문(orig): While getting out of his truck, an employee misstepped and re-injured a previous hernia in his left lower abdomen.
- 변형 문장(mixed): truck에서 내리다가 misstep 하여 이전에 있던 hernia를 left lower abdomen에 re-injure 함.
- 정답: G (Overexertion or bodily reaction)
- 모델 답(mixed 조건): D
- 모델 응답 근거(일부): Based on the report, the worker was stepping down from a truck, made a misstep, and re-injured their hernia. Stepping down and experiencing a misstep resulting in a fall, slip, or trip (or strain from the awkward movement) is best categorized under falls, slips, or trips. However, specifically stepp...
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=G가 pred=D로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B65 — gemini:gemini-3.5-flash-lite — mixed

- id: B65_mixed
- 원문(orig): An employee was using a pipe wrench to loosen a part in a vise. When the wrench moved, the employee's thigh muscles were torn at both knees. The employee was hospitalized, requiring surgery.
- 변형 문장(mixed): vise에 물린 part를 pipe wrench로 풀다가 wrench가 움직이면서 양쪽 knee 위 thigh muscle이 torn 되어 hospitalized 후 surgery가 필요했음.
- 정답: G (Overexertion or bodily reaction)
- 모델 답(mixed 조건): F
- 모델 응답 근거(일부): Based on the report, the injury occurred while using a pipe wrench to loosen a part, causing the wrench to slip and the employee's thigh muscles to tear. This involves being struck by or against an object/tool (the wrench moving suddenly and causing injury).   FINAL ANSWER: F
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=G가 pred=F로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B07 — openai:gpt-4o-mini — symbols

- id: B07_symbols
- 원문(orig): An employee was struck by a patient and knocked to the floor, requiring hospitalization and surgery on her neck and back.
- 변형 문장(symbols): EE was struck by pt & knocked to floor, req. hosp. & sx on her neck & back.
- 정답: A (Violence and other injuries by persons or animals)
- 모델 답(symbols 조건): F
- 모델 응답 근거(일부): FINAL ANSWER: F
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=A가 pred=F로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B53 — openai:gpt-4o-mini — symbols

- id: B53_symbols
- 원문(orig): An employee was cutting onions with an onion chopper and amputated the tip of his left thumb.
- 변형 문장(symbols): EE was cutting onions w/ onion chopper & amp. tip of his L thumb.
- 정답: F (Contact with object or equipment)
- 모델 답(symbols 조건): NONE
- 모델 응답 근거(일부): F
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=F가 pred=NONE로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

## B13 — openai:gpt-4o-mini — mixed

- id: B13_mixed
- 원문(orig): An employee was riding an ATV when he came to a terrain that induced a sudden stop. He was thrown over the handle bars and landed on the ground, dislocating his wrists and requiring surgery.
- 변형 문장(mixed): ATV를 타던 중 지형 때문에 sudden stop이 발생해 handle bar 너머로 던져져 땅에 떨어졌고, wrists가 dislocated 되어 surgery가 필요했음.
- 정답: B (Transportation incident)
- 모델 답(mixed 조건): D
- 모델 응답 근거(일부): FINAL ANSWER: D
- 원본 자체 애매함 여부(참고): 같은 bid에서 다른 조건들도 섞여 틀리는 패턴이면 표현 문제, 그렇지 않고 혼동행렬에서 gold=B가 pred=D로 자주 몰리면 원본 자체가 애매할 가능성 있음 (수동 판단 필요)

