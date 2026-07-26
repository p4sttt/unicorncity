---
title: "Repository Exploration & Localization for Coding Agents"
description: "Исследование кодовой базы и локализация как отдельная под-способность coding-агентов: декомпозиция exploration/solving, метрики coverage/ranking, line-range как единица локализации"
type: concept
tags: [llm, agents, coding, retrieval, benchmark, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: []
---

## Definition

**Repository exploration** — этап работы coding-агента, на котором он находит релевантные для задачи участки кода (файлы, функции, диапазоны строк) до того, как рассуждать о правке. **Localization** — более узкая формулировка: определить конкретные code-locations, реализующие целевое поведение или содержащие баг. В 2026 это выделилось в самостоятельную под-способность агента, оцениваемую и оптимизируемую отдельно от итогового resolve.

## Intuition

Холистическая метрика SWE-bench (resolved/unresolved) конфлейтит три разные способности: exploration $\to$ localization $\to$ patch synthesis ([[swe_explore]]). Отсюда две различимые failure-mode: агент либо *не нашёл* релевантный код, либо нашёл, но *не синтезировал* верный патч. Первая долго была скрыта, потому что бинарный score её не разделяет. Практически же локализация — доминирующая статья расхода: агенты тратят ~половину бюджета на поиск бага до первой правки (в среднем 18.5 ходов, 48% взаимодействия, >320k токенов/инстанс — [[sherloc]]).

## Ключевые оси

### 1. Exploration vs solving декомпозиция

В большинстве агентов *одна* модель и исследует, и решает, оставляя exploratory reads/searches в истории solver'а и засоряя контекст. Разделение ролей:
- **Exploration-субагент** ([[fastcontext]]) — вынести исследование в дешёвую специализированную модель, вернуть main-агенту компактные path'ы + line-range'ы. Даёт −60% токенов main-модели.
- **Структурный индекс как tool** ([[code_isnt_memory_structural_index]], [[codebase_memory_tree_sitter_kg]]) — не отдельная модель, а [[structural_codebase_index]], к которому агент делает запросы.

### 2. Локализация как диагноз, а не retrieval

File-path говорит *где*, но не *почему*. [[sherloc]] показывает: локация должна нести structured diagnostic finding (root cause, solution idea, dependencies, testing impact), иначе downstream repair недоспецифицирован. Аналогично [[harness_handbook]] делает behavior localization (найти *все* места, реализующие поведение) до планирования правки.

### 3. Метрики и единица локализации

- **File-level localization** у современных методов уже сильна ($\approx$решена) — [[swe_explore]].
- Горло сместилось на **line-level coverage** и **эффективное ranking** под фиксированным line-budget.
- Единица локализации сходится к **диапазону строк (start, end)**, а не файлу: precise citation в [[fastcontext]], chunk-level (start,end)-метрика в [[sherloc]], line-level ground truth в [[swe_explore]].
- Осторожно с оценкой: «агенту показали путь» $\ne$ «агент дошёл до пути» — различие View A / View B в [[code_isnt_memory_structural_index]].

## Ключевые работы

- [[swe_explore]] — бенчмарк, изолирующий exploration (line-level GT из успешных траекторий)
- [[code_isnt_memory_structural_index]] — причинная абляция структурного индекса; View A/B метрика локализации
- [[codebase_memory_tree_sitter_kg]] — Tree-Sitter knowledge graph через MCP как explorer
- [[fastcontext]] — обученный exploration-субагент (SFT+RL)
- [[sherloc]] — training-free структурная диагностическая локализация
- [[harness_handbook]] — behavior localization для эволюции самого harness'а

## Связь с context management

Exploration-эффективность — частный случай [[context_management_llm_agents]]: exploration-субагент это форма multi-agent decomposition (вынос контекста в независимую модель), а структурный индекс сокращает объём читаемого контекста на входе. Прямо мотивирует архитектуру [[agents_context_representation/index]].

## Open questions

1. Очная ставка: обученный explorer ([[fastcontext]]) vs training-free структурный tool ([[sherloc]], [[code_isnt_memory_structural_index]]) на одном harness — что дешевле при равном resolve?
2. Насколько localization gain конвертируется в resolve при слабых моделях, где локализация — более узкое горло?
3. Оптимальный line-budget: адаптивный vs фиксированный?
4. Как избежать смещения ground truth к путям *успешных* траекторий (альтернативные валидные пути к фиксу)?
