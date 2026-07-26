---
title: "FastContext: Training Efficient Repository Explorer for Coding Agents"
description: "Zhang et al. (Microsoft/SJTU), 2026; выделенный exploration-субагент (4B–30B), обученный SFT+RL, отделяющий исследование репозитория от решения; +5.5% resolve и -60% токенов main-модели в Mini-SWE-Agent"
type: paper-summary
tags: [llm, agents, coding, retrieval, efficiency, rl, fine-tuning]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/FastContext Training Efficient Repository Explorer for Coding Agents-with-annotations.md"]
---

## TL;DR

Repository exploration — крупное горло coding-агентов: поиск релевантного кода жрёт токены и засоряет контекст нерелевантными сниппетами. FastContext выносит исследование в **отдельный exploration-субагент** (специализированные модели 4B–30B), который по запросу делает параллельные tool-calls и возвращает main-агенту компактные file-path'ы с line-range'ами как сфокусированный контекст. В Mini-SWE-Agent даёт до **+5.5% end-to-end resolve** при **-60% токенов** main-модели с маргинальным overhead.

## Core contribution

- Декуплинг: в большинстве агентов *одна* модель и исследует, и решает — exploratory reads/searches остаются в истории solver'а. FastContext разделяет эти роли, оставляя main-агенту чистые улики.
- Специализированные exploration-модели 4B–30B: bootstrap из траекторий сильной reference-модели (SFT) + refine через task-grounded RL-rewards.
- Открытый рецепт (код + данные) — против проприетарных exploration-механизмов Claude Code / Codex / Copilot / Cursor.

## Method

FastContext получает NL-описание issue или запрос на контекст, итеративно планирует и исполняет **параллельные** tool-calls (file read, glob, regex search) и возвращает компактные file-path'ы + line-range'ы.

**Обучение** (SFT + RL) с task-grounded rewards по трём осям:
1. **Broad first-turn search** — широкий охват на первом ходу.
2. **Multi-turn evidence gathering** — многоходовой сбор улик.
3. **Precise citation generation** — точная генерация цитат (path + строки).

Интегрируется как reusable-компонент в минимальные фреймворки (Mini-SWE-Agent) без графов/спец-workflow.

## Key results

- Mini-SWE-Agent + FastContext: **до +5.5%** end-to-end resolution, **до -60%** токенов main-модели, маргинальный overhead.
- Бенчмарки: SWE-bench Multilingual, SWE-bench Pro, SWE-QA.
- Preliminary-анализ: чтение и поиск занимают большую долю tool-use ходов и суммарных токенов main-агента.

## Limitations

- Требует обучения exploration-моделей (SFT+RL) — тяжелее training-free подходов ([[sherloc]]).
- Выигрыш зависит от качества reference-траекторий для bootstrap.
- Оценено в основном на Mini-SWE-Agent; перенос на другие harness'ы менее исследован.

## Related work

- Концепт: [[repository_exploration_coding_agents]] (exploration-vs-solving декомпозиция), [[context_management_llm_agents]] (offload = вариант multi-agent decomposition)
- [[swe_explore]] — бенчмарк тех же авторов (SJTU), изолирующий exploration; общая линия
- [[sherloc]] — training-free альтернатива для той же задачи локализации
- [[code_isnt_memory_structural_index]] — другой ответ на тот же bottleneck (структурный индекс вместо обученного explorer'а)
- Проект: [[agents_context_representation/index]] — subagent-offload это способ реализовать «правильный контекст нужного уровня»

## My notes

- FastContext атакует то же горло, что и структурный индекс ([[code_isnt_memory_structural_index]]), но с противоположной стороны: не «дать агенту лучший retrieval-tool», а «вынести retrieval в дешёвую специализированную модель». Прямое сравнение двух подходов на одном harness было бы очень ценно.
- -60% токенов main-модели = сильное подтверждение тезиса проекта [[agents_context_representation/index]] о том, что exploration-токены доминируют и их можно вынести.
- Reward «precise citation» (path + line-range) перекликается с line-level ground truth в [[swe_explore]] и chunk-level метрикой в [[sherloc]] — поле сходится на line-range как единице локализации.
