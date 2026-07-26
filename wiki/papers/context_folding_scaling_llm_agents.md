---
title: "Scaling Long-Horizon LLM Agents via Context-Folding"
description: "Механизм branch/return для активного управления контекстом агента + FoldGRPO для RL-обучения; 62% BrowseComp-Plus при 32K vs 327K контексте"
type: paper-summary
tags: [llm, agents, rl, context-management, long-horizon, grpo]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2510.11967v1.pdf]
---

## TL;DR

Context-Folding — механизм, позволяющий агенту **самому управлять своим контекстом**: создавать поддеревья (branch) для токен-интенсивных подзадач и сворачивать их (return), оставляя только краткое резюме. FoldGRPO добавляет к стандартному GRPO token-level process rewards, которые направляют агент к правильному поведению ветвления. Итог: агент с 32K активным контекстом превосходит 327K ReAct-baseline.

## Core contribution

1. **Context-Folding** — аgentic механизм с двумя действиями: `branch(description, prompt)` и `return(message)`. Промежуточные шаги внутри ветки удаляются из KV-кэша после `return`, остаётся только `message`.
2. **FoldGRPO** — RL-алгоритм на базе GRPO с динамически свёрнутым контекстом во время rollout + три типа process rewards.
3. **Архитектура plan-execution** — main thread: только планирование; branches: выполнение подзадач (нет вложенных веток).

## Method

### Context-Folding формально

Vanilla ReAct: $p^{ReAct}_\theta(\tau | q) = \prod_{i} \pi_\theta(a_i | q, a_1, o_1, \ldots, a_{i-1}, o_{i-1})$

Context-Folding: $p^{CF}_\theta(\tau | q) = \prod_{i} \pi_\theta(a_i | q, F(\tau_{<i}))$

где $F(\cdot)$ — context manager, сворачивающий сегменты между `branch` и `return`. Ветки делят один KV-cache prefix с main thread $\to$ rollback при `return` эффективен.

### FoldGRPO

Objective стандартный GRPO + process reward $Q_{i,t}$:

$$J_{FoldGRPO} = \mathbb{E}\left[\frac{1}{G}\sum_i\sum_t \min\left(r_{i,t}(\theta)\hat{A}_{i,t}, \text{clip}(\ldots)\hat{A}_{i,t}\right)\right]$$

**Process rewards:**
- **Unfolded Token Penalty** ($Q=-1$): если main-thread превышает 50% лимита — штраф всем токенам в нём (кроме branch-вызовов). Принуждает выносить тяжёлые операции в ветки.
- **Out-of-Scope Penalty** ($Q=-0.2$): GPT-5-nano оценивает, вышел ли агент за пределы заявленной подзадачи в ветке.
- **Failure Penalty** ($Q=-1$): за неудачные вызовы инструментов.

### Инстанциация

| Состояние | Поведение |
|-----------|-----------|
| Planning State (main) | High-level reasoning, декомпозиция, запрет tool-heavy операций |
| Execution State (branch) | Выполнение подзадачи, нет вложенных веток |

## Key results

| Модель | Контекст | BrowseComp-Plus | SWE-Bench Verified |
|--------|----------|-----------------|-------------------|
| GPT-5 (ReAct) | 327K | 79.3% | 71.8% |
| FoldingAgent + FoldGRPO | **$32\text{K} \times 10$** | **62.0%** | **58.0%** |
| ReAct GRPO (short) | 32K | 44.6% | 48.0% |
| SummaryAgent + GRPO | $32\text{K} \times 10$ | 52.7% | 55.0% |
| ReAct (long) | 327K | 47.8% | 55.2% |

RL улучшение: +20.0% BrowseComp-Plus, +8.8% SWE-Bench относительно 327K ReAct baseline.

## Limitations

- Нет вложенных веток $\to$ сложные иерархические задачи ограничены
- Out-of-scope reward использует внешнюю LLM (GPT-5-nano) — дорого при обучении
- Эксперименты только на Seed-OSS-36B; применимость к меньшим моделям неизвестна

## Related work

- [[context_management_llm_agents]] — общая проблематика
- [[grpo_reinforcement_learning]] — базовый RL-алгоритм
- [[darwinian_memory_system]] — комплементарный подход (memory-based)
- [[agent_omit]] — ортогональный подход (omission-based)

## My notes

Ключевой insight: контекст надо сворачивать **по границам подзадач**, а не произвольно. Это сохраняет целостность reasoning. Summary-based подходы делают это хаотично, теряя нити рассуждений.

Интересно, что без RL folding-агент уже чуть лучше summary-baseline, но значительный скачок дают именно process rewards. Это подтверждает: поведение ветвления не возникает само из outcome reward — нужна плотная обратная связь.

Вопрос: применимо ли это к задачам не-agentic LLM (e.g., многошаговые рассуждения без внешних инструментов)?
