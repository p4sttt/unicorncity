# Wiki Log

## [2026-07-12] init | Wiki initialized
Schema written to CLAUDE.md. Directories created: wiki/concepts/, wiki/papers/, wiki/models/, raw/assets/.

## [2026-07-12] ingest | 5 papers from raw/papers/inbox

Added:
- papers/eam_enhancing_anything_with_diffusion_transformers.md
- papers/context_folding_scaling_llm_agents.md
- papers/darwinian_memory_system_gui_agents.md
- papers/agent_omit_adaptive_context_omission.md
- papers/se_ga_self_evolving_gui_agent.md

Added (concepts):
- concepts/context_management_llm_agents.md
- concepts/gui_agents_memory.md

Updated: index.md

## [2026-07-12] ingest | Recursive Language Models

Added: papers/recursive_language_models.md
Updated: index.md, concepts/context_management_llm_agents.md (wikilink добавлен в related work)

## [2026-07-13] ingest | Stacked Borrows + Tree Borrows (Rust aliasing models)

Sources:
- raw/papers/inbox/paper.pdf → raw/papers/processed/stacked_borrows_popl2020.{pdf,md}
- raw/papers/inbox/3735592.pdf → raw/papers/processed/tree_borrows_pldi2025.{pdf,md}

Added:
- papers/stacked_borrows.md
- papers/tree_borrows.md
- concepts/rust_aliasing_model.md

Updated: index.md (добавлена секция PL — Rust Aliasing в Papers и Concepts)

## [2026-07-13] query | HCM MVP implementation plan
Filed: agents_context_representation/mvp_implementation_plan.md — build-vs-buy, 6 этапов, критерии и тест-план
Updated: index.md

## [2026-07-13] query | HCM MVP plan reworked for Java / Spring Boot
Updated: agents_context_representation/mvp_implementation_plan.md — стек переведён на Java (JavaParser+SymbolSolver, JGraphT, Spring AI MCP), добавлен этап Spring-семантики (DI/JPA/Kafka), data_flow-запрос в MVP; index.md

## [2026-07-13] query | HCM MVP plan: сервер возвращён на Python, цель — Java/Spring
Updated: agents_context_representation/mvp_implementation_plan.md — Python-стек (FastMCP, tree-sitter-java, networkx, Qdrant local, fastembed); собственный resolver по объявленным типам вместо JavaSymbolSolver, метрика UNRESOLVED + escape hatch на JavaParser-sidecar; Spring-семантика и data_flow сохранены; index.md

## [2026-07-14] query | HCM MVP plan v3: провайдерная архитектура, Spring вне MVP, добавлен doc-поиск
Updated: agents_context_representation/mvp_implementation_plan.md — интерфейс LanguageProvider/SemanticEnricher + языко-нейтральный FileIR (тест изоляции ядра); Spring-семантика и data_flow перенесены в расширения; новый этап 5 — семантический поиск по документации (md + javadoc, инструмент search_docs) как MVP-прокси Level 2; index.md

## [2026-07-19] ingest | Coding-agent exploration & localization (6 papers)
Added:
- papers/code_isnt_memory_structural_index.md
- papers/codebase_memory_tree_sitter_kg.md
- papers/harness_handbook.md
- papers/fastcontext.md
- papers/sherloc.md
- papers/swe_explore.md
- concepts/repository_exploration_coding_agents.md
- concepts/structural_codebase_index.md
Updated:
- index.md (новая секция Papers «LLM Agents — Coding: Exploration & Localization»; 2 концепта в Agents)
- agents_context_representation/index.md (секция «Эмпирическая валидация» — 6 статей как подтверждение архитектуры)
Moved: 6 pdf+md пар inbox/ → processed/; удалён дубликат «...(1).pdf»

## [2026-07-19] query | HCM project restructure + grounding в литературе
Filed: agents_context_representation/{index,roadmap,evidence}.md
Removed: agents_context_representation/mvp_implementation_plan.md (перенесён в репозиторий проекта ~/src/hierarchical_context_memory/)
Updated: wiki/index.md (Project Ideas — три файла вместо двух)
index.md переписан в 6-секционную суть (статус-кво/проблема/точки улучшения/решение/покрытие/критерии); roadmap.md — goals+фичи (built/proposed P1–P7); evidence.md — академический PoC на 6 статьях

## [2026-07-26] ingest | Domain decomposition + двухсеточные методы (16 papers)
Added:
- papers/lions_schwarz_alternating_i.md
- papers/lions_schwarz_alternating_ii.md
- papers/lions_schwarz_alternating_iii.md
- papers/dryja_widlund_unified_theory.md
- papers/widlund_iterative_substructuring.md
- papers/chan_resasco_dd_preconditioners_framework.md
- papers/marini_quarteroni_relaxation_dd.md
- papers/israeli_hierarchical_dd.md
- papers/kuznetsov_distributed_lagrange_multipliers.md
- papers/acebron_spigler_probabilistic_dd.md
- papers/acebron_spigler_scalable_parallel_elliptic.md
- papers/kim_yang_dd_neural_network.md
- papers/scherbakov_rakhimov_classic_iterative_methods.md
- papers/subspace_uzawa_two_grid.md
- papers/two_grid_entrywise_certificate.md
- papers/streaming_tt_dmd.md
- concepts/domain_decomposition_methods.md
- concepts/schwarz_alternating_method.md
- concepts/schur_complement_substructuring.md
- concepts/abstract_schwarz_framework.md
- concepts/coarse_spaces_two_level_methods.md
- concepts/optimized_schwarz_transmission_conditions.md
- concepts/probabilistic_domain_decomposition.md
- concepts/algebraic_two_grid_methods.md
- concepts/dynamic_mode_decomposition.md
- concepts/tensor_train_decomposition.md
- concepts/physics_informed_neural_networks.md
Updated:
- index.md (3 новые секции Papers: DD классика / DD варианты и приложения / двухсеточные и потоковые; 2 новые секции Concepts)
Moved: 16 pdf inbox/ → processed/ (+10 .md конвертаций)
Заметки: 6 PDF — сканы без текстового слоя (Lions I/II/III, Dryja–Widlund, Widlund, Chan–Resasco),
markitdown дал пустой вывод; прочитаны визуально постранично, .md-конвертаций для них нет.
Israeli.pdf и Kuznetsov.pdf сконвертировались с битой кодировкой лигатур — тоже читались визуально.
Новая для вики предметная область: численные методы. Пересечений с существующими страницами
(qmd search по 7 запросам) не найдено — все страницы созданы с нуля.

## [2026-07-26] ingest | Тензорные алгебры, рандомизированная ЛА, HPC-решатели (17 papers)
Added:
- papers/klus_tensor_based_dmd.md
- papers/he_tensor_dmd_tproduct.md
- papers/saibaba_star_m_dmd.md
- papers/katrutsa_dmd_mori_zwanzig.md
- papers/braman_third_order_tensors_operators.md
- papers/kernfeld_kilmer_aeron_tensor_products.md
- papers/smith_adaptive_matrix_free_lowrank.md
- papers/xiao_rplss.md
- papers/guettel_sketch_and_restart.md
- papers/gillman_librla.md
- papers/andersson_appelo_sublinear_lowrank_poisson.md
- papers/baker_scaling_hypre_100k_cores.md
- papers/wichrowski_coalesced_matrix_free_fe.md
- papers/scroggs_wells_dof_transformations.md
- papers/long_task_based_red_black_gauss_seidel.md
- papers/horowitz_jax_geometric_multigrid_pm.md
- papers/toshev_jax_sph.md
- concepts/tensor_tensor_products.md
- concepts/randomized_linear_algebra.md
- concepts/multigrid_methods.md
- concepts/matrix_free_finite_elements.md
- concepts/differentiable_solvers.md
Updated:
- index.md (3 новые секции Papers, 5 концептов)
- concepts/dynamic_mode_decomposition.md (4 новые статьи + таблица выбора тензорного варианта)
- concepts/tensor_train_decomposition.md (базовая работа Klus; блок Related)
- concepts/algebraic_two_grid_methods.md, coarse_spaces_two_level_methods.md (ссылки на multigrid_methods, hypre)
- concepts/physics_informed_neural_networks.md (ссылка на differentiable_solvers)
- papers/scherbakov_rakhimov_classic_iterative_methods.md (ссылки на differentiable_solvers, hypre)
Moved: 17 pdf+md пар inbox/ → processed/
Заметки: партия добавлена пользователем в inbox уже во время обработки первой партии; обработана
по подтверждению. Все 17 сконвертировались с текстовым слоем, сканов нет. 1117924.pdf (hypre)
конвертировался со слипшимися пробелами — читался программной переразбивкой, не визуально.

## [2026-07-26] rewrite | Многосеточные методы: формализация и общая теория
Added:
- concepts/multigrid_general_theory.md
Updated:
- concepts/multigrid_methods.md (полностью переписан: формальное определение цикла, принцип
  дополнительности через $K_{\mathrm{TG}}$, условие $\gamma c < 1$ линейной стоимости,
  систематика семейства — GMG, C/F, агрегация, редукция/AIR, энергетическая минимизация,
  спектральные, адаптивные/bootstrap, компатибельная релаксация, обучаемые продолжения,
  графовые лапласианы, вспомогательные пространства, FAS, MGRIT)
- concepts/algebraic_two_grid_methods.md (переписан: блочное исключение, идеальная
  интерполяция $P_* = (-A_{ff}^{-1}A_{fc}; I)$ и дополнение Шура как источник всей
  конструкции; три ветви — назначить/измерить/оптимизировать; компатибельная релаксация;
  что ломает рекурсия)
- concepts/coarse_spaces_two_level_methods.md (переписан в связную прозу; спектральная
  конструкция подана как локализация точного ответа общей теории)
- concepts/abstract_schwarz_framework.md (секция «от неравенства к тождеству»)
- index.md (новая секция Concepts «Numerical Analysis — многосеточные методы», 3 записи
  с обновлёнными описаниями)

Ресёрч (внешние источники, в вики как paper-summary пока не заведены): лемма о фиктивном
пространстве Непомнящих 1991 / Xu 1996; Xu SIAM Rev. 1992; тождество Xu–Zikatanov JAMS 2002;
двухсеточное тождество Falgout–Vassilevski–Zikatanov NLAA 2005 и Zikatanov NLAA 2008;
Xu–Zikatanov Acta Numerica 2017; Napov–Notay NLAA 2011 / SISC 2012; Brannick–Falgout SISC 2010;
Manteuffel–Ruge–Southworth ($\ell$AIR) SISC 2018; Ali et al. SISC 2025 (несимметричный случай);
Moussa–Kahl arXiv:2603.26513 (релаксационная теория через Мори–Цванцига); Kyng–Sachdeva FOCS 2016;
Greenfeld ICML 2019, Luz ICML 2020, Taghibakhshi NeurIPS 2021 (обучаемые продолжения).

Тезис, вокруг которого выстроена новая страница: мета-формула $B = \Pi\tilde B\Pi^{\mathsf T}$
с вариационным представлением обратного существует и покрывает всё семейство; двухсеточное
тождество показывает, что $\|E_{\mathrm{TG}}\|_A$ зависит от $P$ только через
$\operatorname{range}(P)$, а оптимальное грубое пространство — собственные векторы пучка
$(A, \tilde M)$. Отсутствует не теория сходимости, а теория аппроксимации грубого пространства
при ограничении на разреженность, плюс многоуровневая композиция и несимметричный случай.

## [2026-07-26] query | Research missing DDM algorithms and convergence theory
Filed: concepts/dual_primal_ddm.md, concepts/mortar_methods.md

## [2026-07-26] query | DDM convergence and total execution time formula
Filed: concepts/ddm_convergence_and_time.md

## [2026-07-26] query | Proposal for unified DDM complexity framework
Filed: proposals/ddm_unified_framework_proposal.md

## [2026-07-26] query | Structured UAF-DDM project directory
Added: ddm_unified_framework/index.md, ddm_unified_framework/roadmap.md
Updated: proposals/ddm_unified_framework_proposal.md (redirect)

## [2026-07-26] ingest | UAF-DDM Math Framework and Cost Model
Added: ddm_unified_framework/theory_foundation.md, ddm_unified_framework/cost_model.md

## [2026-07-26] query | Validate UAF-DDM with 10 classic algorithms
Added: ddm_unified_framework/validation_10_algorithms.md

## [2026-07-26] ingest | UAF-DDM Derivation Engine
Added: ddm_unified_framework/derivation_engine.md, ddm_unified_framework/validation_15_algorithms_derivations.md
Updated: ddm_unified_framework/validation_10_algorithms.md (redirect)

## [2026-07-26] lint | Refactoring UAF-DDM Theory and Derivations
Added: ddm_unified_framework/theory_and_derivation.md, ddm_unified_framework/algorithms_derivations.md
Updated: ddm_unified_framework/theory_foundation.md (redirect), ddm_unified_framework/derivation_engine.md (redirect), ddm_unified_framework/validation_15_algorithms_derivations.md (redirect), ddm_unified_framework/validation_10_algorithms.md (redirect)

## [2026-07-26] query | Expand theory and add 5 new algorithms
Updated: ddm_unified_framework/theory_and_derivation.md (added Asynchrony, Neural spaces), ddm_unified_framework/algorithms_derivations.md (added Async-AS, GenEO, Neural-DDM, Parareal, Lumped FETI-DP)

## [2026-07-26] lint | Expert fixes and architecture separation
Updated: ddm_unified_framework/index.md, ddm_unified_framework/roadmap.md, ddm_unified_framework/cost_model.md, ddm_unified_framework/algorithms_derivations.md, ddm_unified_framework/theory_and_derivation.md
Fixed: Corrected dimensionless $\kappa$ bounds, added literature citations, formalized async trade-off (Chazan & Miranker), removed Neural-DDM, moved Kernel Fusion to Cost Model, added 1D Poisson Proof-of-Concept.
