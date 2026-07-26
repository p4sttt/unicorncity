---
title: "Context Management for LLM Agents"
description: "Стратегии управления контекстным окном в долгосрочных LLM-агентах: сжатие, сворачивание, пропуск, память"
type: concept
tags: [llm, agents, context-management, long-horizon, efficiency]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: []
---

## Definition

Context management — семейство методов, позволяющих LLM работать с вводом или историей взаимодействий, превышающими доступное контекстное окно. Охватывает два ортогональных измерения: (1) **длина входного prompt'а** — сколько данных нужно обработать; (2) **длина истории взаимодействий** — сколько reasoning-шагов накопилось. Ключевая проблема второго типа: ReAct-агент линейно накапливает историю, что ведёт к деградации качества и $O(n^2)$ затратам на attention.

## Intuition

Агент похож на человека, решающего многоступенчатую задачу: не нужно держать в голове каждый промежуточный шаг — достаточно помнить результаты и ключевые выводы. Context management формализует это интуитивное "забывание несущественного".

## Formal description

Vanilla ReAct trajectory: $\tau = (a_1, o_1, a_2, o_2, \ldots, a_T, o_T)$

Context grows as $|\tau| = O(T)$, attention cost = $O(|\tau|^2)$.

**Goal**: найти функцию $F(\tau_{<t})$ такую, что $|\tilde{\tau}| \ll |\tau|$, но $P(\text{success} | \tilde{\tau}) \approx P(\text{success} | \tau)$.

## Таксономия подходов

### 1. Summarization-based

Постфактум сворачивает контекст через LLM-суммаризацию при переполнении окна.
- Прерывает reasoning flow в произвольный момент
- Теряет детали, нужные для финальной суммаризации

### 2. Context Folding ([[context_folding_scaling_llm_agents]])

Агент **сам** управляет контекстом через `branch` / `return`: создаёт поддерево для подзадачи и сворачивает его по завершении, оставляя только outcome summary.
- Складывание по границам подзадач $\to$ сохраняет reasoning coherence
- Обучается через FoldGRPO с process rewards

### 3. Adaptive Omission ([[agent_omit_adaptive_context_omission]])

Агент адаптивно пропускает мысли и наблюдения в конкретных ходах, где они избыточны.
- Ключевой факт: thoughts фронт-загружены (критичны в ходах 1, T), observations накапливаются линейно
- Оптимальные для пропуска — промежуточные ходы (2–6)

### 4. Memory systems ([[gui_agents_memory]])

Выносит долгосрочный контекст во внешнюю память; извлекает релевантные фрагменты в каждый момент времени.
- Non-parametric: DMS — evolutionary in-context cache
- Parametric: SE-GA — MASE дообучает модель на собранном опыте

### 5. Recursive Language Models ([[recursive_language_models]])

Prompt хранится как переменная в REPL-среде; LLM пишет Python-код, который итерируется по срезам prompt'а и рекурсивно вызывает себя. В историю root-модели добавляется только metadata вывода (constant size).
- Решает проблему длины входного prompt'а, а не истории взаимодействий
- Поддерживает $O(|P|)$ и $O(|P|^2)$ семантическую работу над входом
- Не требует обучения; fine-tuning на 1K примерах даёт +28%

### 6. Multi-agent decomposition

Распределяет задачу по нескольким агентам с независимыми контекстами (handcrafted workflows).

## Две ортогональные проблемы

| Проблема | Методы |
|----------|--------|
| Длинный входной **prompt** | RLM (symbolic recursion), RAG/retrieval |
| Длинная **история взаимодействий** | Context Folding, Agent-Omit, Summarization, Memory systems |

RLM и Context-Folding дополнительны: RLM читает огромный документ внутри ветки, Folding сворачивает историю между ветками.

## Сравнение методов

| Метод | Requires Training | Что сжимает | Key Mechanism |
|-------|------------------|-------------|---------------|
| Summarization | Нет | Историю взаимодействий | Post-hoc LLM summary |
| Context Folding | Да (RL) | Историю взаимодействий | Branch/return actions |
| Agent-Omit | Да (SFT + RL) | Историю взаимодействий | Selective thought/obs omission |
| RLM | Нет / мало (1K) | Входной prompt | REPL + symbolic recursion |
| DMS | Нет | Историю в памяти | Evolutionary memory cache |
| SE-GA | Да (SFT + RL) | Историю в памяти | Parametric experience encoding |

## Key papers

- [[recursive_language_models]] — symbolic recursion для длинных входных промптов
- [[context_folding_scaling_llm_agents]] — активное складывание истории по подзадачам
- [[agent_omit_adaptive_context_omission]] — адаптивный пропуск мыслей/наблюдений
- [[darwinian_memory_system_gui_agents]] — эволюционная память
- [[se_ga_self_evolving_gui_agent]] — иерархическая память + self-evolution

## Open questions

1. Могут ли RLM + Context-Folding работать совместно (RLM как sub-call engine внутри веток)?
2. Могут ли folding + omission работать совместно (ортогональные оси: когда сворачивать vs что пропускать)?
3. Как масштабировать context management на >100-шаговые траектории?
4. Есть ли оптимальная гранулярность подзадачи для folding — зависит ли она от домена?
