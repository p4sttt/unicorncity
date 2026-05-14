---
title: "Типы сходимости. Закон больших чисел"
description: ""
date: 2026-05-14
status: "in-progress"
---

# Типы сходимости 

Выделяют следующие типы сходимости
- сходимость по вероятности
- сходимость по распределению (слабая сходимость)
- сходимость почти наверное
- сходимость в среднем

Схема отношений сходимости:

$$
\begin{array}{ccccc}
X_n \xrightarrow{\text{п.н.}} X & & X_n \xrightarrow{L^1} X \\
& \searrow & \swarrow & \\
& X_n \xrightarrow{P} X & \Longrightarrow & X_n \xrightarrow{d} X
\end{array}
$$

Здесь сходимость в среднем понимается как сходимость в $L^1$. Сходимость по распределению самая слабая: она следует из сходимости по вероятности, а значит также из сходимости почти наверное и сходимости в среднем. Сходимость почти наверное и сходимость в среднем в общем случае не следуют друг из друга.


## Сходимость по вероятности

Будем говорить, что последовательность случайных величин $X_i$ сходится к случайной величине $X$ по вероятности, если выполнено условие

$$
X_{n}\xrightarrow{P} X \iff \forall\varepsilon>0 \lim_{ n \to \infty } P(\mid X_{n}-X\mid  > \varepsilon) =0 
$$

Независимость и одинаковое распределение здесь не требуются; достаточно, чтобы $X_i$ и $X$ были заданы на одном вероятностном пространстве.

# Друзья сходимости по вероятности

## Неравенство Маркова

Если для случайной величины $X$ существует математическое ожидание $\mathbb{E}[\mid X\mid]<\infty$, то

$$
\forall\varepsilon>0:\Pr[\mid X \mid \geq\varepsilon]\leq \frac{\mathbb{E}[\mid X\mid ]}{\varepsilon}
$$

**Доказательство**: Рассмотрим случайную величину

$$
Y=\begin{cases}
0,& \mid X\mid < \varepsilon \\
\varepsilon, & \mid X\mid \geq \varepsilon
\end{cases}
$$

Заметим, что $\forall\varepsilon>0$ выполнено $Y\leq \mid X\mid$. Тогда, взяв математическое ожидание от обеих сторон неравенства, получаем

$$
\begin{array}{r}
\begin{align}
\mathbb{E}[Y] \leq \mathbb{E}[\mid X\mid]&  \\
\implies& 0\cdot \Pr\left[\mid X\mid <\varepsilon\right]+\varepsilon \cdot \Pr\left[\mid X\mid \geq\varepsilon\right]\leq \mathbb{E}[\mid X\mid ] \\
\implies&\Pr\left[\mid X\mid \geq\varepsilon\right]\leq \frac{\mathbb{E}[\mid X\mid ]}{\varepsilon}  \\
\end{align} \\
\blacksquare
\end{array}
$$

## Неравенство Чебышева

Если для случайной величины $X$ существует конечная дисперсия $\operatorname{Var}[ X]<\infty$, тогда $\forall\varepsilon>0$

$$
\Pr\left[\mid X-\mathbb{E}[X]\mid \geq\varepsilon\right]\leq \frac{\operatorname{Var}\left[X\right]}{\varepsilon^2}  
$$

**Доказательство**: Применим неравенство Маркова к неотрицательной случайной величине $Y=(X-\mathbb{E}[X])^2$:

$$
\begin{array}{r}
\begin{align}
\Pr\left[\mid X-\mathbb{E}[X]\mid \geq\varepsilon\right]
&=\Pr\left[(X-\mathbb{E}[X])^2\geq\varepsilon^2\right] \\
&\leq \frac{\mathbb{E}\left[(X-\mathbb{E}[X])^2\right]}{\varepsilon^2}
=\frac{\operatorname{Var}[X]}{\varepsilon^2}
\end{align} \\
\blacksquare
\end{array}
$$

Зачем все это может понадобиться? Чтобы доказать сходимость по вероятности, нужно анализировать $\Pr\left[\mid X_{n}-X\mid\geq\varepsilon\right]$. Для этого часто нужно знать $F_{X_{n}}(t)$, что не всегда возможно и не очень удобно. Неравенства Маркова и Чебышева дают грубые, но универсальные верхние оценки для произвольных распределений.

## Всякие свойства 

**Теорема Манна-Вальда-Слуцкого**: пусть $X_n\xrightarrow{P}X$, $Y_n\xrightarrow{P}Y$, а $g$ -- непрерывная функция подходящей размерности. Тогда

$$
g(X_n)\xrightarrow{P}g(X)
$$

и выполняются обычные правила предельного перехода:

$$
\begin{array}{rcl}
X_n+Y_n &\xrightarrow{P}& X+Y, \\
X_n-Y_n &\xrightarrow{P}& X-Y, \\
X_nY_n &\xrightarrow{P}& XY, \\
\frac{X_n}{Y_n} &\xrightarrow{P}& \frac{X}{Y}, \quad \text{если } \Pr[Y=0]=0.
\end{array}
$$

В форме Слуцкого: если $X_n\xrightarrow{d}X$ и $Y_n\xrightarrow{P}c$, где $c$ -- константа, то $X_n+Y_n\xrightarrow{d}X+c$, $X_nY_n\xrightarrow{d}cX$ и при $c\neq0$ выполнено $\frac{X_n}{Y_n}\xrightarrow{d}\frac{X}{c}$.

# Закон больших чисел

## Теорема Чебышева

Еще этот результат называют слабым законом больших чисел.

Пусть последовательность случайных величин $X_{1},X_{2},\dots$ такая, что величины:
- попарно независимы
- одинаково распределены
- существует второй момент, то есть $\mathbb{E}[X_{i}^2]< \infty$; тогда $\operatorname{Var}\left[X_{i}\right]<\infty$

Тогда

$$
\frac{X_{1}+\dots+X_{n}}{n}\xrightarrow{P}\mathbb{E}[X_{i}]=\mu
$$

**Доказательство**: Введем случайную величину $S_{n}=X_{1}+\dots+X_{n}$, тогда

$$
\mathbb{E}\left[ \frac{S_{n}}{n} \right]=\frac{1}{n}\mathbb{E}\left[ S_{n} \right] =\frac{1}{n}\sum_{i}\mathbb{E}[X_{i}]=\frac{1}{n}\cdot n\cdot \mathbb{E}[X_{1}]=\mu
$$

И запишем для полученного результата неравенство Чебышева:

$$
\begin{array}{r}
\begin{align}
\Pr\left[\left| \frac{S_{n}}{n}-\mu\right|\geq\varepsilon\right]
&\leq \frac{\operatorname{Var}\left[\frac{S_{n}}{n}\right]}{\varepsilon^2}  \\
&= \frac{\operatorname{Var}\left[S_n\right]}{n^2\varepsilon^2} \\
&= \frac{\operatorname{Var}\left[X_{1}+\dots+X_{n}\right]}{n^2\varepsilon^2}  \\
&= \frac{n\sigma^2}{n^2\varepsilon^2}=\frac{1}{n}\cdot\frac{\sigma^2}{\varepsilon^2} \xrightarrow[n\to \infty]{} 0
\end{align} \\
\blacksquare
\end{array}
$$

## Теорема Хинчина

Пусть $X_{1},X_{2},\dots$ -- независимые одинаково распределенные случайные величины и $\mathbb{E}|X_i|<\infty$. Тогда

$$
\frac{X_{1}+\dots+X_{n}}{n}\xrightarrow{P}\mathbb{E}[X_i]=\mu
$$

Разница с теоремой Чебышева: теорема Хинчина не требует существования второго момента и конечной дисперсии. Достаточно конечного первого абсолютного момента.

**Доказательство**: Обозначим характеристическую функцию $X_i$ через $\varphi(t)=\mathbb{E}e^{itX_i}$. Так как $\mathbb{E}|X_i|<\infty$, то при $t\to0$

$$
\varphi(t)=1+i\mu t+o(t)
$$

Для $\overline{X}_n=\frac{X_{1}+\dots+X_{n}}{n}$ характеристическая функция равна

$$
\varphi_{\overline{X}_n}(t)
=\left(\varphi\left(\frac{t}{n}\right)\right)^n
=\left(1+\frac{i\mu t}{n}+o\left(\frac{1}{n}\right)\right)^n
\xrightarrow[n\to\infty]{} e^{i\mu t}
$$

Это характеристическая функция константы $\mu$. Значит, $\overline{X}_n\xrightarrow{d}\mu$. Сходимость по распределению к константе эквивалентна сходимости по вероятности, поэтому $\overline{X}_n\xrightarrow{P}\mu$.

## Теорема Колмогорова

Пусть $X_{1},X_{2},\dots$ -- независимые одинаково распределенные случайные величины и $\mathbb{E}|X_i|<\infty$. Тогда

$$
\frac{X_{1}+\dots+X_{n}}{n}\xrightarrow{\text{п.н.}}\mathbb{E}[X_i]=\mu
$$

Это сильный закон больших чисел: он утверждает сходимость почти наверное, а не только сходимость по вероятности.

## Теорема Маркова

Пусть $X_{1},X_{2},\dots$ -- случайные величины с конечными дисперсиями, $S_n=X_1+\dots+X_n$. Если

$$
\frac{\operatorname{Var}[S_n]}{n^2}\xrightarrow[n\to\infty]{}0
$$

то

$$
\frac{S_n-\mathbb{E}[S_n]}{n}\xrightarrow{P}0
$$

Разница с теоремой Чебышева: здесь не требуется одинаковое распределение, а попарная независимость в формулировке заменяется более общим условием $\frac{\operatorname{Var}[S_n]}{n^2}\to0$. Теорема Чебышева получается как частный случай, потому что при попарной независимости и одинаковом распределении $\operatorname{Var}[S_n]=n\sigma^2$.

**Доказательство**: По неравенству Чебышева для любого $\varepsilon>0$

$$
\Pr\left[\left|\frac{S_n-\mathbb{E}[S_n]}{n}\right|\geq\varepsilon\right]
\leq \frac{\operatorname{Var}[S_n]}{n^2\varepsilon^2}
\xrightarrow[n\to\infty]{}0
$$

Значит, по определению сходимости по вероятности $\frac{S_n-\mathbb{E}[S_n]}{n}\xrightarrow{P}0$.
