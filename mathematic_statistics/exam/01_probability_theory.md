---
title: "Раздел 1. Основы теории вероятностей и случайные величины"
description: "Аксиоматика Колмогорова, одномерные и многомерные случайные величины, числовые характеристики"
date: 2026-06-20
status: done
---

# Раздел 1. Основы теории вероятностей и случайные величины

## 1.1. Аксиоматика и базовые формулы

### Вероятностное пространство
**Вероятностное пространство** — тройка $(\Omega, \mathcal{F}, \mathbb{P})$, где:
1. $\Omega$ — множество элементарных исходов $\omega$.
2. $\mathcal{F}$ — $\sigma$-алгебра событий:
   - $\Omega \in \mathcal{F}$;
   - $A \in \mathcal{F} \implies A^c = \Omega \setminus A \in \mathcal{F}$;
   - $A_n \in \mathcal{F}, n \in \mathbb{N} \implies \bigcup_{n=1}^{\infty} A_n \in \mathcal{F}$.
3. $\mathbb{P}$ — вероятностная мера на $\mathcal{F}$:
   - $\mathbb{P}(A) \ge 0, \quad \forall A \in \mathcal{F}$;
   - $\mathbb{P}(\Omega) = 1$;
   - $\sigma$-аддитивность: для попарно непересекающихся $A_n \in \mathcal{F}$ ($A_i \cap A_j = \emptyset$ при $i \neq j$):
     $$\mathbb{P}\left(\sum_{n=1}^{\infty} A_n\right) = \sum_{n=1}^{\infty} \mathbb{P}(A_n)$$

### Непрерывность вероятностной меры
**Теорема о непрерывности вероятности:**
1. Если $A_n \uparrow A$ ($A_1 \subset A_2 \subset \dots$ и $A = \bigcup_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.
2. Если $A_n \downarrow A$ ($A_1 \supset A_2 \supset \dots$ и $A = \bigcap_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.

**Доказательство:**
1. Пусть $B_1 = A_1$, $B_k = A_k \setminus A_{k-1}$ для $k \ge 2$. Тогда $\{B_k\}$ попарно не пересекаются, $\sum_{k=1}^{n} B_k = A_n$, $\sum_{k=1}^{\infty} B_k = A$.
   $$\mathbb{P}(A) = \mathbb{P}\left(\sum_{k=1}^{\infty} B_k\right) = \sum_{k=1}^{\infty} \mathbb{P}(B_k) = \lim_{n\to\infty} \sum_{k=1}^{n} \mathbb{P}(B_k) = \lim_{n\to\infty} \mathbb{P}(A_n)$$
2. Пусть $C_n = A_n^c$. Тогда $C_n \uparrow A^c$. Из п. 1:
   $$\lim_{n\to\infty} \mathbb{P}(C_n) = \mathbb{P}(A^c) \implies \lim_{n\to\infty} (1 - \mathbb{P}(A_n)) = 1 - \mathbb{P}(A) \implies \lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$$
   $\blacksquare$

### Условная вероятность и независимость
**Условная вероятность** события $A$ при условии $B$ ($\mathbb{P}(B) > 0$):
$$\mathbb{P}(A \mid B) = \frac{\mathbb{P}(AB)}{\mathbb{P}(B)}$$

**Независимость событий:**
1. События $A$ и $B$ независимы, если $\mathbb{P}(AB) = \mathbb{P}(A)\mathbb{P}(B)$.
2. Семейство $\{A_i\}_{i \in I}$ независимо в совокупности, если для любого конечного подмножества $\{i_1, \dots, i_k\} \subset I$:
   $$\mathbb{P}\left(\bigcap_{j=1}^{k} A_{i_j}\right) = \prod_{j=1}^{k} \mathbb{P}(A_{i_j})$$

**Пример Бернштейна (попарная независимость без независимости в совокупности):**
Тетраэдр с гранями: К, З, С, КЗС. $\Omega = \{\text{К}, \text{З}, \text{С}, \text{КЗС}\}$, $\mathbb{P}(\omega) = 1/4$.
События: $A_1 = \{\text{К}, \text{КЗС}\}$, $A_2 = \{\text{З}, \text{КЗС}\}$, $A_3 = \{\text{С}, \text{КЗС}\}$.
$\mathbb{P}(A_1) = \mathbb{P}(A_2) = \mathbb{P}(A_3) = 1/2$.
$A_i \cap A_j = \{\text{КЗС}\} \implies \mathbb{P}(A_i A_j) = 1/4 = \mathbb{P}(A_i)\mathbb{P}(A_j)$ (попарно независимы).
$A_1 \cap A_2 \cap A_3 = \{\text{КЗС}\} \implies \mathbb{P}(A_1 A_2 A_3) = 1/4 \neq \mathbb{P}(A_1)\mathbb{P}(A_2)\mathbb{P}(A_3) = 1/8$ (зависимы в совокупности).

### Полная вероятность и байесовский подход
Для полной группы событий $\{H_i\}_{i=1}^{\infty}$ ($\sum_{i=1}^{\infty} H_i = \Omega$, $\mathbb{P}(H_i) > 0$):
**Формула полной вероятности:**
$$\mathbb{P}(A) = \sum_{i=1}^{\infty} \mathbb{P}(A \mid H_i)\mathbb{P}(H_i)$$

**Формула Байеса** ($\mathbb{P}(A) > 0$):
$$\mathbb{P}(H_k \mid A) = \frac{\mathbb{P}(A \mid H_k)\mathbb{P}(H_k)}{\sum_{i=1}^{\infty} \mathbb{P}(A \mid H_i)\mathbb{P}(H_i)}$$

**Доказательство:**
$$A = A \cap \left(\sum_{i=1}^{\infty} H_i\right) = \sum_{i=1}^{\infty} (A \cap H_i) \implies \mathbb{P}(A) = \sum_{i=1}^{\infty} \mathbb{P}(A \cap H_i) = \sum_{i=1}^{\infty} \mathbb{P}(A \mid H_i)\mathbb{P}(H_i)$$
$$\mathbb{P}(H_k \mid A) = \frac{\mathbb{P}(H_k \cap A)}{\mathbb{P}(A)} = \frac{\mathbb{P}(A \mid H_k)\mathbb{P}(H_k)}{\mathbb{P}(A)}$$
$\blacksquare$

---

## 1.2. Одномерные случайные величины и их законы

### Понятие случайной величины
**Случайная величина** $X$ на $(\Omega, \mathcal{F}, \mathbb{P})$ — измеримая функция $X: (\Omega, \mathcal{F}) \to (\mathbb{R}, \mathcal{B}(\mathbb{R}))$, то есть:
$$X^{-1}(B) \in \mathcal{F}, \quad \forall B \in \mathcal{B}(\mathbb{R})$$
Индуцированное распределение вероятностей на $(\mathbb{R}, \mathcal{B}(\mathbb{R}))$:
$$\mathbb{P}_X(B) = \mathbb{P}(X^{-1}(B)), \quad B \in \mathcal{B}(\mathbb{R})$$

### Функция распределения
**Функция распределения** $F_X(x) = \mathbb{P}(X < x)$.
Свойства:
1. Монотонность: $x_1 < x_2 \implies F_X(x_1) \le F_X(x_2)$.
2. Непрерывность слева: $\lim_{x \to x_0 - 0} F_X(x) = F_X(x_0)$.
3. Асимптотика: $\lim_{x \to -\infty} F_X(x) = 0$, $\lim_{x \to +\infty} F_X(x) = 1$.

**Доказательство свойств:**
1. Пусть $x_1 < x_2$. $\{X < x_1\} \subset \{X < x_2\} \implies \mathbb{P}(X < x_1) \le \mathbb{P}(X < x_2)$.
2. Пусть $x_n \uparrow x_0$. $A_n = \{X < x_n\} \uparrow A = \{X < x_0\}$. По непрерывности меры $\lim F_X(x_n) = \mathbb{P}(A) = F_X(x_0)$.
3. При $x_n \downarrow -\infty$, $\{X < x_n\} \downarrow \emptyset \implies \lim F_X(x_n) = 0$. При $x_n \uparrow +\infty$, $\{X < x_n\} \uparrow \Omega \implies \lim F_X(x_n) = 1$.
   $\blacksquare$

### Типы распределений
1. **Дискретное:** $\sum_k \mathbb{P}(X=x_k) = 1$, $F_X(x) = \sum_{k: x_k < x} \mathbb{P}(X=x_k)$.
2. **Абсолютно непрерывное:** $F_X(x) = \int_{-\infty}^{x} p_X(t) \, dt$, где $p_X(t) \ge 0$, $\int_{-\infty}^{\infty} p_X(t) \, dt = 1$.
3. **Сингулярное:** $F_X(x)$ непрерывна, но точки ее роста имеют лебегову меру ноль.
**Теорема Лебега о разложении:** $F(x) = c_d F_d(x) + c_{ac} F_{ac}(x) + c_s F_s(x)$, где $c_d, c_{ac}, c_s \ge 0, c_d+c_{ac}+c_s=1$.

### Предельные теоремы в схемах Бернулли
**Теорема Пуассона:** Если $n p_n \to \lambda > 0$ при $n \to \infty$, то для любого $k \in \{0, 1, 2, \dots\}$:
$$\lim_{n\to\infty} C_n^k p_n^k (1 - p_n)^{n-k} = \frac{\lambda^k e^{-\lambda}}{k!}$$
**Доказательство:**
Обозначим $\lambda_n = n p_n \to \lambda$.
$$P_n(k) = \frac{n(n-1)\dots(n-k+1)}{n^k} \frac{\lambda_n^k}{k!} \left(1 - \frac{\lambda_n}{n}\right)^n \left(1 - \frac{\lambda_n}{n}\right)^{-k}$$
При $n \to \infty$: $\frac{n(n-1)\dots(n-k+1)}{n^k} \to 1$, $\lambda_n^k \to \lambda^k$, $\left(1 - \frac{\lambda_n}{n}\right)^n \to e^{-\lambda}$, $\left(1 - \frac{\lambda_n}{n}\right)^{-k} \to 1$.
Отсюда $\lim_{n\to\infty} P_n(k) = \frac{\lambda^k e^{-\lambda}}{k!}$. $\blacksquare$

**Теорема Реньи:** Если $X_p \sim \operatorname{Geom}(p)$, то $Y_p = p X_p \xrightarrow{d} \operatorname{Exp}(1)$ при $p \to 0$.
**Доказательство:**
Для $y > 0$:
$$F_{Y_p}(y) = 1 - \mathbb{P}\left(X_p \ge \left\lceil \frac{y}{p} \right\rceil\right) = 1 - (1 - p)^{\left\lceil \frac{y}{p} \right\rceil}$$
При $p \to 0$, $\ln(1-p)^{\left\lceil y/p \right\rceil} \approx \frac{y}{p}(-p) = -y \implies \lim_{p\to 0} F_{Y_p}(y) = 1 - e^{-y}$. $\blacksquare$

**Геометрическое распределение:** $\mathbb{P}(X=k) = p q^{k-1}, k \ge 1$.
Свойство отсутствия последействия: $\mathbb{P}(X \ge n+m \mid X \ge n) = \mathbb{P}(X \ge m)$.
**Показательное распределение:** $p(x) = \lambda e^{-\lambda x} \mathbb{I}(x \ge 0)$.
Свойство отсутствия последействия: $\mathbb{P}(X \ge t+s \mid X \ge t) = \mathbb{P}(X \ge s)$.

---

## 1.3. Числовые характеристики и многомерные случайные величины

### Математическое ожидание
**Математическое ожидание** — интеграл Лебега по вероятностной мере $\mathbb{P}$:
$$\mathbb{E}[X] = \int_{\Omega} X(\omega) \, d\mathbb{P}(\omega)$$
Свойства:
1. $\mathbb{E}[aX+bY] = a\mathbb{E}[X] + b\mathbb{E}[Y]$.
2. $X \le Y$ п.н. $\implies \mathbb{E}[X] \le \mathbb{E}[Y]$.
3. Вычисление: $\mathbb{E}[g(X)] = \int_{\mathbb{R}} g(x) \, dF_X(x)$.

### Дисперсия и моменты
**Дисперсия:** $\mathbb{D}[X] = \mathbb{E}[(X - \mathbb{E}[X])^2]$.
**Медиана** $m$ определяется как: $\mathbb{P}(X < m) \le 1/2 \le \mathbb{P}(X \le m)$.
**Теорема:** $\mathbb{E}[|X-c|]$ минимально при $c = m$.
**Доказательство:**
Пусть $c > m$.
$$|x-c| - |x-m| \ge (c-m)\mathbb{I}(x \le m) - (c-m)\mathbb{I}(x > m)$$
$$\mathbb{E}[|X-c|] - \mathbb{E}[|X-m|] \ge (c-m)[\mathbb{P}(X \le m) - \mathbb{P}(X > m)] = (c-m)[2\mathbb{P}(X \le m) - 1] \ge 0$$
$\blacksquare$

### Многомерные случайные величины и свертка
$F_{\mathbf{X}}(x_1, \dots, x_d) = \mathbb{P}(X_1 < x_1, \dots, X_d < x_d)$.
Независимость: $F_{\mathbf{X}}(x_1, \dots, x_d) = \prod_{i=1}^d F_{X_i}(x_i)$.
**Плотность суммы независимых величин $Z = X+Y$ (свертка):**
$$p_Z(z) = \int_{-\infty}^{\infty} p_X(x) p_Y(z - x) \, dx$$
**Доказательство:**
$$F_Z(z) = \iint_{x+y < z} p_X(x) p_Y(y) \, dx \, dy = \int_{-\infty}^{z} \left( \int_{-\infty}^{\infty} p_X(x) p_Y(u - x) \, dx \right) \, du \implies p_Z(z) = F'_Z(z)$$
$\blacksquare$

### Ковариация и коэффициент корреляции
$$\operatorname{Cov}(X, Y) = \mathbb{E}[(X - \mathbb{E}[X])(Y - \mathbb{E}[Y])], \quad \rho(X, Y) = \frac{\operatorname{Cov}(X, Y)}{\sqrt{\mathbb{D}[X]\mathbb{D}[Y]}}$$
**Свойства $\rho(X, Y)$:**
1. $|\rho(X, Y)| \le 1$.
2. $|\rho(X, Y)| = 1 \iff Y = aX + b$ п.н. ($a \neq 0$).
**Доказательство:**
Пусть $U = X - \mathbb{E}[X]$, $V = Y - \mathbb{E}[Y]$. Для любого $t \in \mathbb{R}$:
$$\mathbb{E}[(tU+V)^2] = t^2 \mathbb{D}[X] + 2t \operatorname{Cov}(X, Y) + \mathbb{D}[Y] \ge 0 \implies D/4 = (\operatorname{Cov}(X, Y))^2 - \mathbb{D}[X]\mathbb{D}[Y] \le 0 \implies |\rho| \le 1$$
Если $|\rho| = 1$, то $D = 0 \implies \mathbb{E}[(t_0 U + V)^2] = 0 \implies t_0 U + V = 0$ п.н. $\implies Y = aX + b$ п.н. $\blacksquare$

### Условное математическое ожидание
**Условное математическое ожидание** $\mathbb{E}[X \mid \mathcal{G}]$ относительно $\mathcal{G} \subset \mathcal{F}$ — $\mathcal{G}$-измеримая случайная величина, удовлетворяющая:
$$\int_{G} \mathbb{E}[X \mid \mathcal{G}] \, d\mathbb{P} = \int_{G} X \, d\mathbb{P}, \quad \forall G \in \mathcal{G}$$
Свойства:
1. $\mathbb{E}[\mathbb{E}[X \mid \mathcal{G}]] = \mathbb{E}[X]$.
2. $\mathbb{E}[YX \mid \mathcal{G}] = Y \mathbb{E}[X \mid \mathcal{G}]$ п.н. при $\mathcal{G}$-измеримой $Y$.
3. $\mathbb{E}[\mathbb{E}[X \mid \mathcal{G}_2] \mid \mathcal{G}_1] = \mathbb{E}[X \mid \mathcal{G}_1]$ п.н. при $\mathcal{G}_1 \subset \mathcal{G}_2$.
