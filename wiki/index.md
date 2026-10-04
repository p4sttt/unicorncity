---
title: "Research Wiki Index"
description: "Каталог paper summaries, concepts, model cards и исследовательских проектов в Research Wiki."
type: note
tags: ["llm", "dl", "rl", "math"]
status: done
date: 2026-09-26
updated: 2026-10-04
sources: []
---

# Wiki Index

## Papers

### Programming Languages — Rust Aliasing
- [[stacked_borrows]] — Jung et al., POPL 2020; операционная семантика Rust с per-location borrow stack; обосновывает интрапроцедурный alias analysis через UB для нарушений стекового порядка
- [[tree_borrows]] — Villani et al., PLDI 2025; замена стека деревом + state machine на узел; -54% ложных UB на 30K crates; поддерживает two-phase borrows и read-read reorderings

### Computer Vision
- [[eam_enhancing_anything_with_diffusion_transformers]] — Huawei, 2025; DiT-based blind super-resolution с тройным потоком $\Psi$-DiT и progressive MIM

### LLM Agents — Context Management
- [[recursive_language_models]] — MIT CSAIL, 2025; prompt как REPL-переменная + символьная рекурсия; обработка 10M+ токенов, +26% медианы над GPT-5
- [[context_folding_scaling_llm_agents]] — ByteDance/CMU, 2025; механизм branch/return + FoldGRPO; 62% BrowseComp-Plus при 32K контексте
- [[agent_omit_adaptive_context_omission]] — HKUST/Didi, ICML 2026; адаптивный пропуск thoughts/observations; 8B достигает уровня frontier LLM

### LLM Agents — GUI & Memory
- [[darwinian_memory_system_gui_agents]] — Didi/CUHK, 2026; training-free эволюционная память; +18% accuracy, +34% stability
- [[se_ga_self_evolving_gui_agent]] — Tianjin/SJTU, ICML 2026; TTME + MASE self-evolution; 89% ScreenSpot, 75.8% AndroidControl-High

### LLM Agents — Coding: Exploration & Localization
- [[code_isnt_memory_structural_index]] — SuperAGI, 2026; leak-audited причинная абляция структурного индекса; +40pp localization, +8.5pp resolve без cost-penalty
- [[codebase_memory_tree_sitter_kg]] — Vogel et al., 2026; open-source Tree-Sitter KG через MCP (66 языков, SQLite); 10x меньше токенов при 83% vs 92% качества
- [[fastcontext]] — Microsoft/SJTU, 2026; обученный exploration-субагент (4B–30B); +5.5% resolve, -60% токенов main-модели
- [[sherloc]] — NVIDIA/TU Darmstadt, 2026; training-free структурная диагностическая локализация; SOTA 84.33% acc@1, +5.95pp resolve при инъекции
- [[swe_explore]] — SJTU, 2026; бенчмарк repository exploration (848 issues, 10 языков); line-level ground truth из успешных траекторий
- [[harness_handbook]] — Tencent HY LLM Frontier, 2026; behavior-centric представление harness'а + BGPD для behavior localization

### Numerical Analysis — Domain Decomposition: классика
- [[lions_schwarz_alternating_i]] — P.-L. Lions, DD1 1988; вариационная интерпретация метода Шварца как итерации ортогональных проекций в гильбертовом пространстве
- [[lions_schwarz_alternating_ii]] — P.-L. Lions, DD2 1989; сходимость Шварца через принцип максимума и времена выхода броуновского движения — работает там, где вариационной интерпретации нет
- [[lions_schwarz_alternating_iii]] — P.-L. Lions, DD3 1990; передача выпуклой комбинации Дирихле- и Нейман-данных даёт Robin-условие на интерфейсе — предок оптимизированного Шварца
- [[dryja_widlund_unified_theory]] — Dryja & Widlund, DD3 1990; аддитивный Шварц как общая рамка — substructuring оказывается его частным случаем, $\kappa(P)$ оценивается через $C_0^2$ и число цветов
- [[widlund_iterative_substructuring]] — Widlund, DD1 1988; теория substructuring для многих подструктур, нижняя оценка скорости без глобального обмена, теоремы о продолжении
- [[chan_resasco_dd_preconditioners_framework]] — Chan & Resasco, DD1 1988; спектральная диагонализация интерфейсного оператора для сепарабельных задач — точный обратный, к которому сводятся все известные предобусловливатели
- [[marini_quarteroni_relaxation_dd]] — Marini & Quarteroni, Numer. Math. 55 (1989); итерация Дирихле–Нейман с релаксацией $\theta$, $h$-независимый фактор сходимости и автоматический выбор оптимального $\theta$

### Numerical Analysis — Domain Decomposition: варианты и приложения
- [[israeli_hierarchical_dd]] — Israeli, Braverman, Averbuch, DD13 2001; неитерационное спектральное решение Пуассона через иерархическое сшивание соседних подобластей за log k шагов
- [[kuznetsov_distributed_lagrange_multipliers]] — Yu. Kuznetsov, DD13 2001; три применения распределённых множителей Лагранжа — композитные материалы, фиктивная область и overlapping DD — с оценками $\kappa$, не зависящими от контраста
- [[acebron_spigler_probabilistic_dd]] — Acebrón & Spigler, DD16 2005; Монте-Карло по формуле Фейнмана–Каца даёт несколько значений на интерфейсе, что полностью развязывает подобласти — масштабируемо и отказоустойчиво
- [[acebron_spigler_scalable_parallel_elliptic]] — Acebrón & Spigler, DD17 2007; MPI-сравнение PDD с настоящим детерминированным DD (pARMS) на MareNostrum: время PDD не растёт до 1024 процессоров
- [[kim_yang_dd_neural_network]] — Kim & Yang; аддитивный Шварц над разделёнными нейросетями — разбиение единицы убирает высококонтрастную ошибку у границы наложения и оживляет грубую задачу
- [[scherbakov_rakhimov_classic_iterative_methods]] — Щербаков и Рахимов, МГУ; сравнительный разбор шести классических итерационных DD-методов (DN, NN, Schur, AS, MS, RAS) с реализацией на JAX и 164 бенчмарками

### Numerical Analysis — двухсеточные методы и потоковые разложения
- [[subspace_uzawa_two_grid]] — Numerical Archeology, июль 2026; грубое пространство порождается локальными спектрами при заданном пороге $\tau$, и $\kappa(BA) = \max(1, C_{\mathrm{stab}})$ становится назначаемым числом
- [[two_grid_entrywise_certificate]] — Numerical Archeology, июль 2026; вычислимая граница $\kappa(BA)$ за один проход по разреженной матрице — без спектральных задач, геометрии и различения внутренних/граничных узлов
- [[streaming_tt_dmd]] — Numerical Archeology, 2026; карта режимов вместо заявки о превосходстве: растущее преимущество по памяти, две доказанные ловушки метрик и закон $\lambda^* = 1 - c(\delta/\sigma)^{2/3}$

### Numerical Analysis — DMD и тензорные алгебры
- [[klus_tensor_based_dmd]] — Klus, Gelß, Peitz, Schütte, Nonlinearity 2018; TT-формат уже содержит информацию о псевдообратном развёртки, поэтому DMD считается прямо на низкоранговом представлении
- [[he_tensor_dmd_tproduct]] — He, Hu, Lou, Chen, 2025; DMD в алгебре t-product для многомерных данных — изображений, видео, сетей высшего порядка — без расплющивания
- [[saibaba_star_m_dmd]] — Saibaba, Kilmer et al., 2025; DMD в $\star_M$-рамке даёт лучшее сжатие при равном хранении, связывается с physics-informed DMD и допускает рандомизированный потоковый алгоритм
- [[katrutsa_dmd_mori_zwanzig]] — Katrutsa, Utyuzhnikov, Oseledets, 2022; формализм Мори–Цванцига учитывает влияние неизмеренных переменных, первый порядок разложения решается градиентно через autodiff
- [[braman_third_order_tensors_operators]] — Braman, LAA 2010; $n\times n\times n$ тензоры действуют на пространстве $n\times n$ матриц — свободный модуль, представимость любого линейного преобразования, собственные значения как трубчатые скаляры
- [[kernfeld_kilmer_aeron_tensor_products]] — Kernfeld, Kilmer, Aeron, LAA 2015; t-product обобщается на произвольное обратимое линейное преобразование — все определения и факторизации формулируются в трансформ-домене

### Numerical Analysis — рандомизированная линейная алгебра
- [[smith_adaptive_matrix_free_lowrank]] — Smith, Do, Chen, 2026; рандомизированный индикатор ошибки, точный до машинной точности, плюс rank-pruning, развязывающий размер блока от итогового ранга
- [[xiao_rplss]] — Xiao, Li, Needell, 2026; PLSS с частичным доступом к матрице — конечное завершение плюс экспоненциальная сходимость, устойчиво к пропускам данных
- [[guettel_sketch_and_restart]] — Güttel, Liu, Nyman, 2026; общий вид $B_m f(H_m)e_1\beta$ объединяет крыловские и скетчированные приближения, давая единый механизм рестарта для $f(A)b$
- [[gillman_librla]] — Gillman & Gimbutas, 2026; первая устойчивая и эффективная библиотека рандомизированных факторизаций сразу в MATLAB, Python и Julia, с режимами фиксированного ранга и допуска
- [[andersson_appelo_sublinear_lowrank_poisson]] — Andersson & Appelö, 2026; Cross-DEIM + транспонирование-свободный DST-решатель Пуассона в PyTorch; сублинейное масштабирование по числу узлов сетки

### Numerical Analysis — HPC, matrix-free FEM и дифференцируемые решатели
- [[baker_scaling_hypre_100k_cores]] — Baker, Falgout, Kolev, Yang, LLNL 2011; исследование слабой масштабируемости PFMG/SMG/BoomerAMG/AMS на $>10^5$ ядер, решена задача с 1.049 триллиона неизвестных
- [[wichrowski_coalesced_matrix_free_fe]] — Wichrowski, 2026; поэлементный вектор как постоянное первичное представление; примально-дуальная теорема эквивалентности загоняет всю коммуникацию в предобусловливатель
- [[scroggs_wells_dof_transformations]] — Scroggs & Wells, 2026; автоматическое построение DOF-преобразований для произвольного элемента типа Чиарле только из его определения — реализовано в Basix/FEniCSx
- [[long_task_based_red_black_gauss_seidel]] — Long, Ramirez-Hidalgo, Frommer, Pleiter, 2026; task-based модели убирают глобальные барьеры и дают устойчивость к аппаратной асинхронности при сопоставимой производительности
- [[horowitz_jax_geometric_multigrid_pm]] — Horowitz, MNRAS 2026; multigrid как конкурент FFT на фиксированных сетках и как единственный работающий решатель на подвижных — до $2\times$ сокращения GPU-времени
- [[toshev_jax_sph]] — Toshev et al., ICLR 2024 AI4DiffEq workshop; лагранжев SPH-решатель в JAX с верифицированными градиентами, обратной задачей и solver-in-the-loop

## Concepts

### Programming Languages
- [[rust_aliasing_model]] — операционные модели алиасинга в Rust (SB и TB): принцип исключения, borrow stack/tree, UB, Miri

### Agents
- [[context_management_llm_agents]] — таксономия подходов к управлению контекстом LLM-агентов
- [[gui_agents_memory]] — типы памяти и эволюционные механизмы для GUI-агентов
- [[repository_exploration_coding_agents]] — исследование кодовой базы и локализация как отдельная под-способность coding-агентов
- [[structural_codebase_index]] — персистентный индекс поверх структуры кода (semantic+lexical+call-graph / Tree-Sitter KG) как tool для агента

### Numerical Analysis — Domain Decomposition
- [[domain_decomposition_methods]] — разбиение краевой задачи на подзадачи в подобластях; таксономия overlapping/non-overlapping, one-level/two-level
- [[ddm_convergence_and_time]] — факторы сходимости (число обусловленности) и общая формула вычислительной сложности (таймингов) DDM
- [[schwarz_alternating_method]] — старейший DD-метод: поочерёдное решение в перекрывающихся подобластях; мультипликативный, аддитивный и restricted-варианты
- [[schur_complement_substructuring]] — оператор Пуанкаре–Стеклова на интерфейсе, дискретное дополнение Шура S и семейство методов Дирихле–Нейман / Нейман–Нейман
- [[abstract_schwarz_framework]] — разложение пространства на подпространства, сумма проекторов $P = \sum_i P_i$ и оценка $\kappa(P)$ через константу устойчивого разложения $C_0^2$
- [[coarse_spaces_two_level_methods]] — почему без глобального уровня $\kappa$ растёт как $H^{-2}$, и как строится грубое пространство — от кусочно-линейного через ядра локальных операторов к спектральному (GenEO), где константа назначается, а не выводится
- [[optimized_schwarz_transmission_conditions]] — передача выпуклой комбинации Дирихле- и Нейман-данных через интерфейс (условие Робена) вместо чистого следа
- [[probabilistic_domain_decomposition]] — формула Фейнмана–Каца даёт значения решения в отдельных точках интерфейса без решения всей задачи, что полностью развязывает подобласти
- [[dual_primal_ddm]] — методы FETI-DP и BDDC; строгая сшивка по углам/граням (primal) и слабая по рёбрам (dual)
- [[mortar_methods]] — методы стыковых элементов; слабая сшивка несовпадающих сеток через множители Лагранжа

### Numerical Analysis — многосеточные методы
- [[multigrid_general_theory]] — мета-формула подпространственных коррекций, тождества Сюя–Зикатанова и двухсеточное тождество; число обусловленности как функционал грубого подпространства — и границы, где эта картина перестаёт работать
- [[multigrid_methods]] — иерархия уровней, на каждом из которых релаксация гасит то, чего не представляет грубая поправка; формальное определение цикла, условия линейной стоимости и систематика семейства — от геометрического multigrid до решателей для графовых лапласианов
- [[algebraic_two_grid_methods]] — двухуровневый предобусловливатель как приближённое блочное исключение: идеальная интерполяция и дополнение Шура, обобщённая форма Узавы, и три способа обойтись без них — назначить константу, измерить её или минимизировать при ограничении на разреженность

### Numerical Analysis — прочее

- [[moscow_problem]] — Московская проблема: источники, решения ранга 2 и доказательство спектральной оценки для всех положительных весов K4 с коэффициентом 5.75877 < 6
- [[dynamic_mode_decomposition]] — линейный оператор, подогнанный по парам снапшотов; его спектр приближает спектр Купмана — и почему он почти нечувствителен к качеству подпространства
- [[tensor_train_decomposition]] — цепочка ядер с bond-рангами; хранение $\Theta(d r^2 n^{1/d})$ вместо $\Theta(n)$, и когда это действительно выигрывает
- [[physics_informed_neural_networks]] — аппроксимация решения УрЧП нейросетью через residual loss; ошибка аппроксимации vs. ошибка оптимизации и роль NTK
- [[tensor_tensor_products]] — третьепорядковые тензоры как линейные операторы над свободным модулем трубчатых скаляров; t-product через FFT и его обобщение на любое обратимое преобразование
- [[randomized_linear_algebra]] — случайное скетчирование как способ заменить полный доступ к матрице оценкой: низкоранговые факторизации, Kaczmarz-типа решатели, скетчированный Арнольди
- [[matrix_free_finite_elements]] — действие оператора пересчитывается на лету из поэлементных данных через sum factorization; почему это выигрывает на GPU и что стоит поперёк
- [[differentiable_solvers]] — решатель как чистая функция в JAX/PyTorch: градиенты сквозь весь пайплайн открывают обратные задачи, solver-in-the-loop и field-level inference

## Models

## Project Ideas

### HCM — Hierarchical Context Memory
- [[agents_context_representation/index]] — суть проекта: локальный MCP-сервер с персистентной многоуровневой памятью поверх кодовой базы (статус-кво → проблема → точки улучшения → решение → критерии успеха)
- [[agents_context_representation/roadmap]] — высокоуровневые goals и фичи (built / в MVP / предложенные из литературы 2026)
- [[agents_context_representation/evidence]] — proof of concept: обоснование идей проекта статьями coding-агентов 2026 (академический разбор)

### Numerical Analysis — Domain Decomposition: UAF-DDM Project
- [[ddm_unified_framework/index]] — суть проекта: единый функционал $\mathcal{F}$, связывающий сходимость и вычислительную сложность (статус-кво → проблема → решение)
- [[ddm_unified_framework/roadmap]] — roadmap развития математического аппарата и Auto-DDM
- [[ddm_unified_framework/theory_and_derivation]] — алгебра примитивов и механизм математического вывода спектральных оценок
- [[ddm_unified_framework/cost_model]] — аппаратная модель стоимости $Cost(\mathcal{G})$ и единое оптимизационное уравнение
- [[ddm_unified_framework/algorithms_derivations]] — строгий вывод $\kappa$ и стоимости для 15 алгоритмов через Derivation Engine

## Archived
