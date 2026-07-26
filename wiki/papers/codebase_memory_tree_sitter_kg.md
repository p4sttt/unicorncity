---
title: "Codebase-Memory: Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP"
description: "Vogel et al., 2026; open-source персистентный knowledge graph по коду (Tree-Sitter, 66 языков, SQLite) с 14 MCP-tool'ами; 10x меньше токенов и 2.1x меньше tool-calls при 83% vs 92% качества против file-explorer"
type: paper-summary
tags: [llm, agents, coding, retrieval, mcp, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/Codebase-Memory Tree-Sitter-Based Knowledge Graphs for LLM Code Exploration via MCP-with-annotations.md"]
---

## TL;DR

Open-source система, превращающая структуру кодовой базы в персистентный **knowledge graph** (Tree-Sitter, 66 языков, хранение в SQLite), доступный агенту через 14 типизированных **MCP**-tool'ов вместо сырого чтения файлов. На 31 репозитории даёт качество ответов 83% против 92% у file-exploration агента, но при **10x меньше токенов** и **2.1x меньше tool-calls**; для graph-native запросов (hub detection, caller ranking) сравнивается или превосходит explorer на 19 из 31 языка.

## Core contribution

- Knowledge-graph архитектура кода: Tree-Sitter parsing (66 языков) + multi-phase build pipeline с параллельной экстракцией + 6-strategy call resolution + Louvain community detection, хранение в едином SQLite-файле без внешних зависимостей.
- MCP-интерфейс из 14 типизированных tool'ов (call-path tracing, impact analysis, hub detection) с sub-миллисекундной задержкой запроса — совместим с любым MCP-агентом.
- Head-to-head оценка на 31 языке с систематическим анализом, где graph-based retrieval выигрывает, а где file-based exploration остаётся необходимым.

## Method

Трёхстадийный pipeline (Parse → Build → Serve):
1. **Parse** — обход Tree-Sitter AST: определения (функции, методы, классы, интерфейсы, enum'ы, типы с сигнатурами/возвратами/декораторами/complexity/export-статусом), call-sites, импорты, references, trait-реализации. Для Go/C/C++ — гибрид с LSP-style type resolution (method receivers, pointer indirection, package-qualified идентификаторы).
2. **Build** — multi-phase pipeline с параллельными worker-пулами $\to$ per-worker in-memory буферы $\to$ merge $\to$ flush в SQLite (WAL). Louvain-детекция сообществ.
3. **Serve** — MCP-сервер, 14 tool'ов (4 indexing + 4 query + 3 analysis + 3 code).

Инкрементальная синхронизация: file-watcher + content-hash (XXH3) $\to$ переиндексируются только изменённые файлы. Поставка — единый статически слинкованный C-бинарь с нулевыми runtime-зависимостями.

## Key results

- 31 реальный репозиторий: **83% answer quality** vs **92%** у file-exploration агента.
- **10x меньше токенов**, **2.1x меньше tool-calls**.
- Для graph-native запросов (hub detection, caller ranking) — паритет или превосходство над explorer на 19/31 языке.
- Мотивация из смежных работ: input-токены доминируют в стоимости agentic coding даже с кэшированием; LoCoBench-Agent показывает Pareto-фронт comprehension-efficiency.

## Limitations

- Небольшая просадка качества (83% vs 92%) — граф не покрывает всё, где file-based exploration остаётся нужным.
- Ground-truth оценки — «answer quality», менее строго, чем executable resolve-метрики.
- Точность call-graph зависит от языка (для динамических/сложных языков — fallback-парсер).

## Related work

- Концепт: [[structural_codebase_index]], [[repository_exploration_coding_agents]]
- [[code_isnt_memory_structural_index]] — тот же класс структурного индекса, но с причинной абляцией внутри коммерческого harness
- Проект: [[agents_context_representation/index]] — прямая референс-реализация Level 1 (граф кодовой базы через MCP)

## My notes

- Ближайший к проекту [[agents_context_representation/index]] артефакт: Tree-Sitter KG + MCP + инкрементальная инвалидация через content-hash — ровно предлагаемый Level 1 и механизм устаревания памяти.
- Ключевой torg: -17pp качества за -90% токенов. Гипотеза проекта — что гибрид (граф как навигация + точечное чтение файлов) закроет разрыв качества, сохранив выигрыш токенов.
- Louvain community detection как способ выделять «модульные границы» — потенциально полезно для Level 2 (архитектурные конвенции) проекта.
