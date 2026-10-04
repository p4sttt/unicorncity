# Источники по Московской проблеме

Дата поиска: 4 октября 2026 года. Основной синтез: [[moscow_problem]]. Реестр охватывает прямую литературу и методы, важные для оценки направлений решения. Первичные тексты использовались для математических утверждений; справочные страницы — для обнаружения новых работ. Отсутствие иной публикации в поиске не доказывает её отсутствия.

## Прямая литература

| № | Источник | Что читать и зачем |
|---|---|---|
| 1 | [AI4OPT, The Moscow problem](https://ai4opt.fmin.xyz/The_%E2%80%9CMoscow_problem%E2%80%9D/) | Исходная страница пользователя, редактирование 14.10.2025. Статус частных случаев устарел; полный текст прочитан. |
| 2 | [Goreinov, Tyrtyshnikov, Zamarashkin, A theory of pseudoskeleton approximations, 1997](https://doi.org/10.1016/S0024-3795(96)00301-1) | Истоки гипотезы и CUR. Проверены издательская запись/аннотация; классическая оценка дополнительно выведена непосредственно. Полное чтение издательского PDF не заявляется. |
| 3 | [Nesterenko, Submatrices with the best-bounded inverses: revisiting the hypothesis](https://arxiv.org/abs/2303.07492) | v3, 26.08.2024; начало 2023. Полный HTML: геометрия и случай 4×2. |
| 4 | [Nesterenko, Studying real and complex two-column matrices](https://arxiv.org/abs/2408.16631) | v1, 29.08.2024. Полный HTML: многоугольники и различие полей. |
| 5 | [Nesterenko, About subspaces the most deviating from the coordinate ones](https://arxiv.org/abs/2511.02387) | v2, 11.05.2026; начало 04.11.2025. Проверены введение, Theorems 3.1/4.1, графовая энергетическая рекурсия и пределы численного вывода. |
| 6 | [Sengupta, Pautov, On the submatrices with the best-bounded inverses](https://arxiv.org/abs/2604.05944) | v5, 16.04.2026; начало 07.04.2026. Полное доказательство ранга 2. |
| 7 | [Nesterenko, The equality criterion for real two-column matrices](https://arxiv.org/abs/2604.14050) | v2, 02.05.2026; начало 15.04.2026. Полный текст; критерий равенства. |
| 8 | [Nesterenko, An asymptotically tight upper bound for complex two-column matrices](https://arxiv.org/abs/2604.24087) | v1, 27.04.2026. Proposition 1 и доказательство: новая комплексная константа. |
| 9 | [Open Problems in NLA, RA-18](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/randomized-and-low-rank-approximation/RA-18/README.md) | Вторичный реестр состояния, проверка страницы от 13.09.2026. Помог обнаружить следующую рукопись. |
| 10 | [Holden, рукопись от 13.09.2026](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/references/holden-ra18-2026-09-13/manuscript/ra18.pdf) | Проверены исходник и основные доказательства §§2–3, 7. Структурный вещественный случай и отрицательный результат о комплексном универсальном множителе. GitHub submission, без установленного внешнего рецензирования. |

У работ 3–8 проверены arXiv-версии; сведения о рецензировании не додумывались. Для 10 [исходник](https://raw.githubusercontent.com/ajt60gaibb/OpenProblemsInNLA/main/references/holden-ra18-2026-09-13/manuscript/ra18.tex) позволяет проверить аргумент независимо; [AI-аудит](https://github.com/ajt60gaibb/OpenProblemsInNLA/blob/main/references/holden-ra18-2026-09-13/independent-review.md) не равен формальной или внешней человеческой проверке.

## Отбор строк и устойчивые подматрицы

| № | Источник | Роль и ограничение |
|---|---|---|
| 11 | [Gu, Eisenstat, Efficient algorithms for computing a strong rank-revealing QR factorization, 1996](https://math.berkeley.edu/~mgu/MA273/Strong_RRQR.pdf) | Theorem 3.2; алгоритмический контроль выбора базиса, сохраняющий фактор $r(n-r)$. |
| 12 | [Goreinov et al., How to Find a Good Submatrix, 2010](https://doi.org/10.1142/9789812836021_0015) | Практический maxvol и связь с cross-приближением; полезен как baseline. |
| 13 | [Osinsky, Close to optimal column approximations with a single SVD](https://arxiv.org/abs/2308.09068) | Быстрый выбор с гарантиями максимального объёма; улучшение стоимости построения, не новая целевая константа. |
| 14 | [Dereziński, Warmuth, Unbiased estimates for linear regression via volume sampling, 2017](https://proceedings.neurips.cc/paper_files/paper/2017/hash/54e36c5ff5f6a1802925ca009f3ebb68-Abstract.html) | Theorem 4: момент обратного грамиана; применимость при точной мощности, но иной спектральный контроль. |
| 15 | [Allen-Zhu et al., Near-Optimal Design of Experiments via Regret Minimization, 2017](https://proceedings.mlr.press/v70/allen-zhu17e.html) | Theorem 1.1 и условия мощности; для выбора без возвращения нужен избыток относительно размерности. |
| 16 | [Brown, Laddha, Singh, 2024](https://doi.org/10.1016/j.orl.2024.107186) | Смежный алгоритмический результат о максимизации минимального собственного значения в фиксированной размерности; не универсальная оценка Московской задачи. |

## Спектральные методы

| № | Источник | Роль и ограничение |
|---|---|---|
| 17 | [Spielman, Srivastava, An Elementary Proof of the Restricted Invertibility Theorem](https://arxiv.org/abs/0911.1114) | Theorem 2; конструктивный отбор неполного набора. |
| 18 | [Naor, Youssef, Restricted invertibility revisited](https://arxiv.org/abs/1601.00948) | Дополнительный первичный контекст усилений restricted invertibility; не прямое решение. |
| 19 | [Marcus, Spielman, Srivastava, Interlacing Families III](https://arxiv.org/abs/1712.07766) | §§1,5: Jacobi/Laguerre и точные размеры; граница полного базиса остаётся трудной. |
| 20 | [Ravichandran, Principal submatrices, restricted invertibility and a quantitative Gauss–Lucas theorem](https://arxiv.org/abs/1609.04187) | Theorem 1.3; главные блоки и производные характеристического многочлена. |
| 21 | [Marcus, Spielman, Srivastava, Interlacing Families II](https://arxiv.org/abs/1306.3969) | Corollary 1.5; Kadison–Singer и спектральные разбиения, без нужной мощности части. |
| 22 | [Batson, Spielman, Srivastava, Twice-Ramanujan Sparsifiers, SIAM Review](https://epubs.siam.org/doi/10.1137/130949117) | Спектральное разреживание с весами; не переносить его гарантию на ровно $r$ невзвешенных строк. |

## Геометрия, графы и сертификаты

| № | Источник | Роль |
|---|---|---|
| 23 | [Hausmann, Knutson, Polygon spaces and Grassmannians, 1997](https://arxiv.org/abs/dg-ga/9602012) | Геометрическая основа многоугольной редукции; проверены аннотация и связь в прямых работах. |
| 24 | [Kassel, Wu, Transfer current and pattern fields in spanning trees, 2015](https://arxiv.org/abs/1312.2946) | Фон для transfer-current матриц; не утверждает Московскую оценку. Проверены библиографическая запись и роль в графовой работе. |
| 25 | [Speyer, Tropical Linear Spaces](https://arxiv.org/abs/math/0410455) | Смежный матроидный контекст, отмеченный Nesterenko; перенос на задачу остаётся предположением. |
| 26 | [Lasserre, Global Optimization with Polynomials and the Problem of Moments, 2001](https://doi.org/10.1137/S1052623400366802) | Основа моментных релаксаций; новый сертификат Московской задачи здесь не найден. |
| 27 | [Parrilo, Semidefinite programming relaxations for semialgebraic problems, 2003](https://www.mit.edu/~parrilo/pubs/files/SDPrelaxations.pdf) | Основа SOS-подхода и проверки алгебраических неравенств. |

## Метод поиска и ограничения

Искались точные названия, “Moscow problem”, “Goreinov Tyrtyshnikov Zamarashkin conjecture”, “best-bounded inverses”, фамилии авторов, цитирующие продолжения 2025–2026 годов, а также maxvol, volume sampling, E-optimal design и restricted invertibility. Пройдены ссылки исходной страницы и библиографии прямых работ. Широкие запросы с “Moscow” дают много нерелевантных результатов; заключения основаны на точных математических источниках.

Полностью проверены основные прямые аргументы, необходимые для карты состояния; смежная литература проверялась по конкретным применяемым теоремам либо отмечена как библиографический фон. Ни общий вещественный контрпример, ни полное доказательство в просмотренном корпусе не обнаружены. Это литературный аудит и исследовательская оценка, не экспертное рецензирование всех перечисленных статей.
