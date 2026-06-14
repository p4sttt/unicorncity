---
title: "Чеклист формул по электродинамике"
description: "Фундаментальные законы, выводы уравнений Максвелла и основы волновой теории в лаконичном виде"
state: done
date: 2026-06-13
---

# 1. Фундаментальные законы (Экспериментальный базис)

Эти законы постулированы на основе физического эксперимента и не могут быть выведены математически из других принципов.

### Закон сохранения заряда
> **Интуиция**: Заряд — это фундаментальное свойство материи, он не может исчезать в никуда или возникать из ничего. Изменение заряда в замкнутой области пространства возможно только в том случае, если заряд пересекает ее границу (переносится током).
>
> Пусть $Q$ — полный заряд внутри фиксированного объема $V$, ограниченного замкнутой поверхностью $S$. Изменение заряда за время $\mathrm{d}t$ равно $\mathrm{d}Q$. Поток заряда через границу за единицу времени — это сила тока $I$.
>
> Поскольку вектор внешней нормали к поверхности $S$ направлен наружу, вытекающий ток уносит заряд (уменьшает $Q$). Следовательно, скорость изменения заряда отрицательна при положительном вытекающем токе:

$$
\frac{\mathrm{d}Q}{\mathrm{d}t} = -I
$$

### Закон Кулона
> **Интуиция**: Точечный заряд в трехмерном пространстве создает вокруг себя поле с центральной симметрией. Линии поля расходятся радиально. На расстоянии $r$ от заряда площадь сферы, которую пронизывают эти линии, равна $4\pi r^2$.
>
> Поскольку полный поток поля через любую такую сферу должен оставаться постоянным (закон сохранения «силы» источника), плотность силовых линий падает обратно пропорционально площади сферы, то есть как $1/r^2$.
>
> Изотропность пространства требует, чтобы сила взаимодействия двух зарядов была направлена строго вдоль соединяющей их прямой (любое отклонение выделило бы направление вращения, нарушая симметрию):

$$
\vec{F}_{12} = \frac{1}{4\pi\varepsilon_0} \frac{q_1 q_2}{|\vec{r}_2 - \vec{r}_1|^3} (\vec{r}_2 - \vec{r}_1)
$$

### Сила Лоренца (Магнитное взаимодействие)
> **Интуиция**: В отличие от электрического поля, действующего на покоящиеся заряды, магнитное поле обнаруживает себя только тогда, когда заряд движется со скоростью $\vec{v}$.
>
> Опыт показывает, что магнитные силы не совершают работы над свободным зарядом, то есть всегда перпендикулярны вектору скорости (сохраняя кинетическую энергию постоянной). Они также перпендикулярны направлению самого магнитного поля $\vec{B}$.
>
> Единственный способ составить из векторов $\vec{v}$ и $\vec{B}$ силу, ортогональную обоим — использовать векторное произведение:

$$
\vec{F} = q\vec{E} + q[\vec{v}, \vec{B}]
$$

### Закон электромагнитной индукции Фарадея
> **Интуиция**: Изменение магнитного потока $\Phi_B$ во времени порождает вихревое электрическое поле.
>
> Знак минус в законе (правило Ленца) гарантирует закон сохранения энергии и устойчивость мира. Если бы знак был положительным, то любое случайное изменение магнитного поля вызывало бы ток, который усиливал бы это изменение, порождая лавинообразный саморазгон поля и токов до бесконечности без затрат внешней работы.
>
> Знак минус обеспечивает противодействие системы внешним изменениям:

$$
\mathcal{E}_i = -\frac{\mathrm{d}\Phi_B}{\mathrm{d}t}
$$

---

# 2. Вывод уравнений электро- и магнитостатики и энергии полей

Ниже приведены лаконичные выводы основных локальных уравнений и энергетических характеристик.

### Уравнение непрерывности (Локальное сохранение заряда)
$$
Q = \int_V \rho \, \mathrm{d}V, \quad I = \oint_S (\vec{j}, \mathrm{d}\vec{S})
$$

$$
\frac{\mathrm{d}}{\mathrm{d}t} \int_V \rho \, \mathrm{d}V = -\oint_S (\vec{j}, \mathrm{d}\vec{S})
$$

$$
\int_V \frac{\partial \rho}{\partial t} \mathrm{d}V = -\int_V \operatorname{div}\vec{j} \, \mathrm{d}V
$$

$$
\boxed{\frac{\partial \rho}{\partial t} + \operatorname{div}\vec{j} = 0}
$$

### Дивергенция электрического поля (Закон Гаусса)
$$
\vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3} \mathrm{d}V'
$$

$$
\operatorname{div}\vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \operatorname{div}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) \mathrm{d}V'
$$

$$
\text{Используя тождество: } \operatorname{div}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) = 4\pi \delta(\vec{r} - \vec{r}')
$$

$$
\operatorname{div}\vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \cdot 4\pi \delta(\vec{r} - \vec{r}') \mathrm{d}V'
$$

$$
\boxed{\operatorname{div}\vec{E} = \frac{\rho}{\varepsilon_0}} \iff \oint_S (\vec{E}, \mathrm{d}\vec{S}) = \frac{1}{\varepsilon_0}\int_V \rho \, \mathrm{d}V
$$

### Ротор электростатического поля (Потенциальность)
$$
\vec{E} = \frac{q}{4\pi\varepsilon_0 r^3} \vec{r}
$$

$$
\oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = \frac{q}{4\pi\varepsilon_0} \oint_{\Gamma} \frac{\mathrm{d}r}{r^2} = 0
$$

$$
\text{По теореме Стокса: } \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = \int_S (\operatorname{rot}\vec{E}, \mathrm{d}\vec{S}) = 0
$$

$$
\boxed{\operatorname{rot}\vec{E} = 0} \implies \vec{E} = -\operatorname{grad}\varphi
$$

### Дивергенция магнитного поля (Соленоидальность)

$$
\vec{B}(\vec{r}) = \frac{\mu_0}{4\pi} \int_V \frac{[\vec{j}(\vec{r}'), \vec{r} - \vec{r}']}{|\vec{r} - \vec{r}'|^3} \mathrm{d}V'
$$

$$
\operatorname{div}\vec{B}(\vec{r}) = \frac{\mu_0}{4\pi} \int_V \operatorname{div}_{\vec{r}} \left( \frac{[\vec{j}(\vec{r}'), \vec{r} - \vec{r}']}{|\vec{r} - \vec{r}'|^3} \right) \mathrm{d}V'
$$

$$
\text{Используя тождество } \operatorname{div}[\vec{F}, \vec{G}] = (\vec{G}, \operatorname{rot}\vec{F}) - (\vec{F}, \operatorname{rot}\vec{G}) \text{ для } \vec{F} = \vec{j}(\vec{r}') \text{ и } \vec{G} = \frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}:
$$

$$
\operatorname{div}_{\vec{r}} \left( \left[\vec{j}(\vec{r}'), \frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right] \right) = -\left( \vec{j}(\vec{r}'), \operatorname{rot}_{\vec{r}}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) \right)
$$

$$
\text{Так как } \frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3} = -\nabla_{\vec{r}}\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) \text{ и ротор градиента тождественно равен нулю:}
$$

$$
\operatorname{rot}_{\vec{r}}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) = -\operatorname{rot}_{\vec{r}}\operatorname{grad}_{\vec{r}}\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) = 0
$$

$$
\boxed{\operatorname{div}\vec{B} = 0} \iff \oint_S (\vec{B}, \mathrm{d}\vec{S}) = 0
$$

### Ротор магнитного поля (Закон Ампера в вакууме)
$$
\vec{B} = \operatorname{rot}\vec{A}, \quad \vec{A} = \frac{\mu_0}{4\pi} \int_V \frac{\vec{j}(\vec{r}')}{|\vec{r} - \vec{r}'|} \mathrm{d}V'
$$

$$
\operatorname{rot}\vec{B} = \operatorname{rot}\operatorname{rot}\vec{A} = \operatorname{grad}\operatorname{div}\vec{A} - \Delta\vec{A}
$$

$$
\text{В кулоновской калибровке } \operatorname{div}\vec{A} = 0:
$$

$$
\operatorname{rot}\vec{B} = -\Delta\vec{A} = -\frac{\mu_0}{4\pi} \int_V \vec{j}(\vec{r}') \Delta\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) \mathrm{d}V'
$$

$$
\text{Учитывая, что } \Delta\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) = -4\pi \delta(\vec{r} - \vec{r}'):
$$

$$
\operatorname{rot}\vec{B} = -\frac{\mu_0}{4\pi} \int_V \vec{j}(\vec{r}') \left( -4\pi \delta(\vec{r} - \vec{r}') \right) \mathrm{d}V'
$$

$$
\boxed{\operatorname{rot}\vec{B} = \mu_0 \vec{j}} \iff \oint_{\Gamma} (\vec{B}, \mathrm{d}\vec{l}) = \mu_0 I
$$

### Энергия электростатического поля
$$
W_e = \frac{1}{2} \int_V \rho \varphi \, \mathrm{d}V
$$

$$
\text{Используя теорему Гаусса в среде } \rho = \operatorname{div}\vec{D}:
$$

$$
W_e = \frac{1}{2} \int_V \operatorname{div}\vec{D} \cdot \varphi \, \mathrm{d}V
$$

$$
\text{Применяя тождество } \operatorname{div}(\varphi\vec{D}) = \varphi\operatorname{div}\vec{D} + (\vec{D}, \nabla\varphi):
$$

$$
W_e = \frac{1}{2} \int_V \operatorname{div}(\varphi\vec{D}) \, \mathrm{d}V - \frac{1}{2} \int_V (\vec{D}, \nabla\varphi) \, \mathrm{d}V
$$

$$
\text{Первый интеграл по теореме Остроградского-Гаусса обращается в нуль на бесконечности:}
$$

$$
\oint_{\partial V} \varphi (\vec{D}, \mathrm{d}\vec{S}) \to 0
$$

$$
\text{Учитывая локальную связь } \vec{E} = -\nabla\varphi:
$$

$$
\boxed{W_e = \frac{1}{2} \int_V (\vec{D}, \vec{E}) \, \mathrm{d}V}
$$

### Энергия магнитного поля
$$
\mathrm{d}A = I \, \mathrm{d}\Phi_B
$$

$$
\text{Выражая поток через векторный потенциал } \Phi_B = \oint (\vec{A}, \mathrm{d}\vec{l}):
$$

$$
\mathrm{d}W_m = \oint I (\vec{A}, \mathrm{d}\vec{l}) = \int_V (\vec{j}, \vec{A}) \, \mathrm{d}V
$$

$$
\text{Используя уравнение закона Ампера } \vec{j} = \operatorname{rot}\vec{H}:
$$

$$
\mathrm{d}W_m = \int_V (\operatorname{rot}\vec{H}, \vec{A}) \, \mathrm{d}V
$$

$$
\text{Применяя тождество } \operatorname{div}[\vec{H}, \vec{A}] = (\vec{A}, \operatorname{rot}\vec{H}) - (\vec{H}, \operatorname{rot}\vec{A}):
$$

$$
\mathrm{d}W_m = \int_V (\vec{H}, \operatorname{rot}\vec{A}) \, \mathrm{d}V + \int_V \operatorname{div}[\vec{H}, \vec{A}] \, \mathrm{d}V
$$

$$
\text{Второй интеграл переходит в интеграл по бесконечно удаленной поверхности и обращается в нуль:}
$$

$$
\oint_{\partial V} [\vec{H}, \vec{A}] \cdot \mathrm{d}\vec{S} \to 0
$$

$$
\text{С учетом определения } \vec{B} = \operatorname{rot}\vec{A}:
$$

$$
\mathrm{d}W_m = \int_V (\vec{H}, \mathrm{d}\vec{B}) \, \mathrm{d}V
$$

$$
\text{Для линейных сред } (\vec{B} = \mu\mu_0\vec{H}) \text{ интегрирование дает:}
$$

$$
\boxed{W_m = \frac{1}{2} \int_V (\vec{B}, \vec{H}) \, \mathrm{d}V}
$$

---

# 3. Переход к нестационарным полям

### Обобщение закона Фарадея
$$
\mathcal{E}_i = \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}), \quad \Phi_B = \int_S (\vec{B}, \mathrm{d}\vec{S})
$$

$$
\oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = -\frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{B}, \mathrm{d}\vec{S})
$$

$$
\text{По теореме Стокса: } \int_S (\operatorname{rot}\vec{E}, \mathrm{d}\vec{S}) = -\int_S \frac{\partial \vec{B}}{\partial t} \mathrm{d}\vec{S}
$$

$$
\boxed{\operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t}}
$$

### Введение тока смещения
Уравнение магнитостатики $\operatorname{rot}\vec{B} = \mu_0 \vec{j}$ противоречит закону сохранения заряда $\operatorname{div}\vec{j} + \frac{\partial \rho}{\partial t} = 0$, так как $\operatorname{div}\operatorname{rot}\vec{B} \equiv 0$, что требовало бы $\operatorname{div}\vec{j} = 0$.

$$
\operatorname{rot}\vec{B} = \mu_0 (\vec{j} + \vec{j}_{\text{см}})
$$

$$
\operatorname{div}\operatorname{rot}\vec{B} = \mu_0 \operatorname{div}(\vec{j} + \vec{j}_{\text{см}}) = 0 \implies \operatorname{div}\vec{j}_{\text{см}} = -\operatorname{div}\vec{j} = \frac{\partial \rho}{\partial t}
$$

$$
\text{Из закона Гаусса: } \rho = \operatorname{div}\vec{D} \implies \operatorname{div}\vec{j}_{\text{см}} = \frac{\partial}{\partial t}(\operatorname{div}\vec{D}) = \operatorname{div}\left(\frac{\partial \vec{D}}{\partial t}\right)
$$

$$
\vec{j}_{\text{см}} = \frac{\partial \vec{D}}{\partial t}
$$

$$
\boxed{\operatorname{rot}\vec{H} = \vec{j} + \frac{\partial \vec{D}}{\partial t}}
$$

---

# 4. Потенциалы электромагнитного поля и калибровка

### Обоснование существования потенциалов (Теоремы векторного анализа)
- **Существование векторного потенциала $\vec{A}$**:
  Из 4-го уравнения Максвелла:

$$
\operatorname{div}\vec{B} = 0
$$

  *Теорема векторного анализа*: Если дивергенция векторного поля всюду равна нулю (поле соленоидально), то его можно представить как ротор другого векторного поля $\vec{A}$:

$$
\boxed{\vec{B} = \operatorname{rot}\vec{A}}
$$

- **Существование скалярного потенциала $\varphi$**:
  Подставим $\vec{B} = \operatorname{rot}\vec{A}$ во 2-е уравнение Максвелла:

$$
\operatorname{rot}\vec{E} = -\frac{\partial}{\partial t}(\operatorname{rot}\vec{A}) \implies \operatorname{rot}\left(\vec{E} + \frac{\partial \vec{A}}{\partial t}\right) = 0
$$

  *Теорема векторного анализа*: Если ротор векторного поля равен нулю (поле безвихревое), то его можно выразить через градиент некоторого скалярного поля $\varphi$:

$$
\vec{E} + \frac{\partial \vec{A}}{\partial t} = -\operatorname{grad}\varphi \implies \boxed{\vec{E} = -\operatorname{grad}\varphi - \frac{\partial \vec{A}}{\partial t}}
$$

### Неоднозначность потенциалов (Градиентная инвариантность)
Физические поля $\vec{E}$ и $\vec{B}$ не изменятся при переходе к новым потенциалам $\vec{A}'$ и $\varphi'$ с использованием произвольной скалярной функции $\psi(\vec{r}, t)$:

$$
\vec{A}' = \vec{A} + \operatorname{grad}\psi
$$

$$
\varphi' = \varphi - \frac{\partial \psi}{\partial t}
$$

Доказательство инвариантности:

$$
\vec{B}' = \operatorname{rot}\vec{A}' = \operatorname{rot}\vec{A} + \operatorname{rot}\operatorname{grad}\psi = \vec{B} + 0 = \vec{B}
$$

$$
\vec{E}' = -\operatorname{grad}\varphi' - \frac{\partial \vec{A}'}{\partial t} = -\operatorname{grad}\left(\varphi - \frac{\partial\psi}{\partial t}\right) - \frac{\partial}{\partial t}\left(\vec{A} + \operatorname{grad}\psi\right) = -\operatorname{grad}\varphi - \frac{\partial \vec{A}}{\partial t} = \vec{E}
$$

### Калибровочные условия
Для однозначного определения потенциалов накладывают дополнительные условия связи.

- **Кулоновская калибровка**:

$$
\operatorname{div}\vec{A} = 0
$$

  > **Интуиция**: Устраняет продольную степень свободы векторного потенциала. Применяется главным образом в магнитостатике, где сводит уравнения для $\vec{A}$ к простому уравнению Пуассона. При этом скалярный потенциал $\varphi$ мгновенно определяется распределением зарядов в пространстве (как в электростатике), что крайне удобно в нерелятивистских задачах.

- **Лоренцевская калибровка**:

$$
\operatorname{div}\vec{A} + \frac{1}{c^2} \frac{\partial \varphi}{\partial t} = 0
$$

  > **Интуиция**: Объединяет пространственные и временные производные потенциалов в лоренц-инвариантное условие. Она восстанавливает четырехмерную пространственно-временную симметрию, соответствуя условию поперечности четырехпотенциала ($\partial_\mu A^\mu = 0$). Позволяет полностью разделить уравнения для $\vec{A}$ и $\varphi$, сводя их к независимым волновым уравнениям Даламбера.

---

# 5. Полная система уравнений Максвелла

### В дифференциальной форме
$$
\operatorname{rot}\vec{H} = \vec{j} + \frac{\partial \vec{D}}{\partial t}
$$

$$
\operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t}
$$

$$
\operatorname{div}\vec{D} = \rho
$$

$$
\operatorname{div}\vec{B} = 0
$$

### В интегральной форме
$$
\oint_{\Gamma} (\vec{H}, \mathrm{d}\vec{l}) = I + \frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{D}, \mathrm{d}\vec{S})
$$

$$
\oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = -\frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{B}, \mathrm{d}\vec{S})
$$

$$
\oint_S (\vec{D}, \mathrm{d}\vec{S}) = Q
$$

$$
\oint_S (\vec{B}, \mathrm{d}\vec{S}) = 0
$$

---

# 6. Вывод основных формул волновой теории

### Волновые уравнения для потенциалов (Уравнения Даламбера)
Подставим выражение $\vec{E} = -\operatorname{grad}\varphi - \frac{\partial \vec{A}}{\partial t}$ в уравнение $\operatorname{div}\vec{E} = \frac{\rho}{\varepsilon_0}$:

$$
\operatorname{div}\left( -\operatorname{grad}\varphi - \frac{\partial \vec{A}}{\partial t} \right) = \frac{\rho}{\varepsilon_0} \implies -\Delta\varphi - \frac{\partial}{\partial t}(\operatorname{div}\vec{A}) = \frac{\rho}{\varepsilon_0}
$$

Применяя калибровочное условие Лоренца $\operatorname{div}\vec{A} = -\frac{1}{c^2}\frac{\partial\varphi}{\partial t}$:

$$
-\Delta\varphi - \frac{\partial}{\partial t}\left( - \frac{1}{c^2} \frac{\partial\varphi}{\partial t} \right) = \frac{\rho}{\varepsilon_0}
$$

$$
\boxed{\Delta\varphi - \frac{1}{c^2}\frac{\partial^2\varphi}{\partial t^2} = -\frac{\rho}{\varepsilon_0}} \iff \square \varphi = -\frac{\rho}{\varepsilon_0}
$$

где $\square = \Delta - \frac{1}{c^2}\frac{\partial^2}{\partial t^2}$ — оператор Даламбера (даламбериан).

Для векторного потенциала $\vec{A}$, используя $\operatorname{rot}\vec{B} = \mu_0\vec{j} + \frac{1}{c^2}\frac{\partial\vec{E}}{\partial t}$ в вакууме:

$$
\operatorname{rot}\operatorname{rot}\vec{A} = \mu_0\vec{j} + \frac{1}{c^2}\frac{\partial}{\partial t}\left( -\operatorname{grad}\varphi - \frac{\partial \vec{A}}{\partial t} \right)
$$

$$
\operatorname{grad}\operatorname{div}\vec{A} - \Delta\vec{A} = \mu_0\vec{j} - \frac{1}{c^2}\operatorname{grad}\frac{\partial\varphi}{\partial t} - \frac{1}{c^2}\frac{\partial^2\vec{A}}{\partial t^2}
$$

Используя градиент калибровки Лоренца $\operatorname{grad}\left( \operatorname{div}\vec{A} + \frac{1}{c^2}\frac{\partial\varphi}{\partial t} \right) = 0$:

$$
\boxed{\Delta\vec{A} - \frac{1}{c^2}\frac{\partial^2\vec{A}}{\partial t^2} = -\mu_0\vec{j}} \iff \square \vec{A} = -\mu_0\vec{j}
$$

### Волновое уравнение (в вакууме для векторов полей: $\vec{j}=0, \rho=0$)
$$
\operatorname{rot}\vec{E} = -\mu_0 \frac{\partial \vec{H}}{\partial t}, \quad \operatorname{rot}\vec{H} = \varepsilon_0 \frac{\partial \vec{E}}{\partial t}
$$

$$
\operatorname{rot}\operatorname{rot}\vec{E} = -\mu_0 \frac{\partial}{\partial t}(\operatorname{rot}\vec{H})
$$

$$
\operatorname{grad}\operatorname{div}\vec{E} - \Delta\vec{E} = -\mu_0 \varepsilon_0 \frac{\partial^2 \vec{E}}{\partial t^2}
$$

$$
\text{Так как } \operatorname{div}\vec{E} = 0 \text{ и } c = \frac{1}{\sqrt{\varepsilon_0\mu_0}}:
$$

$$
\boxed{\Delta\vec{E} - \frac{1}{c^2}\frac{\partial^2\vec{E}}{\partial t^2} = 0}
$$

### Плоская электромагнитная волна
$$
\vec{E}(\vec{r}, t) = \vec{E}_0 e^{i(\omega t - \vec{k}\vec{r})}, \quad \vec{H}(\vec{r}, t) = \vec{H}_0 e^{i(\omega t - \vec{k}\vec{r})}
$$

$$
\text{Подставляем в дифференциальные операторы: } \nabla \to -i\vec{k}, \quad \frac{\partial}{\partial t} \to i\omega
$$

$$
\operatorname{div}\vec{E} = 0 \implies (\vec{k}, \vec{E}) = 0 \quad (\text{Поперечность})
$$

$$
\operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t} \implies -i[\vec{k}, \vec{E}] = -i\omega\mu\mu_0 \vec{H}
$$

$$
\vec{H} = \frac{1}{\omega\mu\mu_0} [\vec{k}, \vec{E}] = \frac{k}{\omega\mu\mu_0} [\vec{e}_k, \vec{E}]
$$

$$
\text{С учетом } \frac{\omega}{k} = v = \frac{1}{\sqrt{\varepsilon\varepsilon_0\mu\mu_0}}:
$$

$$
\boxed{\vec{H} = \sqrt{\frac{\varepsilon\varepsilon_0}{\mu\mu_0}} [\vec{e}_k, \vec{E}]}
$$

### Вектор Умова-Пойнтинга и закон сохранения энергии
$$
\operatorname{div}[\vec{E}, \vec{H}] = (\vec{H}, \operatorname{rot}\vec{E}) - (\vec{E}, \operatorname{rot}\vec{H})
$$

$$
\operatorname{div}[\vec{E}, \vec{H}] = \left(\vec{H}, -\frac{\partial \vec{B}}{\partial t}\right) - \left(\vec{E}, \vec{j} + \frac{\partial \vec{D}}{\partial t}\right)
$$

$$
\operatorname{div}[\vec{E}, \vec{H}] = -\frac{\partial}{\partial t}\left(\frac{(\vec{E}, \vec{D}) + (\vec{H}, \vec{B})}{2}\right) - (\vec{j}, \vec{E})
$$

$$
\text{Вводя плотность энергии } w = \frac{(\vec{E},\vec{D})+(\vec{H},\vec{B})}{2} \text{ и вектор Пойнтинга } \vec{S} = [\vec{E}, \vec{H}]:
$$

$$
\boxed{\operatorname{div}\vec{S} + \frac{\partial w}{\partial t} = -(\vec{j}, \vec{E})}
$$
