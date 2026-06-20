---
title: "Раздел 2. Предельные теоремы и сходимости"
description: "Сходимости случайных величин, вероятностные неравенства, законы больших чисел и центральная предельная теорема"
date: 2026-06-20
status: done
---

# Раздел 2. Предельные теоремы и сходимости

## 2.1. Виды сходимости и неравенства

### Виды сходимости

Последовательность случайных величин $\{X_n\}_{n=1}^{\infty}$ сходится к случайной величине $X$:

1. **Почти наверное** ($X_n \xrightarrow{\text{п.н.}} X$):

   $$\mathbb{P}\left(\left\{\omega \in \Omega : \lim_{n\to\infty} X_n(\omega) = X(\omega)\right\}\right) = 1$$

2. **По вероятности** ($X_n \xrightarrow{\mathbb{P}} X$):

   $$\forall \varepsilon > 0: \lim_{n\to\infty} \mathbb{P}(|X_n - X| \ge \varepsilon) = 0$$

3. **В среднем порядка $p \ge 1$** ($X_n \xrightarrow{L^p} X$):

   $$\lim_{n\to\infty} \mathbb{E}[|X_n - X|^p] = 0 \quad (\mathbb{E}[|X_n|^p] < \infty, \, \mathbb{E}[|X|^p] < \infty)$$

4. **По распределению** ($X_n \xrightarrow{d} X$):

   $$\lim_{n\to\infty} F_{X_n}(x) = F_X(x) \quad \text{во всех точках непрерывности } F_X(x)$$

Иерархия сходимостей:

- $X_n \xrightarrow{\text{п.н.}} X \implies X_n \xrightarrow{\mathbb{P}} X$.

- $X_n \xrightarrow{L^p} X \implies X_n \xrightarrow{\mathbb{P}} X$.

- $X_n \xrightarrow{\mathbb{P}} X \implies X_n \xrightarrow{d} X$.

**Доказательство импликации $X_n \xrightarrow{\text{п.н.}} X \implies X_n \xrightarrow{\mathbb{P}} X$:**

Пусть $A_n(\varepsilon) = \bigcup_{k=n}^{\infty} \{|X_k - X| \ge \varepsilon\}$ для $\varepsilon > 0$.

Последовательность $A_n(\varepsilon)$ убывает по включению к $A(\varepsilon) = \{|X_k - X| \ge \varepsilon \text{ б.ч.}\}$.

Поскольку $\{\omega: X_n(\omega) \not\to X(\omega)\} = \bigcup_{m=1}^{\infty} A(1/m)$, из сходимости п.н. следует $\mathbb{P}(A(\varepsilon)) = 0$.

По непрерывности меры $\lim_{n\to\infty} \mathbb{P}(A_n(\varepsilon)) = \mathbb{P}(A(\varepsilon)) = 0$.

Так как $\{|X_n - X| \ge \varepsilon\} \subset A_n(\varepsilon)$, по монотонности вероятности:

$$0 \le \mathbb{P}(|X_n - X| \ge \varepsilon) \le \mathbb{P}(A_n(\varepsilon)) \xrightarrow[n\to\infty]{} 0$$

$\blacksquare$

**Доказательство импликации $X_n \xrightarrow{\mathbb{P}} X \implies X_n \xrightarrow{d} X$:**

Для $\varepsilon > 0$:

$$\{X_n < x\} = \{X_n < x, \, |X_n - X| < \varepsilon\} \cup \{X_n < x, \, |X_n - X| \ge \varepsilon\}$$

$$\implies F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$

Аналогично:

$$F(x - \varepsilon) \le F_n(x) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$

Отсюда:

$$F(x - \varepsilon) - \mathbb{P}(|X_n - X| \ge \varepsilon) \le F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$

При $n \to \infty$:

$$F(x - \varepsilon) \le \liminf_{n\to\infty} F_n(x) \le \limsup_{n\to\infty} F_n(x) \le F(x + \varepsilon)$$

Если $x$ — точка непрерывности $F$, то устремляя $\varepsilon \to 0$, получаем $\lim_{n\to\infty} F_n(x) = F(x)$. $\blacksquare$

**Контрпример $X_n \xrightarrow{\mathbb{P}} 0 \not\implies X_n \xrightarrow{\text{п.н.}} 0$:**

$\Omega = [0, 1]$, $\mathbb{P}$ — мера Лебега. Последовательность индикаторов интервалов $I_n$:

$I_1 = [0, 1], I_2 = [0, 1/2], I_3 = [1/2, 1], I_4 = [0, 1/3], I_5 = [1/3, 2/3], I_6 = [2/3, 1], \dots$.

Пусть $X_n(\omega) = \mathbb{I}_{I_n}(\omega)$.

$\forall \varepsilon \in (0, 1): \mathbb{P}(|X_n| \ge \varepsilon) = \mathbb{P}(X_n = 1) = \lambda(I_n) \to 0 \implies X_n \xrightarrow{\mathbb{P}} 0$.

Для любого $\omega \in [0, 1]$ последовательность $X_n(\omega)$ содержит бесконечно много $0$ и $1$ (предел не существует), поэтому $\mathbb{P}(\lim_{n\to\infty} X_n = 0) = 0$.

### Вероятностные неравенства

**Неравенство Маркова:** Для неотрицательной $Y$ и $\varepsilon > 0$:

$$\mathbb{P}(Y \ge \varepsilon) \le \frac{\mathbb{E}[Y]}{\varepsilon}$$

**Доказательство:**

$$\mathbb{E}[Y] = \int_{\Omega} Y \, d\mathbb{P} = \int_{\{Y \ge \varepsilon\}} Y \, d\mathbb{P} + \int_{\{Y < \varepsilon\}} Y \, d\mathbb{P} \ge \int_{\{Y \ge \varepsilon\}} \varepsilon \, d\mathbb{P} = \varepsilon \mathbb{P}(Y \ge \varepsilon)$$

$\blacksquare$

**Неравенство Чебышева:** Для любой $X$ с конечной дисперсией и $\varepsilon > 0$:

$$\mathbb{P}(|X - \mathbb{E}[X]| \ge \varepsilon) \le \frac{\mathbb{D}[X]}{\varepsilon^2}$$

**Доказательство:** Применить неравенство Маркова к $Y = (X - \mathbb{E}[X])^2$ при пороге $\varepsilon^2$:

$$\mathbb{P}(|X - \mathbb{E}[X]| \ge \varepsilon) = \mathbb{P}\left((X - \mathbb{E}[X])^2 \ge \varepsilon^2\right) \le \frac{\mathbb{E}[(X - \mathbb{E}[X])^2]}{\varepsilon^2} = \frac{\mathbb{D}[X]}{\varepsilon^2}$$

$\blacksquare$

**Неравенство Гаусса (Высочанского–Петунина):**

Для унимодального $X$ с модой $m$ и $\sigma_m^2 = \mathbb{E}[(X-m)^2]$:

$$\mathbb{P}(|X - m| \ge r) \le \frac{4}{9} \frac{\sigma_m^2}{r^2} \quad \text{при } r \ge \sqrt{8/3}\sigma_m$$

Для $r = 3\sigma$ это дает правило «трех сигм»: $\mathbb{P}(|X - \mathbb{E}[X]| \ge 3\sigma) \le \frac{4}{81} \approx 0.0494$.

**Неравенство Колмогорова:**

Для независимых $X_1, \dots, X_n$ с $\mathbb{E}[X_i] = 0, \mathbb{D}[X_i] = \sigma_i^2$, и $S_k = \sum_{i=1}^k X_i$:

$$\mathbb{P}\left(\max_{1 \le k \le n} |S_k| \ge \varepsilon\right) \le \frac{\mathbb{D}[S_n]}{\varepsilon^2}$$

**Доказательство:**

Пусть $A_k = \{|S_k| \ge \varepsilon, \, |S_j| < \varepsilon \text{ при } j < k\}$. Тогда $A = \sum_{k=1}^n A_k = \{\max |S_k| \ge \varepsilon\}$.

$$\mathbb{D}[S_n] = \mathbb{E}[S_n^2] \ge \sum_{k=1}^{n} \mathbb{E}[S_n^2 \mathbb{I}_{A_k}]$$

Поскольку $S_n = S_k + (S_n - S_k)$:

$$\mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}] + 2 \mathbb{E}[S_k (S_n - S_k) \mathbb{I}_{A_k}]$$

В силу независимости $S_k \mathbb{I}_{A_k}$ и $S_n - S_k$, и учитывая $\mathbb{E}[S_n - S_k] = 0$:

$$\mathbb{E}[S_k (S_n - S_k) \mathbb{I}_{A_k}] = 0 \implies \mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}] \ge \varepsilon^2 \mathbb{P}(A_k)$$

$$\mathbb{D}[S_n] \ge \sum_{k=1}^{n} \varepsilon^2 \mathbb{P}(A_k) = \varepsilon^2 \mathbb{P}(A)$$

$\blacksquare$

**Лемма Бореля–Кантелли:**

1. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) < \infty$, то $\mathbb{P}(\limsup A_n) = 0$.

2. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) = \infty$ и $\{A_n\}$ независимы, то $\mathbb{P}(\limsup A_n) = 1$.

**Доказательство:**

1. Пусть $A^* = \limsup A_n = \bigcap_{n=1}^{\infty} \bigcup_{k=n}^{\infty} A_k \implies \mathbb{P}(A^*) \le \sum_{k=n}^{\infty} \mathbb{P}(A_k) \to 0$ при $n \to \infty$.

2. $\mathbb{P}((A^*)^c) = \mathbb{P}(\bigcup_{n=1}^\infty \bigcap_{k=n}^\infty A_k^c)$.

   $\mathbb{P}(\bigcap_{k=n}^{M} A_k^c) = \prod_{k=n}^{M} (1 - \mathbb{P}(A_k)) \le \exp\left(-\sum_{k=n}^M \mathbb{P}(A_k)\right) \to 0$ при $M \to \infty \implies \mathbb{P}(\bigcap_{k=n}^\infty A_k^c) = 0$.

   $\blacksquare$

---

## 2.2. Закон больших чисел (ЗБЧ) и ЦПТ

### Закон больших чисел

**ЗБЧ Чебышева:** Если $X_n$ попарно независимы, одинаково распределены, и $\mathbb{D}[X_1] = \sigma^2 < \infty$:

$$\frac{1}{n} \sum_{i=1}^{n} X_i \xrightarrow[n\to\infty]{\mathbb{P}} \mathbb{E}[X_1]$$

**Доказательство:** Пусть $\mu = \mathbb{E}[X_1]$, $S_n = \sum_{i=1}^n X_i$. По неравенству Чебышева:

$$\mathbb{P}\left(\left|\frac{S_n}{n} - \mu\right| \ge \varepsilon\right) \le \frac{\mathbb{D}[S_n/n]}{\varepsilon^2} = \frac{n \sigma^2}{n^2 \varepsilon^2} = \frac{\sigma^2}{n \varepsilon^2} \xrightarrow[n\to\infty]{} 0$$

$\blacksquare$

**ЗБЧ Хинчина:** Если $X_n$ независимы, одинаково распределены, и $\mathbb{E}[|X_1|] < \infty$, то:

$$\frac{1}{n} \sum_{i=1}^{n} X_i \xrightarrow[n\to\infty]{\mathbb{P}} \mathbb{E}[X_1]$$

**УЗБЧ Колмогорова:** Если $X_n$ независимы, одинаково распределены, то $\frac{1}{n}\sum_{i=1}^{n} X_i \xrightarrow{\text{п.н.}} \mathbb{E}[X_1] \iff \mathbb{E}[|X_1|] < \infty$.

**Лемма Кронекера:** Если $a_n \uparrow \infty$ и $\sum_{n=1}^{\infty} \frac{x_n}{a_n}$ сходится, то $\lim_{n\to\infty} \frac{1}{a_n} \sum_{i=1}^{n} x_i = 0$.

### Характеристические функции

**Характеристическая функция (ХФ):** $\varphi_X(t) = \mathbb{E}[e^{itX}]$.

Свойства:

1. $\varphi(0) = 1, \, |\varphi(t)| \le 1$.

2. $\varphi(-t) = \overline{\varphi(t)}$.

3. $\varphi_{aX+b}(t) = e^{itb} \varphi_X(at)$.

4. $\varphi_{X+Y}(t) = \varphi_X(t)\varphi_Y(t)$ при независимости $X, Y$.

5. Если $\mathbb{E}[|X|^k] < \infty$, то $\varphi(t) = \sum_{j=0}^{k} \frac{(it)^j}{j!} \mathbb{E}[X^j] + o(t^k)$ при $t \to 0$.

**Теорема Леви (непрерывности):** $X_n \xrightarrow{d} X \iff \varphi_{X_n}(t) \to \varphi_X(t)$ для каждого $t \in \mathbb{R}$, где $\varphi_X(t)$ непрерывна в $t=0$.

**Доказательство теоремы Хинчина методом ХФ:**

Пусть $\varphi(t)$ — ХФ для $X_1$, $\mathbb{E}[X_1] = \mu$. При $t \to 0$: $\varphi(t) = 1 + i\mu t + o(t)$.

ХФ для $\overline{X}_n = \frac{S_n}{n}$:

$$\varphi_{\overline{X}_n}(t) = \left( \varphi\left(\frac{t}{n}\right) \right)^n = \left( 1 + \frac{i\mu t}{n} + o\left(\frac{1}{n}\right) \right)^n \xrightarrow[n\to\infty]{} e^{i\mu t}$$

По теореме Леви $\overline{X}_n \xrightarrow{d} \mu$, что эквивалентно $\overline{X}_n \xrightarrow{\mathbb{P}} \mu$. $\blacksquare$

### Центральная предельная теорема

**ЦПТ Линдеберга–Леви:**

Для независимых одинаково распределенных $X_n$ с $\mathbb{E}[X_1] = \mu$ и $\mathbb{D}[X_1] = \sigma^2 > 0$:

$$Y_n = \frac{\sum_{i=1}^{n} X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow[n\to\infty]{d} \mathcal{N}(0, 1)$$

**Доказательство:**

Пусть $\mu=0, \sigma^2=1$. ХФ для $X_1$: $\varphi(t) = 1 - \frac{t^2}{2} + o(t^2)$.

ХФ для $Y_n = \frac{S_n}{\sqrt{n}}$:

$$\varphi_{Y_n}(t) = \left( \varphi\left(\frac{t}{\sqrt{n}}\right) \right)^n = \left( 1 - \frac{t^2}{2n} + o\left(\frac{1}{n}\right) \right)^n \xrightarrow[n\to\infty]{} e^{-t^2/2}$$

По теореме Леви $Y_n \xrightarrow{d} \mathcal{N}(0, 1)$. $\blacksquare$

**Условие Линдеберга (для независимых $X_k$, $B_n^2 = \sum_{k=1}^n \mathbb{D}[X_k]$):**

$$\forall \varepsilon > 0: \lim_{n\to\infty} \frac{1}{B_n^2} \sum_{i=1}^{n} \mathbb{E}\left[ (X_i - \mathbb{E}[X_i])^2 \mathbb{I}(|X_i - \mathbb{E}[X_i]| \ge \varepsilon B_n) \right] = 0$$

**Условие Ляпунова (для некоторого $\delta > 0$):**

$$\lim_{n\to\infty} \frac{1}{B_n^{2+\delta}} \sum_{i=1}^{n} \mathbb{E}\left[ |X_i - \mathbb{E}[X_i]|^{2+\delta} \right] = 0$$

**Доказательство импликации Условие Ляпунова $\implies$ Условие Линдеберга:**

Пусть $Z_i = X_i - \mathbb{E}[X_i]$. На множестве $\{|Z_i| \ge \varepsilon B_n\}$ справедливо:

$$Z_i^2 \le Z_i^2 \frac{|Z_i|^\delta}{\varepsilon^\delta B_n^\delta} = \frac{|Z_i|^{2+\delta}}{\varepsilon^\delta B_n^\delta}$$

$$\frac{1}{B_n^2} \sum_{i=1}^{n} \mathbb{E}\left[ Z_i^2 \mathbb{I}(|Z_i| \ge \varepsilon B_n) \right] \le \frac{1}{\varepsilon^\delta B_n^{2+\delta}} \sum_{i=1}^{n} \mathbb{E}[|Z_i|^{2+\delta}] \to 0$$

$\blacksquare$
