---
title: "Чеклист теорем с доказательствами"
description: "Полный перечень ключевых теорем курсов теории вероятностей и математической статистики со строгими выводами"
state: done
date: 2026-06-20
---

# Чеклист теорем по теории вероятностей и математической статистике

## 1. Теория вероятностей

### Теорема о непрерывности вероятностной меры
1. Если $A_n \uparrow A$ ($A_1 \subset A_2 \subset \dots$ и $A = \bigcup_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.
2. Если $A_n \downarrow A$ ($A_1 \supset A_2 \supset \dots$ и $A = \bigcap_{n=1}^{\infty} A_n$), то $\lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$.

**Доказательство:**
1. Пусть $B_1 = A_1, \, B_k = A_k \setminus A_{k-1}$ для $k \ge 2$. События $B_i$ не пересекаются, $\sum_{k=1}^{n} B_k = A_n$, $\sum_{k=1}^{\infty} B_k = A$.
   $$\mathbb{P}(A) = \mathbb{P}\left(\sum_{k=1}^{\infty} B_k\right) = \sum_{k=1}^{\infty} \mathbb{P}(B_k) = \lim_{n\to\infty} \sum_{k=1}^{n} \mathbb{P}(B_k) = \lim_{n\to\infty} \mathbb{P}(A_n)$$
2. Пусть $C_n = A_n^c \implies C_n \uparrow A^c$. По доказанному п. 1:
   $$\lim_{n\to\infty} \mathbb{P}(C_n) = \mathbb{P}(A^c) \implies \lim_{n\to\infty} (1 - \mathbb{P}(A_n)) = 1 - \mathbb{P}(A) \implies \lim_{n\to\infty} \mathbb{P}(A_n) = \mathbb{P}(A)$$
$\blacksquare$

### Связь сходимостей случайных величин
1. $X_n \xrightarrow{\text{п.н.}} X \implies X_n \xrightarrow{\mathbb{P}} X$.
2. $X_n \xrightarrow{\mathbb{P}} X \implies X_n \xrightarrow{d} X$.

**Доказательство:**
1. Пусть $X_n \xrightarrow{\text{п.н.}} X$. Зафиксируем $\varepsilon > 0$. Пусть $A_n(\varepsilon) = \bigcup_{k=n}^{\infty} \{|X_k - X| \ge \varepsilon\}$.
   $A_n(\varepsilon) \downarrow A(\varepsilon) = \{|X_k - X| \ge \varepsilon \text{ б.ч.}\}$.
   Из сходимости п.н. следует $\mathbb{P}(A(\varepsilon)) = 0$. По непрерывности меры:
   $$\lim_{n\to\infty} \mathbb{P}(A_n(\varepsilon)) = \mathbb{P}(A(\varepsilon)) = 0$$
   Поскольку $\{|X_n - X| \ge \varepsilon\} \subset A_n(\varepsilon)$, то $\mathbb{P}(|X_n - X| \ge \varepsilon) \le \mathbb{P}(A_n(\varepsilon)) \to 0$.
2. Пусть $X_n \xrightarrow{\mathbb{P}} X$. Обозначим $F_n(x) = \mathbb{P}(X_n < x), F(x) = \mathbb{P}(X < x)$.
   $$\{X_n < x\} = \{X_n < x, \, |X_n - X| < \varepsilon\} \cup \{X_n < x, \, |X_n - X| \ge \varepsilon\} \implies F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$
   Аналогично $F(x - \varepsilon) \le F_n(x) + \mathbb{P}(|X_n - X| \ge \varepsilon)$.
   $$F(x - \varepsilon) - \mathbb{P}(|X_n - X| \ge \varepsilon) \le F_n(x) \le F(x + \varepsilon) + \mathbb{P}(|X_n - X| \ge \varepsilon)$$
   При $n \to \infty$: $F(x - \varepsilon) \le \liminf F_n(x) \le \limsup F_n(x) \le F(x + \varepsilon)$.
   В точках непрерывности $F$ при $\varepsilon \to 0$ получаем $\lim_{n\to\infty} F_n(x) = F(x)$.
$\blacksquare$

### Неравенство Колмогорова
Пусть $X_1, \dots, X_n$ независимы, $\mathbb{E}[X_i] = 0, \mathbb{D}[X_i] = \sigma_i^2$, $S_k = \sum_{i=1}^k X_i$. Тогда:
$$\mathbb{P}\left(\max_{1 \le k \le n} |S_k| \ge \varepsilon\right) \le \frac{\mathbb{D}[S_n]}{\varepsilon^2}$$

**Доказательство:**
Пусть $A_k = \{|S_k| \ge \varepsilon, \, |S_1| < \varepsilon, \dots, |S_{k-1}| < \varepsilon\}$. События $A_k$ не пересекаются, $\bigcup A_k = \{\max |S_k| \ge \varepsilon\}$.
$$\mathbb{D}[S_n] = \mathbb{E}[S_n^2] \ge \sum_{k=1}^{n} \mathbb{E}[S_n^2 \mathbb{I}_{A_k}]$$
Поскольку $S_n^2 = (S_k + (S_n - S_k))^2 \ge S_k^2 + 2 S_k(S_n - S_k)$:
$$\mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}] + 2 \mathbb{E}[S_k(S_n - S_k) \mathbb{I}_{A_k}]$$
В силу независимости $S_k \mathbb{I}_{A_k}$ и $S_n - S_k$, и учитывая $\mathbb{E}[S_n - S_k] = 0$:
$$\mathbb{E}[S_k(S_n - S_k) \mathbb{I}_{A_k}] = 0 \implies \mathbb{E}[S_n^2 \mathbb{I}_{A_k}] \ge \mathbb{E}[S_k^2 \mathbb{I}_{A_k}] \ge \varepsilon^2 \mathbb{P}(A_k)$$
$$\mathbb{D}[S_n] \ge \sum_{k=1}^{n} \varepsilon^2 \mathbb{P}(A_k) = \varepsilon^2 \mathbb{P}\left(\max_{1 \le k \le n} |S_k| \ge \varepsilon\right)$$
$\blacksquare$

### Лемма Бореля–Кантелли
1. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) < \infty$, то $\mathbb{P}(\limsup A_n) = 0$.
2. Если $\sum_{n=1}^{\infty} \mathbb{P}(A_n) = \infty$ и $\{A_n\}$ независимы, то $\mathbb{P}(\limsup A_n) = 1$.

**Доказательство:**
1. Пусть $A^* = \limsup A_n = \bigcap_{n=1}^{\infty} \bigcup_{k=n}^{\infty} A_k \implies \mathbb{P}(A^*) \le \sum_{k=n}^{\infty} \mathbb{P}(A_k) \to 0$ при $n \to \infty$.
2. $\mathbb{P}((A^*)^c) = \mathbb{P}(\bigcup_{n=1}^\infty \bigcap_{k=n}^\infty A_k^c)$.
   $\mathbb{P}(\bigcap_{k=n}^{M} A_k^c) = \prod_{k=n}^{M} (1 - \mathbb{P}(A_k)) \le \exp\left(-\sum_{k=n}^M \mathbb{P}(A_k)\right) \to 0$ при $M \to \infty \implies \mathbb{P}(\bigcap_{k=n}^\infty A_k^c) = 0$.
$\blacksquare$

### Центральная предельная теорема (Линдеберга–Леви)
Для независимых одинаково распределенных $X_n$ с $\mathbb{E}[X_1] = \mu, \mathbb{D}[X_1] = \sigma^2 > 0$:
$$Y_n = \frac{\sum_{i=1}^{n} X_i - n\mu}{\sigma\sqrt{n}} \xrightarrow{d} \mathcal{N}(0, 1)$$

**Доказательство:**
Пусть $\mu=0, \sigma^2=1$. ХФ для $X_1$: $\varphi(t) = 1 - \frac{t^2}{2} + o(t^2)$.
ХФ для $Y_n = S_n/\sqrt{n}$:
$$\varphi_{Y_n}(t) = \left(\varphi\left(\frac{t}{\sqrt{n}}\right)\right)^n = \left(1 - \frac{t^2}{2n} + o\left(\frac{1}{n}\right)\right)^n \xrightarrow[n\to\infty]{} e^{-t^2/2}$$
По теореме непрерывности Леви $Y_n \xrightarrow{d} \mathcal{N}(0, 1)$. $\blacksquare$

---

## 2. Математическая статистика

### Теорема факторизации Неймана–Пирсона
Статистика $T(\mathbf{X})$ достаточна $\iff L(\mathbf{x}; \theta) = g(T(\mathbf{x}); \theta) h(\mathbf{x})$.

**Доказательство (дискретный случай):**
1. Необходимость: $\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x}) = \mathbb{P}_{\theta}(T(\mathbf{X}) = T(\mathbf{x})) \mathbb{P}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = T(\mathbf{x}))$. Обозначим $g(T(\mathbf{x}); \theta) = \mathbb{P}_{\theta}(T(\mathbf{X}) = T(\mathbf{x}))$, $h(\mathbf{x}) = \mathbb{P}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = T(\mathbf{x}))$ (не зависит от $\theta$).
2. Достаточность: При $T(\mathbf{x}) = t$:
   $$\mathbb{P}_{\theta}(\mathbf{X} = \mathbf{x} \mid T(\mathbf{X}) = t) = \frac{g(t; \theta) h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} g(T(\mathbf{y}); \theta) h(\mathbf{y})} = \frac{h(\mathbf{x})}{\sum_{\mathbf{y}: T(\mathbf{y})=t} h(\mathbf{y})}$$
   выражение не зависит от $\theta$. $\blacksquare$

### Неравенство Рао–Крамера
В регулярном эксперименте для оценки $\hat{\theta}$ со смещением $b(\theta) = \mathbb{E}_{\theta}[\hat{\theta}] - \tau(\theta)$:
$$\mathbb{D}_{\theta}[\hat{\theta}] \ge \frac{(\tau'(\theta) + b'(\theta))^2}{I_n(\theta)}$$

**Доказательство:**
Пусть $U(\mathbf{X}; \theta) = \frac{\partial \ln L(\mathbf{X}; \theta)}{\partial \theta}$. Из нормировки $\mathbb{E}_{\theta}[U] = 0 \implies \mathbb{D}_{\theta}[U] = I_n(\theta)$.
Дифференцируя по $\theta$ уравнение $\mathbb{E}_{\theta}[\hat{\theta}] = \tau(\theta) + b(\theta)$:
$$\int \hat{\theta}(\mathbf{x}) \frac{\partial \ln L}{\partial \theta} L \, d\mathbf{x} = \tau'(\theta) + b'(\theta) \implies \mathbb{E}_{\theta}[\hat{\theta} U] = \tau'(\theta) + b'(\theta) \implies \operatorname{Cov}_{\theta}(\hat{\theta}, U) = \tau'(\theta) + b'(\theta)$$
По неравенству Коши-Буняковского:
$$(\operatorname{Cov}_{\theta}(\hat{\theta}, U))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] \mathbb{D}_{\theta}[U] \implies (\tau'(\theta) + b'(\theta))^2 \le \mathbb{D}_{\theta}[\hat{\theta}] I_n(\theta)$$
$\blacksquare$

### Теорема Рао–Блекуэлла–Колмогорова
Пусть $\hat{\theta}$ — несмещенная оценка $\theta$ с конечной дисперсией, $T$ — достаточная статистика.
Для $\hat{\theta}^* = \mathbb{E}[\hat{\theta} \mid T]$ выполнено: $\mathbb{E}_{\theta}[\hat{\theta}^*] = \theta$ и $\mathbb{D}_{\theta}[\hat{\theta}^*] \le \mathbb{D}_{\theta}[\hat{\theta}]$.

**Доказательство:**
$\hat{\theta}^*$ не содержит $\theta$ по достаточности $T$.
$\mathbb{E}_{\theta}[\hat{\theta}^*] = \mathbb{E}_{\theta}[\mathbb{E}[\hat{\theta} \mid T]] = \mathbb{E}_{\theta}[\hat{\theta}] = \theta$.
По закону полной дисперсии:
$$\mathbb{D}_{\theta}[\hat{\theta}] = \mathbb{E}_{\theta}[\mathbb{D}[\hat{\theta} \mid T]] + \mathbb{D}_{\theta}[\hat{\theta}^*] \ge \mathbb{D}_{\theta}[\hat{\theta}^*]$$
$\blacksquare$

### Лемма Неймана–Пирсона
Для проверки простых гипотез наиболее мощная критическая область имеет вид $W = \{\mathbf{x} : L_1(\mathbf{x}) > c L_0(\mathbf{x})\}$, где $\mathbb{P}_{\theta_0}(W) = \alpha$.

**Доказательство:**
Пусть $W'$ — любая другая область с $\mathbb{P}_{\theta_0}(W') \le \alpha$.
Для любого $\mathbf{x}$: $(\mathbb{I}_W(\mathbf{x}) - \mathbb{I}_{W'}(\mathbf{x})) (L_1(\mathbf{x}) - c L_0(\mathbf{x})) \ge 0$.
Интегрируя по выборочному пространству:
$$\int (\mathbb{I}_W - \mathbb{I}_{W'}) (L_1 - c L_0) \, d\mathbf{x} \ge 0 \implies \mathbb{P}_{\theta_1}(W) - \mathbb{P}_{\theta_1}(W') - c(\mathbb{P}_{\theta_0}(W) - \mathbb{P}_{\theta_0}(W')) \ge 0$$
$$\implies \beta - \beta' \ge c(\alpha - \alpha') \ge 0 \implies \beta \ge \beta'$$
$\blacksquare$

### Теорема Фишера о нормальных выборках
Пусть $X_i \sim \mathcal{N}(a, \sigma^2)$ независимы.
1. Выборочное среднее $\bar{X}$ и исправленная выборочная дисперсия $S_0^2$ независимы.
2. $\frac{(n-1)S_0^2}{\sigma^2} \sim \chi^2(n-1)$.

**Доказательство:**
Пусть $a=0, \sigma^2=1$. Сделаем ортогональное преобразование $\mathbf{Y} = C\mathbf{X}$, где первая строка матрицы $C$ равна $(1/\sqrt{n}, \dots, 1/\sqrt{n})$.
Так как преобразование ортогонально, $Y_i \sim \mathcal{N}(0, 1)$ независимы.
$$Y_1 = \sqrt{n}\bar{X} \implies Y_1^2 = n\bar{X}^2$$
$$\sum_{i=1}^{n} X_i^2 = \sum_{i=1}^{n} Y_i^2 \implies \sum_{i=2}^{n} Y_i^2 = \sum_{i=1}^{n} X_i^2 - n\bar{X}^2 = (n-1)S_0^2$$
Поскольку $\bar{X} = Y_1/\sqrt{n}$, а $S_0^2 = \frac{1}{n-1} \sum_{i=2}^n Y_i^2$, они независимы.
Величина $(n-1)S_0^2 = \sum_{i=2}^n Y_i^2$ есть сумма квадратов $n-1$ независимых стандартных нормальных величин, следовательно, $(n-1)S_0^2 \sim \chi^2(n-1)$. $\blacksquare$
