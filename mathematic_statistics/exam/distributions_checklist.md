---
title: "Чеклист по распределениям и их свойствам"
description: "Полный справочник по дискретным и непрерывным распределениям с выводами моментов, характеристических и производящих функций"
state: done
date: 2026-06-20
---

# Чеклист по распределениям и их свойствам с выводами

## 1. Дискретные распределения

Связь числовых характеристик с производящей функцией $P(z) = \mathbb{E}[z^X]$ и характеристической функцией $\varphi(t) = \mathbb{E}[e^{itX}] = P(e^{it})$:

$$\mathbb{E}[X] = P'(1), \quad \mathbb{D}[X] = P''(1) + P'(1) - (P'(1))^2$$

### Распределение Бернулли ($\operatorname{Bern}(p)$)

**Закон распределения:** $\mathbb{P}(X = 1) = p, \quad \mathbb{P}(X = 0) = q = 1-p$.

**Вывод PGF, CF и моментов:**

1. $P(z) = \mathbb{E}[z^X] = z^0 q + z^1 p = q + pz$.

2. $\varphi(t) = P(e^{it}) = q + p e^{it}$.

3. $P'(z) = p \implies \mathbb{E}[X] = P'(1) = p$.

4. $P''(z) = 0 \implies \mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = 0 + p - p^2 = p(1-p) = pq$.

$\blacksquare$

### Биномиальное распределение ($\operatorname{Bin}(n, p)$)

**Закон распределения:** $\mathbb{P}(X = k) = C_n^k p^k q^{n-k}, \quad k \in \{0, 1, \dots, n\}$.

**Вывод PGF, CF и моментов:**

1. $P(z) = \mathbb{E}[z^X] = \sum_{k=0}^{n} C_n^k (pz)^k q^{n-k} = (q + pz)^n$.

2. $\varphi(t) = P(e^{it}) = (q + p e^{it})^n$.

3. $P'(z) = n(q + pz)^{n-1} p \implies \mathbb{E}[X] = P'(1) = np$.

4. $P''(z) = n(n-1)(q + pz)^{n-2} p^2 \implies P''(1) = n(n-1)p^2$.

5. $\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = n(n-1)p^2 + np - n^2 p^2 = npq$.

$\blacksquare$

### Распределение Пуассона ($\operatorname{Poi}(\lambda)$)

**Закон распределения:** $\mathbb{P}(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k \in \{0, 1, 2, \dots\}$.

**Вывод PGF, CF и моментов:**

1. $P(z) = \mathbb{E}[z^X] = e^{-\lambda} \sum_{k=0}^{\infty} \frac{(\lambda z)^k}{k!} = e^{-\lambda} e^{\lambda z} = e^{\lambda(z-1)}$.

2. $\varphi(t) = P(e^{it}) = e^{\lambda(e^{it}-1)}$.

3. $P'(z) = \lambda e^{\lambda(z-1)} \implies \mathbb{E}[X] = P'(1) = \lambda$.

4. $P''(z) = \lambda^2 e^{\lambda(z-1)} \implies P''(1) = \lambda^2$.

5. $\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \lambda^2 + \lambda - \lambda^2 = \lambda$.

$\blacksquare$

### Геометрическое распределение ($\operatorname{Geom}(p)$)

**Закон распределения:** $\mathbb{P}(X = k) = p q^{k-1}, \quad k \in \{1, 2, 3, \dots\}$.

**Вывод PGF, CF и моментов:**

1. $P(z) = \mathbb{E}[z^X] = \sum_{k=1}^{\infty} z^k p q^{k-1} = pz \sum_{k=1}^{\infty} (qz)^{k-1} = \frac{pz}{1 - qz}$.

2. $\varphi(t) = P(e^{it}) = \frac{p e^{it}}{1 - q e^{it}}$.

3. $P'(z) = \frac{p}{(1 - qz)^2} \implies \mathbb{E}[X] = P'(1) = \frac{1}{p}$.

4. $P''(z) = \frac{2pq}{(1 - qz)^3} \implies P''(1) = \frac{2q}{p^2}$.

5. $\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \frac{2q}{p^2} + \frac{1}{p} - \frac{1}{p^2} = \frac{q}{p^2}$.

$\blacksquare$

### Отрицательное биномиальное распределение ($\operatorname{NegBin}(r, p)$)

**Закон распределения:** $\mathbb{P}(X = k) = C_{k+r-1}^{k} p^r q^k, \quad k \in \{0, 1, 2, \dots\}$.

**Вывод PGF, CF и моментов:**

1. $P(z) = p^r \sum_{k=0}^{\infty} C_{k+r-1}^k (qz)^k = p^r (1 - qz)^{-r}$.

2. $\varphi(t) = \left( \frac{p}{1 - q e^{it}} \right)^r$.

3. $P'(z) = \frac{rq p^r}{(1-qz)^{r+1}} \implies \mathbb{E}[X] = P'(1) = \frac{rq}{p}$.

4. $P''(z) = \frac{r(r+1)q^2 p^r}{(1-qz)^{r+2}} \implies P''(1) = \frac{r(r+1)q^2}{p^2}$.

5. $\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \frac{r(r+1)q^2}{p^2} + \frac{rq}{p} - \frac{r^2 q^2}{p^2} = \frac{rq}{p^2}$.

$\blacksquare$

### Гипергеометрическое распределение ($\operatorname{Hyper}(N, M, n)$)

**Закон распределения:** $\mathbb{P}(X = k) = \frac{C_M^k C_{N-M}^{n-k}}{C_N^n}$.

**Вывод моментов:**

Представим $X = \sum_{i=1}^{n} Y_i$, где $Y_i \sim \operatorname{Bern}(p)$ с $p = M/N$.

1. $\mathbb{E}[X] = \sum_{i=1}^n \mathbb{E}[Y_i] = n \frac{M}{N}$.

2. $\mathbb{D}[X] = n \mathbb{D}[Y_1] + n(n-1)\operatorname{Cov}(Y_1, Y_2)$.

   $\mathbb{D}[Y_1] = p(1-p) = \frac{M}{N}\left(1 - \frac{M}{N}\right)$.

   $\mathbb{E}[Y_1 Y_2] = \mathbb{P}(Y_1 = 1, Y_2 = 1) = \frac{M(M-1)}{N(N-1)}$.

   $\operatorname{Cov}(Y_1, Y_2) = \frac{M(M-1)}{N(N-1)} - \frac{M^2}{N^2} = -\frac{M(N-M)}{N^2(N-1)}$.

   $\mathbb{D}[X] = n \frac{M(N-M)}{N^2} - n(n-1) \frac{M(N-M)}{N^2(N-1)} = n \frac{M}{N}\left(1 - \frac{M}{N}\right) \frac{N-n}{N-1}$.

$\blacksquare$

---

## 2. Непрерывные распределения

Связь ХФ $\varphi(t) = \mathbb{E}[e^{itX}]$ с моментами: $\mathbb{E}[X^k] = i^{-k} \varphi^{(k)}(0)$.

### Равномерное распределение ($\operatorname{U}(a, b)$)

**Плотность:** $p(x) = \frac{1}{b-a} \mathbb{I}(x \in [a, b])$.

**Вывод CF и моментов:**

1. $\varphi(t) = \int_{a}^{b} e^{itx} \frac{1}{b-a} \, dx = \frac{e^{itb} - e^{ita}}{it(b-a)}$.

2. $\mathbb{E}[X] = \int_{a}^{b} x \frac{1}{b-a} \, dx = \frac{a+b}{2}$.

3. $\mathbb{E}[X^2] = \int_{a}^{b} x^2 \frac{1}{b-a} \, dx = \frac{a^2 + ab + b^2}{3}$.

4. $\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{(b-a)^2}{12}$.

$\blacksquare$

### Показательное распределение ($\operatorname{Exp}(\lambda)$)

**Плотность:** $p(x) = \lambda e^{-\lambda x} \mathbb{I}(x \ge 0)$.

**Вывод CF и моментов:**

1. $\varphi(t) = \lambda \int_{0}^{\infty} e^{-(\lambda - it)x} \, dx = \frac{\lambda}{\lambda - it} = \left(1 - \frac{it}{\lambda}\right)^{-1}$.

2. $\varphi'(t) = \frac{i}{\lambda} \left(1 - \frac{it}{\lambda}\right)^{-2} \implies \mathbb{E}[X] = \frac{1}{i} \varphi'(0) = \frac{1}{\lambda}$.

3. $\varphi''(t) = -\frac{2}{\lambda^2} \left(1 - \frac{it}{\lambda}\right)^{-3} \implies \mathbb{E}[X^2] = -\varphi''(0) = \frac{2}{\lambda^2}$.

4. $\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{1}{\lambda^2}$.

$\blacksquare$

### Нормальное распределение ($\mathcal{N}(\mu, \sigma^2)$)

**Плотность:** $p(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$.

**Нормировка:** $J = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{-z^2/2} \, dz$.

$$J^2 = \frac{1}{2\pi} \int_{0}^{2\pi} d\theta \int_{0}^{\infty} e^{-r^2/2} r \, dr = \int_{0}^{\infty} e^{-u} \, du = 1 \implies J = 1$$

**Вывод CF и моментов:**

Для $Y \sim \mathcal{N}(0, 1)$:

$$\varphi'_Y(t) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} i y e^{ity} e^{-y^2/2} \, dy = -t \varphi_Y(t) \implies \varphi_Y(t) = e^{-t^2/2}$$

Для $X = \sigma Y + \mu$:

$$\varphi_X(t) = e^{it\mu} \varphi_Y(\sigma t) = \exp\left(it\mu - \frac{\sigma^2 t^2}{2}\right) \implies \mathbb{E}[X] = \mu, \, \mathbb{D}[X] = \sigma^2$$

$\blacksquare$

### Распределение Гамма ($\operatorname{Gamma}(\alpha, \beta)$)

**Плотность:** $p(x) = \frac{2^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x} \mathbb{I}(x \ge 0)$.

**Вывод CF и моментов:**

1. $\varphi(t) = \frac{\beta^\alpha}{\Gamma(\alpha)} \int_{0}^{\infty} x^{\alpha-1} e^{-(\beta - it)x} \, dx = \left( 1 - \frac{it}{\beta} \right)^{-\alpha}$.

2. $\varphi'(t) = \frac{i\alpha}{\beta} \left( 1 - \frac{it}{\beta} \right)^{-\alpha-1} \implies \mathbb{E}[X] = \frac{\alpha}{\beta}$.

3. $\varphi''(t) = -\frac{\alpha(\alpha+1)}{\beta^2} \left( 1 - \frac{it}{\beta} \right)^{-\alpha-2} \implies \mathbb{E}[X^2] = \frac{\alpha(\alpha+1)}{\beta^2}$.

4. $\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{\alpha}{\beta^2}$.

$\blacksquare$

### Распределение Хи-квадрат ($\chi^2(k)$)

Эквивалентно $\operatorname{Gamma}(k/2, 1/2)$.

**Плотность:** $p(x) = \frac{1}{2^{k/2}\Gamma(k/2)} x^{k/2-1} e^{-x/2} \mathbb{I}(x \ge 0)$.

**Вывод CF и моментов:**

1. $\varphi(t) = (1 - 2it)^{-k/2}$.

2. $\mathbb{E}[X] = \frac{k/2}{1/2} = k$.

3. $\mathbb{D}[X] = \frac{k/2}{(1/2)^2} = 2k$.

$\blacksquare$

### Распределение Коши ($\operatorname{Cauchy}(a, b)$)

**Плотность:** $p(x) = \frac{1}{\pi b \left(1 + \left(\frac{x-a}{b}\right)^2\right)}$.

**Вывод CF методом вычетов ($a=0, b=1$):**

Для $t > 0$ контур $\Gamma_R$ в верхней полуплоскости имеет полюс в $z=i$:

$$\operatorname{Res}_{z=i} \frac{e^{itz}}{1+z^2} = \frac{e^{-t}}{2i}$$

$$\oint_{\Gamma_R} \frac{e^{itz}}{1+z^2} \, dz = 2\pi i \frac{e^{-t}}{2i} = \pi e^{-t} \implies \varphi(t) = e^{-t}$$

С учетом симметрии $\varphi(t) = e^{-|t|}$. Для общего случая: $\varphi_X(t) = e^{iat - b|t|}$.

Моменты не существуют, так как $\varphi(t)$ не дифференцируема в $t=0$.

$\blacksquare$
