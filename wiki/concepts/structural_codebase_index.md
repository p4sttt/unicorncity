---
title: "Structural Codebase Index"
description: "Персистентный индекс кодовой базы поверх структуры кода (semantic + lexical + call-graph / Tree-Sitter knowledge graph), доступный агенту как tool; инкрементальная инвалидация, MCP-экспозиция"
type: concept
tags: [llm, agents, coding, retrieval, mcp, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: []
---

## Definition

**Structural codebase index** — персистентный индекс, построенный поверх *структуры* кода (а не только его текста), к которому coding-агент обращается как к tool'у вместо повторного чтения файлов и grep'а. Типично объединяет несколько представлений: семантическое (эмбеддинги), лексическое (exact-match) и структурное (граф вызовов/зависимостей). Строится один раз per-repo и инкрементально обновляется при изменениях.

## Intuition

Фундаментальный mismatch: LLM-агенты оперируют неструктурированным текстом, а вопросы разработчика структурны — call-graph'ы, цепочки зависимостей, границы модулей, impact analysis («что сломается, если я изменю эту функцию?»). Text-based exploration не может выразить транзитивные связи без итеративного следования по ссылкам, каждая итерация жрёт токены и повышает риск потери контекста. Индекс кодирует структуру один раз, отвечая на структурные запросы за один tool-call.

## Компоненты

Канонический три-компонентный индекс ([[code_isnt_memory_structural_index]]):

1. **Semantic (vector) index** — эмбеддинги code-chunk'ов для семантического сходства.
2. **Lexical (BM25) index** — идентификаторы и токены для exact-match recall.
3. **Call-graph index** — определения + рёбра вызовов для структурной достижимости; строится через **Tree-Sitter** AST.

Hybrid retrieval сливает хиты трёх индексов и возвращает ранжированный список (path + snippet + score + источник).

## Реализация как knowledge graph

[[codebase_memory_tree_sitter_kg]] инстанциирует индекс как явный **knowledge graph**:
- **Nodes**: определения (функции, методы, классы, интерфейсы, типы с сигнатурами).
- **Edges**: call-sites, импорты, references, trait-реализации.
- Хранение: SQLite (нулевые зависимости), Louvain community detection для модульных границ.
- Экспозиция: **MCP** — типизированные tool'ы (call-path tracing, impact analysis, hub detection).

## Инкрементальная инвалидация

Ключевая проблема памяти о коде — устаревание после изменений. Решения:
- **Merkle-tree diff** по рабочей копии — переиндексируются только затронутые chunk'и ([[code_isnt_memory_structural_index]]).
- **File-watcher + content-hash (XXH3)** — ре-индекс изменённых файлов ([[codebase_memory_tree_sitter_kg]]).
- **Авторесинк после каждого непустого repo-diff** ([[harness_handbook]]).

## Эмпирика: окупается ли индекс

- Причинно (внутри одного harness, фиксированная модель): +40pp file-level localization (acc@5 44.3%$\to$84.5%), +8.5pp resolve — **без штрафа по стоимости**, ниже \$/solved ([[code_isnt_memory_structural_index]]).
- vs file-exploration: 83% качества против 92%, но 10x меньше токенов и 2.1x меньше tool-calls ([[codebase_memory_tree_sitter_kg]]).
- Вывод: ценность индекса привязана к доле **multi-file** изменений, где structural ranking окупается.

## Варианты и смежное

- **Обученный explorer** вместо индекса — [[fastcontext]] (специализированная модель вместо структуры).
- **Import-tree navigation** как облегчённый структурный слой — [[sherloc]].
- **Behavior-centric** представление вместо implementation-centric — [[harness_handbook]].

## Ключевые работы

- [[code_isnt_memory_structural_index]] — три-компонентный индекс + причинная абляция
- [[codebase_memory_tree_sitter_kg]] — Tree-Sitter KG через MCP, open-source
- [[repository_exploration_coding_agents]] — зачем нужен индекс (горло exploration)
- [[agents_context_representation/index]] — проект: индекс как Level 1 иерархической памяти

## Open questions

1. Оптимальный вес трёх компонентов (semantic/lexical/graph) — зависит ли от языка и типа задачи?
2. Гибрид «граф для навигации + точечное чтение файлов» — закрывает ли разрыв качества 83%$\to$92% при сохранении выигрыша токенов?
3. Стоимость построения индекса vs выигрыш: при какой доле multi-file задач индекс окупается в проде?
