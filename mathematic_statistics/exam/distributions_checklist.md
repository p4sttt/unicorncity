---
title: "Чеклист по распределениям и их свойствам"
description: "Полный справочник по дискретным и непрерывным распределениям с выводами моментов, характеристических и производящих функций"
state: done
date: 2026-06-20
---

# Чеклист по распределениям и их свойствам с выводами

Этот чеклист содержит исчерпывающее руководство по основным вероятностным распределениям, изучаемым в рамках классического курса теории вероятностей и математической статистики. Для каждого распределения приведены: строгое определение (включая плотность или таблицу распределения), вывод производящей функции, характеристической функции, а также вывод математического ожидания и дисперсии.

---

## 1. Дискретные распределения

Дискретные случайные величины принимают не более чем счетное число значений из множества $\{x_k\}$. Основными инструментами работы с ними являются **вероятностная производящая функция (PGF)** $P(z) = \mathbb{E}[z^X] = \sum_k z^{x_k} \mathbb{P}(X=x_k)$ и **характеристическая функция (CF)** $\varphi(t) = \mathbb{E}[e^{itX}] = P(e^{it})$.
Математическое ожидание и дисперсия выражаются через производные PGF в точке $z=1$:
$$\mathbb{E}[X] = P'(1), \quad \mathbb{D}[X] = P''(1) + P'(1) - (P'(1))^2$$

### Распределение Бернулли ($\operatorname{Bern}(p)$)
Случайная величина $X$ принимает значения $1$ (успех) с вероятностью $p$ и $0$ (неудача) с вероятностью $q = 1-p$.

> **Формулировка**
>
> $$\mathbb{P}(X = 1) = p, \quad \mathbb{P}(X = 0) = q \equiv 1-p; \quad p \in [0, 1]$$

#### Вывод PGF, CF и моментов
1. **Производящая функция:**
   $$P(z) = \mathbb{E}[z^X] = z^0 \cdot q + z^1 \cdot p = q + pz$$
2. **Характеристическая функция:**
   $$\varphi(t) = \mathbb{E}[e^{itX}] = P(e^{it}) = q + p e^{it}$$
3. **Математическое ожидание:**
   Вычислим первую производную PGF: $P'(z) = p$.
   $$\mathbb{E}[X] = P'(1) = p$$
4. **Дисперсия:**
   Вычислим вторую производную PGF: $P''(z) = 0$. Тогда:
   $$\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = 0 + p - p^2 = p(1-p) = pq$$
   $\blacksquare$

### Биномиальное распределение ($\operatorname{Bin}(n, p)$)
Случайная величина $X$ равна количеству успехов в серии из $n$ независимых испытаний Бернулли с вероятностью успеха $p$.

> **Формулировка**
>
> $$\mathbb{P}(X = k) = C_n^k p^k q^{n-k}, \quad k \in \{0, 1, \dots, n\}; \quad q = 1-p$$

#### Вывод PGF, CF и моментов
1. **Производящая функция:**
   $$P(z) = \mathbb{E}[z^X] = \sum_{k=0}^{n} z^k C_n^k p^k q^{n-k} = \sum_{k=0}^{n} C_n^k (pz)^k q^{n-k}$$
   По формуле бинома Ньютона:
   $$P(z) = (q + pz)^n$$
2. **Характеристическая функция:**
   $$\varphi(t) = P(e^{it}) = (q + p e^{it})^n$$
3. **Математическое ожидание:**
   Дифференцируем PGF по $z$: $P'(z) = n(q + pz)^{n-1} \cdot p$. Подставляя $z=1$:
   $$\mathbb{E}[X] = P'(1) = np(q + p)^{n-1} = np$$
4. **Дисперсия:**
   Дифференцируем PGF второй раз: $P''(z) = n(n-1)(q + pz)^{n-2} \cdot p^2$. Подставляя $z=1$:
   $$P''(1) = n(n-1)p^2$$
   Находим дисперсию:
   $$\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = n(n-1)p^2 + np - (np)^2 = n^2 p^2 - np^2 + np - n^2 p^2 = np(1-p) = npq$$
   $\blacksquare$

### Распределение Пуассона ($\operatorname{Poi}(\lambda)$)
Описывает число событий, произошедших за фиксированный промежуток времени при постоянной средней интенсивности $\lambda$.

> **Формулировка**
>
> $$\mathbb{P}(X = k) = \frac{\lambda^k e^{-\lambda}}{k!}, \quad k \in \{0, 1, 2, \dots\}; \quad \lambda > 0$$

#### Вывод PGF, CF и моментов
1. **Производящая функция:**
   $$P(z) = \mathbb{E}[z^X] = \sum_{k=0}^{\infty} z^k \frac{\lambda^k e^{-\lambda}}{k!} = e^{-\lambda} \sum_{k=0}^{\infty} \frac{(\lambda z)^k}{k!}$$
   Используя разложение экспоненты в ряд Тейлора:
   $$P(z) = e^{-\lambda} e^{\lambda z} = e^{\lambda(z-1)}$$
2. **Характеристическая функция:**
   $$\varphi(t) = P(e^{it}) = e^{\lambda(e^{it}-1)}$$
3. **Математическое ожидание:**
   Находим первую производную PGF: $P'(z) = \lambda e^{\lambda(z-1)}$. Подставляя $z=1$:
   $$\mathbb{E}[X] = P'(1) = \lambda$$
4. **Дисперсия:**
   Находим вторую производную: $P''(z) = \lambda^2 e^{\lambda(z-1)} \implies P''(1) = \lambda^2$.
   $$\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \lambda^2 + \lambda - \lambda^2 = \lambda$$
   Таким образом, для распределения Пуассона математическое ожидание равно дисперсии: $\mathbb{E}[X] = \mathbb{D}[X] = \lambda$. $\blacksquare$

### Геометрическое распределение ($\operatorname{Geom}(p)$)
Определим $X$ как общее число испытаний до первого успеха включительно в независимых испытаниях Бернулли.

> **Формулировка**
>
> $$\mathbb{P}(X = k) = p q^{k-1}, \quad k \in \{1, 2, 3, \dots\}; \quad q = 1-p$$

#### Вывод PGF, CF и моментов
1. **Производящая функция:**
   $$P(z) = \mathbb{E}[z^X] = \sum_{k=1}^{\infty} z^k p q^{k-1} = pz \sum_{k=1}^{\infty} (qz)^{k-1}$$
   Для $|z| < 1/q$ сумма представляет собой сходящуюся бесконечно убывающую геометрическую прогрессию со знаменателем $qz$:
   $$P(z) = \frac{pz}{1 - qz}$$
2. **Характеристическая функция:**
   $$\varphi(t) = P(e^{it}) = \frac{p e^{it}}{1 - q e^{it}}$$
3. **Математическое ожидание:**
   Дифференцируем PGF:
   $$P'(z) = \frac{p(1 - qz) - pz(-q)}{(1 - qz)^2} = \frac{p}{(1 - qz)^2}$$
   Подставляем $z=1$:
   $$\mathbb{E}[X] = P'(1) = \frac{p}{(1 - q)^2} = \frac{p}{p^2} = \frac{1}{p}$$
4. **Дисперсия:**
   Дифференцируем PGF второй раз:
   $$P''(z) = \left( p(1-qz)^{-2} \right)' = 2pq(1-qz)^{-3} = \frac{2pq}{(1-qz)^3}$$
   Подставляем $z=1$:
   $$P''(1) = \frac{2pq}{p^3} = \frac{2q}{p^2}$$
   Вычисляем дисперсию:
   $$\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \frac{2q}{p^2} + \frac{1}{p} - \frac{1}{p^2} = \frac{2q + p - 1}{p^2}$$
   Поскольку $2q + p - 1 = 2(1-p) + p - 1 = 1 - p = q$:
   $$\mathbb{D}[X] = \frac{q}{p^2} = \frac{1-p}{p^2}$$
   $\blacksquare$

### Отрицательное биномиальное распределение ($\operatorname{NegBin}(r, p)$)
Случайная величина $X$ равна количеству неудач до получения $r$-го успеха в испытаниях Бернулли.

> **Формулировка**
>
> $$\mathbb{P}(X = k) = C_{k+r-1}^{k} p^r q^k, \quad k \in \{0, 1, 2, \dots\}; \quad q = 1-p$$

#### Вывод PGF, CF и моментов
1. **Производящая функция:**
   $$P(z) = \sum_{k=0}^{\infty} z^k C_{k+r-1}^k p^r q^k = p^r \sum_{k=0}^{\infty} C_{k+r-1}^k (qz)^k$$
   Используя разложение Тейлора для отрицательной степени $(1-x)^{-r} = \sum_{k=0}^{\infty} C_{k+r-1}^k x^k$, получаем:
   $$P(z) = p^r (1 - qz)^{-r} = \left( \frac{p}{1-qz} \right)^r$$
2. **Характеристическая функция:**
   $$\varphi(t) = \left( \frac{p}{1 - q e^{it}} \right)^r$$
3. **Математическое ожидание:**
   $$P'(z) = r \left( \frac{p}{1-qz} \right)^{r-1} \cdot \frac{pq}{(1-qz)^2} = \frac{rq p^r}{(1-qz)^{r+1}}$$
   Подставляя $z=1$:
   $$\mathbb{E}[X] = P'(1) = \frac{rq p^r}{p^{r+1}} = \frac{rq}{p}$$
4. **Дисперсия:**
   Дифференцируем второй раз:
   $$P''(z) = \frac{(r+1)rq^2 p^r}{(1-qz)^{r+2}} \implies P''(1) = \frac{r(r+1)q^2}{p^2}$$
   Находим дисперсию:
   $$\mathbb{D}[X] = P''(1) + P'(1) - (\mathbb{E}[X])^2 = \frac{r(r+1)q^2}{p^2} + \frac{rq}{p} - \frac{r^2 q^2}{p^2} = \frac{rq^2 + rqp}{p^2} = \frac{rq(q+p)}{p^2} = \frac{rq}{p^2}$$
   $\blacksquare$

### Гипергеометрическое распределение ($\operatorname{Hyper}(N, M, n)$)
Выборка объема $n$ извлекается без возвращения из совокупности объема $N$, содержащей $M$ «успешных» элементов. Случайная величина $X$ — число успехов в выборке.

> **Формулировка**
>
> $$\mathbb{P}(X = k) = \frac{C_M^k C_{N-M}^{n-k}}{C_N^n}, \quad \max(0, n - (N - M)) \le k \le \min(n, M)$$

#### Вывод моментов напрямую
Поскольку схема без возвращения не позволяет представить $X$ как сумму независимых величин, представим её как $X = \sum_{i=1}^{n} Y_i$, где $Y_i = 1$, если $i$-й извлеченный элемент является успешным, и $0$ в противном случае.
Величина $Y_i$ имеет распределение Бернулли.
Вероятность того, что $i$-й элемент успешен: $\mathbb{P}(Y_i = 1) = \frac{M}{N}$. Таким образом, $\mathbb{E}[Y_i] = \frac{M}{N} = p$.
1. **Математическое ожидание:**
   В силу линейности математического ожидания (не зависящей от независимости):
   $$\mathbb{E}[X] = \sum_{i=1}^{n} \mathbb{E}[Y_i] = n \frac{M}{N}$$
2. **Дисперсия:**
   Для зависимых величин дисперсия суммы равна:
   $$\mathbb{D}[X] = \sum_{i=1}^{n} \mathbb{D}[Y_i] + \sum_{i \neq j} \operatorname{Cov}(Y_i, Y_j) = n \mathbb{D}[Y_1] + n(n-1)\operatorname{Cov}(Y_1, Y_2)$$
   Вычислим характеристики компонент:
   $$\mathbb{D}[Y_1] = p(1-p) = \frac{M}{N}\left(1 - \frac{M}{N}\right)$$
   Для ковариации найдем $\mathbb{E}[Y_1 Y_2] = \mathbb{P}(Y_1 = 1, Y_2 = 1) = \mathbb{P}(Y_1 = 1) \mathbb{P}(Y_2 = 1 \mid Y_1 = 1) = \frac{M}{N} \cdot \frac{M-1}{N-1}$.
   $$\operatorname{Cov}(Y_1, Y_2) = \mathbb{E}[Y_1 Y_2] - \mathbb{E}[Y_1]\mathbb{E}[Y_2] = \frac{M(M-1)}{N(N-1)} - \frac{M^2}{N^2} = \frac{M}{N} \left( \frac{M-1}{N-1} - \frac{M}{N} \right) = -\frac{M(N-M)}{N^2(N-1)}$$
   Подставляем в формулу дисперсии:
   $$\mathbb{D}[X] = n \frac{M(N-M)}{N^2} - n(n-1) \frac{M(N-M)}{N^2(N-1)} = n \frac{M(N-M)}{N^2} \left[ 1 - \frac{n-1}{N-1} \right] = n \frac{M}{N}\left(1 - \frac{M}{N}\right) \frac{N-n}{N-1}$$
   Коэффициент $\frac{N-n}{N-1}$ называется поправкой на конечность генеральной совокупности. $\blacksquare$

---

## 2. Непрерывные распределения

Для непрерывных распределений основным аппаратом исследования числовых характеристик является характеристическая функция $\varphi(t) = \mathbb{E}[e^{itX}] = \int_{-\infty}^{\infty} e^{itx} p(x) \, dx$. Моменты находятся через разложение в ряд Тейлора или дифференцирование: $\mathbb{E}[X^k] = i^{-k} \varphi^{(k)}(0)$.

### Равномерное распределение ($\operatorname{U}(a, b)$)
Плотность постоянна на отрезке $[a, b]$.

> **Формулировка**
>
> $$p(x) = \frac{1}{b-a} \mathbb{I}(x \in [a, b])$$

#### Вывод CF и моментов
1. **Характеристическая функция:**
   $$\varphi(t) = \int_{a}^{b} e^{itx} \frac{1}{b-a} \, dx = \left. \frac{e^{itx}}{it(b-a)} \right|_a^b = \frac{e^{itb} - e^{ita}}{it(b-a)}$$
2. **Математическое ожидание:**
   Вычислим интеграл напрямую:
   $$\mathbb{E}[X] = \int_{a}^{b} x \frac{1}{b-a} \, dx = \left. \frac{x^2}{2(b-a)} \right|_a^b = \frac{b^2 - a^2}{2(b-a)} = \frac{a+b}{2}$$
3. **Дисперсия:**
   Вычислим второй начальный момент:
   $$\mathbb{E}[X^2] = \int_{a}^{b} x^2 \frac{1}{b-a} \, dx = \left. \frac{x^3}{3(b-a)} \right|_a^b = \frac{b^3 - a^3}{3(b-a)} = \frac{a^2 + ab + b^2}{3}$$
   Тогда дисперсия равна:
   $$\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{a^2 + ab + b^2}{3} - \frac{a^2 + 2ab + b^2}{4} = \frac{4a^2 + 4ab + 4b^2 - 3a^2 - 6ab - 3b^2}{12} = \frac{(b-a)^2}{12}$$
   $\blacksquare$

### Показательное (экспоненциальное) распределение ($\operatorname{Exp}(\lambda)$)

> **Формулировка**
>
> $$p(x) = \lambda e^{-\lambda x} \mathbb{I}(x \ge 0); \quad \lambda > 0$$

#### Вывод CF и моментов
1. **Характеристическая функция:**
   $$\varphi(t) = \int_{0}^{\infty} e^{itx} \lambda e^{-\lambda x} \, dx = \lambda \int_{0}^{\infty} e^{-(\lambda - it)x} \, dx$$
   Так как $\operatorname{Re}(\lambda - it) = \lambda > 0$, интеграл сходится на бесконечности:
   $$\varphi(t) = \lambda \left. \frac{e^{-(\lambda - it)x}}{-(\lambda - it)} \right|_0^\infty = \frac{\lambda}{\lambda - it} = \left(1 - \frac{it}{\lambda}\right)^{-1}$$
2. **Математическое ожидание:**
   Продифференцируем характеристическую функцию по $t$:
   $$\varphi'(t) = -\left(1 - \frac{it}{\lambda}\right)^{-2} \cdot \left(-\frac{i}{\lambda}\right) = \frac{i}{\lambda} \left(1 - \frac{it}{\lambda}\right)^{-2}$$
   Тогда математическое ожидание равно:
   $$\mathbb{E}[X] = \frac{1}{i} \varphi'(0) = \frac{1}{i} \frac{i}{\lambda} = \frac{1}{\lambda}$$
3. **Дисперсия:**
   Дифференцируем второй раз:
   $$\varphi''(t) = \frac{i}{\lambda} (-2) \left(1 - \frac{it}{\lambda}\right)^{-3} \cdot \left(-\frac{i}{\lambda}\right) = -\frac{2}{\lambda^2} \left(1 - \frac{it}{\lambda}\right)^{-3}$$
   Второй момент:
   $$\mathbb{E}[X^2] = \frac{1}{i^2} \varphi''(0) = -1 \cdot \left(-\frac{2}{\lambda^2}\right) = \frac{2}{\lambda^2}$$
   Вычисляем дисперсию:
   $$\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{2}{\lambda^2} - \frac{1}{\lambda^2} = \frac{1}{\lambda^2}$$
   $\blacksquare$

### Нормальное распределение ($\mathcal{N}(\mu, \sigma^2)$)

> **Формулировка**
>
> $$p(x) = \frac{1}{\sigma \sqrt{2\pi}} \exp\left(-\frac{(x-\mu)^2}{2\sigma^2}\right)$$

#### Интеграл Пуассона (Нормировка)
Докажем, что $\int_{-\infty}^{\infty} p(x) \, dx = 1$. Сделаем замену $z = (x-\mu)/\sigma$, тогда $dx = \sigma dz$. Интеграл примет вид:
$$J = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{-z^2/2} \, dz$$
Рассмотрим квадрат этого интеграла и перейдем к полярным координатам ($z_1 = r\cos\theta, \, z_2 = r\sin\theta, \, dz_1 dz_2 = r \, dr \, d\theta$):
$$J^2 = \frac{1}{2\pi} \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} e^{-(z_1^2 + z_2^2)/2} \, dz_1 \, dz_2 = \frac{1}{2\pi} \int_{0}^{2\pi} d\theta \int_{0}^{\infty} e^{-r^2/2} r \, dr$$
Интеграл по углу равен $2\pi$. Сделаем во втором интеграле замену $u = r^2/2, \, du = r \, dr$:
$$J^2 = \frac{2\pi}{2\pi} \int_{0}^{\infty} e^{-u} \, du = \left. -e^{-u} \right|_0^\infty = 1 \implies J = 1$$

#### Вывод CF и моментов
Сначала найдем характеристическую функцию стандартного нормального распределения $Y \sim \mathcal{N}(0, 1)$:
$$\varphi_Y(t) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{ity} e^{-y^2/2} \, dy$$
Продифференцируем $\varphi_Y(t)$ по $t$:
$$\varphi'_Y(t) = \frac{1}{\sqrt{2\pi}} \int_{-\infty}^{\infty} i y e^{ity} e^{-y^2/2} \, dy = \frac{i}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{ity} \, d\left(-e^{-y^2/2}\right)$$
Интегрируем по частям, полагая $u = e^{ity}, \, dv = d\left(-e^{-y^2/2}\right)$:
$$\varphi'_Y(t) = \frac{i}{\sqrt{2\pi}} \left[ \left. -e^{ity} e^{-y^2/2} \right|_{-\infty}^{\infty} - \int_{-\infty}^{\infty} (-e^{-y^2/2}) (it e^{ity}) \, dy \right]$$
Внеинтегральный член равен 0 в силу экспоненциального затухания $e^{-y^2/2}$ на бесконечности. Получаем:
$$\varphi'_Y(t) = -\frac{t}{\sqrt{2\pi}} \int_{-\infty}^{\infty} e^{ity} e^{-y^2/2} \, dy = -t \varphi_Y(t)$$
Мы получили линейное дифференциальное уравнение первого порядка:
$$\frac{d\varphi_Y}{\varphi_Y} = -t \, dt \implies \ln \varphi_Y(t) = -\frac{t^2}{2} + C$$
Так как $\varphi_Y(0) = 1$, константа $C = 0$. Получаем:
$$\varphi_Y(t) = e^{-t^2/2}$$
Для общего случая $X = \sigma Y + \mu$ применим свойство линейного преобразования ХФ:
$$\varphi_X(t) = e^{it\mu} \varphi_Y(\sigma t) = \exp\left(it\mu - \frac{\sigma^2 t^2}{2}\right)$$
Моменты находятся разложением логарифма ХФ в ряд Тейлора:
$$\ln \varphi_X(t) = it\mu - \frac{\sigma^2 t^2}{2} \equiv it\mathbb{E}[X] - \frac{t^2}{2} \mathbb{D}[X] \implies \mathbb{E}[X] = \mu, \, \mathbb{D}[X] = \sigma^2$$
$\blacksquare$

### Распределение Гамма ($\operatorname{Gamma}(\alpha, \beta)$)

> **Формулировка**
>
> $$p(x) = \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x} \mathbb{I}(x \ge 0); \quad \alpha > 0, \, \beta > 0$$

Здесь $\Gamma(\alpha) = \int_0^\infty u^{\alpha-1} e^{-u} \, du$ — гамма-функция Эйлера.

#### Вывод CF и моментов
1. **Характеристическая функция:**
   $$\varphi(t) = \int_{0}^{\infty} e^{itx} \frac{\beta^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{-\beta x} \, dx = \frac{\beta^\alpha}{\Gamma(\alpha)} \int_{0}^{\infty} x^{\alpha-1} e^{-(\beta - it)x} \, dx$$
   Сделаем замену переменной в комплексной плоскости: $u = (\beta - it)x$, тогда $dx = \frac{du}{\beta - it}$.
   $$\varphi(t) = \frac{\beta^\alpha}{\Gamma(\alpha)} \frac{1}{(\beta - it)^\alpha} \int_{0}^{\infty} u^{\alpha-1} e^{-u} \, du$$
   По определению гамма-функции интеграл равен $\Gamma(\alpha)$, они сокращаются:
   $$\varphi(t) = \frac{\beta^\alpha}{(\beta - it)^\alpha} = \left( 1 - \frac{it}{\beta} \right)^{-\alpha}$$
2. **Математическое ожидание:**
   Дифференцируем ХФ:
   $$\varphi'(t) = -\alpha \left( 1 - \frac{it}{\beta} \right)^{-\alpha-1} \cdot \left(-\frac{i}{\beta}\right) = \frac{i\alpha}{\beta} \left( 1 - \frac{it}{\beta} \right)^{-\alpha-1}$$
   $$\mathbb{E}[X] = \frac{1}{i} \varphi'(0) = \frac{\alpha}{\beta}$$
3. **Дисперсия:**
   Дифференцируем второй раз:
   $$\varphi''(t) = \frac{i\alpha}{\beta} (-\alpha-1) \left( 1 - \frac{it}{\beta} \right)^{-\alpha-2} \cdot \left(-\frac{i}{\beta}\right) = -\frac{\alpha(\alpha+1)}{\beta^2} \left( 1 - \frac{it}{\beta} \right)^{-\alpha-2}$$
   Находим второй момент:
   $$\mathbb{E}[X^2] = -\varphi''(0) = \frac{\alpha(\alpha+1)}{\beta^2}$$
   Дисперсия:
   $$\mathbb{D}[X] = \mathbb{E}[X^2] - (\mathbb{E}[X])^2 = \frac{\alpha^2 + \alpha}{\beta^2} - \frac{\alpha^2}{\beta^2} = \frac{\alpha}{\beta^2}$$
   $\blacksquare$

### Распределение Хи-квадрат ($\chi^2(k)$)
Распределение суммы квадратов $k$ независимых случайных величин со стандартным нормальным распределением $\mathcal{N}(0, 1)$. Является частным случаем гамма-распределения $\operatorname{Gamma}(\alpha = k/2, \beta = 1/2)$.

> **Формулировка**
>
> $$p(x) = \frac{1}{2^{k/2}\Gamma(k/2)} x^{k/2-1} e^{-x/2} \mathbb{I}(x \ge 0)$$

#### Вывод CF и моментов
Поскольку $\chi^2(k)$ эквивалентно $\operatorname{Gamma}(k/2, 1/2)$, подставим эти значения параметров в полученные ранее общие формулы:
1. **Характеристическая функция:**
   $$\varphi(t) = \left( 1 - \frac{it}{1/2} \right)^{-k/2} = (1 - 2it)^{-k/2}$$
2. **Математическое ожидание:**
   $$\mathbb{E}[X] = \frac{\alpha}{\beta} = \frac{k/2}{1/2} = k$$
3. **Дисперсия:**
   $$\mathbb{D}[X] = \frac{\alpha}{\beta^2} = \frac{k/2}{1/4} = 2k$$
   $\blacksquare$

### Распределение Коши ($\operatorname{Cauchy}(a, b)$)
Является классическим примером распределения с «тяжелыми хвостами», для которого не определены моменты.

> **Формулировка**
>
> $$p(x) = \frac{1}{\pi b \left(1 + \left(\frac{x-a}{b}\right)^2\right)}, \quad x \in \mathbb{R}; \quad b > 0$$

#### Вывод CF методом вычетов (для стандартного случая $a=0, b=1$)
Вычислим характеристическую функцию:
$$\varphi(t) = \frac{1}{\pi} \int_{-\infty}^{\infty} \frac{e^{itx}}{1+x^2} \, dx$$
Пусть сначала $t > 0$. Рассмотрим контурный интеграл от функции $f(z) = \frac{e^{itz}}{1+z^2}$ по замкнутому контуру $\Gamma_R$, состоящему из отрезка $[-R, R]$ вещественной оси и полуокружности $C_R = \{z = R e^{i\theta}, \, \theta \in [0, \pi]\}$ в верхней полуплоскости.
Функция $f(z) = \frac{e^{itz}}{(z-i)(z+i)}$ имеет единственный простой полюс в верхней полуплоскости в точке $z=i$.
Вычислим вычет в этом полюсе:
$$\operatorname{Res}_{z=i} f(z) = \lim_{z \to i} (z-i)\frac{e^{itz}}{(z-i)(z+i)} = \frac{e^{-t}}{2i}$$
По основной теореме о вычетах:
$$\oint_{\Gamma_R} f(z) \, dz = 2\pi i \operatorname{Res}_{z=i} f(z) = 2\pi i \frac{e^{-t}}{2i} = \pi e^{-t}$$
С другой стороны:
$$\oint_{\Gamma_R} f(z) \, dz = \int_{-R}^{R} \frac{e^{itx}}{1+x^2} \, dx + \int_{C_R} f(z) \, dz$$
По лемме Жордана, поскольку $t > 0$, интеграл по полуокружности стремится к нулю при $R \to \infty$:
$$\lim_{R \to \infty} \int_{C_R} f(z) \, dz = 0$$
Переходя к пределу при $R \to \infty$, получаем для $t > 0$:
$$\int_{-\infty}^{\infty} \frac{e^{itx}}{1+x^2} \, dx = \pi e^{-t} \implies \varphi(t) = e^{-t}$$
Поскольку $\varphi(-t) = \overline{\varphi(t)}$, для любых значений $t \in \mathbb{R}$ окончательно имеем:
$$\varphi(t) = e^{-|t|}$$
Для общего случая $\operatorname{Cauchy}(a, b)$ с помощью линейного преобразования получаем:
$$\varphi_X(t) = e^{iat - b|t|}$$
Поскольку $\varphi(t) = e^{-|t|}$ не дифференцируема в точке $t=0$, у распределения Коши **не существуют** математическое ожидание и дисперсия (соответствующие интегралы Лебега расходятся). $\blacksquare$
