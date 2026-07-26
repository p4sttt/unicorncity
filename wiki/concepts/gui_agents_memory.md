---
title: "Memory Systems for GUI Agents"
description: "Типы памяти (эпизодическая, семантическая, опытная) и эволюционные механизмы в MLLM-агентах для автоматизации GUI"
type: concept
tags: [llm, agents, gui, memory, mllm]
status: in-progress
created: 2026-07-12
updated: 2026-07-12
sources: []
---

## Definition

GUI-агенты автоматизируют взаимодействие с графическими интерфейсами (мобильные приложения, веб, десктоп). Память — механизм преодоления двух базовых ограничений: (1) контекстное окно не вмещает полную историю задачи; (2) стратегии прошлых задач не переносятся в новые без явного хранения.

## Intuition

Человек, освоивший бронирование авиабилетов на одном сайте, легко справляется с похожим сайтом — он помнит паттерн, а не каждое нажатие. GUI-память формализует это: хранит паттерны (опытная), правила (семантическая) и текущий прогресс (эпизодическая).

## Три типа памяти (по SE-GA)

### Эпизодическая память

Скользящее окно последних действий: $C^{epi}_t = [m_k]_{k=\epsilon}^{t-1}$, $m_k = \langle o_k, a_k, o_{k+1} \rangle$.
- Назначение: отслеживать прогресс в текущей задаче
- Ограничение: не переносится между задачами

### Семантическая память

Абстрактные правила взаимодействия, накопленные со временем (напр. "Login before accessing restricted pages").
- Retrieval через cosine similarity текстовых embeddings
- Аналог procedural memory / long-term knowledge

### Опытная память

Успешные траектории аналогичных прошлых задач.
- Dual retrieval: семантика инструкции + визуальное сходство текущего экрана
- Детерминированное воспроизведение $\to$ устранение variance генерации

## Evolutionary Memory (DMS)

[[darwinian_memory_system_gui_agents]] добавляет к этим типам механизм отбора:

- **$\varepsilon$-мутация**: с вероятностью $\varepsilon$ решает подзадачу заново — если эффективнее, заменяет
- **Survival value**: popularity $\times$ decay $\times$ reliability $\to$ auto-pruning через Elbow Method
- **Байесовская оценка рисков**: высоко-рисковые записи создают evolutionary pressure

## Parametric vs Non-parametric

| Подход | Тип | Примеры |
|--------|-----|---------|
| RAG-based cache | Non-parametric | DMS, EchoTrail-GUI |
| Fine-tuning на опыте | Parametric | SE-GA MASE |
| Hybrid | Параметрический + кэш | SE-GA (TTME + MASE) |

Non-parametric: быстрый запуск, но не улучшает базовую политику.
Parametric: медленнее, но улучшения "встроены" в модель навсегда.

## Ключевые проблемы поля

1. **Context pollution** — устаревшие стратегии засоряют память $\to$ решение: DMS survival value
2. **Granularity mismatch** — монолитные траектории слишком жёсткие для динамичных GUI $\to$ решение: DMS sub-task decomposition
3. **Cold start** — нет памяти для новых приложений → частичное решение: SE-GA semantic memory с universal rules

## Key papers

- [[se_ga_self_evolving_gui_agent]] — TTME иерархическая память + MASE
- [[darwinian_memory_system_gui_agents]] — эволюционная self-regulating память
- [[context_management_llm_agents]] — обобщённый взгляд на context management

## Open questions

- Как масштабировать memory при сотнях приложений? Нужна ли иерархия памяти по приложению?
- Оптимальный $\lambda$ в dual retrieval SE-GA: когда визуальное сходство важнее семантического?
