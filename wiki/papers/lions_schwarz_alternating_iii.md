---
title: "On the Schwarz Alternating Method III: A Variant for Nonoverlapping Subdomains"
description: "P.-L. Lions, DD3 1990; передача выпуклой комбинации Дирихле- и Нейман-данных даёт Robin-условие на интерфейсе — предок оптимизированного Шварца"
type: paper-summary
tags: [numerical-analysis, pde, domain-decomposition, theory]
status: in-progress
created: 2026-07-26
updated: 2026-07-26
sources: ["raw/papers/processed/On_the_Schwarz_Alternating_Method_III_A_Variant_for_Nonoverlapping_Subdomains_(Lions).pdf"]
---

# On the Schwarz Alternating Method III: A Variant for Nonoverlapping Subdomains

P. L. Lions (CEREMADE, Paris-Dauphine; консультант CISI Ingénierie). Third International
Symposium on Domain Decomposition Methods, 1990, гл. 11, с. 202–223.

## TL;DR

Новый DD-метод, вдохновлённый Шварцем, но **не требующий наложения**: на каждом шаге в
каждой подобласти решается то же уравнение Лапласа, а между подобластями передаётся
**выпуклая комбинация данных Неймана и Дирихле**, что даёт на каждом интерфейсе условие
типа Робена (Фурье). Допускает произвольное число подобластей, все обрабатываются
одинаково и параллельно, включая внутренние. Это прямой предок семейства **optimized
Schwarz**.

## Core contribution

Мотивация сформулирована прямо: требование наложения — «серьёзное ограничение, не говоря
уже об очевидной или интуитивной трате усилий в области, разделяемой двумя подобластями».
Метод убирает это требование, не жертвуя ни симметрией обработки подобластей, ни
параллельностью, ни возможностью иметь внутренние подобласти.

## Method

$\Omega = \Omega_1 \cup \dots \cup \Omega_m \cup \Sigma$, где $\Omega_i$ дизъюнктны,
$\Sigma = \bigcup \gamma_{ij}$, $\gamma_{ij} = \partial\Omega_i \cap \partial\Omega_j$.
Модельная задача $-\Delta u = f$ в $\Omega$, $u = 0$ на $\partial\Omega = \Gamma$.

Итерация: по начальным приближениям $(u_i^0)$ в $H^2(\Omega_i) \cap H^1_\Gamma(\Omega_i)$
строятся

$$
(3)\quad -\Delta u_i^{n+1} = f \text{ в } \Omega_i, \qquad u_i^{n+1} \in H^1_\Gamma(\Omega_i)
$$

$$
(4)\quad \frac{\partial u_i^{n+1}}{\partial n_{ij}} + \lambda_{ij} u_i^{n+1}
= \frac{\partial u_j^n}{\partial n_{ij}} + \lambda_{ij} u_j^n \ \text{ на } \gamma_{ij},
\qquad \forall j \ne i,\ \ \lambda_{ij} = \lambda_{ji} > 0
$$

где $n_{ij} = -n_{ji}$ — единичная внешняя нормаль к $\partial\Omega_i$ на $\gamma_{ij}$.
Смысл (3)–(4) уточняется вариационной формулировкой: $v \in H^1_\Gamma(\Omega_i)$
удовлетворяет

$$
\int_{\Omega_i} \nabla v \cdot \nabla \varphi \, dx
+ \sum_{j \ne i} \int_{\gamma_{ij}} g_{ij} \varphi \, dS
= \int_{\Omega_i} f \varphi \, dx \qquad \forall \varphi \in H^1_\Gamma(\Omega_i)
$$

Для $n \ge 1$ разность двух последовательных итератов удовлетворяет однородной задаче:

$$
-\Delta(u_i^{n+1} - u_i^{n-1}) = 0 \text{ в } \Omega_i
$$
$$
\frac{\partial}{\partial n_{ij}} (u_i^{n+1} - u_i^{n-1})
= \lambda_{ij} \bigl\{ 2u_j^n - u_i^{n+1} - u_i^{n-1} \bigr\} \text{ на } \gamma_{ij}
$$

Это и есть объект, для которого доказываются энергетические оценки.

## Key results

- **§III: сходимость в модельном случае** (Лаплас, однородный Дирихле) через «несколько
  деликатные энергетические оценки». Ни вариационной интерпретации через проекции, ни
  прямого принципа максимума здесь нет — обе линии частей I и II не переносятся, нужна
  новая техника.
- **§IV: конвекция.** Метод сходится и для уравнения Лапласа с конвективными членами,
  причём — что подчёркивается отдельно — **выпуклые веса $\lambda_{ij}$ на интерфейсах не
  нужно ограничивать** из-за наличия конвекции.
- **§V: расширения**, включая перечень уравнений, к которым метод применим.
- Метод допускает **произвольное число произвольных непересекающихся подобластей** (при
  необходимости они даже могут перекрываться), все обрабатываются параллельно и
  равноправно; в частности разрешены «внутренние подобласти», не касающиеся $\partial\Omega$.

## Limitations

- **Оптимального выбора $\lambda_{ij}$ в статье нет** — доказывается только сходимость при
  $\lambda_{ij} > 0$. Именно оптимизация $\lambda$ (и переход к операторным условиям
  второго порядка вместо скаляра) и составила последующую программу optimized Schwarz.
- Всё в непрерывной постановке; дискретные оценки и зависимость от $h/H$ не рассматриваются.
- Упрощающие геометрические предположения: $\Omega_i$ связны,
  $\bar\Omega_i \cap \bar\Omega_j \cap \bar\Omega_k = \varnothing$, $\gamma_{ij}$ —
  след гладкого многообразия, ортогонально пересекающего $\partial\Omega$.

## Related work

- [[optimized_schwarz_transmission_conditions]] — концепт
- [[lions_schwarz_alternating_i]], [[lions_schwarz_alternating_ii]] — предыдущие части
- [[marini_quarteroni_relaxation_dd]] — параллельная линия: релаксация классических условий
  вместо смены их типа; Лионс явно ссылается на [45], [46] как на родственные методы
- [[schur_complement_substructuring]] — альтернативный non-overlapping-подход
- [[domain_decomposition_methods]]

## My notes

Сравнение с Дирихле–Нейманом полезно держать в голове: DN тоже non-overlapping, но требует
2-раскраски графа смежности подобластей, которая может не существовать (нечётные циклы), и
даёт несимметричный P⁻¹S. Метод Лионса снимает оба ограничения одним ходом — потому что
не назначает подобластям роли вообще.

Условие $\lambda_{ij} = \lambda_{ji} > 0$ — единственное ограничение на параметры. То, что
оно не должно подкручиваться при добавлении конвекции, довольно неочевидно: обычно именно
конвекция рушит симметричные конструкции.
