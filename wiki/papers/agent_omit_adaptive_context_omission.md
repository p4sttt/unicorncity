---
title: "Agent-Omit: Adaptive Context Omission for Efficient LLM Agents"
description: "Фреймворк для адаптивного пропуска избыточных мыслей и наблюдений в LLM-агентах; 8B-модель достигает уровня frontier LLM при меньшем числе токенов"
type: paper-summary
tags: [llm, agents, efficiency, context-management, rl, icml2026]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2602.04284v2.pdf]
---

## TL;DR

Agent-Omit доказывает, что мысли и наблюдения вносят **неравный вклад** в разных ходах взаимодействия: промежуточные ходы часто избыточны, а первые и последние — критичны. Двухэтапный фреймворк (синтез cold-start данных + omit-aware RL) учит 8B-модель адаптивно пропускать ненужные токены, достигая уровня 7 frontier LLM при лучшем балансе эффективность/качество. ICML 2026.

## Core contribution

1. **Quantitative analysis**: впервые эмпирически доказано, что thought necessity и observation utility зависят от номера хода, а не одинаковы для всей траектории.
2. **Agent Omission Behavior Synthesis**: построение cold-start датасета через Monte-Carlo rollouts для выявления "опустимых" ходов.
3. **Omit-Aware Agentic RL**: dual sampling + omission reward для прогрессивного улучшения адаптивности.
4. **Теоретическая гарантия**: отклонение omission policy ограничено сверху KL-дивергенцией.

## Method

### Ключевой эмпирический результат

На WebShop (Qwen3-8B) распределение токен-затрат:
- Thoughts: **45.1%** (фронт-загруженные: ходы 1–2 потребляют больше всего)
- Observations: **52.2%** (линейный рост из-за стекирования)
- Actions: 2.7%

Из Monte-Carlo анализа: **серые зоны** существуют — ходы 2–6 чаще всего можно пропустить без потери точности. Ход 1 (планирование) и последние ходы (финальная суммаризация) — критичны.

### Формализация

Агент на каждом ходу $t$ генерирует:
- Thought $\tau_t$ (chain-of-thought) — может быть пустым `∅`
- Action $a_t$ с Omission Set $\Gamma_t \subseteq \{1, \ldots, t-1\}$ — индексы ходов, чьи наблюдения удаляются

### Stage 1: Agent Omission Behavior Synthesis

1. **Omission Turn Identification**: проходим траекторию вперёд; для каждого хода t явно удаляем $\tau_t$ или $o_t$, запускаем агент до конца. Если accuracy $\ge$ baseline при меньшем числе токенов $\to$ ход "опустимый".

2. **Hierarchical Synthesis**:
   - Single-turn omission: учим формату (empty thought `<think></think>`; omit command `<omit tool_response N...>`)
   - Multi-turn omission: учим продолжать reasoning под опущенным историческим контекстом

3. **Cold-start training**: SFT на синтетических данных.

### Stage 2: Omit-Aware Agentic RL

**Dual Sampling**:
- Full Trajectory $y$: полная траектория с omission actions $\to$ оценивает общую эффективность
- Partial Trajectory $y'$: контекст до хода t + single-turn omission $\to$ оценивает локальную политику

**Omission Reward** = Task Reward (correctness) + Efficiency Reward (токенная экономия, нормированная по baseline):

$$R_{eff} = \frac{\text{TokenBase} - \text{TokenOmit}}{\text{TokenBase}}$$

## Key results

На 5 бенчмарках (DeepSearch, WebShop, TextCraft, BabyAI, SciWorld):

| Модель | Accuracy | Token Cost |
|--------|----------|-----------|
| DeepSeek-R1-0528 | ~сопоставимо | $3$–$4\times$ больше |
| o3 | ~сопоставимо | >> |
| **Agent-Omit-8B** | **сопоставимо** | **лучший trade-off** |

Обученный агент адаптивно пропускает **3–4 хода** thought/observation, преимущественно в средних ходах — в точном соответствии с эмпирическим анализом.

## Limitations

- Cold-start синтез требует rollout'ов на каждой обучающей задаче (дорого)
- Omission policy зависит от домена: что опустимо в WebShop, может быть критично в SciWorld
- Не рассматривает совместную оптимизацию с context folding / memory systems

## Related work

- [[context_management_llm_agents]] — смежная проблема
- [[context_folding_scaling_llm_agents]] — ортогональный подход (сворачивание vs пропуск)
- [[chain_of_thought]] — что именно пропускается
- [[grpo_reinforcement_learning]] — базовый RL

## My notes

Самый ценный вклад — это, пожалуй, сам quantitative analysis, а не метод. Факт, что thoughts фронт-загружены, а observations накапливаются линейно, объясняет, почему простое трункирование не работает: надо удалять из середины, а не хвоста.

Интересен теоретический результат: KL-bound на deviation of omission policy. Это даёт гарантию, что при небольшом KL (т.е. когда политика "похожа" на исходную) omission не сильно меняет поведение агента — формальное обоснование безопасности пропуска.

Открытый вопрос: что происходит с omission policy при распределении задач, сильно отличающемся от обучающего? Предполагаю деградацию — нужна few-shot адаптация.
