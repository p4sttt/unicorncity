---
title: "Harness Handbook: Making Evolving Agent Harnesses Readable, Navigable, and Editable"
description: "Wang et al. (Tencent HY LLM Frontier), 2026; behavior-centric представление harness-кодовой базы из static analysis + LLM, связывающее поведения с кодом; BGPD-workflow улучшает behavior localization и качество edit-плана при меньших токенах"
type: paper-summary
tags: [llm, agents, coding, retrieval, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/2607.13285v1.md"]
---

## TL;DR

Способность AI-агента зависит не только от модели, но и от **harness'а** (сборка промптов, управление состоянием, вызов tool'ов, координация исполнения), который приходится постоянно править. Первый шаг любой правки — **behavior localization**: найти все места кода, реализующие целевое поведение. Harness Handbook — автоматически синтезируемое *behavior-centric* представление, организующее знание вокруг того, *что harness делает*, и связывающее каждое поведение с исходным кодом. Улучшает локализацию и качество edit-плана при меньшем числе planner-токенов.

## Core contribution

- Формализует **behavior localization** как отдельную задачу: найти все code-locations, реализующие описанное в modification-request поведение (необходимо *до* планирования правки).
- Harness Handbook — операциональное behavior-представление: вместо организации знания по файлам/функциям организует его по поведениям harness'а и линкует к коду. Строится автоматически из static program analysis + LLM-assisted behavioral structuring; авторесинхронизируется после каждого непустого repo-diff.
- **Behavior-Guided Progressive Disclosure (BGPD)** — workflow, ведущий агента от high-level описания поведения к деталям реализации послойно (L1 System Overview $\to$ L2 Component Overview $\to$ L3 Unit Deep Dive) и верифицирующий кандидатов против текущего кода.

## Method

Три части: (1) *представление* — исходники, организованные вокруг runtime-поведения (архитектура, execution workflow, design principles, main loop); (2) *construction pipeline* — строит Handbook из репозитория через статический анализ + LLM-структурирование; (3) *modification workflow* — BGPD с прогрессивным раскрытием и авторесинком после diff'а.

Ключевая проблема, которую решает: production-harness'ы велики, сильно связаны и behaviorally distributed по файлам/функциям/execution-стадиям/переходам состояний, тогда как modification-request описывает *что* система должна делать. Существующие code-search / repo-index / long-context подходы организуют знание по файлам-функциям-модулям и оставляют разработчику/агенту самому восстанавливать mapping «поведение → реализация».

## Key results

- Оценка на modification-requests из двух open-source harness'ов.
- Handbook-Assisted планирование улучшает behavior localization и качество edit-плана при **меньшем** числе planner-токенов.
- Наибольший выигрыш — для изменений с разбросанными по коду implementation-sites, редко исполняемыми путями и cross-module взаимодействиями.

## Limitations

- Оценка на двух harness'ах; генерализация на другие типы систем не показана.
- Качество Handbook зависит от LLM-структурирования (возможны ошибки/пропуски behaviour-mapping).
- Фокус на локализации до правки, а не на генерации самих edit'ов.

## Related work

- Концепт: [[repository_exploration_coding_agents]] — behavior localization это специализация задачи локализации
- [[code_isnt_memory_structural_index]], [[codebase_memory_tree_sitter_kg]] — implementation-centric представления; Handbook явно контрастирует с ними как behavior-centric
- [[sherloc]] — тоже добавляет к локализации структурный/диагностический слой, но для bug-repair, а не harness-evolution
- Проект: [[agents_context_representation/index]] — behavior-centric слой близок к Level 2 (семантические конвенции)

## My notes

- Интересный ортогональный угол ко всем остальным статьям кластера: не «где баг», а «где реализовано поведение X» для эволюции самого агента. Мета-уровень: harness правит harness.
- Progressive Disclosure (L1$\to$L2$\to$L3) — прямая параллель иерархической памяти проекта [[agents_context_representation/index]]: разные уровни абстракции по требованию, а не всё сразу.
- Авторесинк после каждого diff'а — тот же механизм инвалидации, что у [[codebase_memory_tree_sitter_kg]]; подтверждает, что «память устаревает после изменений» — общая болевая точка.
