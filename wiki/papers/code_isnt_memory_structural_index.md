---
title: "Code Isn't Memory: A Structural Codebase Index Inside a Coding Agent"
description: "SuperAGI, 2026; leak-audited причинная абляция структурного индекса кодовой базы (semantic+lexical+call-graph) внутри coding-агента; +40pp localization, +8.5pp resolve при отсутствии cost-penalty"
type: paper-summary
tags: [llm, agents, coding, retrieval, benchmark, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/Code Isn't Memory A Structural Codebase Index Inside a Coding Agent-with-annotations.md"]
---

## TL;DR

Первая leak-audited, model-controlled **причинная абляция** структурного индекса кодовой базы, встроенного в реальный coding-агент. Внутри фиксированного harness на фиксированной модели (Claude Opus 4.7) включение индекса поднимает file-level localization (acc@5) с 44.3% до 84.5% и resolve с 41.9% до 50.4% — **без штрафа по стоимости** и с меньшей ценой за solve. Переформулирует вопрос деплоя с «слишком ли дорог структурный индекс» на «есть ли в workload multi-file изменения, где structural ranking окупается».

## Core contribution

- Изолирует индекс *причинно*: тумблер ON/OFF внутри одного harness (SuperCoder), всё остальное идентично, плюс кросс-harness проверка против agentic-grep baseline (OpenCode).
- Разделяет два ранее смешанных вопроса: (1) внутри-harness эффект индекса (SC-ON vs SC-OFF), (2) воспроизводим ли эффект альтернативным open-source harness (SC-ON vs OpenCode).
- Публикует полный аудит-артефакт: per-cell exclusion ledger, leak-audit скрипт, dual-view localization extractor, results DB.

## Method

**Три арма** на одном наборе инстансов, модель Claude Opus 4.7 фиксирована, 3 seed'а:
- **SC-ON** — SuperCoder с двумя tool'ами контекст-движка: `codebase_search` и `codebase_graph`.
- **SC-OFF** — тот же harness, из схемы убраны ровно эти два tool'а, всё прочее идентично.
- **OpenCode** — независимый open-source агент на ripgrep + read (agentic-grep, без структурного индекса).

**Структурный индекс** (context engine) — отдельный сервис, per-repo, строится один раз, инкрементально обновляется через Merkle-diff по рабочей копии. Три компонента:
1. **Vector index** — эмбеддинги code-chunk'ов (семантическое сходство).
2. **Call-graph index** — определения + рёбра вызовов (структурная достижимость), строится через tree-sitter AST.
3. **Lexical (BM25) index** — идентификаторы и токены (exact-match recall).

Hybrid retrieval сливает хиты трёх индексов и возвращает ранжированный список.

**View A vs View B localization** (ключевой методологический вклад): View A (legacy) засчитывает любой путь, который агент *увидел*, включая кандидатов из result-списка движка. View B засчитывает только пути, до которых агент реально *дошёл* — result-список движка это указатель, а не прибытие; агент должен выбрать grep/read/edit по кандидату, чтобы путь вошёл в траекторию. NL-аргументы запроса к движку сохраняются в обоих view. Различие — ровно одна строка в алгоритме извлечения; правило применяется единообразно ко всем армам (для SC-OFF/OpenCode это no-op).

## Key results

- **Внутри-harness (причинно, §6.2):** View B acc@5 44.3% $\to$ 84.5% (paired Wilcoxon p<0.0001); resolve 41.9% $\to$ 50.4% (p=0.003); статистически нулевая разница per-cell cost, при этом ниже \$/solved.
- **Кросс-harness (§6.1):** SC-ON $\ge$ OpenCode на resolve (50.4% vs 45.3% mean, p=0.087) и на View B acc@5 (84.5% vs 75.3%, p=0.080) без штрафа по стоимости; \$2.30/solved у SC-ON против \$2.92 у OpenCode.
- Бенчмарки: SWE-PolyBench Verified + SWE-bench Pro public, 91 инстанс (34 Go, 20 Java, 37 Python).

## Limitations

- Одна модель (Claude Opus 4.7) — контролирует capability, но ограничивает генерализацию.
- Малые paired-n (75/80/78) → resolve-level тесты недомощны; авторы явно фиксируют это на каждом тесте.
- Только Go/Java/Python; JS/TS не покрыты.
- In-ancestry leak-остаток: где gold-fix достижим в базовой истории, scrub не может его убрать без изменения задачи — detect-and-exclude уменьшает, но не устраняет класс.
- Backend-сервис, хостящий три индекса, внутренний и не входит в released-артефакт.

## Related work

- Концепт: [[structural_codebase_index]], [[repository_exploration_coding_agents]]
- [[codebase_memory_tree_sitter_kg]] — та же идея структурного индекса, но open-source Tree-Sitter KG через MCP
- [[fastcontext]], [[sherloc]] — альтернативные подходы к тому же bottleneck'у (offload / диагностическая локализация)
- [[swe_explore]] — бенчмарк, изолирующий exploration; View B здесь — тот же field-move (agent-targeted surface)
- Проект: [[agents_context_representation/index]] — эмпирически валидирует Level 1 (граф кодовой базы)

## My notes

- Главный сдвиг рамки: индекс не *дублирует* то, чего уже достигает компетентный agentic-grep — но и не регрессирует агента; выигрыш локализации огромен, resolve скромнее. Значит ценность индекса привязана к доле multi-file задач.
- Разделение View A/View B — важный урок для оценки любой памяти coding-агента: «показали путь» $\ne$ «агент использовал путь». Прямо применимо к метрикам проекта [[agents_context_representation/index]].
- Открытый вопрос: насколько localization gain (+40pp) конвертируется в resolve при более слабой модели, где localization — более узкое горло?
