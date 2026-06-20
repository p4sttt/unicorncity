---
title: "Чеклист теорем с доказательствами"
description: "Полный перечень ключевых теорем курсов теории вероятностей и математической статистики со строгими выводами"
state: done
date: 2026-06-20
---

# Чеклист теорем по теории вероятностей и математической статистике

Этот чеклист представляет собой сборник ключевых математических теорем курса. Каждая теорема снабжена строгой формулировкой с указанием всех условий регулярности/сходимости и детальным пошаговым доказательством.

---

## 1. Теория вероятностей

### Теорема о непрерывности вероятностной меры
Связывает сигма-аддитивность вероятности с её предельными свойствами.

> **Формулировка**
>
> Пусть $(\Omega, \mathcal{F}, \mathbb{P})$ — вероятностное пространство.
> 1. Если $A_n \uparrow A$ (то есть $A_1 \subset A_2 \subset \dots$ и $A = \bigcup_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.
> 2. Если $A_n \downarrow A$ (то есть $A_1 \supset A_2 \supset \dots$ и $A = \bigcap_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.

#### Доказательство
1. Для возрастающей последовательности $\{A_n\}$ введем дизъюнктные события:
   $$B_1 = A_1, \quad B_k = A_k \setminus A_{k-1} \text{ для всех } k \ge 2$$
   По построению $B_i \cap B_j = \emptyset$ при $i \neq j$. Заметим, что:
   $$\bigcup_{k=1}^{n} B_k = A_n \quad \text{и} \quad \bigcup_{k=1}^{\infty} B_k = A$$
   В силу аксиомы $\sigma$-аддитивности вероятности:
   $$\mathbb{P}(A) = \mathbb{P}\left(\sum_{k=1}^{\infty} B_k\right) = \sum_{k=1}^{\infty} \mathbb{P}(B_k) = \lim_{n\to\infty} \sum_{k=1}^{n} \mathbb{P}(B_k)$$
   Поскольку для любого конечного $n$ выполнено $\sum_{k=1}^{n} \mathbb{P}(B_k) = \mathbb{P}(A_n)$ в силу конечной аддитивности, получаем:
   $$\mathbb{P}(A) = \lim_{n\to\infty} \mathbb{P}(A_n)$$
2. Для убывающей последовательности $\{A_n\}$ рассмотрим дополнения $C_n = A_n^c$. Поскольку $A_n \supset A_{n+1}$, имеем $C_n \subset C_{n+1}$.
   Следовательно, $C_n \uparrow C$, где $C = \bigcup_{n=1}^{\infty} A_n^c = \left(\bigcap_{n=1}^{\infty} A_n\right)^c = A^c$.
   Применяя доказанную часть 1 к возрастающей последовательности $\{C_n\}$, имеем:
   $$\lim_{n\to\infty} \mathbb{P}(C_n) = \mathbb{P}(C) \implies \lim_{n\to\infty} (1 - \mathbb{P}(A_n)) = 1 - \mathbb{P}(A) \implies \lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$$
   $\blacksquare$

### Связь сходимостей случайных величин
Иерархия типов сходимости последовательностей случайных величин.

> **Формулировка**
>
> 1. Если $X_n \xrightarrow{\text{п.н.}} X$, то $X_n \xrightarrow{\mathbb{P}} X$.
> 2. Если $X_n \xrightarrow{\mathbb{P}} X$, то $X_n \xrightarrow{d} X$.

#### Доказательство
1. Пусть $X_n \xrightarrow{\text{п.н.}} X$. Зафиксируем $\varepsilon > 0$. Введем события:
   $$A_n(\varepsilon) = \bigcup_{k=n}^{\infty} \{|X_k - X| \ge \varepsilon\}$$
   Последовательность $A_n(\varepsilon)$ монотонно убывает по включению к событию:
   $$A(\varepsilon) = \bigcap_{n=1}^{\infty} A_n(\varepsilon) = \{|X_k - X| \ge \varepsilon \text{ бесконечно часто}\}$$
   По определению сходимости почти наверное, мера множества расходимости равна нулю, следовательно, $\mathbb{P}(A(\varepsilon)) = 0$.
   По свойству непрерывности вероятностной меры на убывающих событиях:
   $$\lim_{n\to\infty} \mathbb{P}(A_n(\varepsilon)) = \mathbb{P}(A(\varepsilon)) = 0$$
   Поскольку $\{|X_n - X| \ge \varepsilon\} \subset A_n(\varepsilon)$, в силу монотонности вероятности:
   $$0 \le \mathbb{P}(|X_n - X| \ge \varepsilon) \le \mathbb{P}(A_n(\varepsilon)) \to 0 \quad \text{при } n \to \infty$$
   Значит, $X_n \xrightarrow{\mathbb{P}} X$.
2. Пусть $X_n \xrightarrow{\mathbb{P}} X$. Обозначим $F_n(x) = \mathbb{P}(X_n < x)$ и $F(x) = \mathbb{P}(X < x)$. Зафиксируем $\varepsilon > 0$.
   Событие $\{X_n < x\}$ представим как:
   $$\{X_n < x\} = \{X_n < x, \, |X_n - X| < \varepsilon\} \cup \{X_n < x, \, |X_n - X| \ge \varepsilon\}$$
   Если $X_n < x$ и $|X_n - X| < \varepsilon$, то $X \le X_n + |X_n - X| < x + \varepsilon$. Отсюда:
   $$F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$
   Аналогично, рассматривая событие $\{X < x - \varepsilon\}$:
   $$F(x - \varepsilon) \le F_n(x) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$
   Объединяя, получаем:
   $$F(x - \varepsilon) - \mathbb{P}(|X_n - X| \ge \varepsilon) \le F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$
   Перейдем к пределу при $n \to \infty$ (учитывая, что $\mathbb{P}(|X_n - X| \ge \varepsilon) \to 0$):
   $$F(x - \varepsilon) \le \liminf_{n\to\infty} F_n(x) \le \limsup_{n\to\infty} F_n(x) \le F(x + \varepsilon)$$
   Если $x$ — точка непрерывности функции $F(x)$, то устремляя $\varepsilon \to 0$, получаем $\lim_{\varepsilon\to 0} F(x \pm \varepsilon) = F(x)$.
   По теореме о двух милиционерах получаем $\lim_{n\to\infty} F_n(x) = F(x)$. $\blacksquare$

### Неравенство Колмогорова
Служит основой для доказательства усиленного закона больших чисел.

> **Формулировка**
>
> Пусть $X_1, \dots, X_n$ — независимые случайные величины с $\mathbb{E}[X_i] = 0$ и конечными дисперсиями $\mathbb{D}[X_i] = \sigma_i^2$. Тогда для любого $\varepsilon > 0$:
> $$\mathbb{P}\left(\max_{1 \le k \le n} |S_k| \ge \varepsilon\right) \le \frac{\mathbb{D}[S_n]}{\varepsilon^2}$$
> где $S_k = X_1 + \dots + X_k$.

#### Доказательство
Введем события $A_k$, означающие, что превышение порога $\varepsilon$ впервые произошло на шаге $k$:
$$A_k = \{|S_k| \ge \varepsilon, \, |S_1| < \varepsilon, \dots, |S_{k-1}| < \varepsilon\}, \quad k = 1, \dots, n$$
Эти события попарно не пересекаются, причем их объединение совпадает с событием $A = \{\max_{1 \le k \le n} |S_k| \ge \varepsilon\}$.
Запишем дисперсию конечной суммы $S_n$:
$$\mathbb{D}[S_n] = \mathbb{E}[S_n^2] \ge \mathbb{E}[S_n^2 \mathbb{I}_A] = \sum_{k=1}^{n} \mathbb{E}[S_n^2 \mathbb{I}_{A_k}]$$
Представим $S_n = S_k + (S_n - S_k)$. Тогда $S_n^2 = S_k^2 + 2 S_k(S_n - S_k) + (S_n - S_k)^2 \ge S_k^2 + 2 S_k(S_n - S_k)$.
Подставим это под знак математического ожидания:
$$\mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}] + 2 \mathbb{E}[S_k(S_n - S_k) \mathbb{I}_{A_k}]$$
Поскольку $S_k \mathbb{I}_{A_k}$ зависит только от $X_1, \dots, X_k$, а разность $S_n - S_k = \sum_{i=k+1}^{n} X_i$ зависит только от $X_{k+1}, \dots, X_n$, в силу независимости случайных величин имеем:
$$\mathbb{E}[S_k(S_n - S_k) \mathbb{I}_{A_k}] = \mathbb{E}[S_k \mathbb{I}_{A_k}] \mathbb{E}[S_n - S_k] = 0$$
так как $\mathbb{E}[S_n - S_k] = \sum_{i=k+1}^{n} \mathbb{E}[X_i] = 0$.
Таким образом:
$$\mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}]$$
На множестве $A_k$ выполнено неравенство $|S_k| \ge \varepsilon \implies S_k^2 \ge \varepsilon^2$. Следовательно:
$$\mathbb{E}[S_k^2 \mathbb{I}_{A_k}] \ge \varepsilon^2 \mathbb{P}(A_k)$$
Суммируя по всем $k$ от $1$ до $n$, находим:
$$\mathbb{D}[S_n] \ge \sum_{k=1}^{n} \varepsilon^2 \mathbb{P}(A_k) = \varepsilon^2 \mathbb{P}\left(\max_{1 \le k \le n} |S_k| \ge \varepsilon\right)$$
Разделив на $\varepsilon^2$, получаем исходное неравенство. $\blacksquare$

### Лемма Бореля–Кантелли
Инструмент для анализа бесконечного числа событий.

> **Формулировка**
>
> Пусть $\{A_n\}_{n=1}^{\infty}$ — последовательность событий.
> 1. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) < \infty$, то $\mathbb{P}(\limsup_{n\to\infty} A_n) = 0$.
> 2. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) = \infty$ и события $\{A_n\}$ независимы в совокупности, то $\mathbb{P}(\limsup_{n\to\infty} A_n) = 1$.

#### Доказательство
1. Пусть ряд сходится. Обозначим $A^* = \limsup_{n\to\infty} A_n = \bigcap_{n=1}^{\infty} \bigcup_{k=n}^{\infty} A_k$.
   Для любого $n \in \mathbb{N}$ выполнено включение $A^* \subset \bigcup_{k=n}^{\infty} A_k$.
   В силу субаддитивности вероятности:
   $$\mathbb{P}(A^*) \le \mathbb{P}\left(\bigcup_{k=n}^{\infty} A_k\right) \le \sum_{k=n}^{\infty} \mathbb{P}(A_k)$$
   Поскольку ряд сходится, предел остатка ряда стремится к нулю:
   $$\lim_{n\to\infty} \sum_{k=n}^{\infty} \mathbb{P}(A_k) = 0 \implies \mathbb{P}(A^*) = 0$$
2. Пусть ряд расходится и события независимы. Покажем, что $\mathbb{P}((A^*)^c) = 0$, где $(A^*)^c = \bigcup_{n=1}^{\infty} \bigcap_{k=n}^{\infty} A_k^c$.
   Для этого достаточно доказать, что для каждого $n$:
   $$\mathbb{P}\left(\bigcap_{k=n}^{\infty} A_k^c\right) = 0$$
   Рассмотрим конечное пересечение для $M > n$. В силу независимости событий $\{A_k^c\}$:
   $$\mathbb{P}\left(\bigcap_{k=n}^{M} A_k^c\right) = \prod_{k=n}^{M} (1 - \mathbb{P}(A_k))$$
   Используя неравенство $1-x \le e^{-x}$:
   $$\prod_{k=n}^{M} (1 - \mathbb{P}(A_k)) \le \exp\left(-\sum_{k=n}^{M} \mathbb{P}(A_k)\right)$$
   Поскольку ряд расходится, $\lim_{M\to\infty} \sum_{k=n}^{M} \mathbb{P}(A_k) = \infty$.
   Переходя к пределу по непрерывности вероятности при $M \to \infty$:
   $$\mathbb{P}\left(\bigcap_{k=n}^{\infty} A_k^c\right) = \lim_{M\to\infty} \mathbb{P}\left(\bigcap_{k=n}^{M} A_k^c\right) \le \lim_{M\to\infty} \exp\left(-\sum_{k=n}^{M} \mathbb{P}(A_k)\right) = 0$$
   Счетное объединение событий нулевой вероятности дает нулевую вероятность, следовательно, $\mathbb{P}((A^*)^c) = 0 \implies \mathbb{P}(A^*) = 1$. $\blacksquare$

### Центральная предельная теорема (Линдеберга–Леви)
Обосновывает появление нормального закона.

> **Формулировка**
>
> Пусть $\{X_n\}_{n=1}^{\infty}$ — последовательность независимых одинаково распределенных случайных величин с $\mathbb{E}[X_1] = \mu$ и $\mathbb{D}[X_1] = \sigma^2 > 0$. Тогда при $n \to \infty$:
> $$Y_n = \frac{\sum_{i=1}^{n} X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

#### Доказательство
Без потери общности положим $\mu=0$ и $\sigma^2=1$. Обозначим через $\varphi(t)$ характеристическую функцию величины $X_1$.
Поскольку существуют первые два момента, разложение Тейлора характеристической функции в окрестности нуля имеет вид:
$$\varphi(t) = 1 + i\mathbb{E}[X_1]t - \frac{\mathbb{E}[X_1^2]t^2}{2} + o(t^2) = 1 - \frac{t^2}{2} + o(t^2), \quad t \to 0$$
Выразим характеристическую функцию случайной величины $Y_n = \frac{S_n}{\sqrt{n}}$:
$$\varphi_{Y_n}(t) = \mathbb{E}\left[\exp\left(it\frac{S_n}{\sqrt{n}}\right)\right] = \left(\varphi\left(\frac{t}{\sqrt{n}}\right)\right)^n = \left(1 - \frac{t^2}{2n} + o\left(\frac{t^2}{n}\right)\right)^n$$
Для любого фиксированного $t$ при $n \to \infty$ выражение в скобках имеет вид $1 + \frac{x_n}{n}$, где $x_n = -t^2/2 + o(1) \to -t^2/2$.
Используя замечательный предел $\lim (1 + x_n/n)^n = e^x$:
$$\lim_{n\to\infty} \varphi_{Y_n}(t) = e^{-t^2/2}$$
Функция $e^{-t^2/2}$ является непрерывной в нуле характеристической функцией стандартного нормального распределения $\mathcal{N}(0, 1)$.
По теореме непрерывности Леви, слабая сходимость характеристических функций влечет слабую сходимость распределений:
$$Y_n \xrightarrow{d} \mathcal{N}(0, 1)$$
$\blacksquare$

---

## 2. Математическая статистика

### Теорема факторизации Неймана–Пирсона
Позволяет находить достаточные статистики.

> **Формулировка**
>
> Статистика $T(\mathbf{X})$ достаточна для $\theta$ тогда и только тогда, когда плотность совместного распределения (функция правдоподобия) представима в виде:
> $$L(\mathbf{x}; \theta) = g(T(\mathbf{x}); \theta) h(\mathbf{x})$$

#### Доказательство (дискретный случай)
1. **Необходимость:** Пусть статистика $T$ достаточна.
   По определению условной вероятности:
   $$\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x}) = \mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x}, \, T(\mathbf{X}) = T(\mathbf{x})) = \mathbb{P}_{\theta}(T(\mathbf{X}) = T(\mathbf{x})) \cdot \mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = T(\mathbf{x}))$$
   Введем обозначения:
   $$g(t; \theta) = \mathbb{P}_{\theta}(T(\mathbf{X}) = t), \quad h(\mathbf{x}) = \mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = T(\mathbf{x}))$$
   Поскольку $T$ достаточна, условная вероятность $h(\mathbf{x})$ не зависит от $\theta$. Мы получили разложение:
   $$L(\mathbf{x}; \theta) = g(T(\mathbf{x}); \theta) h(\mathbf{x})$$
2. **Достаточность:** Пусть выполнено указанное разложение. Найдем условную вероятность:
   $$\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = t) = \frac{\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x}, \, T(\mathbf{X}) = t)}{\mathbb{P}_{\theta}(T(\mathbf{X}) = t)}$$
   Если $T(\mathbf{x}) \neq t$, то условная вероятность равна нулю. Если $T(\mathbf{x}) = t$, то:
   $$\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = t) = \frac{g(t; \theta) h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} g(T(\mathbf{y}); \theta) h(\mathbf{y})} = \frac{g(t; \theta) h(\mathbf{x})}{g(t; \theta) \sum_{\mathbf{y}: T(\mathbf{y})=t} h(\mathbf{y})} = \frac{h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} h(\mathbf{y})}$$
   Полученная величина не содержит параметра $\theta$, что доказывает достаточность статистики $T$. $\blacksquare$

### Неравенство Рао–Крамера
Определяет предел точности точечных оценок.

> **Формулировка**
>
> В регулярном статистическом эксперименте для любой оценки $\hat{\theta}(\mathbf{X})$ параметра $\tau(\theta)$ со смещением $b(\theta) = \mathbb{E}_{\theta}[\hat{\theta}] - \tau(\theta)$ выполнено:
> $$\mathbb{D}_{\theta}[\hat{\theta}] \ge \frac{(\tau'(\theta) + b'(\theta))^2}{I_n(\theta)}$$

#### Доказательство
Продифференцируем по $\theta$ условие нормировки плотности правдоподобия $\int_{\mathbb{R}^n} L(\mathbf{x}; \theta) \, d\mathbf{x} = 1$:
$$\int_{\mathbb{R}^n} \frac{\partial L(\mathbf{x}; \theta)}{\partial \theta} \, d\mathbf{x} = 0 \implies \int_{\mathbb{R}^n} \left( \frac{\partial \ln L(\mathbf{x}; \theta)}{\partial \theta} \right) L(\mathbf{x}; \theta) \, d\mathbf{x} = 0$$
Это означает, что для скор-функции $U(\mathbf{X}; \theta) = \frac{\partial \ln L(\mathbf{X}; \theta)}{\partial \theta}$ выполнено $\mathbb{E}_{\theta}[U] = 0$.
Ее дисперсия равна информации Фишера в выборке: $\mathbb{D}_{\theta}[U] = \mathbb{E}_{\theta}[U^2] = I_n(\theta)$.
Продифференцируем по $\theta$ выражение для математического ожидания оценки:
$$\mathbb{E}_{\theta}[\hat{\theta}] = \int_{\mathbb{R}^n} \hat{\theta}(\mathbf{x}) L(\mathbf{x}; \theta) \, d\mathbf{x} = \tau(\theta) + b(\theta)$$
Дифференцируя под интегралом, получаем:
$$\int_{\mathbb{R}^n} \hat{\theta}(\mathbf{x}) \frac{\partial \ln L(\mathbf{x}; \theta)}{\partial \theta} L(\mathbf{x}; \theta) \, d\mathbf{x} = \tau'(\theta) + b'(\theta) \implies \mathbb{E}_{\theta}[\hat{\theta} U] = \tau'(\theta) + b'(\theta)$$
Поскольку $\mathbb{E}_{\theta}[U] = 0$, ковариация между $\hat{\theta}$ и $U$ равна:
$$\operatorname{Cov}_{\theta}(\hat{\theta}, U) = \mathbb{E}_{\theta}[\hat{\theta} U] - \mathbb{E}_{\theta}[\hat{\theta}]\mathbb{E}_{\theta}[U] = \tau'(\theta) + b'(\theta)$$
Применяя неравенство Коши-Буняковского к ковариации:
$$(\operatorname{Cov}_{\theta}(\hat{\theta}, U))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] \mathbb{D}_{\theta}[U] \implies (\tau'(\theta) + b'(\theta))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] I_n(\theta)$$
Разделив обе части на $I_n(\theta)$, получаем исходное неравенство. $\blacksquare$

### Теорема Рао–Блекуэлла–Колмогорова
Метод улучшения оценок с помощью достаточных статистик.

> **Формулировка**
>
> Пусть $\hat{\theta}$ — несмещенная оценка для $\theta$ с конечной дисперсией, а $T$ — достаточная статистика.
> Тогда оценка $\hat{\theta}^* = \mathbb{E}[\hat{\theta} \mid T]$ является статистикой, несмещена для $\theta$, и $\mathbb{D}_{\theta}[\hat{\theta}^*] \le \mathbb{D}_{\theta}[\hat{\theta}]$.

#### Доказательство
1. Так как статистика $T$ достаточна, условное распределение $\mathbf{X}$ при фиксированном $T$ не зависит от параметра $\theta$, а значит, и условное ожидание $\hat{\theta}^* = \mathbb{E}[\hat{\theta} \mid T]$ является корректно определенной статистикой (не содержит $\theta$).
2. По закону полного математического ожидания:
   $$\mathbb{E}_{\theta}[\hat{\theta}^*] = \mathbb{E}_{\theta}[\mathbb{E}[\hat{\theta} \mid T]] = \mathbb{E}_{\theta}[\hat{\theta}] = \theta$$
   что доказывает несмещенность.
3. По закону полной дисперсии:
   $$\mathbb{D}_{\theta}[\hat{\theta}] = \mathbb{E}_{\theta}[\mathbb{D}[\hat{\theta} \mid T]] + \mathbb{D}_{\theta}[\mathbb{E}[\hat{\theta} \mid T]] = \mathbb{E}_{\theta}[\mathbb{D}[\hat{\theta} \mid T]] + \mathbb{D}_{\theta}[\hat{\theta}^*]$$
   Поскольку условная дисперсия неотрицательна, ее математическое ожидание $\mathbb{E}_{\theta}[\mathbb{D}[\hat{\theta} \mid T]] \ge 0$, откуда:
   $$\mathbb{D}_{\theta}[\hat{\theta}] \ge \mathbb{D}_{\theta}[\hat{\theta}^*]$$
   Равенство достигается тогда и только тогда, когда $\mathbb{D}[\hat{\theta} \mid T] = 0$ почти наверное, то есть когда оценка $\hat{\theta}$ сама является функцией от достаточной статистики $T$. $\blacksquare$

### Лемма Неймана–Пирсона
Построение наиболее мощного критерия проверки простых гипотез.

> **Формулировка**
>
> При проверке $H_0: \theta = \theta_0$ против альтернативы $H_1: \theta = \theta_1$ критическая область вида $W = \{\mathbf{x} : L(\mathbf{x}; \theta_1) > c L(\mathbf{x}; \theta_0)\}$ с размером $\mathbb{P}_{\theta_0}(W) = \alpha$ является наиболее мощной среди всех критериев уровня значимости не выше $\alpha$.

#### Доказательство
Пусть $W'$ — любая другая критическая область с размером $\alpha' = \mathbb{P}_{\theta_0}(W') \le \alpha$. Обозначим мощности критериев через $\beta = \mathbb{P}_{\theta_1}(W)$ и $\beta' = \mathbb{P}_{\theta_1}(W')$.
Для любого исхода $\mathbf{x}$ рассмотрим выражение:
$$d(\mathbf{x}) = (\mathbb{I}_W(\mathbf{x}) - \mathbb{I}_{W'}(\mathbf{x})) (L(\mathbf{x}; \theta_1) - c L(\mathbf{x}; \theta_0))$$
Покажем, что $d(\mathbf{x}) \ge 0$ почти всюду:
- Если $\mathbf{x} \in W$, то $\mathbb{I}_W = 1 \implies \mathbb{I}_W - \mathbb{I}_{W'} \ge 0$. Также $L(\mathbf{x}; \theta_1) - c L(\mathbf{x}; \theta_0) > 0$. Произведение $\ge 0$.
- Если $\mathbf{x} \notin W$, то $\mathbb{I}_W = 0 \implies \mathbb{I}_W - \mathbb{I}_{W'} \le 0$. Также $L(\mathbf{x}; \theta_1) - c L(\mathbf{x}; \theta_0) \le 0$. Произведение $\ge 0$.
Интегрируя это выражение по всему выборочному пространству:
$$\int_{\mathbb{R}^n} (\mathbb{I}_W(\mathbf{x}) - \mathbb{I}_{W'}(\mathbf{x})) (L(\mathbf{x}; \theta_1) - c L(\mathbf{x}; \theta_0)) \, d\mathbf{x} \ge 0$$
$$\implies \int_{\mathbb{R}^n} \mathbb{I}_W L_1 \, d\mathbf{x} - \int_{\mathbb{R}^n} \mathbb{I}_{W'} L_1 \, d\mathbf{x} - c \left( \int_{\mathbb{R}^n} \mathbb{I}_W L_0 \, d\mathbf{x} - \int_{\mathbb{R}^n} \mathbb{I}_{W'} L_0 \, d\mathbf{x} \right) \ge 0$$
Используя определения мощностей и размеров критических областей:
$$\beta - \beta' - c (\alpha - \alpha') \ge 0 \implies \beta - \beta' \ge c(\alpha - \alpha')$$
Поскольку по условию $\alpha' \le \alpha$ и $c > 0$, правая часть $c(\alpha - \alpha') \ge 0$. Следовательно:
$$\beta - \beta' \ge 0 \implies \beta \ge \beta'$$
что доказывает максимальную мощность критерия $W$. $\blacksquare$

### Теорема Фишера о нормальных выборках
Определяет свойства выборочных характеристик для нормальной выборки.

> **Формулировка**
>
> Пусть $X_1, \dots, X_n$ — независимая выборка из распределения $\mathcal{N}(a, \sigma^2)$. Тогда:
> 1. Выборочное среднее $\bar{X}$ и выборочная исправленная дисперсия $S_0^2$ независимы.
> 2. Случайная величина $\frac{(n-1)S_0^2}{\sigma^2}$ имеет распределение $\chi^2(n-1)$.

#### Доказательство
Положим $a=0$ и $\sigma=1$. Совместная плотность элементов выборки равна:
$$p(\mathbf{x}) = \frac{1}{(2\pi)^{n/2}} \exp\left(-\frac{1}{2}\sum_{i=1}^{n} x_i^2\right)$$
Рассмотрим линейную замену $\mathbf{Y} = C \mathbf{X}$ с ортогональной матрицей $C$ порядка $n \times n$. Зададим первую строку матрицы $C$ как:
$$\mathbf{c}_1^T = \left(\frac{1}{\sqrt{n}}, \frac{1}{\sqrt{n}}, \dots, \frac{1}{\sqrt{n}}\right)$$
Остальные строки выберем так, чтобы матрица $C$ была ортогональной. Поскольку преобразование ортогонально, оно сохраняет длину вектора $\sum_{i=1}^{n} Y_i^2 = \sum_{i=1}^{n} X_i^2$, а Якобиан равен 1. Совместная плотность вектора $\mathbf{Y}$ равна:
$$p_{\mathbf{Y}}(\mathbf{y}) = \frac{1}{(2\pi)^{n/2}} \exp\left(-\frac{1}{2}\sum_{i=1}^{n} y_i^2\right)$$
Таким образом, величины $Y_1, \dots, Y_n$ независимы и имеют стандартное нормальное распределение $\mathcal{N}(0, 1)$.
Выразим первую координату:
$$Y_1 = \sum_{j=1}^{n} c_{1j} X_j = \sum_{j=1}^{n} \frac{1}{\sqrt{n}} X_j = \sqrt{n} \bar{X} \implies Y_1^2 = n \bar{X}^2$$
Распишем сохранение длины вектора:
$$\sum_{i=1}^{n} X_i^2 = Y_1^2 + \sum_{i=2}^{n} Y_i^2 = n \bar{X}^2 + \sum_{i=2}^{n} Y_i^2$$
Отсюда получаем:
$$\sum_{i=2}^{n} Y_i^2 = \sum_{i=1}^{n} X_i^2 - n \bar{X}^2 = \sum_{i=1}^{n} (X_i - \bar{X})^2 = (n-1)S_0^2$$
Поскольку $\bar{X} = Y_1/\sqrt{n}$ зависит только от $Y_1$, а величина $S_0^2 = \frac{1}{n-1} \sum_{i=2}^{n} Y_i^2$ зависит только от независимых с $Y_1$ компонент $Y_2, \dots, Y_n$, то $\bar{X}$ и $S_0^2$ независимы.
Величина $\frac{(n-1)S_0^2}{\sigma^2} = \sum_{i=2}^{n} Y_i^2$ в силу стандартности нормальных величин $Y_2, \dots, Y_n$ представляет собой сумму квадратов $n-1$ независимых стандартных нормальных величин. По определению это означает, что:
$$\frac{(n-1)S_0^2}{\sigma^2} \sim \chi^2(n-1)$$
$\blacksquare$
