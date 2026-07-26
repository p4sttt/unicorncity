A new probabilistic approach to the domain
decomposition method

Juan A. Acebr¶on1 and Renato Spigler2

1 Departamento de Autom¶atica, Escuela Polit¶ecnica, Universidad de Alcal¶a,

Crta. Madrid{Barcelona, Km. 31.600, 28871 Alcal¶a de Henares, Madrid, Spain
juan.acebron@uah.es

2 Dipartimento di Matematica, Universit(cid:181)a di \Roma Tre,",

Largo S. Leonardo Murialdo 1, 00146 Roma, Italy
spigler@mat.uniroma3.it

A hybrid numerical scheme based on a probabilistic method along with a clas-
sical domain decomposition is proposed for solving numerically linear elliptic
boundary-value problems. Full decoupling can be accomplished by computing
few values of the solution inside the domain by Monte Carlo or quasi-Monte
Carlo techniques, and interpolating on the nodal points where the solution has
been obtained previously. Thus, this method appears to be fault-tolerant as
well as suited for time decomposition. Some examples are shown to illustrate
performance and scalability.

1 Introduction

The domain decomposition method is nowadays considered one of the most
natural ways to exploit parallel architectures in solving boundary-value prob-
lems for partial diﬁerential equations (PDEs). The main idea consists of de-
coupling the original problem into several sub-problems, and was proposed
originally in the seminal work of H. A. Schwarz in 1870. More precisely, the
given domain is divided into a number of subdomains, and then assign the
task of the numerical solution on such separate subdomains to diﬁerent pro-
cessors. However, the computation cannot run independently for each subdo-
main, because they are coupled together through an internal interface, where
the solution is unknown. Therefore, for every computational time step, pro-
cessors have to exchange data along these interfaces, slowing down the overall
performance.

In fact, due to the global character of the PDE, the solution cannot be
obtained at a single point inside the domain prior to solving the full problem.
Consequently, certain iterations are required across the chosen (or prescribed)
interfaces, in order to determine approximate values of the sought solution

2

Juan A. Acebr¶on and Renato Spigler

inside the original domain. There exists two approaches for a domain decom-
position depending on whether domains are overlapping or not overlapping,
see [DA94, QUA99, TOS05], e.g. Being the domains coupled, some additional
numerical work is needed, and therefore, it is doubtful whether full scalability
can be attained as the number of the subdomains (hence, of the processsors)
increases unboundedly.

In order to overcome such a drawback, a new method has been recently
proposed [AN05, AN05b]. The core of the method is based on combining a
certain probabilistic method suited for solving elliptic and parabolic partial
diﬁerential equations along with a classical domain decomposition method,
namely a probabilistic domain decomposition method (PDD). This approach
allows to obtain the solution in some points, internal to the domain, without
solving ﬂrst the entire problem. In fact, this can be done by means of the
probabilistic representation of the solution. The basic idea is to compute only
few values of the solution on certain chosen interfaces, and then interpolate
to get continuous approximations. These can be used as boundary values to
decouple the problem into sub-problems, see Fig. 1. Each of such sub-problems
can then be solved independently on a separate processor. Clearly, neither
communication among the processors, nor iteration across the interfaces is
needed.

1

3

1

3

2

4

2

4

Fig. 1. Sketchy diagram illustrating the numerical method, splitting the initial
domain › into four subdomains, ›1; ›2; ›3; ›4.

Solving numerically boundary-value problems for linear elliptic and parabolic

partial diﬁerential equations by the probabilistic representation of their solu-
tions, essentially by a Monte Carlo method, is known since long time, see
[CH98, KAL86]. It is based on the well-known Feymann-Kac formula, which
is a representation extremely powerful, and inherently parallel since it al-

W
W
W
W
W
W
W
W
W
A new probabilistic approach to the domain decomposition method

3

lows for obtaining the solution in single points inside the domain. However, it
can be hardly used because requires evaluating accurately the ﬂrst exit point
along with the ﬂrst exit time from the domain, as well as solving numerically
a boundary value problem for a stochastic diﬁerential equation. Both issues,
however, can be managed reasonably resorting to several powerful numerical
and asymptotic techniques, extracted from probability theory, number theory
and statistical physics, see [AN05c, JS00, JS03].

2 Generalities

To the purpose of illustration, let conﬂne ourselves to the case of the Dirichlet
problem for a linear elliptic equation,

Lu ¡ c(x)u = f (x); x 2 › ‰ R2;

uj@› = g;

(1)

2
i;j=1 aij(x)@i@j +

2
i=1 bi(x)@i is a linear elliptic operator with
where L :=
smooth coe–cients, c(x) ‚ 0, boundary @› of the domain › also smooth,
as well as the boundary data, g, and the source term, f . The probabilistic
representation is given by,

P

P

u(x) = EL

x •

g(ﬂ(¿@›))e

¡

¿@›
0

R

c(ﬂ(s)) ds ¡

Z

0

¿@›

f (ﬂ(t)) e

¡

t

0

c(ﬂ(s)) ds dt

;

‚

R

(2)
see [FRE85, KAR91], e.g., where ﬂ(t) is the (vector-valued) stochastic process
associated to the elliptic operator L, which solves the system of (Ito type)
stochastic diﬁerential equations (SDEs)

dﬂ = b(x)dt + (cid:190)(x)dW (t);

(3)

where W (t) represents the 2-dimensional standard brownian motion (also
called Wiener process), and ¿@› is the ﬂrst passage (or hitting) time of the
path ﬂ(t) started at the point x to @›. As usual, the dependence of ﬂ on the
chance variable, running on the underlying probability space, is not displayed.
When the operator L is the Laplace operator, ¢, the stochastic process ﬂ(t)
reduces to the standard 2-dimensional brownian motion. The drift vector,
b in (3) is the same appearing in the operator L, that is b(x) = (b1; b2)T ,
while the diﬁusion matrix, (cid:190), is related to the coe–cients aij by the relation
(cid:190)(cid:190)T = a · (ai;j)i;j=1;2.

The representation formula in (2) is used to obtain few values of the solu-
tion at some points inside the domain ›. The expected value is approximated
by an arithmetic mean (which is known to provide the best estimator) over
N realizations of the process ﬂ, at the price of a (statistical) error of order
of N ¡1=2. The main catch of using a Monte Carlo method rests on this fact,
which entails a rather poor accuracy, unless N is taken extremely large. An

4

Juan A. Acebr¶on and Renato Spigler

alternative, however, do exist, and consists of resorting to sequences of quasi-
random numbers [NIE92], which have been used succesfully in mathematical
ﬂnance, and recently applied in solving stochastic diﬁerential equations with
high e–ciency [AN05c]. Using quasi-random numbers allows for speeding up
the calculations with respect to the classical Monte Carlo method based on
pseudorandom numbers, since now the statistical error becomes of order of
N ¡1. Such a method is called quasi- Monte Carlo.

Since evaluating the solution via a probabilistic method may require a large
number of realizations (large sample size) in order to reduce the associated
statistical error, we compute the solution in a few points along the interfaces
between subdomains. Such points will be used as nodal points to evaluate
interpolating the solution at the interfaces.

Apart from the statistical error, there are however other sources of numer-
ical error which aﬁect the evaluation of u(x) by means of (2), besides that due
to the ﬂnite sample size mentioned above. These are due to: (i) the truncation
error made in the numerical solution of the SDEs in (3); (ii) the uncertainty
of estimating ﬂrst exit times; (iii) the numerical quadrature errors in (2). Es-
timating precisely the ﬂrst exit times and the ﬂrst exit points (which are also
needed for problems with c(x) and f (x) not vanishing for all x) has been of-
ten overlooked in the existing literature. An e–cient way to locate accurately
the ﬂrst exit time is based on the use of an exponential timestepping, see
[JS00, JS03]. All these sources of error have been analyzed in [AN05, AN05b].
At the present time, machines working in the peta(cid:176)ops regime, and en-
dowed with hundred of thousands or even millions of processors are planned
for the near future, and taking full advantage from massive parallel computing
would be highly desirable. With such machines, the issue of scalability remains
open, at least in some cases. As it was pointed out in [KEY98], Schwarz-type
DD methods are not truly scalable, at least in the theoretical sense, since their
parallel e–ciency in solving elliptic problems is subject to degradation as the
number of processors, p, goes to inﬂnity, indeed when p starts being over the
thousands. It seems however that things go better, in practice, for a number
of reasons, described in [KEY98].

In addition, the possibility of failure of even few processors is very likely to
occur frequently [GEI03]. Therefore, algorithms which are scalable and fault-
tolerant at the same time would be extremely important if not mandatory.

The method proposed here seems to be free of the aforementioned draw-
backs. In fact, decoupling is complete, and it was shown in [AN05, AN05b]
that scalability is attained with respect to an arbitrary number of subdomains
or processors, and the algorithm is naturally fault-tolerant. The latter prop-
erty rests on two ingredients, one due to the intrinsic parallelizability of the
Monte Carlo methods, and to the full decoupling that can be realized.

A new probabilistic approach to the domain decomposition method

5

3 Numerical examples

Below we show some examples to illustrate the numerical method here pro-
posed. It is worth to stress that, even though the \pivotal" values generated
by Monte Carlo or by quasi-Monte Carlo are poorly accurate (unless an ex-
tremely large sample, N , of realizations is used), and the Chebyshev interpo-
lation adds some additional error, the numerical error inside each subdomain
is dominated by the boundary errors, due to the maximum principle, and
decays rapidly going inside.

Note that a comparison with a true deterministic DD method has not yet
been done, being shown only a comparison with \parallel ﬂnite diﬁerences".
However, we do not expect that our algorithm migh outperform necessarily
any given deterministic DD method, but, rather, that our approach might win
over others regarding full scalability and fault-tolerance.

All codes have been implemented using OpenMP, which is a standard
parallelization library, designed for shared memory computer architectures.
We simply used a 16 processor IBM Power 3 machine, working at 375 MHz
clock, and with a peak performance of 24 GFLOPS.
Example 1. Let consider the Dirichlet problem [AN05b]

y2 + 1
2

uxx +

x2 + 1
2

uyy + x ux + y2 uy ¡ (x3 + y2)u =

P cos(2x + y) + Q sin(2x + y)

in › = (0; 1) £ (0; 1);

(4)

P = 1 + x(4 + x + 2x2) + 2x y + x(4 + x)y2 + y3;

[¡2 + x4 + 2x5 + 2x3 y + y(5 ¡ 4y + 6y2) + x2(1 + y + 6y2)]

(5)

Q = ¡

1
2

with the boundary data

u(x; y)j@› =

(x2 + y) sin(2x + y)

the solution being u(x; y) = (x2 + y) sin(2x + y).

£

@› ;

⁄

(6)

Table 1. CPU time in seconds for example 1

Processors PFD

P DDT otal P DDM onte Carlo P DDF D

4
9
16

9200:107 2087:947
4098:381 489:684
2638:937 175:168

3:492
3:872
3:365

2084:015
485:484
171:508

In Fig. 2a and 2b, the pointwise numerical error is shown, made corre-
spondingly to the PDD with pseudorandom sequence of numbers, and quasi-
random, respectively. Here only two nodes on each interface have been used.

6

Juan A. Acebr¶on and Renato Spigler

(a)

0

0.1

0.2

0.3

0.4

y

0.5

0.6

0.7

0.8

0.9

1
0

(b)

0

0.1

0.2

0.3

0.4

y

0.5

0.6

0.7

0.8

0.9

1
0

0.03

0.025

0.02

0.015

0.01

0.005

0

0.03

0.025

0.02

0.015

0.01

0.005

0.2

0.4

x

0.6

0.8

1

0.2

0.4

x

0.6

0.8

1

Fig. 2. Example 2. Pointwise numerical error in: (a) the PDD algorithm, and (b) the
¡3.
quasi-PDD algorithm. Parameters are N = 104, ¢x = ¢y = 2 £ 10

¡3, ¢t = 10

It should be remarked that the quasi-PDD algorithm outperforms the PDD
algorithm. The second column (PFD) in Table 1 shows the total computa-
tional time (in seconds) spent by the parallel ﬂnite diﬁerence algorithm using
p = 4, 9, and 16 processors, which corresponds to 4, 9, and 16 subdomains.
The corresponding time spent by the PDD algorithm is shown in the third
column. In the last two columns, such a quantity is split into two parts, i.e,
that required by the Monte Carlo simulation, and that needed by the local
solvers. The two methods have been compared for about the same maximum
error, 10¡3. In both algorithms the CPU time decreases as p increases, and
this trend is more dramatic in the PDD algorithm. Moreover, the CPU time
decreases for each given number of processors, passing from PFD to PDD, and
this behavior is more pronounced, when the number of processors is higher.
Example 2. Consider the so-called Stommel model, which is a two dimen-
sional model for ocean circulation, and is given by

uxx + uyy + ﬂ ux = ¡ﬁ sin(…y=2)

in › = (0; 1) £ (0; 1);

(7)

with the boundary data u(x; y)j@› = 0, and ﬁ = 10, ﬂ = 1. In this example
an analytical solution is unknown, and to quantify the numerical error, an
accurate numerical solution obtained solving the elliptic equation by a multi-
grid method has been used instead. Similarly to the previuous example, it is
shown in Fig. 3 the contour plots for the pointwise numerical errors.

4 Conlusions

A hybrid method based on a probabilistic approach along with a classical
domain decomposition for the numerical solution of elliptic partial diﬁeren-

A new probabilistic approach to the domain decomposition method

7

(a)

0

0.1

0.2

0.3

0.4

y

0.5

0.6

0.7

0.8

0.9

1
0

0.08

0.07

0.06

0.05

0.04

0.03

0.02

0.01

0

(b)

0

0.1

0.2

0.3

0.4

y

0.5

0.6

0.7

0.8

0.9

1
0

0.08

0.07

0.06

0.05

0.04

0.03

0.02

0.01

0

0.2

0.4

x

0.6

0.8

1

0.2

0.4

x

0.6

0.8

1

Fig. 3. Example 2. Pointwise numerical error in: (a) the PDD algorithm, and (b)
the quasi-PDD algorithm. Parameters are as in Fig. 2

tial equation, has been described. The associated stochastic diﬁerential equa-
tion is solved by Monte Carlo simulation only at very few points of a given
interface internal to the domain. Then, the solution at the interface is con-
structed interpolating by using such points as nodal points. Consequently, a
full splitting into several subdomains, to be handled by separate processors
acting simultaneously, can be accomplished. Since it has been shown in the
literature that the ensuing error may dominate, an essential ingredient of the
algorithm consists of a suitable boundary treatment. Moreover, it has been
shown that e–cieny can be increased adopting sequences of \quasi-random
numbers" (instead of the more customary pseudorandom numbers).

It is worthwhile noticing that a comparison with true deterministic domain
decomposition algorithms has not been made yet. This has been done only
with parallel ﬂnite diﬁerences. Such an algorithm allows for an automatic
distribution of the computational load among the prescribed subdomains. We
do not expect that our code might be necessarily competitive with the existing
deterministic codes, but, rather, that it might compete as for its scalability
and fault-tolerance properties. In fact, such approach allows for a complete
decoupling among processors, without degrading the overall performance due
to strong interprocessors communication. Therefore, it appears to be well
suited for grid computing and nowadays supercomputers with hundreds of
thousands of processors or more.

The availability of such a large number of processors in supercomputers,
and to put every available processor to work, suggests to think about devel-
oping new strategies of parallelization, which exploit now time [FT03]. The
method proposed here can be generalized to account for parabolic partial dif-
ferential equations, where the time evolution of the solution should be now

8

Juan A. Acebr¶on and Renato Spigler

taken into account. In fact, the probabilistic method can be used as well now
to evaluate the solution of a parabolic partial diﬁerential equation in any given
point and time inside the spatio-temporal domain.

References

[AN05] Acebr¶on, J.A., Busico, M.P., Lanucara, P., Spigler, R.: Domain decompo-
sition solution of elliptic boundary-value problems via Monte Carlo and
quasi-Monte Carlo methods. SIAM J. Sci. Comput., in print (2005).

[AN05b] Acebr¶on, J.A., Busico, M.P., Lanucara, P., Spigler, R.: Probabilistically-
induced domain decomposition methods for elliptic boundary-value prob-
lems. Submitted (2005).

[AN05c] Acebr¶on, J.A., Spigler, R.: Fast simulations of stochastic dynamical sys-

[CH98]

tems. J. Comput. Phys., in print (2005).
Ca(cid:176)isch, R.E.: Monte Carlo and quasi Monte Carlo methods. Acta Nu-
merica, 1{49 (1998)

[DA94] Dryja, M., Widlund, O.B.: Domain decomposition algorithms with small

[FT03]

overlap. SIAM J. Sci. Comput., 15, 604{620 (1994)
Farhat, C., Chandesris, M.: Time-decomposed parallel time-integrators:
theory and feasibility studies for (cid:176)uid, structure, and (cid:176)uid-structure ap-
plications. Int. J. Numer. Meth. Engng., 58, 1397{1434 (2003)
[FRE85] Freidlin, M.: Functional integration and partial diﬁerential equations. In:

Annals of Mathematics Studies no. 109. Princeton Univ. Press (1985)

[GEI03] Geist, G.A.: Progress towards Petascale Virtual Machines. In: Dongarra,

[JS00]

[JS03]

J. (ed) Lecture Notes in Computer Science. Springer, Berlin (2003).
Jansons, K.M., Lythe, G.D.: E–cient numerical solution of stochastic
diﬁerential equations using exponential timestepping. J. Statist. Phys.,
100, 1097{1109 (2000)
Jansons, K.M., Lythe, G.D.: Exponential timestepping with boundary test
for stochastic diﬁerential equations. SIAM J. Sci. Comput., 24, 1809{1822
(2003)

[KAL86] Kalos, M.H., Withlock, P.A.: Monte Carlo methods, Vol. I: Basics. Wiley,

New York (1986)

[KAR91] Karatzas, I., Shreve, S.E.: Brownian motion and stochastic calculus, 2nd

ed. Springer, Berlin Heidelberg New York (1991)

[KEY98] Keyes, D.E.: How scalable is domain decomposition in practice?. In:
Eleventh International Conference on Domain Decomposition Methods
(London, 1998). DDM.org, 286-297 (electronic). Augsburg (1999)

[NIE92] Niederreiter, H.: Random number generation and quasi Monte-Carlo

methods. SIAM (1992).

[QUA99] Quarteroni, A., Valli, A.: Domain decomnposition methods for partial dif-
ferential equations. Oxford Science Publications, Clarendon Press (1999)
[TOS05] Toselli, A., Widlund, O.: Domain Decomposition Methods - Algorithms
and Theory. Springer Series in Computational Mathematics, Vol. 34
(2005).


