---
title: "SHERLOC: Structured Diagnostic Localization for Code Repair Agents"
description: "Tamoyan et al. (NVIDIA/TU Darmstadt), 2026; training-free reasoning-LLM + компактные repo-tools + self-recovery; SOTA-локализация (84.33% acc@1 SWE-Bench Lite) + структурные diagnostic-findings, дающие +5.95pp resolve при -36.7% localization-токенов"
type: paper-summary
tags: [llm, agents, coding, retrieval, benchmark, efficiency]
status: in-progress
created: 2026-07-19
updated: 2026-07-19
sources: ["raw/papers/processed/SHERLOC Structured Diagnostic Localization for Code Repair Agents-with-annotations.md"]
---

## TL;DR

LLM-агенты тратят ~половину бюджета на локализацию бага до первой правки (в среднем 18.5 ходов, 48% взаимодействия, >320k токенов/инстанс). Существующие localization-фреймворки оценивают себя как file-retrieval, отдавая локации *без диагностического контекста*. SHERLOC — **training-free** фреймворк: reasoning-LLM + компактные LLM-friendly repo-tools + self-recovery, который для каждой локации выдаёт структурированный **diagnostic finding**. Достигает SOTA-локализации (84.33% acc@1 на SWE-Bench Lite, 81.27% recall@1 на Verified), а инъекция его локаций+находок в repair-агентов даёт в среднем **+5.95pp resolve** при **-36.7% localization-** и **-23.1% total-токенов**.

## Core contribution

- Тезис: file-path говорит агенту *где* смотреть, но не *почему*; путь без root-cause гипотезы оставляет repair недоспецифицированным. SHERLOC явно производит candidate locations + root-cause анализ + actionable solution guidance.
- Для каждой предсказанной локации — структурированный finding из 5 полей: *location explanation, root cause, solution idea, dependencies, testing impact*.
- Structure-agnostic метрика локализации: chunk-level метрики над (start, end) line-span'ами (coverage recall, precision, average tightness) — альтернатива function-/class-/module-level оценке, т.к. не каждый patch-target лежит в синтаксической единице.
- Cross-family transfer с контролем валидности: работает через семейства моделей, gains держатся при маскировании путей из issue-текста.

## Method

**Training-free**: reasoning-LLM (Qwen3, DeepSeek и др.) + компактный набор LLM-friendly repo-tools:
- View File, Repository Tree, Search String, Import Tree (import-graph navigation).

**Self-recovery** слой: context truncation, loop detection, malformed-tool-call repair, final-turn synthesis. Без fine-tuning, без RL, без multi-agent debate.

RQ1 — может ли один reasoning-LLM с компактным структурным интерфейсом сравниться с task-specifically обученными локализаторами. RQ2 — переносятся ли локации+находки в repair-агентов и как сдвигается resolve/cost.

## Key results

- **SWE-Bench Lite:** $84.33\% \pm 0.72$ file-level acc@1 (Qwen3-235B) — SOTA, выше OrcaLoca (83.33%), SWERank (83.21%), SWE-Debate (81.67%).
- **SWE-Bench Verified:** $81.27\% \pm 1.16$ recall@1 (Qwen3-235B).
- На ~30B (Qwen3-30B): 75–76% — паритет/превосходство над agentic-методами того же масштаба.
- Инъекция в repair-агентов (OpenHands и др.): **+5.95pp** resolve на SWE-Bench Verified, **-36.7%** localization-токенов, **-23.1%** total-токенов.
- Абляции: tool-suite, self-recovery и reasoning-mode все вносят вклад; gains держатся при маскировании путей из issue.

## Limitations

- Оценка на SWE-Bench Lite/Verified (Python); мультиязычность не в фокусе.
- Лучшие числа на очень крупных моделях (235B/671B); на 30B ниже.
- Локация $\ne$ решение: сильная локализация не транслируется автоматически в resolve (мотивация RQ2).

## Related work

- Концепт: [[repository_exploration_coding_agents]] (локализация как под-задача), [[structural_codebase_index]] (import-tree = облегчённый структурный слой)
- [[code_isnt_memory_structural_index]] — тоже отделяет localization-метрику от resolve; SHERLOC training-free vs встроенный индекс
- [[fastcontext]] — обученная альтернатива для того же горла локализации
- [[swe_explore]] — chunk/line-level метрика перекликается со structure-agnostic оценкой SHERLOC
- Проект: [[agents_context_representation/index]] — 5-польный diagnostic finding близок к Level 3 (эволюционная база решений)

## My notes

- Самый практичный вывод для проекта [[agents_context_representation/index]]: локация должна нести диагностику, а не только путь. 5-польный finding (root cause / solution idea / dependencies / testing impact) — почти готовая схема записи в experiential-память Level 3.
- Training-free и уже SOTA — сильный аргумент, что структурированный tool-интерфейс + self-recovery важнее fine-tuning. Контрапункт к [[fastcontext]] (обученный explorer). Пара для очной ставки.
- Chunk-level (start,end)-метрика — лучший кандидат в общую метрику локализации для проекта, т.к. structure-agnostic; сходится с line-range из [[fastcontext]]/[[swe_explore]].
