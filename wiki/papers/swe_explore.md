---
title: "SWE-Explore: Benchmarking How Coding Agents Explore Repositories"
description: "Zhang et al. (SJTU), 2026; бенчмарк, изолирующий repository exploration как line-level цель (848 issues, 10 языков, 203 репо); ground truth из траекторий успешных решений; agentic-explorers формируют tier выше классического retrieval"
type: paper-summary
tags: [llm, agents, coding, retrieval, benchmark]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/SWE-Explore Benchmarking How Coding Agents Explore Repositories-with-annotations.md"]
---

## TL;DR

SWE-bench сводит каждую задачу к бинарному resolved/unresolved, скрывая под-способности агента (repository understanding, retrieval, localization, diagnosis). SWE-Explore изолирует **repository exploration**: по (репо, issue) explorer возвращает ранжированный список релевантных code-region'ов под фиксированным line-budget. 848 issues, 10 языков, 203 репо; **line-level ground truth** выведен из независимых траекторий, успешно решивших ту же issue. Метрики coverage/ranking/context-efficiency сильно коррелируют с downstream repair; agentic-explorers формируют явный tier выше классического retrieval.

## Core contribution

- Превращает exploration в *сравнимую* цель оценки: sparse-retrievers, интерактивные агенты и long-context селекторы сравниваются как производители одного ранжированного region-списка под line-budget — без необходимости писать/валидировать патч.
- Line-level ground truth: из независимых успешных траекторий дистиллируются именно те code-region'ы, которые их solution-пути реально консультировали. Даёт видимость на уровне строк, а не файлов/функций.
- Оценка по трём осям (coverage, ranking, context-efficiency), проверенно трекающим downstream repair-поведение.

## Method

Мотивация (Figure 1): холистический resolution rate конфлейтит exploration + localization + patch synthesis. Две различимые failure-mode: агент либо не исследовал релевантный код, либо собрал достаточно улик, но не синтезировал верный патч. Первую existing-бенчмарки прячут.

Формат вывода намеренно прост — ранжированный список region'ов под фиксированным line-budget; скорится против line-level ground truth вопросом «как рано surface'ится evidence, на которое реально опирались решившие траектории». Спарен с проверкой, что более высокий exploration-score → лучший repair.

## Key results

- Покрытие: 848 issues, 10 языков программирования, 203 open-source репо.
- **Agentic explorers образуют tier выше классического retrieval.**
- File-level localization у современных методов уже сильна; ключевые дифференцирующие оси SOTA — **line-level coverage** и **эффективное ranking**.
- Метрики exploration сильно коррелируют с downstream repair-поведением (валидировано парной проверкой).

## Limitations

- Ground truth выведен из траекторий *успешных* решений — может недооценивать альтернативные валидные пути к фиксу.
- Exploration оценивается изолированно; реальный агент чередует exploration с редактированием.
- Line-budget фиксирован — не отражает адаптивные бюджеты в проде.

## Related work

- Концепт: [[repository_exploration_coding_agents]] — SWE-Explore это его каноничный бенчмарк
- [[fastcontext]] — того же ядра авторов (SJTU/Microsoft); explorer-субагент, оцениваемый в этой парадигме
- [[sherloc]] — chunk-level (start,end)-метрика близка к line-level coverage здесь
- [[code_isnt_memory_structural_index]] — View B localization это тот же field-move (agent-targeted surface)
- Проект: [[agents_context_representation/index]] — даёт метрику для оценки Level 1 (граф) как explorer'а

## My notes

- Даёт проекту [[agents_context_representation/index]] готовую метрику и бенчмарк: можно оценивать граф кодовой базы как explorer по coverage/ranking/efficiency, а не только по итоговому resolve.
- Сильный эмпирический факт: file-level localization «решена», горло сместилось на line-level coverage + ranking. Значит структурный индекс проекта должен возвращать line-range'ы, а не файлы.
- Кластер сходится: [[fastcontext]] (citation = line-range), [[sherloc]] (chunk-span), SWE-Explore (line-level GT) — единица локализации в 2026 это диапазон строк, не файл.
