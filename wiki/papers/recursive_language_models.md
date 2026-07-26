---
title: "Recursive Language Models"
description: "Inference-time paradigm: prompt как внешняя переменная в REPL + символьная рекурсия $\\to$ обработка 10M+ токенов без context window ограничений"
type: paper-summary
tags: [llm, long-context, inference, agents, context-management, recursion, repl]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2512.24601v3.pdf]
---

## TL;DR

RLM (Recursive Language Model) — inference-time обёртка вокруг любой LLM: вместо того чтобы подавать длинный prompt в нейросеть напрямую, он хранится как переменная в REPL-среде. Модель пишет код, который обращается к фрагментам prompt'а и рекурсивно вызывает себя. Итог: обработка промптов на порядок больше контекстного окна при сопоставимой стоимости. RLM(GPT-5, depth=1) превосходит базовый GPT-5 на +26% медианного улучшения по 4 задачам, +130% к CodeAct, +13% к Claude Code.

## Core contribution

1. **Prompt-as-environment**: произвольно длинный prompt хранится как переменная `P` в REPL — модель манипулирует им символьно, не копируя в контекстное окно.
2. **Символьная рекурсия**: LLM пишет программы на Python, которые итерируются по срезам `P` и вызывают sub-RLM в циклах $\to$ $\Omega(|P|)$ или $\Omega(|P|^2)$ параллельных/последовательных вызовов.
3. **Constant-size history**: в историю root-модели добавляется только метаданные (длина, prefix) stdout каждой итерации — не сам контент.
4. **RLM-Qwen3-8B**: первая нативно-рекурсивная модель, обученная на 1 000 примерах; +28% медианного улучшения над базовым Qwen3-8B.

## Method

### Три ключевых отличия от "похожих" scaffolds

| Свойство | RLM (Algorithm 1) | Неэффективный scaffold (Algorithm 2) |
|---|---|---|
| Где живёт prompt | В REPL-переменной `P` | В LLM context window (hist) |
| Как генерируется ответ | Через REPL-переменную `Final` | Через `Finish` action прямо из LM |
| Рекурсия | Программная (в Python-цикле) | Вербальная (явный sub-call action) |

Недостатки Algorithm 2: (1) промпт в context $\to$ inherits window limits; (2) output через Finish $\to$ ограничен context window; (3) рекурсия только явная, не в цикле $\to$ $O(1)$ sub-calls, не $O(|P|)$.

### Алгоритм

```python
# Инициализация
state = InitREPL(prompt=P)          # P → переменная в REPL
state = AddFunction(state, sub_RLM) # рекурсивная функция доступна как модуль

hist = [Metadata(state)]            # только метаданные о P (длина, короткий prefix)

while True:
    code = LLM(hist)                # модель пишет Python-код
    state, stdout = REPL(state, code)
    hist += [code, Metadata(stdout)] # только metadata stdout, не весь контент!
    if state["Final"] is set:
        return state["Final"]
```

Sub-RLM-вызов — обычная Python-функция внутри REPL, вызываемая в циклах. Рекурсивная глубина ограничена параметром `max_depth`.

### Конфигурация в экспериментах

- Root LM: GPT-5 (medium reasoning)
- Sub-LM: GPT-5-mini (баланс качество/стоимость)
- Глубины: 0 (нет sub-calls), 1 (sub-LLM), 2–3 (sub-RLM)
- Fine-tuning: 1 000 траекторий Qwen3-Coder-480B на LongBenchPro → RLM-Qwen3-8B

### Таксономия задач по сложности обработки

| Задача | Сложность | Что требует |
|--------|-----------|------------|
| S-NIAH | $O(1)$ | Найти константное число "иголок" |
| BrowseComp+ (1K docs) | $O(1)$ docs, но multi-hop | Агрегация информации из нескольких документов |
| OOLONG | $O(n)$ линейная | Семантическая разметка и агрегация ВСЕХ строк |
| OOLONG-Pairs | $O(n^2)$ квадратичная | Агрегация пар элементов |

## Key results

| Метод | CodeQA | BrowseComp+ | OOLONG | OOLONG-Pairs |
|-------|--------|-------------|--------|--------------|
| GPT-5 (base) | 58.0* | 24.0* | 36.0 | 0.1 |
| Compaction | 58.0 | 24.0 | 44.1 | 0.31 |
| CodeAct + sub-calls | 24.0* | 24.0* | 32.0 | 0.1 |
| Claude Code | 84.0 | 12.0* | 48.0 | 6.5 |
| **RLM(GPT-5, d=1)** | **88.0** | **62.0** | **58.0** | **58.0** |
| RLM(GPT-5, d=3) | 92.0 | 58.0 | 58.0 | 76.0 |

`*` = метод упирался в context window limits. OOLONG-Pairs: GPT-5 base $\approx$ 0.1% F1, RLM(d=1) = 58% — разрыв в $580\times$.

**Fine-tuning (малый масштаб):**
- RLM-Qwen3-8B: +28.3% медианного улучшения над Qwen3-8B
- Обучение на 1 000 примерах из несвязанных доменов
- На трёх задачах из четырёх приближается к уровню vanilla GPT-5

**Стоимость:** RLM медианно дешевле или сопоставимо с base model; outlier-траектории делают среднее дороже.

## Limitations

- Root model видит только metadata stdout $\to$ не подходит для задач с очень плотными "непрерывными" рассуждениями (надо держать много промежуточных значений)
- Требует от LLM умения писать код → деградирует на моделях без code capabilities
- Fine-tuning на 1 000 примерах пока только proof-of-concept, не production-ready
- Глубокая рекурсия (d=3) не всегда лучше d=1: на CodeQA и BrowseComp+ d=1 достаточно или даже лучше

## Related work

- [[context_management_llm_agents]] — таксономия подходов; RLM $\to$ категория "symbolic recursion"
- [[context_folding_scaling_llm_agents]] — дополнительный подход: folding управляет историей взаимодействий, RLM — длиной входного prompt'а
- [[agent_omit_adaptive_context_omission]] — ортогональная ось: omission внутри фиксированного контекста
- [[chain_of_thought]] — reasoning models как вдохновение (inference-time compute)

## My notes

Ключевой conceptual shift: проблему длинного контекста обычно решают через сжатие ("уместить больше в окно"). RLM переформулирует задачу: prompt — не то, что надо запихнуть в модель, а то, что надо исследовать символьно извне. Это сдвиг парадигмы, аналогичный переходу от "читаю всю книгу сразу" к "пишу программу, которая обращается к нужным страницам".

Интересна строгая таксономия задач по $O(1)/O(n)/O(n^2)$: она объясняет, почему frontier LLM хорошо решают NIAH (constant-complexity), но ломаются на OOLONG-Pairs. Context rot — не просто "потеря внимания" на длинных контекстах, это неспособность выполнить $O(n^2)$ работу за один forward pass.

Связь с Context-Folding ([[context_folding_scaling_llm_agents]]): Context-Folding управляет историей agent-environment взаимодействий (вертикальная ось времени), RLM управляет длиной входного prompt'а (горизонтальная ось данных). Они решают разные проблемы и могут сочетаться.

Вопрос: что будет, если использовать RLM как sub-call engine для Context-Folding? Folding обрабатывает "когда сворачивать историю", RLM обрабатывает "как читать огромный документ внутри ветки". Потенциально мощная комбинация для deep research агентов.
