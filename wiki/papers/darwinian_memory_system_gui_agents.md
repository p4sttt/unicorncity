---
title: "Darwinian Memory: A Training-Free Self-Regulating Memory System for GUI Agent Evolution"
description: "Эволюционная память для GUI-агентов: survival-of-fittest pruning, $\\varepsilon$-мутация, Байесовская оценка рисков — без дообучения"
type: paper-summary
tags: [llm, agents, gui, memory, training-free, mllm, evolutionary]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2601.22528v1.pdf]
---

## TL;DR

DMS (Darwinian Memory System) превращает память GUI-агента в динамическую экосистему по принципу «выживает сильнейший». Ключевые механизмы: декомпозиция траекторий на переиспользуемые единицы (Precondition $\to$ Goal), $\varepsilon$-мутация для выхода из локальных оптимумов, и адаптивное прунинг устаревших записей по multi-factor survival value. Работает поверх любой MLLM без дообучения.

## Core contribution

1. **Структурная реконструкция памяти**: хранит не монолитные траектории, а единицы $m = (p, \tau, s_{\mathrm{meta}})$, где $p = \langle \text{Precondition}, \text{Goal} \rangle$ — семантический индекс.
2. **$\varepsilon$-Mutation**: с вероятностью $\varepsilon$ агент игнорирует извлечённую память и решает подзадачу с нуля; если новая траектория эффективнее (короче), она перезаписывает старую.
3. **Utility-driven Natural Selection**: многофакторный survival value (popularity + temporal decay + reliability penalty) управляет автоматическим pruning через метод локтя (Elbow Method).
4. **Байесовская оценка рисков**: трансформирует высоко-рисковые воспоминания в evolutionary pressure — компеллирует агент к исследованию лучших путей.

## Method

### Архитектура Planner-Actor

Плановщик (P) декомпозирует задачу $T$ на $k \le 5$ подзадач `{p_1, ..., p_k}`. Актор (A) последовательно выполняет их, взаимодействуя с GUI.

При сбое на `p_i` $\to$ Replanning: P генерирует новый план по обновлённому наблюдению.

### Конструкция памяти

Вместо суммаризации атомарных действий (дорого, галлюциногенно) DMS использует планы P как **готовые ground-truth summaries** для атомарных действий Актора. Formат записи:

```
m = (p, tau, s_meta)
  p:      Precondition + Goal (текст, семантический индекс)
  tau:    полная атомарная траектория (на диске)
  s_meta: Success, Reuse Count, Created/Last Used Time
```

Decoupled storage: summary-embeddings в dense index (FAISS), $\tau$ — на диске.

### $\varepsilon$-Mutation Strategy

```python
if retrieved_memory and random() < 1 - epsilon:
    replay(tau_retrieved)          # детерминированное воспроизведение
else:
    tau_prime = Actor.solve_from_scratch(s_t, q)  # мутация
    if success(tau_prime) and len(tau_prime) < len(tau_retrieved):
        overwrite(tau_retrieved, tau_prime)          # in-place evolutionary update
```

### Self-Regulation (Survival Value)

Каждая запись имеет survival value:

$$V(m) = \alpha \cdot \text{Popularity}(m) \cdot e^{-\beta \cdot \Delta t} - \gamma \cdot \text{ReliabilityPenalty}(m)$$

Периодически запускается Elbow Method по распределению $V$ $\to$ удаляются записи в long tail. Это предотвращает накопление токсичных приоров.

### Dual-Factor Retrieval

Retrieval Score = weighted sum(semantic similarity(Q, p), visual similarity(o_t, reference screenshot)).

## Key results

На мульти-приложных GUI benchmark (Qwen2.5-VL-72B, Qwen3-VL-30B, GLM-4.5V, Seed1.6-VL):

| Метрика | Улучшение от DMS |
|---------|-----------------|
| Accuracy | **+18.0–25.4 pp** |
| Stability | **+11.9–22.4 pp** |
| Task Latency | **-0.68–4.75%** |

DMS улучшает все базовые модели без изменения их весов.

## Limitations

- Требует качественного Planner для формирования корректных $\langle \text{Precondition}, \text{Goal} \rangle$ единиц
- $\varepsilon$-мутация добавляет overhead в inference (иногда нужно решать задачу заново)
- Эффективность зависит от частоты повторяющихся подзадач — в одноразовых уникальных задачах выигрыш меньше

## Related work

- [[gui_agents_memory]] — обзор подходов к памяти в GUI-агентах
- [[se_ga_self_evolving_gui_agent]] — похожий подход, но с дообучением
- [[context_folding_scaling_llm_agents]] — memory vs context compression

## My notes

Биологическая аналогия неожиданно работает: "survival of the fittest" для записей памяти естественно решает проблему устаревания. Это лучше, чем LRU или простой TTL, потому что учитывает фактическую полезность и риск.

Ключевой insight: монолитные траектории — плохой формат памяти для GUI, потому что GUI-среда нестационарна (меняется layout, версии приложений). Гранулярные единицы Precondition$\to$Goal устойчивее к таким изменениям.

Вопрос: как DMS работает при редких, уникальных задачах (когда не из чего учиться)? По всей видимости, $\varepsilon$-мутация в таких случаях просто всегда срабатывает, и система деградирует до обычного актора.
