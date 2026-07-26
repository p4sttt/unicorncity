---
title: "Tree Borrows"
description: "Villani, Hostert, Dreyer, Jung; PLDI 2025; замена стека в Stacked Borrows деревом + state machine на узел; принимает на 54% меньше тест-кейсов как UB, поддерживает two-phase borrows и read-read reorderings"
type: paper-summary
tags: [pl-theory, rust, aliasing, operational-semantics, unsafe, compiler-optimizations, formal-verification]
status: done
created: 2026-07-13
updated: 2026-07-13
sources:
  - raw/papers/processed/tree_borrows_pldi2025.md
---

## TL;DR

Tree Borrows (TB) — преемник [[stacked_borrows]], устраняющий три его ключевых ограничения: отсутствие two-phase borrows, статические bounds на диапазон памяти ссылки, и невозможность переупорядочивать соседние чтения. Вместо per-location стека тегов TB хранит дерево ссылок, каждый узел которого прогоняет state machine (Reserved / Unique / Frozen / Disabled). Проверка на 30 000 crates: TB отклоняет как UB на 54% меньше реального кода, чем SB, при практически нулевом регрессе.

## Core contribution

1. **Tree вместо Stack**: иерархия ссылок представлена деревом; branching factor > 1 позволяет отслеживать two-phase borrows и несколько «живых» дочерних ссылок одновременно.
2. **State machine на узел**: каждый узел/тег в каждой ячейке памяти хранит состояние (`Reserved → Unique → Frozen → Disabled`), меняющееся при локальных и foreign accesses.
3. **Динамические reference ranges**: raw pointer наследует тег родительской ссылки, что разрешает выход за статические type bounds.
4. **Read-read reordering**: состояние `Frozen` (`Unique` после foreign read) не теряет read-permission → смена порядка двух чтений не создаёт UB.

## Method

### Дерево и теги

Каждая ссылка при создании получает новый тег и вставляется в дерево как потомок той ссылки/переменной, из которой создана. Raw pointer **не получает** нового тега — наследует тег родителя (ключевое отличие от SB).

### State machine (рис. 1 из статьи)

```
&mut T  → начало: Reserved
&T      → начало: Frozen
raw ptr → наследует тег родителя
```

| Состояние | Local Read | Local Write | Foreign Read | Foreign Write |
|-----------|-----------|-------------|--------------|---------------|
| Reserved  | OK        | → Unique    | OK           | → Disabled    |
| Unique    | OK        | OK          | → Frozen     | → Disabled    |
| Frozen    | OK        | UB          | OK           | → Disabled    |
| Disabled  | UB        | UB          | —            | —             |

*Для protected references: переход в Disabled заменяется немедленным UB; плюс Reserved с conflicted-флагом при foreign read → local write вызывает UB.*

### Two-phase borrows и состояние Reserved

Неявные mutable borrows (v.push(v.len())) начинают жизнь как `Reserved`, допуская foreign reads в период «резервации». Первая запись активирует ссылку (→ `Unique`). Это решает главную боль SB, где two-phase borrows трактовались как raw pointers.

### Frozen для read-read reordering

Когда `Unique`-ссылка встречает foreign read, она переходит в `Frozen`, а не `Disabled`. `Frozen` по-прежнему допускает чтения, поэтому порядок двух независимых чтений можно менять без UB — редкий случай, когда меньше UB даёт больше оптимизаций.

### Динамические reference ranges

`&mut v[0] as *mut i32` создаёт разрешение `Reserved` не только для байт под `v[0]`, но **на весь аллок**. Так raw pointer может легально обратиться к `v[1]` — паттерн, отклоняемый SB.

### Протекторы

Функция-аргумент получает protected-тег (как в SB, но мощнее):
- protected `Unique` → foreign read вместо `Frozen` → немедленный UB.
- Добавлен conflicted-флаг: если protected Reserved получил foreign read, то последующий local write → UB. Это оправдывает «поднять запись выше чтения» (Example 14 из статьи).
- При снятии протектора выполняются **implicit accesses** (implicit read для Frozen/Reserved, implicit write для Unique) — гарантирует, что состояния source и target сходятся к моменту окончания вызова.

### Formal verification

Proofs in Rocq (~32K LOC), используя Simuliris (relational separation logic поверх Iris). Доказаны:
- Удаление дублированных reads (Example 17).
- Удаление избыточного write при protected mutable reference (Example 18).
- Read-read reordering (Example 19) — в sequential модели.

## Key results

| Метрика | Значение |
|---------|----------|
| Тест-кейсов всего | 674 748 (30 000 crates) |
| Passed filtering | ~68% |
| Borrow UB под SB | 6 568 тестов |
| Borrow UB под TB | 3 023 теста (−54%) |
| Тестов, которые SB принимал, а TB отклоняет | 31 |

Все 31 «сломанных» кейса связаны с SB-специфичным «quirk» raw pointer handling или c Interior Mutability без правильного UnsafeCell; для большинства был разработан и принят исправляющий патч.

## Limitations

- **Activating write нельзя двигать вниз** (ограничение доказательного фреймворка).
- Оптимизации, требующие reasoning о data races, пока не верифицированы формально.
- No framework для доказательства корректности *программ* под TB (есть для optimizations); это — за рамками статьи.
- Performance в Miri под TB медленнее, чем под SB (больше timeouts на большие циклы).

## Related work

- [[stacked_borrows]] — предшественник; TB заменяет его во всех смыслах для практического кода
- [[rust_aliasing_model]] — концептуальный обзор
- Simuliris / Iris — proof framework, используемый для формальных доказательств TB
- Miri — TB реализован в Miri, доступен через `MIRIFLAGS="-Zmiri-tree-borrows"`
- LLVM `noalias` — TB спроектирован так, чтобы гарантировать корректность всех оптимизаций, которые LLVM выполняет под noalias

## My notes

- Переход от стека к дереву — минимальное расширение структуры, но устраняет все три главных кейса несовместимости с реальным кодом.
- `Frozen` — элегантное решение: «я всё ещё читабелен, но потерял уникальность» — одновременно обозначает деградировавший `&mut T` и исходное состояние `&T`.
- Raw pointer без нового тега — радикальная идея по сравнению с SB; логична, потому что raw pointer «это просто адрес родителя без type-system checks».
- Conflicted-флаг в Reserved — price за поддержку two-phase borrows; делает семантику чуть менее минималистичной, но необходимым.
- 54% сокращение при 31 новом нарушении → очевидный Net Win; практически доказывает, что SB был слишком строгим.
