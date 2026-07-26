---
title: "SE-GA: Memory-Augmented Self-Evolution for GUI Agents"
description: "GUI-агент с иерархической памятью (TTME) и двухэтапным self-evolution обучением (MASE); 89% ScreenSpot, 75.8% AndroidControl-High. ICML 2026."
type: paper-summary
tags: [llm, agents, gui, memory, self-evolution, rl, grpo, mllm, icml2026]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2605.16883v1.pdf]
---

## TL;DR

SE-GA решает две проблемы GUI-агентов: (1) потеря критической информации из ранних шагов из-за ограниченного контекстного окна и (2) неспособность переиспользовать успешные стратегии прошлых задач. TTME — иерархическая память (эпизодическая + семантическая + опытная), MASE — pipeline обучения, который использует данные TTME для дообучения VLM. ICML 2026.

## Core contribution

1. **TTME (Test-Time Memory Extension)** — иерархическое хранилище M = (M_EPI, M_SEM, M_EXP) с тремя уровнями памяти, активно накапливающее успешные траектории в реальном времени.
2. **MASE (Memory-Augmented Self-Evolution)** — двухэтапный обучающий pipeline: Grounding Training (SFT с Hindsight Goal-Shifting) + Self-Evolution Training (GRPO с динамическим порогом клиппинга).
3. **Hindsight Goal-Shifting** — аугментация данных: для частично успешных траекторий модифицируем цель в соответствии с реально достигнутым состоянием $\to$ более стабильный SFT.

## Method

### Три уровня памяти TTME

**Эпизодическая память M_EPI** — скользящее окно последних действий:

$$C^{epi}_t = [m_k]_{k=\epsilon}^{t-1}, \quad \epsilon = \max(1, t-H)$$

где $m_k = \langle o_k, a_k, o_{k+1} \rangle$. Окно H предотвращает устаревшую информацию.

**Семантическая память M_SEM** — абстрактные правила взаимодействия:

$$m^{sem}_i = \langle k^{sem}_i, d_i \rangle$$

где $d_i$ — описание правила (напр. "Login before accessing restricted pages"), $k^{sem}_i = \phi(Q_{hist})$ — embedding. Retrieval через cosine similarity.

**Опытная память M_EXP** — успешные траектории прошлых задач:

$$m^{exp}_i = \langle \tau_i, g(\tau_i), k^{intent}_i, k^{task}_i \rangle$$

Dual retrieval: $S^{exp}(Q, o_t) = \lambda \cdot \text{Sim}(\phi(Q), k^{intent}) + (1-\lambda) \cdot \text{Sim}(\psi(o_t), k^{task})$

Текстовый + визуальный encoder для точного recall по семантике И визуальному состоянию экрана.

### MASE: двухэтапное обучение

**Stage I: Grounding Training (SFT)**

Hindsight Goal-Shifting: для траектории, где агент достиг состояния $s'$ вместо цели $g$, переформулируем инструкцию как "достигни $s'$" $\to$ превращаем частичный провал в полный успех для обучения.

**Stage II: Self-Evolution Training (GRPO)**

Модифицированный GRPO с динамическим upper threshold:

$$\rho^{clip}_{i,t} = \text{clip}\left(r_{i,t}, 1 - \epsilon_{low}, 1 + \epsilon_{cur}\right)$$

где $\epsilon_{cur}$ снижается по мере обучения — постепенно ужесточает constraint для стабильного обучения в high-variance GUI-среде.

Данные для RL: собираются самим агентом через TTME во время inference (online self-collection).

## Key results

| Benchmark | SE-GA | Previous SOTA |
|-----------|-------|---------------|
| ScreenSpot | **89.0%** | ~80% |
| AndroidControl-High | **75.8%** | ~65% |
| AndroidWorld | значительное улучшение | — |

SE-GA демонстрирует сильную обобщающую способность на динамических средах (AndroidWorld требует реального взаимодействия с устройством).

## Limitations

- M_EXP требует накопления успешных траекторий $\to$ холодный старт на новых приложениях
- MASE требует дообучения (в отличие от DMS)
- Визуальный encoder для M_EXP добавляет latency при retrieval

## Related work

- [[gui_agents_memory]] — обзор memory в GUI-агентах
- [[darwinian_memory_system]] — training-free альтернатива
- [[grpo_reinforcement_learning]] — базовый RL-алгоритм
- [[hindsight_experience_replay]] — вдохновение для Hindsight Goal-Shifting

## My notes

Связь между TTME и MASE очень элегантна: TTME накапливает данные в inference $\to$ MASE дообучает на них $\to$ улучшенная модель собирает ещё лучшие данные. Это настоящий self-improvement loop без человеческой разметки.

Hindsight Goal-Shifting — умная идея для GUI: в отличие от языковых задач, GUI-действия частично обратимы и состояния конкретны. Это позволяет точно сформулировать "достигнутую" цель ретроспективно.

Сравнение с DMS: SE-GA требует обучения и собирает опыт через дообучение (параметрическое); DMS — non-parametric, работает без обучения. В реальной системе они дополнительны: DMS как быстрый inference-time cache, MASE как долгосрочное улучшение базовой политики.
