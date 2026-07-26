---
title: "EAM: Enhancing Anything with Diffusion Transformers for Blind Super-Resolution"
description: "DiT-based blind SR framework with triple-flow $\\Psi$-DiT architecture, progressive MIM training, and subject-aware prompting"
type: paper-summary
tags: [cv, diffusion, transformers, super-resolution, low-level-vision, dit]
status: done
created: 2026-07-12
updated: 2026-07-12
sources: [raw/papers/processed/2505.05209v4.pdf]
---

## TL;DR

EAM (Enhancing Anything Model) заменяет парадигму ControlNet в диффузионном супер-разрешении. Вместо изолированного контрольного ответвления авторы строят тройной поток (text + noisy latent + LR latent) на базе DiT, соединяя ветки через attention. Это снимает ключевое ограничение ControlNet: деградированный LR теперь напрямую взаимодействует с main-branch модели.

## Core contribution

1. **$\Psi$-DiT** — тройной поток на базе MM-DiT (Flux/SD3): три отдельных потока токенов (текст, зашумленный латент, LR-латент), связанных через cross-modal attention. Контрольная ветка текста заморожена; обучается только новая LR-ветка.
2. **Progressive MIM (PMS)** — curriculum-обучение: маска начинается с высокого ratio ($\approx$T2I-режим) и постепенно снижается, плавно переводя модель из text-to-image в image-to-image. Стабилизирует обучение и улучшает детализацию.
3. **Subject-aware prompting** — VLM (MiniCPM) с in-context learning: сначала локализует фокальные области изображения, затем даёт подробное описание фокуса и спекулятивное описание фона. Промпты богаче и тематически точнее.

## Method

### $\Psi$-DiT (Triple-flow)

Оригинальный MM-DiT (двойной поток: текст + latent) расширен до тройного:

```
Text tokens  ─────┐
Noisy latent ─────┤──── Joint Attention ────► output
LR latent    ─────┘
```

Новый модуль **SSCM** (Separable Stream Control Module) конкатенирует QKV noisy latent и LR latent по токенному измерению для совместного attention. После сплиттинга:
- Часть noisy latent → merge с основной веткой через linear + zero-init layer
- Часть LR latent → MLP → следующий блок

Инициализация весов LR-ветки — копия весов noisy latent branch (близкая модальность).

### Progressive MIM Strategy

Ratio маски убывает по формуле:
$$r = 1 - (1 - r_{min}) \cdot (\lfloor p \cdot c / k \rfloor + \sigma) / c, \quad p < k$$

После $p \geq k$: $r = r_{min}$ (SFT на полных парах). Это даёт:
- Начало: большая маска → модель "думает", что это T2I → прогревает генерацию
- Конец: маленькая маска → модель учится восстанавливать конкретный LR контент

### Subject-aware prompts

Пайплайн: MiniCPM получает exemplar-пары (изображение → идеальный промпт) через in-context learning → автоматически аннотирует весь датасет. Промпты содержат детальное описание фокальных зон + спекулятивные описания фона.

## Key results

| Метод | RealPhoto (LPIPS↓) | DIV2K (PSNR↑) |
|-------|-------------------|----------------|
| SeeSR | — | — |
| SUPIR | — | — |
| **EAM** | **SOTA** | **SOTA** |

EAM превосходит PASD, SeeSR, SUPIR, DiffBIR по перцептивным метрикам (LPIPS, DISTS) и визуальному качеству на реальных датасетах. Абляции подтверждают: тройной поток > ControlNet; PMS критичен для стабильности; subject-aware промпты улучшают детализацию лиц и текстур.

## Limitations

- Базовая модель — закрытый DiT (по-видимому Flux или FLUX.1-dev); результаты привязаны к конкретной архитектуре
- PMS усложняет pipeline обучения по сравнению с простым SFT
- Inference медленнее ГАН-методов из-за диффузионных шагов

## Related work

- [[diffusion_transformers]] — архитектура MM-DiT как основа
- [[blind_super_resolution]] — постановка задачи
- [[controlnet]] — преодолеваемая парадигма
- [[masked_image_modeling]] — используется как вспомогательный приём

## My notes

Ключевой insight: ControlNet изолирует ветки через feature injection, что мешает main-branch "видеть" LR. $\Psi$-DiT решает это через attention — LR участвует в формировании joint representation наравне с текстом. Вопрос: насколько это переносимо на другие DiT-базы (DiT-XL, SiT)?

Progressive MIM — элегантный способ использовать curriculum learning для задач image-to-image поверх T2I-модели. Потенциально применимо к другим low-level задачам (деблюр, инпейнтинг).
