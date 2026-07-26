---
title: "UAF-DDM: Функционал стоимости и Оптимизация"
description: "Математическая модель вычислительной стоимости (Cost Model), объединяющая затраты на флопсы, память, сеть и синхронизации GPU в единое уравнение времени"
type: concept
tags: [numerical-analysis, pde, domain-decomposition, performance, hpc]
status: in-progress
created: 2026-07-26
updated: 2026-07-26
sources: []
---

# UAF-DDM: Функционал стоимости и Оптимизация

Фундаментальная идея UAF-DDM заключается в том, что теоретически идеальный метод по числу итераций (с минимальным $\kappa$) часто является самым медленным на практике из-за стоимости глобальных операций. Чтобы решить эту проблему, мы строим **Cost Model** (модель стоимости) для любого графа $\mathcal{G}$, собранного из наших примитивов.

## 1. Единое уравнение времени (Time-to-Solution)

Для сгенерированного графа $\mathcal{G}$, время решения раскладывается на:
$$ Cost(\mathcal{G}) = T_{setup}(\mathcal{G}) + N_{iter}(\kappa(\mathcal{G})) \times T_{step}(\mathcal{G}) $$

Функция $N_{iter}(\dots)$ берется из теоретического предсказания (Абстрактный Шварц, см. [[theory_foundation]]). Аппаратная модель концентрируется на вычислении $T_{setup}$ и $T_{step}$.

## 2. Стоимость базовых примитивов на профиле железа $\mathcal{H}$

Аппаратный профиль $\mathcal{H}$ задается параметрами: $\pi$ (FLOPS), $\beta$ (Memory Bandwidth), $L_{net}$ (Network Latency), $B_{net}$ (Network Bandwidth), $L_{sync}$ (Kernel Launch/GPU Sync Latency).

Для каждого примитива в графе вычисляется его стоимость:
*   **Локальный решатель $\mathcal{S}_i$**:
    - Если $\mathcal{S}_i$ — прямая факторизация: $Cost(\mathcal{S}_i) \approx \frac{N_{local}^{1.5}}{\pi} + L_{sync}$ (для 2D).
    - Если $\mathcal{S}_i$ — итерационный multigrid: $Cost(\mathcal{S}_i) \approx \frac{N_{local}}{\beta} + k \cdot L_{sync}$.
*   **Грубое пространство $\mathcal{S}_0$**:
    - Стоимость глобальной MPI-редукции и решения матрицы размера $N_{sub} \times N_{sub}$:
      $Cost(\mathcal{S}_0) \approx \frac{N_{sub}^3}{\pi} + L_{net} \log(P)$.
*   **Операторы $R_i, R_i^T, D_i$**:
    - Стоимость лимитируется памятью: $Cost(R_i) \approx \frac{|V_{overlap}|}{\beta} + L_{sync}$.
*   **Цикл Крылова $\mathcal{K}$**:
    - Накладные расходы на глобальные скалярные произведения: $Cost(\mathcal{K}) \approx 2 \cdot L_{net} \log(P) + L_{sync}$.

## 3. Architecture-Aware Cost Refinements

Стоимость примитивов из §2 — это нижние границы. Реальная производительность определяется топологией графа $\mathcal{G}$ и архитектурой $\mathcal{H}$.

### 3.1. Topology Penalty: множитель $L_{sync}$

Топология сборки операторов $\mathcal{S}_i$ определяет число последовательных синхронизаций:

| Топология | Формула $\mathcal{P}^{-1}$ | Множитель $L_{sync}$ |
|---|---|---|
| Аддитивная (Parallel) | $\sum R_i^T \mathcal{S}_i R_i$ | $\times 1$ |
| Мультипликативная (Sequential) | $\prod (I - R_i^T \mathcal{S}_i R_i A)$ | $\times N_c$ (число цветов графа) |
| Двухуровневая (Hybrid) | $R_0^T \mathcal{S}_0 R_0 + \sum R_i^T \mathcal{S}_i R_i$ | $\times 2$ (local + coarse) |

**Следствие.** При $N_c \gg 1$ мультипликативная топология порождает $T_{step} \geq N_c \cdot L_{sync}$, что делает метод неработоспособным на GPU даже при $N_{iter} = 1$. Это **алгебраическое объяснение** того, почему Multiplicative Schwarz и Dirichlet-Neumann непригодны для GPU.

### 3.2. Kernel Fusion (GPU-specific)

Если соседние аддитивные примитивы ($R_i^T, \mathcal{S}_i, R_i, D_i$) компилируются в единое GPU-ядро (Kernel Fusion), то $L_{sync}$ суммируется не для каждого примитива, а однократно для всего fused-блока.

В формуле стоимости это означает замену:
$$\sum_{\text{primitives}} L_{sync} \quad \longrightarrow \quad |\text{fused blocks}| \cdot L_{sync}$$

Функционал стоимости явно поощряет графы $\mathcal{G}$, поддающиеся такому слиянию (аддитивные топологии).

> **Замечание.** Kernel Fusion — это инженерная оптимизация, не влияющая на математические оценки $\kappa$. Она влияет только на $T_{step}$ в Cost Model.

## 4. Оптимизационная задача (Auto-DDM)

Поиск оптимального метода DDM сводится к решению задачи математического программирования на графе примитивов:

$$ \min_{\mathcal{G} \in \mathbb{G}} \left( T_{setup}(\mathcal{G}; \mathcal{H}) + \frac{\sqrt{\kappa(\mathcal{G})}}{2} \ln\left(\frac{2}{\epsilon}\right) \times T_{step}(\mathcal{G}; \mathcal{H}) \right) $$

Где $\mathbb{G}$ — пространство всех допустимых вычислительных графов (DAG) декомпозиции.
Решая эту задачу (аналитически для простых случаев или методами машинного обучения для сложных), UAF-DDM способен **автоматически открыть** метод FETI-DP для распределенных систем с высоким $L_{net}$ или предложить новый гибридный метод для мощных GPU с тензорными ядрами ($\pi \to \infty$).

## 5. Proof-of-Concept: Оптимальная декомпозиция для 1D Пуассона

**Задача.** $-u'' = f$ на $[0,1]$, $n$ DOF, двухуровневый AS с перекрытием $\delta = h$.

**Параметры.** $N$ подобластей, $N_{loc} = n/N$ DOF в каждой, coarse space размером $N$.

**Число итераций.** Из абстрактной теоремы Шварца для AS-2 с $\delta = h$:
$$\kappa = O(1 + H/\delta) = O(n/N) \quad \implies \quad N_{iter} = O\left(\sqrt{n/N} \cdot \ln(2/\epsilon)\right)$$

**Стоимость шага.** На профиле $\mathcal{H}$ с параметрами $\pi$ (FLOPS), $\beta$ (Memory BW), $L_{net}$ (Network Latency):
$$T_{step} = \underbrace{\frac{n/N}{\beta}}_{T_{local}} + \underbrace{\frac{N^3}{\pi} + L_{net}\log N}_{T_{coarse}}$$

(Для 1D: локальное решение memory-bound, coarse solve — dense $N \times N$ матрица.)

**Функционал стоимости:**
$$Cost(N) = \sqrt{n/N} \cdot \ln(2/\epsilon) \cdot \left(\frac{n/N}{\beta} + \frac{N^3}{\pi} + L_{net}\log N\right)$$

**Оптимум.** Балансируя $T_{local} = T_{coarse}$ (при $L_{net}\log N \ll N^3/\pi$):
$$\frac{n/N}{\beta} = \frac{N^3}{\pi} \quad \implies \quad N^* = \left(\frac{n\pi}{\beta}\right)^{1/4}$$

**Проверка предельных случаев:**

| Предел | $N^*$ | Интерпретация |
|---|---|---|
| $L_{net} \to \infty$ | $N^* \to 1$ | Сеть — узкое горлышко → единый прямой решатель |
| $\pi \to \infty$ | $N^* \to \infty$ | Бесконечно быстрый процессор → дробить мельче |
| $\beta \to \infty$ | $N^* \to 0$ (т.е. $N^*=1$) | Бесконечная пропускная способность памяти → coarse solve доминирует → меньше подобластей |
| $n \to \infty$ | $N^* \propto n^{1/4}$ | Субоптимальный рост числа подобластей |

**Пример.** Для $n = 10^6$, $\pi = 10^{12}$ FLOPS, $\beta = 10^{11}$ B/s:
$$N^* = \left(\frac{10^6 \cdot 10^{12}}{10^{11}}\right)^{1/4} = (10^7)^{1/4} \approx 56$$

Это число подобластей разумно для задачи такого размера.

> **Значение.** Этот результат демонстрирует, что функционал UAF-DDM способен давать аналитические предсказания для оптимальной конфигурации DDM. Формула $N^* = (n\pi/\beta)^{1/4}$ — **новый результат**, не встречающийся в стандартной литературе DDM.
