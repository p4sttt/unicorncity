Domain Decomposition Algorithms
for Neural Network Approximation
of Partial Diﬀerential Equations

Hyea Hyun Kim and Hee Jun Yang

1 Introduction

With the success of deep learning technology in many application areas, there have
been pioneering approaches to approximate solutions of partial diﬀerential equations
by neural network functions [2, 10, 12, 13]. Such approaches have advantages over
the classical approximation methods in that they can be used without generating
meshes adaptive to problem domains or developing equation dependent numerical
schemes. However, its accuracy, stability, and eﬃciency questions have not yet been
fully answered. In addition, long training time makes the neural network solution
very expensive.

To enhance the neural network solution accuracy, large or deep neural network
functions are usually employed. When training parameters in such large or deep
neural networks, the optimization error becomes problematic to pollute the resulting
computed solution accuracy. To address this issue in the neural network approxima-
tion, we approximate the solution by using partitioned local neural network functions.
For that we ﬁrst form an iterative scheme based on domain decomposition methods
and we then ﬁnd local neural network functions that approximate the local problem
solutions at each iteration. Contrary to the single large or deep neural network case,
the local neural network parameter training can be done more eﬃciently with less
optimization errors.

There have been previous studies that utilize domain decomposition algo-
rithms [14] to enhance the neural network eﬃciency and accuracy. In [8, 9], al-
ternating Schwarz algorithms were developed to second order elliptic problems and
in the author’s previous study [6], additive Schwarz algorithms were proposed to

Hyea Hyun Kim
Department of Applied Mathematics and Institute of Natural Sciences, Kyung Hee University,
Korea, e-mail: hhkim@khu.ac.kr

Hee Jun Yang
Department of Mathematics, Kyung Hee University, Korea, e-mail: yhjj109@khu.ac.kr

27

28

Hyea Hyun Kim and Hee Jun Yang

the same model problems, where the neural network functions are formed based on
overlapping subdomain partitions. In both approaches, the proposed methods showed
promising results but concrete convergence study has not been fully considered.
In [4, 5], partitioned neural network functions are formed based on a non-overlapping
subdomain partition and the global cost function is formed to train the parameters in
the partitioned neural network functions. In their approach, the communication cost
between local neural networks becomes enormous, since the number of epochs in the
parameter training easily becomes more than several tens of thousands in practice.
In the author’s recent work [7], a concrete convergence analysis on one-level
and two-level additive Schwarz algorithms was provided with an assumption on the
approximation error in the local and coarse neural network solutions. The numerical
results on the one-level method are consistent with the convergence analysis. How-
ever, those on the two-level methods show that the coarse problem does not help to
accelerate the convergence and it even pollutes the solution accuracy. By the NTK
(Neural Tangent Kernel) theory [3, 15], when training the parameters in the neural
network approximation, the smooth part of solutions is well approximated and the
residual loss for the diﬀerential equation is well trained than that for the bound-
ary condition. The local neural network solution errors in our proposed method thus
showed high contrast errors near the subdomain boundary that resulted a less smooth
global error during the iteration. The proposed coarse problem in [7] was not suitable
to correct such a non-smooth global error.

In this work, we propose a partitioned neural network by utilizing a partition
of unity functions and we then apply the additive Schwarz algorithm to propose
an iterative solution procedure on the partitioned neural network functions, where
local neural network parameters are trained to approximate local problem solutions
at each iteration. When training the local parameters, only the residual loss for the
diﬀerential equation in each subdomain problem comes in the cost function, and the
boundary condition is enforced directly by multiplying the partition of unity function
as an ansatz to the local neural network function. With this idea, the optimization
error can be reduced when training the local parameters at each iteration compared to
the approaches in [7]. As reported in our previous work [7], the coarse problem in the
two-level method did not work due to the high contrast optimization errors observed
near the boundary of subdomain overlapping region. By utilizing the partition of
unity functions in forming the partitioned neural network approximation, we can
remove such error problems and the coarse problem in the two-level method is thus
expected to work more eﬀectively. Such a partitioned neural network function using
ansatz was ﬁrst proposed in [11] with the aim of obtaining a more accurate neural
network approximation to highly oscillatory solutions.

This paper is organized as follows. In Section 2, we introduce neural network
approximation methods for solving partial diﬀerential equations and in Section 3
we propose one-level and two-level additive Schwarz algorithms for the partitioned
neural network functions, where we present the two methods in our previous work [7]
and extend those methods to the partitioned neural network functions. In Section 4,
numerical results are presented for model elliptic problems and conclusions are
given.

DD Algorithms for Neural Network Approximation

29

2 Neural network approximation for partial diﬀerential

equations

Among several neural network approaches to solutions of partial diﬀerential equa-
tions, we will consider the PINN (Physics Informed Neural Network) method by [12].
Our domain decomposition approach can be applied to other neural network ap-
proximation methods by [2, 10, 13] as well. In the PINN methods, the solution is
approximated with a neural network function 𝑈 (𝑥; 𝜃) and the parameters 𝜃 in the
neural network function are trained to solve supervised learning tasks in order to
satisfy any given laws of physics described by partial diﬀerential equations,

L (𝑢) = 𝑓 ,

in Ω, B (𝑢) = 𝑔,

on 𝜕Ω,

(1)

where L denotes a diﬀerential operator deﬁned for a function 𝑢 and B describes
a given boundary condition on 𝑢, and 𝑓 , 𝑔 are given functions.

We assume that the model problem in (1) is well-posed and the solution 𝑢 exists.
We then approximate the solution 𝑢 in (1) by a neural network, 𝑈 (𝑥; 𝜃), where the
parameters 𝜃 are trained to minimize the cost function

J (𝜃) = J𝑋Ω (𝜃) + J𝑋𝜕Ω (𝜃),

where

J𝑋Ω (𝜃) :=

1
|𝑋Ω|

∑︁

|L (𝑈 (𝑥; 𝜃)) − 𝑓 (𝑥)|2,

J𝑋𝜕Ω (𝜃) :=

|B (𝑈 (𝑥; 𝜃)) − 𝑔(𝑥)|2.

𝑥 ∈𝑋Ω
∑︁

𝑥 ∈𝑋𝜕Ω

1
|𝑋𝜕Ω|

In the above, 𝑋𝐷 denotes the collection of points chosen from the region 𝐷 and |𝑋𝐷 |
denotes the number of points in the set 𝑋𝐷. The cost function J𝑋Ω (𝜃) and J𝑋𝜕Ω (𝜃)
are designed so that the optimized neural network 𝑈 (𝑥; 𝜃) satisﬁes the equations
in (1) derived from physics laws. When training the parameters 𝜃, the following
gradient based method is used,

𝜃 (𝑛+1) = 𝜃 (𝑛) − 𝜖 ∇𝜃 J (𝜃 (𝑛) )

for a given initial 𝜃 (0) and with a suitable learning rate 𝜖. Each gradient update step
is called an epoch and usually more than several hundreds of thousand epochs are
needed in such neural network approximation methods. Overall computation cost in
the PINN is thus very expensive compared to the classical approximation methods.
The error between the exact solution 𝑢(𝑥) and the computed neural network solu-
tion 𝑈 (𝑥; (cid:101)𝜃) can be analyzed as follows. Letting 𝑈 (𝑥; 𝜃∗) be the optimal approximate
solution, we obtain

𝑢(𝑥) − 𝑈 (𝑥; (cid:101)𝜃) = (𝑢(𝑥) − 𝑈 (𝑥; 𝜃∗)) + (𝑈 (𝑥; 𝜃∗) − 𝑈 (𝑥; (cid:101)𝜃)),

30

Hyea Hyun Kim and Hee Jun Yang

where the ﬁrst term in the right hand side is called the approximation error and
the second is the optimization error. The approximation error can be controlled by
enlarging the network size, while the optimization error is diﬃcult to deal with. The
optimization error depends on how to choose the training data set, how to form the
loss functions, and how to perform the gradient based method.

In [11], it was numerically veriﬁed that for highly oscillatory model solutions
PINN requires larger neural network functions and larger training epochs to increase
the approximation solution accuracy. Such approximation property in the PINN was
also analyzed by the NTK (Neural Tangent Kernel) theory, see [15]. To enhance
the training eﬃciency and accuracy, in [11], the approximate solution is formed by
using partitioned neural network functions with a much lesser number of parameters
in each local neural network function than those in the single large neural network
function. When a highly oscillatory solution is localized to a small subdomain, it
becomes less oscillatory and thus it can be well approximated with a smaller neural
network function. The parameter training cost in a smaller neural network function
also becomes much smaller than that in the single larger neural network function. By
utilizing the partitioned neural network functions, we thus expect that for diﬃcult
model problems we can reduce both the approximation error and the optimization
error more eﬀectively than just using a single large neural network function. In
addition, utilizing the parallel computing resources, we can even make our one-level
and two-level methods much more eﬃcient than the single neural network case.

3 Additive Schwarz algorithms for neural network

approximation

In this section, we ﬁrst review the one-level and two-level additive Schwarz algo-
rithms that were proposed in our previous work [7] and their convergence results
under the approximation error assumption on each local and coarse neural network
solutions. We then introduce a partitioned neural network function to approximate
the solution and propose iterative methods on the partitioned neural network function
to ﬁnd the convergent iterates to the solution. The iteration methods can be analyzed
as the same way in our previous study [7] to give the same convergence result. As we
will see in the numerical results later, the partitioned neural network function gives
less optimization errors and thus it gives faster convergence than in the previous
work [7].

Our method is developed for the following model elliptic problem in a bounded

domain Ω, i.e., to ﬁnd 𝑢 in the Hilbert space 𝐻1(Ω) satisfying

−(cid:52)𝑢 = 𝑓 in Ω,

𝑢 = 𝑔 on Ω,

(2)

where 𝐻1 (Ω) denotes the space of square integrable functions up to the ﬁrst deriva-
tives. In the one-level additive Schwarz method, for a given overlapping subdomain
partition,{Ω𝑖 }𝑖 of the domain Ω, with an overlapping width 𝛿, the following iterative

DD Algorithms for Neural Network Approximation

31

scheme is proposed to ﬁnd its solution 𝑢. For a given 𝑢 (𝑛) , the following problem in
each subdomain Ω𝑖 is solved to ﬁnd 𝑢 (𝑛+1)
,

𝑖

−(cid:52)𝑢 (𝑛+1)
𝑖

= 𝑓 in Ω𝑖,

𝑢 (𝑛+1)
𝑖

= 𝑢 (𝑛) in Ω \ Ω𝑖.

(3)

Using 𝑢 (𝑛+1)

𝑖

, the next iterate is then formed to give

𝑢 (𝑛+1) = (1 − 𝑁𝜏)𝑢 (𝑛) + 𝜏

𝑁
∑︁

𝑖=1

𝑢 (𝑛+1)
𝑖

,

where 𝑁 is the number of subdomains in the partition and 𝜏 is a relaxation parameter.
Let 𝑁𝑐 be the maximum number of subdomains sharing the same geometric position
in Ω. With 𝜏 ≤ 1/𝑁𝑐, 𝑢 (𝑛) converges to the solution 𝑢 of (2) under a suitably
chosen space of functions, see [14, 16]. The algorithm can be further extended into
a two-level method by introducing the coarse problem,

−(cid:52)𝑤 (𝑛+1)
0

= 𝑓 + (cid:52)𝑢 (𝑛) in Ω, 𝑤 (𝑛+1)

0

= 0 on 𝜕Ω,

and by including the coarse problem solution to the iteration formula,

𝑢 (𝑛+1) = (1 − 𝑁𝜏)𝑢 (𝑛) + 𝜏

(cid:32)(cid:32) 𝑁
∑︁

(cid:33)

𝑢 (𝑛+1)
𝑖

𝑖=1

(cid:33)

.

+ 𝑤 (𝑛+1)
0

In [7], following similarly as in the analysis for the variational inequalities [1],
under the assumptions on the stable decomposition property and the strengthened
Cauchy-Schwarz inequality, see [14, Section 2.3], the iterates 𝑢 (𝑛) converge to the
exact solution 𝑢 with the convergence rate 𝑅(𝜏),

𝑎(𝑢 − 𝑢 (𝑛+1) , 𝑢 − 𝑢 (𝑛+1) ) ≤ 𝑅(𝜏)𝑎(𝑢 − 𝑢 (𝑛) , 𝑢 − 𝑢 (𝑛) ),

(4)

where 𝑎(𝑢, 𝑣) = ∫

Ω

∇𝑢 · ∇𝑣 𝑑𝑥, and 𝑅(𝜏) is

𝑅(𝜏) = 1 −

2
2 + 𝐶0

𝜏 + 𝑁 2

𝑐 𝜏2 and 𝑅(𝜏) = 1 −

2
2 + 𝐶0

𝜏 + 2(𝑁 2

𝑐 + 1)𝜏2

in the one-level case and two-level case, respectively. In the above, the constant 𝐶0 is
that appears in the stable decomposition property. In a more detail, in the one-level
case, the constant 𝐶0 follows the growth of 𝑁𝑐 𝑁 𝐻/𝛿 and in the two-level case,
the constant 𝐶0 follows the growth of 𝑁𝑐 𝐻/𝛿, under the approximation property
assumption on the coarse Hilbert subspace, see [14, Sections 3.5 and 3.6]. Combining
our convergence analysis in (4) with the bound for 𝐶0, we can thus conclude that for
a suitable choice of 𝜏, the iterates 𝑢 (𝑛) converge to 𝑢 in the Hilbert space 𝐻1

0 (Ω),

|𝑢 (𝑛+1) − 𝑢|1 ≤ 𝐶 |𝑢 (𝑛) − 𝑢|1,

32

Hyea Hyun Kim and Hee Jun Yang

with the constant 𝐶 < 1 increasing to 1 as 𝑁 increasing in the one-level case,
while with the constant 𝐶 being robust as 𝑁 increasing in the two-level case. The
convergent rate 𝐶 in the one-level method deteriorates as the more subdomains in
the partition while it is robust to the increase of the number of subdomains in the
two-level method, that have been also observed in additive Schwarz preconditioners
to algebraic systems in classical numerical methods.

To ﬁnd a neural network approximate solution, at each iteration in the additive
Schwarz methods, we approximate the local problem solution and the coarse problem
solution with neural network functions 𝑈𝑖 (𝑥; 𝜃 (𝑛+1)
) and train the
parameters 𝜃 (𝑛+1)
and 𝜃 (𝑛+1)
to minimize the cost functions related to each local
0
problem and the coarse problem, respectively. The neural network iterates 𝑈 (𝑛+1)
are then deﬁned as

) and 𝑊0 (𝑥; 𝜃 (𝑛+1)

0

𝑖

𝑖

𝑈 (𝑛+1) = (1 − 𝑁𝜏)𝑈 (𝑛) + 𝜏

𝑈 (𝑛+1)
𝑖

+ 𝑊 (𝑛+1)
0

(𝑥, 𝜃 (𝑛+1)
0

)

(cid:33)

,

(cid:32) 𝑁
∑︁

𝑖=1

𝑖

(𝑥) are 𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

where 𝑈 (𝑛+1)
) in Ω𝑖 and 𝑈 (𝑛) (𝑥) in the rest part, i.e., Ω \ Ω𝑖. In
the iteration method, we should store all the previous step parameters to obtain the
resulting ﬁnal step solution as a function of 𝑥, which is not desirable in the practical
calculation.

𝑖

To obtain a more practical method, we rewrite the above iteration formula as

follows: for any 𝑥 in Ω

𝑈 (𝑛+1) (𝑥) = (1−|𝑠(𝑥)|𝜏)𝑈 (𝑛) (𝑥)+𝜏 (cid:169)
(cid:173)
𝑖 ∈𝑠 ( 𝑥)
(cid:171)

∑︁

𝑈𝑖 (𝑥, 𝜃 (𝑛+1)
𝑖

) + 𝑊 (𝑛+1)
0

(𝑥, 𝜃 (𝑛+1)
0

, (5)

)(cid:170)
(cid:174)
(cid:172)

where 𝑠(𝑥) denotes the set of subdomain indices sharing 𝑥 and |𝑠(𝑥)| denotes the
number of elements in the set 𝑠(𝑥). We introduce

(cid:98)𝑈 (𝑛+1) (𝑥) :=

1
|𝑠(𝑥)|

∑︁

(cid:169)
(cid:173)
𝑖 ∈𝑠 ( 𝑥)
(cid:171)

𝑈𝑖 (𝑥, 𝜃 (𝑛+1)
𝑖

) + 𝑊 (𝑛+1)
0

(𝑥, 𝜃 (𝑛+1)
0

(6)

)(cid:170)
(cid:174)
(cid:172)

and rewrite the above iteration formula into

𝑈 (𝑛+1) (𝑥) = (1 − |𝑠(𝑥)|𝜏)𝑈 (𝑛) (𝑥) + |𝑠(𝑥)|𝜏 (cid:98)𝑈 (𝑛+1) (𝑥).
For the iterates (cid:98)𝑈 (𝑛+1) (𝑥), they also converge to 𝑢(𝑥) in the 𝐿2-norm, see [7], and
the following practical one-level (without the term 𝑊 (𝑛+1)
in the iteration formula
in (5) and (6)) and two-level additive Schwarz algorithms are ﬁnally obtained:
Algorithm 1: One-level method (input: 𝑈 (0) , output: (cid:98)𝑈 (𝑛+1) )
Step 0: Let 𝑈 (0) (𝑥) be given and 𝑛 = 0.

0

DD Algorithms for Neural Network Approximation

33

Step 1: Find 𝜃 (𝑛+1)

𝑖

in 𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

𝑖

) for

−(cid:52)𝑢 = 𝑓 in Ω𝑖,

𝑢 = 𝑈 (𝑛) on 𝜕Ω𝑖.

Step 2: Update 𝑈 (𝑛+1) at each data set 𝑋𝜕Ω𝑖 as, see (6),

𝑈 (𝑛+1) (𝑥) = (1 − 𝜏|𝑠(𝑥)|)𝑈 (𝑛) (𝑥) + 𝜏|𝑠(𝑥)| (cid:98)𝑈 (𝑛+1) .
Step 3: Go to Step 1 with 𝑛 = 𝑛 + 1 or set the output as (cid:98)𝑈 (𝑛+1) if the stopping
condition is met.
Algorithm 2: Two-level method (input: 𝑈 (0) , output: (cid:98)𝑈 (𝑛+1) )
Step 0: Let 𝑈 (0) (𝑥) be given and 𝑛 = 0.
Step 1-1: Find 𝜃 (𝑛+1)
) for

in 𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

𝑖

𝑖

−(cid:52)𝑢 = 𝑓 in Ω𝑖,

𝑢 = 𝑈 (𝑛) on 𝜕Ω𝑖.

Step 1-2: Find 𝜃 (𝑛+1)

0

in 𝑊0 (𝑥; 𝜃 (𝑛+1)

0

) for

−(cid:52)𝑤 = 𝑓 + (cid:52)𝑈 (𝑛) in Ω, 𝑤 = 0 on 𝜕Ω.

Step 2: Update 𝑈 (𝑛+1) at each data set 𝑋𝜕Ω𝑖 as, see (6),

𝑈 (𝑛+1) (𝑥) = (1 − 𝜏|𝑠(𝑥)|)𝑈 (𝑛) (𝑥) + 𝜏|𝑠(𝑥)| (cid:98)𝑈 (𝑛+1) .

Step 3: Go to Step 1-1 with 𝑛 = 𝑛 + 1 or set the output as (cid:98)𝑈 (𝑛+1) if the stopping
condition is met.

For the neural network iterates 𝑈 (𝑛) and (cid:98)𝑈 (𝑛) , the following convergence results

are shown

|𝑈 (𝑛+1) − 𝑢|1 ≤ |𝑢 (𝑛+1) − 𝑢|1 +

1
1 − 𝐶

𝜖,

(cid:107) (cid:98)𝑈 (𝑛+1) − 𝑢(cid:107)0 ≤

(cid:18)

𝐶 𝑝
𝜏

|𝑢 (𝑛+1) − 𝑢|1 + |𝑢 (𝑛) − 𝑢|1 +

(cid:19)

𝜖

,

2
1 − 𝐶

where 𝜖 denotes the approximation error in the local and coarse neural network
solutions, 𝑢 (𝑛) are the iterates in the Hilbert space, 𝐶 denotes the convergence rate
in the Hilbert space iterates 𝑢 (𝑛) , (cid:107) · (cid:107)0 denotes the 𝐿2-norm, and 𝐶 𝑝 is the constant
in the Poincare inequality, see [7].

As reported in numerical results in [7], the optimization errors also appear in the
computed neural network solutions and they resulted in less accurate approximate
solutions at each iteration. The resulting errors are observed to have high contrast
near the boundary of the overlapping region, that is harder to be approximated by
the coarse neural network function. Such optimization error behaviors in the neural
network approximation have been analyzed by NTK theory [3, 15]. Regarding the
local problems in our iteration method, the parameters in the local neural network
function are trained to minimize the cost function, consisting of the residual loss

34

Hyea Hyun Kim and Hee Jun Yang

to the diﬀerential equation, and the residual loss to the boundary condition. The
residual loss to the boundary condition is harder to optimize and such optimization
behavior remains as the high contrast error near the overlapping region boundary.

To address such a drawback in our previous method, we form a partitioned neural

network function to approximate the solution 𝑢(𝑥),

𝑈 (𝑥; 𝜃1, · · · , 𝜃 𝑁 ) =

𝑁
∑︁

𝑖=1

𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃𝑖),

where 𝜙𝑖 (𝑥) are a partition of unity functions for the given overlapping subdomain
partition,

𝑁
∑︁

𝑖=1

𝜙𝑖 (𝑥) = 1, 0 ≤ 𝜙𝑖 (𝑥) ≤ 1,

𝜙𝑖 (𝑥) = 0, ∀𝑥 ∈ Ω \ Ω𝑖.

We note that in [11] the parameters 𝜃𝑖 are trained to minimize the following global
cost function without utilizing the partitioned neural network structure for parallel
computing algorithms,

𝐿(𝜃1, · · · , 𝜃 𝑁 ) =

1
|𝑋Ω|

+

1
|𝑋𝜕Ω|

∑︁

|(cid:52)𝑈 (𝑥; 𝜃1, · · · , 𝜃 𝑁 ) + 𝑓 (𝑥)|2

𝑥 ∈𝑋Ω
∑︁

𝑥 ∈𝑋𝜕Ω

|𝑈 (𝑥; 𝜃1, · · · , 𝜃 𝑁 ) − 𝑔(𝑥)|2.

In our work, we propose an iteration method where each local parameters 𝜃𝑖 can be
trained in parallel for a localized problem at each iteration. Such an iterative solution
procedure is more desirable for the partitioned neural networks.

Our new iteration method is as follows:

Algorithm 3: PNN One-level method (input: 𝑈 (0) , output: (cid:98)𝑈 (𝑛+1) )
Step 0: Set the initial iterate 𝑈 (0) = 𝑈 (𝑥; 𝜃 (0)
1
Step 1: Find 𝜃 (𝑛+1)

, · · · , 𝜃 (0)
in 𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃𝑖) to approximate the local problem solution;

𝑁 ).

𝑖

−(cid:52)𝑢 = 𝑓 + (cid:52)((1 − 𝜙𝑖 (𝑥))𝑈 (𝑛) ) in Ω𝑖,

𝑢 = 0 on 𝜕Ω𝑖 ∩ Ω,

𝑢 = 𝑔 on 𝜕Ω𝑖 ∩ 𝜕Ω.

Step 2: Set the next iterate;

𝑈 (𝑛+1) = (1 − 𝛼)𝑈 (𝑛) + 𝛼

𝑁
∑︁

𝑖=1

𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

𝑖

)

Step 3: If the stoping condition is met then set the output (cid:98)𝑈 (𝑥) = (cid:205)𝑁
𝑖=1
otherwise continue the iteration to go back to Step 1.

𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

𝑖

),

DD Algorithms for Neural Network Approximation

35

In Algorithm 3, for the case of ﬂoating subdomains, the zero boundary condition
is already enforced in 𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃 (𝑛+1)
) by the partition of unity function 𝜙𝑖 (𝑥)
and only the diﬀerential equation comes in the loss function. We can thus expect
that the parameter optimization for such a local problem has less optimization errors
than those in Algorithms 1 and 2. Its two-level version can be derived by adding the
coarse correction term 𝑊 (𝑛+1)

to the iterates

𝑖

0

𝑈 (𝑛+1) = (1 − 𝛼)𝑈 (𝑛) + 𝛼

𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃 (𝑛+1)

𝑖

) + 𝑊0(𝑥; 𝜃 (𝑛+1)

0

(cid:33)

)

,

(cid:32) 𝑁
∑︁

𝑖=1

where 𝑊0 (𝑥; 𝜃 (𝑛+1)
lem, i.e., to ﬁnd 𝑤 in a coarse subspace 𝑉0 of 𝐻1(Ω) such that

) is the neural network approximation to the global coarse prob-

0

−(cid:52)𝑤 = 𝑓 + (cid:52)𝑈 (𝑛) , in Ω, 𝑤 = 0, on 𝜕Ω.

For the Algorithm 3 and its two-level version, their convergence can be shown by
following similarly as in our previous work [7]. More rigorous convergence analysis
will be provided in a complete version of the proceeding paper. We note that at each
iteration the local parameters are fully trained for the given diﬀerential equation.
Even the case, local parameter training cost per each iteration is much smaller than
the training cost in the single large neural network. The number of training epochs
is much smaller and the gradient update per epoch is also much cheaper for the
smaller local neural network functions. The trade-oﬀ is that the total training cost in
our proposed method also depends on the number of outer iterations. As the more
subdomains in the partition, the more outer iterations are needed. It is thus important
to include the coarse component to speed up the outer iterations.

4 Numerical results

For the proposed iterative methods, we consider the following simple one-dimensional
model problem to compare their convergence behavior,

−𝑢(cid:48)(cid:48) = 𝑓 (𝑥) in (−1 1), 𝑢(𝑥) = 0 at 𝑥 = −1, 1,

where 𝑓 (𝑥) is chosen to give the exact solution 𝑢(𝑥) = sin(𝜋𝑥).

For the domain (−1 1) we introduce an overlapping subdomain partition
with 10 subdomains. We then consider a partitioned neural network with 10 lo-
cal neural network functions, that are deﬁned on each subdomains in the overlapping
subdomain partition. For all the local neural network functions, the number of pa-
rameters is set as 106. We also use the same size of the coarse neural network
function with 106 parameters in the two-level method. When training the parameters
in the local and coarse neural network functions, we use 10000 training epochs in
the gradient method, where we use the Adam optimizer with the learning rate 0.001.

36

Hyea Hyun Kim and Hee Jun Yang

Fig. 1 Error decay history: Left ﬁgure (Error plots for 𝑈 (𝑛) ), Right ﬁgure (Error plots for (cid:98)𝑈 (𝑛) ),
ASM One level (Algorithm 1), ASM Two level (Algorithm 2), PUASM One level (Algorithm 3),
PUASM Two level (Algorithm 3 with the coarse correction term).

We use randomly selected 100 training data points in each local and coarse problem
parameter training.

In Fig. 1, the convergence history in the proposed methods is presented up to
100 outer iterations. The relative 𝐿2-errors in the neural network approximate so-
lutions at each outer iteration are plotted and compared. In the left ﬁgure, the
errors for the neural network iterates 𝑈 (𝑛) to the exact solution are plotted for the
four proposed methods. In the right ﬁgure, the errors for the practical neural net-
work iterates (cid:98)𝑈 (𝑛) are plotted, see (6) for the ASM Two level (Algorithm 2) and
(cid:98)𝑈 (𝑛) = ((cid:205)𝑁
) for PUASM Two level (Algorithm 3
𝑖=1
0
with the coarse correction term). The error plots in both ﬁgures show that the coarse
correction term in the ASM Two level method does not help to speed up the conver-
gence of the ASM One level. The convergence rate is even larger than the ASM One
level method. As discussed earlier, this is related to the optimization error behaviors
in the local neural network parameter training, that produce high contrast errors near
the boundary of the overlapping region.

)) + 𝑊0 (𝑥; 𝜃 (𝑛)

𝜙𝑖 (𝑥)𝑈𝑖 (𝑥; 𝜃 (𝑛)

𝑖

In the case of the PUASM Two level method, the coarse problem accelerates the
convergence greatly at the early outer iterations. The local problem in the PUASM
case has only the residual loss for the diﬀerential equation and the high contrast
optimization error problems are alleviated in this case with the help of the partition
of unity functions. However, at the later outer iterations, the errors can not be
further reduced due to the practical implementation issue in the partition of unity
functions. The practical implementation issue with the partition of unity functions
needs a further investigation and our future research will be focused on proposing
some new idea in forming and implementing the partition of unity functions that are
suitable for neural network approximation.

Acknowledgements The ﬁrst author is supported by NRF-2022R1A2C100388511.

020406080100Outer iteration10-310-210-1100Relative L2 errorASM One levelASM Two levelPUASM One levelPUASM Two level020406080100Outer iteration10-310-210-1100Relative L2 errorASM One levelASM Two levelPUASM One levelPUASM Two levelDD Algorithms for Neural Network Approximation

37

References

1. Badea, L. and Wang, J. An additive Schwarz method for variational inequalities. Mathematics

of Computation 69(232), 1341–1354 (2000).

2. E, W., Han, J., and Jentzen, A. Deep learning-based numerical methods for high-dimensional
parabolic partial diﬀerential equations and backward stochastic diﬀerential equations. Com-
mun. Math. Stat. 5(4), 349–380 (2017).

3. Jacot, A., Gabriel, F., and Hongler, C. Neural tangent kernel: Convergence and generalization

in neural networks. Advances in neural information processing systems 31 (2018).

4. Jagtap, A. D. and Karniadakis, G. E. Extended physics-informed neural networks (xpinns): A
generalized space-time domain decomposition based deep learning framework for nonlinear
partial diﬀerential equations. Communications in Computational Physics 28(5), 2002–2041
(2020).

5. Jagtap, A. D., Kharazmi, E., and Karniadakis, G. E. Conservative physics-informed neural
networks on discrete domains for conservation laws: Applications to forward and inverse
problems. Computer Methods in Applied Mechanics and Engineering 365, 113028 (2020).
6. Kim, H. H. and Yang, H. J. Domain decomposition algorithms for physics-informed neural
networks. In: Proceedings of the 26th International Conference on Domain Decomposition
Methods (2021).

7. Kim, H. H. and Yang, H. J. Additive Schwarz algorithms for neural network approximate

solutions. arXiv preprint arXiv:2211.00225 (2022).

8. Li, K., Tang, K., Wu, T., and Liao, Q. D3M: A deep domain decomposition method for partial

diﬀerential equations. IEEE Access 8, 5283–5294 (2019).

9. Li, W., Xiang, X., and Xu, Y. Deep domain decomposition method: Elliptic problems. In:

Mathematical and Scientiﬁc Machine Learning, 269–286. PMLR (2020).

10. Long, Z., Lu, Y., and Dong, B. PDE-Net 2.0: learning PDEs from data with a numeric-symbolic

hybrid deep network. J. Comput. Phys. 399, 108925, 17 (2019).

11. Moseley, B., Markham, A., and Nissen-Meyer, T. Finite basis physics-informed neural networks
(FBPINNs): a scalable domain decomposition approach for solving diﬀerential equations.
arXiv preprint arXiv:2107.07871 (2021).

12. Raissi, M., Perdikaris, P., and Karniadakis, G. E. Physics-informed neural networks: a deep
learning framework for solving forward and inverse problems involving nonlinear partial
diﬀerential equations. J. Comput. Phys. 378, 686–707 (2019).

13. Sirignano, J. and Spiliopoulos, K. DGM: a deep learning algorithm for solving partial diﬀer-

ential equations. J. Comput. Phys. 375, 1339–1364 (2018).

14. Toselli, A. and Widlund, O. Domain decomposition methods—algorithms and theory, Springer

Series in Computational Mathematics, vol. 34. Springer-Verlag, Berlin (2005).

15. Wang, S., Yu, X., and Perdikaris, P. When and why PINNs fail to train: A neural tangent kernel

perspective. Journal of Computational Physics 449, 110768 (2022).

16. Xu, J. and Zikatanov, L. The method of alternating projections and the method of subspace

corrections in Hilbert space. J. Amer. Math. Soc. 15(3), 573–597 (2002).


