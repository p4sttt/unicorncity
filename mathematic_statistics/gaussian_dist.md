Нормальное распредление называние распредление случайной величины $x \sim \mathcal{N(\mu, \sigma)}$ с плотность распредение

$$
f_{x}(t)=\frac{1}{\sqrt{ 2\pi\sigma^2 }}\exp \left( -\frac{(t-\mu)^2}{2\sigma^2} \right) 
$$

Соотвественно

$$
\mathbb{E}\left[ X \right] =\int_{-\infty}^{\infty} tf_{x}(t)dt=\mu
$$

и

$$
\operatorname{Var}\left[ X \right] =\sigma^2
$$

(TODO: график нормального распредления через python)

 Центральные моменты трнетьего и четвертого порядка:
 - коэфциенетр ассиемтрии (третьей цегтарльый момент): наскольок перекосило распредленеие 
 - куртосис: насколько толчные хвосты, вычисляет выбросы

Многомерное нормальное распредени 

$$
x \sim \mathcal{N}(\mu, \Sigma)
$$

$$
f(t_{1},\dots,t_{n})=\frac{1}{(\sqrt{ 2\pi })^n}\cdot\frac{1}{\det\Sigma} \cdot \exp \left( \dots \right) 
$$

$$
\begin{bmatrix}
X \\
Y 
\end{bmatrix} \sim
\mathcal{N} \begin{bmatrix}
\begin{matrix}
\mu_{X} \\
\mu_{Y}
\end{matrix}, & 

\end{bmatrix}
$$

есть вектор матожиданий и матрица коварицаий (по диагори стоит дисперсия)

(TODO: графики в зависмости от ковариции и дисперсии)

$$
X \sim \mathcal{N}(\mu, \Sigma)
$$

$$
Y= AX=\dots
$$

Тогда

$$
\mathbb{E}\left[ Y \right] = \dots
$$

$$
\operatorname{Var}\left[ Y \right] =\dots=A\operatorname{Var}\left[ X \right] A^{\top}
$$

(TODO: расписать весьь вывод)



А какие матрциы могут быть коваринцонынми? Какие у них свойства
- Симметричности
- Положительно оперденность
- Какие-то свойства спекра или сигнуряхных чисел
- Ортогональность

(TODO: ответь на вопросы и свойства)
