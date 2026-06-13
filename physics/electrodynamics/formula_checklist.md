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
>
> $$ \frac{\mathrm{d}Q}{\mathrm{d}t} = -I $$

### Закон Кулона
> **Интуиция**: Точечный заряд в трехмерном пространстве создает вокруг себя поле с центральной симметрией. Линии поля расходятся радиально. На расстоянии $r$ от заряда площадь сферы, которую пронизывают эти линии, равна $4\pi r^2$.
>
> Поскольку полный поток поля через любую такую сферу должен оставаться постоянным (закон сохранения «силы» источника), плотность силовых линий падает обратно пропорционально площади сферы, то есть как $1/r^2$.
>
> Изотропность пространства требует, чтобы сила взаимодействия двух зарядов была направлена строго вдоль соединяющей их прямой (любое отклонение выделило бы направление вращения, нарушая симметрию):
>
> $$ \vec{F}_{12} = \frac{1}{4\pi\varepsilon_0} \frac{q_1 q_2}{|\vec{r}_2 - \vec{r}_1|^3} (\vec{r}_2 - \vec{r}_1) $$

### Сила Лоренца (Магнитное взаимодействие)
> **Интуиция**: В отличие от электрического поля, действующего на покоящиеся заряды, магнитное поле обнаруживает себя только тогда, когда заряд движется со скоростью $\vec{v}$.
>
> Опыт показывает, что магнитные силы не совершают работы над свободным зарядом, то есть всегда перпендикулярны вектору скорости (сохраняя кинетическую энергию постоянной). Они также перпендикулярны направлению самого магнитного поля $\vec{B}$.
>
> Единственный способ составить из векторов $\vec{v}$ и $\vec{B}$ силу, ортогональную обоим — использовать векторное произведение:
>
> $$ \vec{F} = q\vec{E} + q[\vec{v}, \vec{B}] $$

### Закон электромагнитной индукции Фарадея
> **Интуиция**: Изменение магнитного потока $\Phi_B$ во времени порождает вихревое электрическое поле.
>
> Знак минус в законе (правило Ленца) гарантирует закон сохранения энергии и устойчивость мира. Если бы знак был положительным, то любое случайное изменение магнитного поля вызывало бы ток, который усиливал бы это изменение, порождая лавинообразный саморазгон поля и токов до бесконечности без затрат внешней работы.
>
> Знак минус обеспечивает противодействие системы внешним изменениям:
>
> $$ \mathcal{E}_i = -\frac{\mathrm{d}\Phi_B}{\mathrm{d}t} $$

---

# 2. Вывод уравнений электро- и магнитостатики

Ниже приведены лаконичные выводы основных локальных уравнений.

### Уравнение непрерывности (Локальное сохранение заряда)
$$ Q = \int_V \rho \, \mathrm{d}V, \quad I = \oint_S (\vec{j}, \mathrm{d}\vec{S}) $$

$$ \frac{\mathrm{d}}{\mathrm{d}t} \int_V \rho \, \mathrm{d}V = -\oint_S (\vec{j}, \mathrm{d}\vec{S}) $$

$$ \int_V \frac{\partial \rho}{\partial t} \mathrm{d}V = -\int_V \operatorname{div}\vec{j} \, \mathrm{d}V $$

$$ \boxed{\frac{\partial \rho}{\partial t} + \operatorname{div}\vec{j} = 0} $$

### Дивергенция электрического поля (Закон Гаусса)
$$ \vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3} \mathrm{d}V' $$

$$ \operatorname{div}\vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \operatorname{div}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) \mathrm{d}V' $$

$$ \text{Используя тождество: } \operatorname{div}\left(\frac{\vec{r} - \vec{r}'}{|\vec{r} - \vec{r}'|^3}\right) = 4\pi \delta(\vec{r} - \vec{r}') $$

$$ \operatorname{div}\vec{E}(\vec{r}) = \frac{1}{4\pi\varepsilon_0} \int_V \rho(\vec{r}') \cdot 4\pi \delta(\vec{r} - \vec{r}') \mathrm{d}V' $$

$$ \boxed{\operatorname{div}\vec{E} = \frac{\rho}{\varepsilon_0}} \iff \oint_S (\vec{E}, \mathrm{d}\vec{S}) = \frac{1}{\varepsilon_0}\int_V \rho \, \mathrm{d}V $$

### Ротор электростатического поля (Потенциальность)
$$ \vec{E} = \frac{q}{4\pi\varepsilon_0 r^3} \vec{r} $$

$$ \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = \frac{q}{4\pi\varepsilon_0} \oint_{\Gamma} \frac{\mathrm{d}r}{r^2} = 0 $$

$$ \text{По теореме Стокса: } \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = \int_S (\operatorname{rot}\vec{E}, \mathrm{d}\vec{S}) = 0 $$

$$ \boxed{\operatorname{rot}\vec{E} = 0} \implies \vec{E} = -\operatorname{grad}\varphi $$

### Дивергенция магнитного поля (Соленоидальность)
$$ \vec{B}(\vec{r}) = \frac{\mu_0}{4\pi} \int_V \frac{[\vec{j}(\vec{r}'), \vec{r} - \vec{r}']}{|\vec{r} - \vec{r}'|^3} \mathrm{d}V' = \frac{\mu_0}{4\pi} \operatorname{rot} \int_V \frac{\vec{j}(\vec{r}')}{|\vec{r} - \vec{r}'|} \mathrm{d}V' $$

$$ \operatorname{div}\vec{B} = \operatorname{div}\operatorname{rot}\vec{A} \equiv 0 $$

$$ \boxed{\operatorname{div}\vec{B} = 0} \iff \oint_S (\vec{B}, \mathrm{d}\vec{S}) = 0 $$

### Ротор магнитного поля (Закон Ампера в вакууме)
$$ \vec{B} = \operatorname{rot}\vec{A}, \quad \vec{A} = \frac{\mu_0}{4\pi} \int_V \frac{\vec{j}(\vec{r}')}{|\vec{r} - \vec{r}'|} \mathrm{d}V' $$

$$ \operatorname{rot}\vec{B} = \operatorname{rot}\operatorname{rot}\vec{A} = \operatorname{grad}\operatorname{div}\vec{A} - \Delta\vec{A} $$

$$ \text{В кулоновской калибровке } \operatorname{div}\vec{A} = 0: $$

$$ \operatorname{rot}\vec{B} = -\Delta\vec{A} = -\frac{\mu_0}{4\pi} \int_V \vec{j}(\vec{r}') \Delta\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) \mathrm{d}V' $$

$$ \text{Учитывая, что } \Delta\left(\frac{1}{|\vec{r} - \vec{r}'|}\right) = -4\pi \delta(\vec{r} - \vec{r}'): $$

$$ \operatorname{rot}\vec{B} = -\frac{\mu_0}{4\pi} \int_V \vec{j}(\vec{r}') \left( -4\pi \delta(\vec{r} - \vec{r}') \right) \mathrm{d}V' $$

$$ \boxed{\operatorname{rot}\vec{B} = \mu_0 \vec{j}} \iff \oint_{\Gamma} (\vec{B}, \mathrm{d}\vec{l}) = \mu_0 I $$

---

# 3. Переход к нестационарным полям

### Обобщение закона Фарадея
$$ \mathcal{E}_i = \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}), \quad \Phi_B = \int_S (\vec{B}, \mathrm{d}\vec{S}) $$

$$ \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = -\frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{B}, \mathrm{d}\vec{S}) $$

$$ \text{По теореме Стокса: } \int_S (\operatorname{rot}\vec{E}, \mathrm{d}\vec{S}) = -\int_S \frac{\partial \vec{B}}{\partial t} \mathrm{d}\vec{S} $$

$$ \boxed{\operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t}} $$

### Введение тока смещения
Уравнение магнитостатики $\operatorname{rot}\vec{B} = \mu_0 \vec{j}$ противоречит закону сохранения заряда $\operatorname{div}\vec{j} + \frac{\partial \rho}{\partial t} = 0$, так как $\operatorname{div}\operatorname{rot}\vec{B} \equiv 0$, что требовало бы $\operatorname{div}\vec{j} = 0$.

$$ \operatorname{rot}\vec{B} = \mu_0 (\vec{j} + \vec{j}_{\text{см}}) $$

$$ \operatorname{div}\operatorname{rot}\vec{B} = \mu_0 \operatorname{div}(\vec{j} + \vec{j}_{\text{см}}) = 0 \implies \operatorname{div}\vec{j}_{\text{см}} = -\operatorname{div}\vec{j} = \frac{\partial \rho}{\partial t} $$

$$ \text{Из закона Гаусса: } \rho = \operatorname{div}\vec{D} \implies \operatorname{div}\vec{j}_{\text{см}} = \frac{\partial}{\partial t}(\operatorname{div}\vec{D}) = \operatorname{div}\left(\frac{\partial \vec{D}}{\partial t}\right) $$

$$ \vec{j}_{\text{см}} = \frac{\partial \vec{D}}{\partial t} $$

$$ \boxed{\operatorname{rot}\vec{H} = \vec{j} + \frac{\partial \vec{D}}{\partial t}} $$

---

# 4. Полная система уравнений Максвелла

### В дифференциальной форме
$$ \operatorname{rot}\vec{H} = \vec{j} + \frac{\partial \vec{D}}{\partial t} $$
$$ \operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t} $$
$$ \operatorname{div}\vec{D} = \rho $$
$$ \operatorname{div}\vec{B} = 0 $$

### В интегральной форме
$$ \oint_{\Gamma} (\vec{H}, \mathrm{d}\vec{l}) = I + \frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{D}, \mathrm{d}\vec{S}) $$
$$ \oint_{\Gamma} (\vec{E}, \mathrm{d}\vec{l}) = -\frac{\mathrm{d}}{\mathrm{d}t} \int_S (\vec{B}, \mathrm{d}\vec{S}) $$
$$ \oint_S (\vec{D}, \mathrm{d}\vec{S}) = Q $$
$$ \oint_S (\vec{B}, \mathrm{d}\vec{S}) = 0 $$

---

# 5. Вывод основных формул волновой теории

### Волновое уравнение (в вакууме: $\vec{j}=0, \rho=0$)
$$ \operatorname{rot}\vec{E} = -\mu_0 \frac{\partial \vec{H}}{\partial t}, \quad \operatorname{rot}\vec{H} = \varepsilon_0 \frac{\partial \vec{E}}{\partial t} $$

$$ \operatorname{rot}\operatorname{rot}\vec{E} = -\mu_0 \frac{\partial}{\partial t}(\operatorname{rot}\vec{H}) $$

$$ \operatorname{grad}\operatorname{div}\vec{E} - \Delta\vec{E} = -\mu_0 \varepsilon_0 \frac{\partial^2 \vec{E}}{\partial t^2} $$

$$ \text{Так как } \operatorname{div}\vec{E} = 0 \text{ и } c = \frac{1}{\sqrt{\varepsilon_0\mu_0}}: $$

$$ \boxed{\Delta\vec{E} - \frac{1}{c^2}\frac{\partial^2\vec{E}}{\partial t^2} = 0} $$

### Плоская электромагнитная волна
$$ \vec{E}(\vec{r}, t) = \vec{E}_0 e^{i(\omega t - \vec{k}\vec{r})}, \quad \vec{H}(\vec{r}, t) = \vec{H}_0 e^{i(\omega t - \vec{k}\vec{r})} $$

$$ \text{Подставляем в дифференциальные операторы: } \nabla \to -i\vec{k}, \quad \frac{\partial}{\partial t} \to i\omega $$

$$ \operatorname{div}\vec{E} = 0 \implies (\vec{k}, \vec{E}) = 0 \quad (\text{Поперечность}) $$

$$ \operatorname{rot}\vec{E} = -\frac{\partial \vec{B}}{\partial t} \implies -i[\vec{k}, \vec{E}] = -i\omega\mu\mu_0 \vec{H} $$

$$ \vec{H} = \frac{1}{\omega\mu\mu_0} [\vec{k}, \vec{E}] = \frac{k}{\omega\mu\mu_0} [\vec{e}_k, \vec{E}] $$

$$ \text{С учетом } \frac{\omega}{k} = v = \frac{1}{\sqrt{\varepsilon\varepsilon_0\mu\mu_0}}: $$

$$ \boxed{\vec{H} = \sqrt{\frac{\varepsilon\varepsilon_0}{\mu\mu_0}} [\vec{e}_k, \vec{E}]} $$

### Вектор Умова-Пойнтинга и закон сохранения энергии
$$ \operatorname{div}[\vec{E}, \vec{H}] = (\vec{H}, \operatorname{rot}\vec{E}) - (\vec{E}, \operatorname{rot}\vec{H}) $$

$$ \operatorname{div}[\vec{E}, \vec{H}] = \left(\vec{H}, -\frac{\partial \vec{B}}{\partial t}\right) - \left(\vec{E}, \vec{j} + \frac{\partial \vec{D}}{\partial t}\right) $$

$$ \operatorname{div}[\vec{E}, \vec{H}] = -\frac{\partial}{\partial t}\left(\frac{(\vec{E}, \vec{D}) + (\vec{H}, \vec{B})}{2}\right) - (\vec{j}, \vec{E}) $$

$$ \text{Вводя плотность энергии } w = \frac{(\vec{E},\vec{D})+(\vec{H},\vec{B})}{2} \text{ и вектор Пойнтинга } \vec{S} = [\vec{E}, \vec{H}]: $$

$$ \boxed{\operatorname{div}\vec{S} + \frac{\partial w}{\partial t} = -(\vec{j}, \vec{E})} $$
