---
title: "Rust Aliasing Model"
description: "Операционные модели алиасинга в Rust (Stacked Borrows и Tree Borrows) — формализация UB для указателей, позволяющая компилятору выполнять интрапроцедурный alias analysis даже при наличии unsafe-кода"
type: concept
tags: [pl-theory, rust, aliasing, operational-semantics, unsafe, compiler-optimizations]
status: done
created: 2026-07-13
updated: 2026-07-13
sources: []
---

## Definition

В Rust тип-система навязывает **принцип исключения**: данные в любой момент времени доступны либо через одну уникальную изменяемую ссылку (`&mut T`), либо через произвольное количество разделяемых неизменяемых ссылок (`&T`), но не одновременно. Это правило называется **aliasing discipline** и является основой для compiler alias analysis.

Aliasing model — это операционная семантика, определяющая, какие программы нарушают дисциплину настолько грубо, что объявляются имеющими **Undefined Behavior (UB)**. Компилятор вправе игнорировать программы с UB при выборе оптимизаций.

## Intuition

Compiler writers хотят знать: «если я переупорядочу вот эти два обращения к памяти — ничего не сломается?». В C/C++ ответ требует дорогого interprocedural analysis. В Rust type system уже заявляет: «`&mut T` уникален, никто другой к нему не прикоснётся». Aliasing model **динамически** проверяет, что это свойство не нарушено unsafe-кодом — и если нарушено, объявляет программу UB, освобождая компилятор от необходимости рассматривать такие случаи.

## Formal description

### Типы ссылок

| Тип | Aliasing | Mutation | Отслеживается |
|-----|---------|----------|---------------|
| `&mut T` | нет | да | borrow checker / aliasing model |
| `&T` | да | нет | borrow checker / aliasing model |
| `*mut T`, `*const T` | произвольный | произвольный | нет (unsafe) |
| `UnsafeCell<T>` | через `&T` | да | особый случай модели |

### Borrow checker (статика)

Компилятор отслеживает **lifetimes** ссылок и через **borrow checking** статически запрещает одновременное существование `&mut T` и любой другой ссылки на те же данные. Ключевые правила:
- Reborrow: `let y = &mut *x` создаёт вложенный lifetime; после `x` снова используется, `y` инвалидируется.
- Lifetime'ы ссылки на аргументы функции не должны заканчиваться раньше возврата из функции.

### Операционные модели (динамика)

Borrow checker работает только с safe-кодом. Unsafe-код обходит проверки — но должен следовать правилам aliasing model, иначе программа имеет UB.

#### Stacked Borrows (POPL 2020, Jung et al.)

→ подробнее: [[stacked_borrows]]

- Каждой ячейке памяти сопоставляется **borrow stack** из тегированных элементов (`Unique(t)`, `SharedRO(t)`, `SharedRW(t)`).
- Каждая ссылка получает уникальный тег при создании (`retag`).
- Доступ через тег `t` требует, чтобы элемент с этим тегом находился в стеке; все элементы **выше** него снимаются (инвалидируются).
- Нарушение → UB.
- Protectors: снятие элемента с активным протектором → UB (для аргументов функций).

Проблемы SB:
1. Не поддерживает two-phase borrows.
2. Статические memory bounds на raw pointers.
3. Соседние чтения нельзя переупорядочивать без ограничений.

#### Tree Borrows (PLDI 2025, Villani et al.)

→ подробнее: [[tree_borrows]]

- Стек заменяется **деревом ссылок**: каждая ссылка — потомок той, из которой была создана.
- Каждый узел хранит **state machine** с состояниями: `Reserved → Unique → Frozen → Disabled`.
- Raw pointer **не получает нового тега** (наследует тег родителя), что разрешает выход за статические bounds.
- Foreign read переводит `Unique → Frozen` (не Disabled), что делает read-read reordering корректным.
- Two-phase borrows: ссылки начинают жизнь в `Reserved`, допускающем foreign reads до первой записи.

### Miri

Интерпретатор Rust, реализующий Stacked Borrows (по умолчанию) и Tree Borrows (`MIRIFLAGS="-Zmiri-tree-borrows"`). Используется авторами для эмпирической валидации моделей на реальном коде.

## Key papers

- [[stacked_borrows]] — Jung et al., POPL 2020; borrow stack + Coq verification
- [[tree_borrows]] — Villani, Hostert, Dreyer, Jung; PLDI 2025; tree + Rocq verification

## Variants

| Аспект | Stacked Borrows | Tree Borrows |
|--------|-----------------|--------------|
| Структура | per-location stack | per-alloc tree |
| Raw pointers | отдельный тег `SharedRW(⊥)` | наследуют тег родителя |
| Two-phase borrows | нет (treated as raw ptr) | `Reserved` state |
| Read-read reordering | не поддерживается | поддерживается через `Frozen` |
| Memory bounds | статические (по типу) | динамические |
| Rejected real-world code | 6 568 тестов | 3 023 теста (−54%) |
| Формальная верификация | Coq | Rocq + Simuliris |

## Open questions

- Как интегрировать алиасинг-модели с reasoning о data races (concurrent Rust)?
- Возможна ли официальная стандартизация aliasing model в Rust (пока оба — предложения, не стандарт)?
- Существует ли aliasing model, позволяющая все оптимизации SB + все оптимизации TB без компромиссов?
- Как формализовать связь TB с LLVM `noalias` семантикой?
