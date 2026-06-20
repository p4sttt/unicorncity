---
title: "Раздел 3. Математическая статистика"
description: "Выборочный метод, точечное оценивание, оптимальность оценок, доверительные интервалы и критерии проверки гипотез"
date: 2026-06-20
status: done
---

# Раздел 3. Математическая статистика

## 3.1. Первичные понятия и выборочные характеристики

### Выборка и статистика
**Статистическая структура** — тройка $(\mathcal{X}, \mathcal{B}, \mathcal{P})$, где $\mathcal{X} \subset \mathbb{R}^n$ — выборочное пространство, $\mathcal{B}$ — борелевская $\sigma$-алгебра, $\mathcal{P} = \{\mathbb{P}_{\theta} : \theta \in \Theta\}$ — семейство распределений.
**Выборка** — случайный вектор $\mathbf{X} = (X_1, \dots, X_n)^T$, где $X_i$ независимы и распределены как $\mathbb{P}_{\theta_0}$.
**Статистика** $T(\mathbf{X})$ — борелевская функция от выборки, не зависящая от $\theta$.

### Вариационный ряд и эмпирическая функция распределения
**Вариационный ряд:** $X_{(1)} \le X_{(2)} \le \dots \le X_{(n)}$, где $X_{(k)}$ — $k$-я порядковая статистика.
**Эмпирическая функция распределения:**
$$F_n(x) = \frac{1}{n} \sum_{i=1}^{n} \mathbb{I}(X_i < x)$$
Свойства: $\mathbb{E}[F_n(x)] = F(x)$, $\mathbb{D}[F_n(x)] = \frac{F(x)(1-F(x))}{n}$.
**Теорема Гливенко–Кантелли:**
$$\mathbb{P}\left(\lim_{n\to\infty} \sup_{x \in \mathbb{R}} |F_n(x) - F(x)| = 0\right) = 1$$

### Выборочные моменты
Выборочное среднее $\bar{X} = \frac{1}{n} \sum_{i=1}^{n} X_i$.
Выборочная дисперсия $S^2 = \frac{1}{n} \sum_{i=1}^{n} (X_i - \bar{X})^2$.
Исправленная выборочная дисперсия $S_0^2 = \frac{1}{n-1} \sum_{i=1}^{n} (X_i - \bar{X})^2$.

**Вывод смещения выборочной дисперсии:**
Обозначим $\mu = \mathbb{E}[X_1]$ и $\sigma^2 = \mathbb{D}[X_1]$.
$$S^2 = \frac{1}{n} \sum_{i=1}^{n} X_i^2 - \bar{X}^2$$
$$\mathbb{E}[X_i^2] = \sigma^2 + \mu^2, \quad \mathbb{E}[\bar{X}^2] = \frac{\sigma^2}{n} + \mu^2$$
$$\mathbb{E}[S^2] = \sigma^2 + \mu^2 - \frac{\sigma^2}{n} - \mu^2 = \frac{n-1}{n} \sigma^2 \implies \mathbb{E}[S_0^2] = \frac{n}{n-1} \mathbb{E}[S^2] = \sigma^2$$
$\blacksquare$

---

## 3.2. Точечное оценивание и оптимальность

### Свойства точечных оценок
1. Несмещенность: $\mathbb{E}_{\theta}[\hat{\theta}_n] = \theta, \quad \forall \theta \in \Theta$.
2. Состоятельность: $\hat{\theta}_n \xrightarrow[n\to\infty]{\mathbb{P}} \theta, \quad \forall \theta \in \Theta$.
3. Оптимальность: UMVUE (ОНУО) $\hat{\theta}_n$ — несмещенная оценка с минимальной дисперсией.

**Теорема о единственности ОНУО:**
Пусть $\hat{\theta}_1$ и $\hat{\theta}_2$ — две ОНУО с дисперсией $d(\theta)$. Пусть $\hat{\theta}^* = \frac{\hat{\theta}_1 + \hat{\theta}_2}{2}$. Она несмещена.
$$\mathbb{D}_{\theta}[\hat{\theta}^*] = \frac{1}{4}\mathbb{D}_{\theta}[\hat{\theta}_1] + \frac{1}{4}\mathbb{D}_{\theta}[\hat{\theta}_2] + \frac{1}{2}\operatorname{Cov}_{\theta}(\hat{\theta}_1, \hat{\theta}_2) \le d(\theta)$$
В силу минимальности дисперсии $\mathbb{D}_{\theta}[\hat{\theta}^*] = d(\theta) \implies \operatorname{Cov}_{\theta}(\hat{\theta}_1, \hat{\theta}_2) = d(\theta) \implies \rho(\hat{\theta}_1, \hat{\theta}_2) = 1 \implies \hat{\theta}_1 = \hat{\theta}_2$ п.н. $\blacksquare$

### Достаточность
**Достаточная статистика:** статистика $T(\mathbf{X})$ такая, что условное распределение выборки при условии $T(\mathbf{X}) = t$ не зависит от $\theta$.
**Теорема факторизации Неймана–Пирсона:**
$T(\mathbf{X})$ достаточна $\iff L(\mathbf{x}; \theta) = g(T(\mathbf{x}); \theta) h(\mathbf{x})$.
**Доказательство (дискретный случай):**
1. Необходимость: $\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x}) = \mathbb{P}_{\theta}(T(\mathbf{X}) = T(\mathbf{x})) \mathbb{P}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = T(\mathbf{x}))$. Обозначим первый множитель $g(T(\mathbf{x}); \theta)$, второй — $h(\mathbf{x})$ (не зависит от $\theta$).
2. Достаточность: При $T(\mathbf{x}) = t$:
   $$\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = t) = \frac{g(t; \theta) h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} g(T(\mathbf{y}); \theta) h(\mathbf{y})} = \frac{h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} h(\mathbf{y})}$$
   выражение не зависит от $\theta$. $\blacksquare$

**Полная статистика:** статистика $T(\mathbf{X})$ такая, что для любой борелевской $g$:
$$\mathbb{E}_{\theta}[g(T)] = 0, \, \forall \theta \implies g(T) = 0 \text{ п.н.}$$

### Теория оптимальных оценок
**Неравенство Рао–Крамера:** В регулярном эксперименте для оценки $\hat{\theta}$ параметра $\tau(\theta)$ со смещением $b(\theta)$:
$$\mathbb{D}_{\theta}[\hat{\theta}] \ge \frac{(\tau'(\theta) + b'(\theta))^2}{I_n(\theta)}$$
где $I_n(\theta) = \mathbb{E}_{\theta}\left[\left( \frac{\partial \ln L(\mathbf{X}; \theta)}{\partial \theta} \right)^2\right]$.
**Доказательство:**
Пусть $U(\mathbf{X}; \theta) = \frac{\partial \ln L(\mathbf{X}; \theta)}{\partial \theta}$. Из нормировки плотности $\mathbb{E}_{\theta}[U] = 0 \implies \mathbb{D}_{\theta}[U] = I_n(\theta)$.
Дифференцируя $\mathbb{E}_{\theta}[\hat{\theta}] = \tau(\theta) + b(\theta)$:
$$\int \hat{\theta}(\mathbf{x}) \frac{\partial \ln L}{\partial \theta} L \, d\mathbf{x} = \tau'(\theta) + b'(\theta) \implies \mathbb{E}_{\theta}[\hat{\theta} U] = \tau'(\theta) + b'(\theta) \implies \operatorname{Cov}_{\theta}(\hat{\theta}, U) = \tau'(\theta) + b'(\theta)$$
По неравенству Коши-Буняковского:
$$(\operatorname{Cov}_{\theta}(\hat{\theta}, U))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] \mathbb{D}_{\theta}[U] \implies (\tau'(\theta) + b'(\theta))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] I_n(\theta)$$
$\blacksquare$

**Теорема Рао–Блекуэлла–Колмогорова:**
Если $\hat{\theta}$ — несмещенная оценка $\theta$ с конечной дисперсией, а $T$ — достаточная статистика, то $\hat{\theta}^* = \mathbb{E}[\hat{\theta} \mid T]$ является статистикой, несмещена, и $\mathbb{D}_{\theta}[\hat{\theta}^*] \le \mathbb{D}_{\theta}[\hat{\theta}]$.
**Доказательство:**
$\hat{\theta}^*$ не содержит $\theta$ по достаточности $T$.
$\mathbb{E}_{\theta}[\hat{\theta}^*] = \mathbb{E}_{\theta}[\mathbb{E}[\hat{\theta} \mid T]] = \mathbb{E}_{\theta}[\hat{\theta}] = \theta$.
По закону полной дисперсии:
$$\mathbb{D}_{\theta}[\hat{\theta}] = \mathbb{E}_{\theta}[\mathbb{D}[\hat{\theta} \mid T]] + \mathbb{D}_{\theta}[\hat{\theta}^*] \ge \mathbb{D}_{\theta}[\hat{\theta}^*]$$
$\blacksquare$

**Теорема Лемана–Шеффе:** Если достаточная статистика $T$ является полной, а $\hat{\theta} = g(T)$ — несмещенная оценка для $\theta$, то она является единственной ОНУО.

---

## 3.3. Методы построения оценок и доверительные интервалы

### Метод моментов (ММ)
Оценки находятся приравниванием теоретических моментов к выборочным:
$$\alpha_r(\theta_1, \dots, \theta_k) = \frac{1}{n} \sum_{i=1}^{n} X_i^r, \quad r = 1, \dots, k$$

### Метод максимального правдоподобия (ММП)
Оценка максимального правдоподобия (ОМП):
$$\hat{\theta}_{ML} = \arg\max_{\theta \in \Theta} L(\mathbf{X}; \theta) \implies \frac{\partial \ln L(\mathbf{X}; \theta)}{\partial \theta} = 0$$
Свойства ОМП: состоятельность, асимптотическая нормальность $\sqrt{n}(\hat{\theta}_{ML} - \theta) \xrightarrow{d} \mathcal{N}(0, I_1^{-1}(\theta))$, асимптотическая эффективность.

### Доверительные интервалы: метод центральной статистики
1. Найти $G(\mathbf{X}; \theta)$, распределение которой известно и не зависит от $\theta$.
2. Выбрать квантили $g_1, g_2$ такие, чтобы $\mathbb{P}_{\theta}(g_1 < G(\mathbf{X}; \theta) < g_2) = 1 - \alpha$.
3. Разрешить неравенство относительно $\theta$: $\mathbb{P}_{\theta}(\underline{\theta}(\mathbf{X}) < \theta < \bar{\theta}(\mathbf{X})) = 1 - \alpha$.

---

## 3.4. Проверка гипотез и нормальные выборки

### Лемма Неймана–Пирсона
Для проверки простых гипотез наиболее мощная область имеет вид $W = \{\mathbf{x} : L_1(\mathbf{x}) > c L_0(\mathbf{x})\}$, где $\mathbb{P}_{\theta_0}(W) = \alpha$.
**Доказательство:**
Пусть $W'$ — любая другая область с $\mathbb{P}_{\theta_0}(W') \le \alpha$.
Для любого $\mathbf{x}$: $(\mathbb{I}_W(\mathbf{x}) - \mathbb{I}_{W'}(\mathbf{x})) (L_1(\mathbf{x}) - c L_0(\mathbf{x})) \ge 0$.
Интегрируя по выборочному пространству:
$$\int (\mathbb{I}_W - \mathbb{I}_{W'}) (L_1 - c L_0) \, d\mathbf{x} \ge 0 \implies \mathbb{P}_{\theta_1}(W) - \mathbb{P}_{\theta_1}(W') - c(\mathbb{P}_{\theta_0}(W) - \mathbb{P}_{\theta_0}(W')) \ge 0$$
$$\implies \beta - \beta' \ge c(\alpha - \alpha') \ge 0 \implies \beta \ge \beta'$$
$\blacksquare$

### Точные распределения и теорема Фишера для нормальных выборок
Пусть $X_i \sim \mathcal{N}(a, \sigma^2)$ независимы.
**Теорема Фишера:**
1. Выборочное среднее $\bar{X}$ и исправленная выборочная дисперсия $S_0^2$ независимы.
2. $\frac{(n-1)S_0^2}{\sigma^2} \sim \chi^2(n-1)$.
**Доказательство:**
Пусть $a=0, \sigma^2=1$. Сделаем ортогональное преобразование $\mathbf{Y} = C\mathbf{X}$, где первая строка матрицы $C$ равна $(1/\sqrt{n}, \dots, 1/\sqrt{n})$.
Так как преобразование ортогонально, $Y_i \sim \mathcal{N}(0, 1)$ независимы.
$$Y_1 = \sqrt{n}\bar{X} \implies Y_1^2 = n\bar{X}^2$$
$$\sum_{i=1}^{n} X_i^2 = \sum_{i=1}^{n} Y_i^2 \implies \sum_{i=2}^{n} Y_i^2 = \sum_{i=1}^{n} X_i^2 - n\bar{X}^2 = (n-1)S_0^2$$
Поскольку $\bar{X} = Y_1/\sqrt{n}$, а $S_0^2 = \frac{1}{n-1} \sum_{i=2}^n Y_i^2$, они независимы.
Величина $(n-1)S_0^2 = \sum_{i=2}^n Y_i^2$ есть сумма квадратов $n-1$ независимых стандартных нормальных величин, следовательно, $(n-1)S_0^2 \sim \chi^2(n-1)$. $\blacksquare$

### Статистические выводы в нормальных выборках
- Доверительный интервал для математического ожидания $a$ при неизвестной $\sigma^2$ строится по статистике Стьюдента:
  $$T = \frac{\bar{X} - a}{S_0/\sqrt{n}} \sim t(n-1)$$
- Доверительный интервал для дисперсии $\sigma^2$ строится по статистике хи-квадрат:
  $$\frac{(n-1)S_0^2}{\sigma^2} \sim \chi^2(n-1)$$
- Сравнение дисперсий двух выборок проводится по статистике Фишера:
  $$F = \frac{S_{0X}^2}{S_{0Y}^2} \sim F(n_X-1, n_Y-1)$$
