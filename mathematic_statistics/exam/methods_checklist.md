---
title: "Чеклист по методам решения задач"
description: "Алгоритмы решения типовых задач по математической статистике с подробными разборами примеров из учебника и задачника Г. И. Ивченко и Ю. И. Медведева"
state: done
date: 2026-06-20
---

# Чеклист по методам решения задач

## 1. Метод 1: Нахождение распределения порядковых статистик

### Алгоритм
1. **Максимум $X_{(n)}$:**
   $$F_{X_{(n)}}(x) = (F(x))^n \implies p_{X_{(n)}}(x) = n (F(x))^{n-1} p(x)$$
2. **Минимум $X_{(1)}$:**
   $$F_{X_{(1)}}(x) = 1 - (1 - F(x))^n \implies p_{X_{(1)}}(x) = n (1 - F(x))^{n-1} p(x)$$

### Пример разбора
Пусть $X_1, \dots, X_n \sim \operatorname{Exp}(\theta)$ независимы: $p(x) = \theta e^{-\theta x}\mathbb{I}(x \ge 0), F(x) = (1 - e^{-\theta x})\mathbb{I}(x \ge 0)$. Найти плотность распределения $X_{(1)}$ и $\mathbb{E}[X_{(1)}]$.

**Решение:**
1. Для $x \ge 0$:
   $$p_{X_{(1)}}(x) = n (1 - F(x))^{n-1} p(x) = n \left(e^{-\theta x}\right)^{n-1} \left(\theta e^{-\theta x}\right) = n \theta e^{-n \theta x}$$
   Для $x < 0$: $p_{X_{(1)}}(x) = 0$.
2. Следовательно, $X_{(1)} \sim \operatorname{Exp}(n\theta)$.
3. $\mathbb{E}[X_{(1)}] = \frac{1}{n\theta}$.
$\blacksquare$

---

## 2. Метод 2: Нахождение ОМП и оценка её эффективности

### Алгоритм
1. Составить функцию правдоподобия $L(\mathbf{X}; \theta) = \prod_{i=1}^{n} p(X_i; \theta)$.
2. Записать уравнение правдоподобия $\frac{\partial \ln L}{\partial \theta} = 0$, найти корень $\hat{\theta}_{ML}$.
3. Проверить знак второй производной $\frac{\partial^2 \ln L}{\partial \theta^2} < 0$.
4. Найти $\mathbb{E}_{\theta}[\hat{\theta}_{ML}]$. При наличии смещения исправить оценку до несмещенной $\hat{\theta}^*$.
5. Вычислить информацию Фишера $I_n( \theta) = -n \mathbb{E}_{\theta}\left[\frac{\partial^2 \ln p(X_1; \theta)}{\partial \theta^2}\right]$.
6. Сравнить $\mathbb{D}_{\theta}[\hat{\theta}^*]$ с границей Рао-Крамера $\frac{1}{I_n(\theta)}$.

### Пример разбора
Пусть $X_1, \dots, X_n \sim \operatorname{Exp}(\theta)$ независимы. Найти ОМП для $\theta$ и проверить эффективность её несмещенной модификации.

**Решение:**
1. $\ln L(\mathbf{X}; \theta) = n \ln \theta - \theta \sum_{i=1}^{n} X_i$.
2. $\frac{\partial \ln L}{\partial \theta} = \frac{n}{\theta} - \sum_{i=1}^{n} X_i = 0 \implies \hat{\theta}_{ML} = \frac{n}{\sum_{i=1}^{n} X_i} = \frac{1}{\bar{X}}$.
3. $\frac{\partial^2 \ln L}{\partial \theta^2} = -\frac{n}{\theta^2} < 0$.
4. Обозначим $S_n = \sum_{i=1}^{n} X_i \sim \operatorname{Gamma}(n, \theta)$ с плотностью $p_{S_n}(s) = \frac{\theta^n}{(n-1)!} s^{n-1} e^{-\theta s}$.
   $$\mathbb{E}_{\theta}[\hat{\theta}_{ML}] = n \mathbb{E}_{\theta}\left[\frac{1}{S_n}\right] = n \int_{0}^{\infty} \frac{1}{s} \frac{\theta^n}{(n-1)!} s^{n-1} e^{-\theta s} \, ds = \frac{n}{n-1}\theta$$
   Исправленная несмещенная оценка: $\hat{\theta}^* = \frac{n-1}{\sum_{i=1}^{n} X_i}$.
5. Информация Фишера: $\ln p(X_1; \theta) = \ln \theta - \theta X_1 \implies \frac{\partial^2 \ln p}{\partial \theta^2} = -\frac{1}{\theta^2} \implies I_n(\theta) = \frac{n}{\theta^2}$.
   Нижняя граница Рао-Крамера: $\frac{1}{I_n(\theta)} = \frac{\theta^2}{n}$.
6. Дисперсия $\hat{\theta}^*$:
   $$\mathbb{E}_{\theta}[(\hat{\theta}^*)^2] = (n-1)^2 \int_{0}^{\infty} \frac{1}{s^2} \frac{\theta^n}{(n-1)!} s^{n-1} e^{-\theta s} \, ds = \frac{(n-1)\theta^2}{n-2} \implies \mathbb{D}_{\theta}[\hat{\theta}^*] = \frac{\theta^2}{n-2}$$
   Поскольку $\mathbb{D}_{\theta}[\hat{\theta}^*] = \frac{\theta^2}{n-2} > \frac{\theta^2}{n}$, оценка не является эффективной при конечных $n$. Асимптотически эффективна: $\lim_{n\to\infty} \frac{\mathbb{D}_{\theta}[\hat{\theta}^*]}{\theta^2/n} = 1$.
$\blacksquare$

---

## 3. Метод 3: Построение оптимальной несмещенной оценки (ОНУО)

### Алгоритм
1. Представить $L(\mathbf{x}; \theta) = g(T(\mathbf{x}); \theta) h(\mathbf{x})$, чтобы найти достаточную статистику $T$.
2. Проверить $T$ на полноту: $\mathbb{E}_{\theta}[g(T)] = 0 \implies g(T) = 0$ п.н.
3. Найти $h(T)$ такую, что $\mathbb{E}_{\theta}[h(T)] = \theta$.
4. По теореме Лемана-Шеффе, $\hat{\theta}^* = h(T)$ — единственная ОНУО.

### Пример разбора
Пусть $X_1, \dots, X_n \sim \operatorname{U}([0, \theta])$ независимы. Найти ОНУО для $\theta$.

**Решение:**
1. Совместная плотность:
   $$L(\mathbf{x}; \theta) = \frac{1}{\theta^n} \mathbb{I}(\max(x_1, \dots, x_n) \le \theta) \mathbb{I}(\min(x_1, \dots, x_n) \ge 0)$$
   Достаточная статистика: $T = X_{(n)} = \max(X_1, \dots, X_n)$.
2. Полнота: плотность $T$ есть $p_T(t) = \frac{n t^{n-1}}{\theta^n}\mathbb{I}(0 \le t \le \theta)$.
   $$\mathbb{E}_{\theta}[g(T)] = \int_{0}^{\theta} g(t) \frac{n t^{n-1}}{\theta^n} \, dt = 0 \quad \forall \theta > 0 \implies \int_{0}^{\theta} g(t) t^{n-1} \, dt = 0 \quad \forall \theta > 0$$
   Дифференцируя по $\theta$: $g(\theta) \theta^{n-1} = 0 \implies g(\theta) = 0$ п.н. Статистика $T$ полна.
3. Несмещенность:
   $$\mathbb{E}_{\theta}[T] = \int_{0}^{\theta} t \frac{n t^{n-1}}{\theta^n} \, dt = \frac{n}{n+1}\theta \implies \mathbb{E}_{\theta}\left[\frac{n+1}{n} T\right] = \theta$$
4. ОНУО: $\hat{\theta}^* = \frac{n+1}{n} X_{(n)}$.
$\blacksquare$

---

## 4. Метод 4: Построение точного доверительного интервала (pivot-метод)

### Алгоритм
1. Выбрать центральную статистику $G(\mathbf{X}; \theta)$, распределение которой известно и не зависит от $\theta$.
2. Выбрать квантили $g_{\alpha/2}, g_{1-\alpha/2}$ такие, чтобы $\mathbb{P}_{\theta}(g_{\alpha/2} < G < g_{1-\alpha/2}) = 1 - \alpha$.
3. Разрешить неравенство относительно $\theta$: $\mathbb{P}_{\theta}(\underline{\theta} < \theta < \bar{\theta}) = 1 - \alpha$.

### Пример разбора
Пусть $X_1, \dots, X_n \sim \mathcal{N}(a, \sigma^2)$ с неизвестными $a, \sigma^2$. Построить доверительный интервал для $a$ уровня доверия $1-\alpha$.

**Решение:**
1. Статистика: $G(a) = \frac{\bar{X} - a}{S_0 / \sqrt{n}} \sim t(n-1)$.
2. Квантили: $\mathbb{P}\left( -t_{1-\alpha/2}(n-1) < \frac{\bar{X} - a}{S_0 / \sqrt{n}} < t_{1-\alpha/2}(n-1) \right) = 1 - \alpha$.
3. Преобразование:
   $$-t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}} < \bar{X} - a < t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}}$$
   $$\iff \bar{X} - t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}} < a < \bar{X} + t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}}$$
   Доверительный интервал: $\left[ \bar{X} - t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}}, \quad \bar{X} + t_{1-\alpha/2}(n-1) \frac{S_0}{\sqrt{n}} \right]$.
$\blacksquare$

---

## 5. Метод 5: Построение наиболее мощного критерия (Нейман-Пирсон)

### Алгоритм
1. Составить отношение правдоподобия $\Lambda(\mathbf{x}) = \frac{L_1(\mathbf{x})}{L_0(\mathbf{x})}$.
2. Записать критическую область: $\Lambda(\mathbf{x}) > c$.
3. Свести неравенство к виду $T(\mathbf{x}) > C$ (или $T(\mathbf{x}) < C$).
4. Найти константу $C$ из условия ошибки первого рода: $\mathbb{P}_{H_0}(T(\mathbf{X}) > C) = \alpha$.
5. Вычислить мощность критерия: $\beta = \mathbb{P}_{H_1}(T(\mathbf{X}) > C)$.

### Пример разбора
Пусть $X_1, \dots, X_n \sim \mathcal{N}(\mu, 1)$ независимы. Построить наиболее мощный критерий уровня значимости $\alpha$ для проверки $H_0: \mu = 0$ против $H_1: \mu = 1$, и вычислить его мощность.

**Решение:**
1. Отношение правдоподобия:
   $$\Lambda(\mathbf{x}) = \frac{(2\pi)^{-n/2} \exp\left(-\frac{1}{2}\sum (x_i - 1)^2\right)}{(2\pi)^{-n/2} \exp\left(-\frac{1}{2}\sum x_i^2\right)} = \exp\left( \sum_{i=1}^{n} x_i - \frac{n}{2} \right)$$
2. Неравенство $\Lambda(\mathbf{x}) > c \iff \bar{X} > C$.
3. Под гипотезой $H_0: \bar{X} \sim \mathcal{N}(0, 1/n) \implies \sqrt{n}\bar{X} \sim \mathcal{N}(0, 1)$.
   $$\mathbb{P}_{H_0}(\bar{X} > C) = 1 - \Phi(\sqrt{n}C) = \alpha \implies C = \frac{z_{1-\alpha}}{\sqrt{n}}$$
   Критическая область: $W = \left\{\mathbf{x} : \bar{X} > \frac{z_{1-\alpha}}{\sqrt{n}}\right\}$.
4. При $H_1: \bar{X} \sim \mathcal{N}(1, 1/n) \implies \sqrt{n}(\bar{X}-1) \sim \mathcal{N}(0, 1)$.
   $$\beta = \mathbb{P}_{H_1}\left(\bar{X} > \frac{z_{1-\alpha}}{\sqrt{n}}\right) = \mathbb{P}_{H_1}\left(\sqrt{n}(\bar{X}-1) > z_{1-\alpha} - \sqrt{n}\right) = 1 - \Phi(z_{1-\alpha} - \sqrt{n}) = \Phi\left(\sqrt{n} - z_{1-\alpha}\right)$$
$\blacksquare$
