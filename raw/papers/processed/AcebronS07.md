A fully scalable parallel algorithm for solving
elliptic partial differential equations
Juan A. Acebr´on1 and Renato Spigler2
1 Departament d’Enginyeria Inform`atica i Matem`atiques,
Universitat Rovira i Virgili, 43007 Tarragona, Spain,
juan.acebron@urv.cat
2 Dipartimento diMatematica, Universit`a “Roma Tre”, 1, Largo S.L. Murialdo,
00146 Rome, Italy
spigler@mat.uniroma3.it
Abstract. Acomparison ismadebetween theprobabilistic domainde-
composition (DD) method and a certain deterministic DD method for
solving linear elliptic boundary-value problems. Since in the determin-
istic approach the CPU time is affected by intercommunications among
the processors, it turnsout that the probabilistic method performs bet-
ter, especially when the numberof subdomains (hence, of processors) is
increased. This fact is clearly illustrated by some examples. The prob-
abilistic DD algorithm has been implemented in an MPI environment,
in order to exploit distributed computer architectures. Scalability and
fault-tolerance of theprobabilistic DD algorithm are emphasized.
1 Introduction and generalities
Domaindecompositionisconsideredasoneofthemostnaturalwaystodecouple
boundary-value (BV) problems for partial differential equations (PDEs) into
subproblems,inordertotakeadvantageofparallelcomputerarchitectures,thus
allowing for high-performance scientific computing of large-scale problems. The
seminal idea of DD can be traced back to the 1870 work of H. A. Schwarz,
and consists of splitting the given domain into a number of subdomains, then
assigning the task of the numerical solution on each separate subdomain to
as many separate processors. A major problem, however, is represented by the
need of having the solution on the interfaces, internal to the domain, which
divide it into subdomains, while solving BV problems for PDEs is global in
character. This means that the solution cannot be obtained even at a single
point inside the domain before solving the entire problem. Consequently, some
iterativeproceduresarerequired,acrossthe chosen(orprescribed)interfaces,in
orderto determine approximatevalues of the soughtsolution inside the original
domain. Both, overlapping (Schwarz-type) and not overlapping domains have
been considered in the literature so far [13]. In both cases, some additional
numericalworkisrequiredinadvancetodecoupletheproblemintosubproblems,
anditisunclearwhetheralgorithmsbasedonsuchstrategiesmightbescalableas
thenumberofthesubdomains(hence,oftheprocessors)increasesunboundedly.

2 Juan A. Acebro´n et al.
Intheclassical(deterministic)DDmethod,animportantissueisrepresented
bytheconditionnumberinherenttotheiterativealgorithmsadoptedtoprecom-
pute interfacialvalues,see [13].In fact,the operatorgoverningsuchaniterative
procedure is typically ill-conditioned.Preconditioning is therefore essential,and
it is necessary to construct optimal and efficient preconditioners. Optimality
means that their spectral condition number (i.e., the ratio between maximum
and minimum eigenvalue) is bounded uniformly with respect to the mesh size,
h, and to the averagediameter, say H, of the subdomains. It is knownfrom the
literature that in Schwarz-type domain decomposition methods, that is those
with overlapping, the aforementioned condition numbers are actually indepen-
dentofboth,handH,providedthattheoverlappingissufficientlywide.Optimal
bounds were indeed found for this case, see [5,7].
A method of completely new type, based on a probabilistically induced do-
main decomposition (PDD), has been recently proposed which avoids the sev-
eralproblemsinherenttotheaforementionedtraditionalapproachtoDD[1,2,4].
Moreover,themethodseemstobespeciallysuitedforheterogeneouscomputing,
due to its low communication overhead,and since it is fault-tolerant.
Nowadays,itseemsthat,usingparallelcomputerswithuptoafewhundreds
of processors in problems with up to few millions of variables, the total compu-
tationalcostisdominatedbythatspentbythelocalsolvers.However,machines
workinginthepetaflopsregimeandendowedwithhundredsofthousandsoreven
millions ofprocessorsareplanned for the near future, and taking full advantage
from massive parallel computing would be highly desirable. Indeed, the IBM
BlueGene isexpectedtobreakthe petaflopsbarrierwithinthe 2007.Withsuch
machines, the issue of scalability remains open, at least in some cases.As it was
pointed outin [11],Schwarz-typeDD methods arenot truly scalable,at leastin
the theoreticalsense,since their parallelefficiency in solvingelliptic problems is
subject to degradation as the number of processors, p, goes to infinity, indeed
when p starts being overthe thousands. It seems howeverthat things go a little
better, in practice, for a number of reasons, as described in [11].
Besides,the possibilityoffailureofevenfew processors(evenofonlyone!)is
very likely to occur frequently [9]. Therefore,algorithms which are scalable and
fault-tolerant at the same time would (and will) be extremely important, if not
mandatory.
Briefly, the idea of the PDD algorithm consists of generating first the val-
ues of the solution at few points inside the domain. Then, an interpolation on
such nodes is constructed, and finally the traces of the solution on the inter-
faces are obtained. This allows to fully decompose the domain into a number
of subdomains, and at the same time this procedure seems to be free of the
previous drawbacks. In fact, decoupling is complete and no conditioning prob-
lem does exist concerning interfacial iteration problems. In [1,2], it was shown
that scalability is attained with respect to an arbitrary number of subdomains
or processors, and the algorithm is naturally fault-tolerant. The latter property
rests on two ingredients, one due to the intrinsic parallelizability of the Monte
Carlo methods, the other to the full decoupling into subdomains that can be

|     |     |     |     |     | A   | fully scalable | parallel | algorithm | 3   |
| --- | --- | --- | --- | --- | --- | -------------- | -------- | --------- | --- |
realized.As for the scalability, it was shownin [1]that the speedup Sp achieved
with p processors, assumed to act independently from each other on p subdo-
√
mains,scalesas Sp ∼c p as p→∞,c being a constant.The ideal(theoretical)
∼
speedup, Sp cp, cannot be attained since some (nonnegligeable) time should
be spent to compute the values of the solution by Monte Carlo at few points.
Here the speedup is defined as the ratio T1/Tp, where T1 is the time spent to
solve sequentially the given problem on the full domain, while Tp is the time
| spent | for solving | the same | problem |     | in parallel | with | p processors. |     |     |
| ----- | ----------- | -------- | ------- | --- | ----------- | ---- | ------------- | --- | --- |
In the paper [4] the essentials of the PDD method developed in [1,2] have
been described, and some additional examples have been presented. In all such
papers, however, the code implementing the PDD algorithm was written in
OpenMPenvironment.Thenumericalresultsworkedoutinthispaperarebased,
instead, on a code written in MPI environment. This has been done in order to
fully exploit distributed computer architectures. The main purpose of this pa-
per is to compare the performance of the PDD and of the deterministic DD
| algorithms |     | implemented | in MPI | environment. |     |     |     |     |     |
| ---------- | --- | ----------- | ------ | ------------ | --- | --- | --- | --- | --- |
| 2          | The | algorithm   |        |              |     |     |     |     |     |
WeconfineourdiscussiontothecaseoftheDirichletproblemforalinearelliptic
| equation | in                 | two dimensions, | i.e., |         |         |     |     |             |     |
| -------- | ------------------ | --------------- | ----- | ------- | ------- | --- | --- | ----------- | --- |
|          | Lu−c(x,y)u=f(x,y), |                 |       | (x,y)∈Ω |         | ⊂R2 | u|  |             |     |
|          |                    |                 |       |         |         |     | ,   | ∂Ω =g(x,y), | (1) |
|          |                    | (cid:2)         |       |         | (cid:2) |     |     |             |     |
where L := 2 aij(x,y)∂i∂j + 2 bi(x,y)∂i is a linear elliptic operator
|     |     | i,j=1 |     |     | i=1 |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
≥
with smooth coefficients, c(x,y) 0, the boundary ∂Ω of the domain Ω also
smooth,as wellasthe boundarydata,g, andthe sourceterm, f.The basicidea
is togenerateonly few valuesofsolution,u,bya probabilisticmethod, allbeing
| based | on the | Monte Carlo | method | [6]. |     |     |     |     |     |
| ----- | ------ | ----------- | ------ | ---- | --- | --- | --- | --- | --- |
In some sense, this approach allows to obtain the solution at any point in-
ternal to Ω without solving the entire problem in advance. This can be realized
| by means | of  | the the probabilistic |     | representation |     |         | of the solution, |            |         |
| -------- | --- | --------------------- | --- | -------------- | --- | ------- | ---------------- | ---------- | ------- |
|          |     | (cid:3)               |     |                |     | (cid:5) |                  |            | (cid:6) |
|          |     |                       |     | (cid:4)        |     |         |                  | (cid:4)    |         |
|          |     |                       |     | τ∂Ωc(β(s))ds−  |     |         | τ ∂Ω             | tc(β(s))ds |         |
|          |     | L                     | −   |                |     |         |                  | −          |         |
| u(x,y)=E |     | x ,y g(β(τ∂Ω))e       |     | 0              |     |         | f(β(t))e         | 0          | dt      |
0
(2)
[8], where β(t) is the two-dimensional stochastic process associated to the ellip-
tic operator L, which solves the system of two Ito-type stochastic differential
| equations | (SDEs) |     |                           |     |     |     |     |     |     |
| --------- | ------ | --- | ------------------------- | --- | --- | --- | --- | --- | --- |
|           |        |     | dβ =b(x,y)dt+σ(x,y)dW(t). |     |     |     |     |     | (3) |
Here W(t) represents the two-dimensional standard Brownian motion (also
called Wiener process), and τ∂Ω is the first passage (or hitting) time of the
path β(t) startedat the point (x,y) to ∂Ω. When the operatorL is the Laplace
operator,Δ,thestochasticprocessβ(t)reducestothestandardtwodimensional
Brownian motion. The drift vector, b = b(x,y) in (3), is the same appearing in

4 Juan A. Acebro´n et al.
the operator L, that is b=(b1,b2)T , while the diffusion matrix, σ =σ(x,y), is
related to the coefficients aij by the relation σσT =a≡(ai,j)i,j=1,2.
Weusetherepresentationformulain(2)toobtainfewvaluesofthesolution,
at some points inside the domain Ω. The expected value is then approximated
byanarithmeticmean(knowntoprovideitsbestestimator)overN realizations
of the process β, at the price of a (statistical) error of order of N−1/2. The
main catch of using a Monte Carlo method rests on this fact, which entails a
rather poor accuracy, unless N is taken extremely large. Even for N not very
large,the computationalcostis high, but inthe PDD algorithmwe limit its use
to very few points. The points where the solution is computed by Monte Carlo
simulationsarethenusedasnodesforinterpolation.Suchinterpolationallowsto
obtain boundary values of solution on certain interfaces internal to the domain,
and hence to fully decouple the original problem into subproblems, see Fig. 1.
We always use Chebyshev interpolation.
The PDD algorithm can be briefly described as follows:
1. Compute only few interfacial values by Monte Carlo simulations.
2. Interpolate on the corresponding nodes to obtain boundary values for the
subdomains.
3. Computethesolutiontotheoriginalproblemineachsubdomainbystandard
methods (e.g., finite differences or finite elements).
Ω
Ω Ω Ω Ω
Ω Ω Ω Ω
1 2 3 4
1 2 3 4
(cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2)
(cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)
(cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2)
(cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0)(cid:2)(cid:0)(cid:2)(cid:0)(cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0) (cid:0) (cid:2) (cid:2) (cid:0)(cid:2)(cid:0)(cid:2)
Fig.1. Sketchydiagram which shows how thePDD algorithm works.
The Monte Carlo approach is trivially parallelizable, since each of the N
problemsabovecanberunnedindependentlyoftheothers.Statedinsuchterms,
clearly,the method appears to be scalable as well. Moreover,it is also naturally
fault-tolerant.Infact,assumingthatafraction,n,oftheN processorsbeingused
fails, meaningful results will be obtained from the remaining N −n processors,

A fully scalable parallel algorithm 5
and it will suffice just to ignore what could have come from the n processors
which have failed. The final error will be slightly worse,of the order of O((N −
n)−1/2). Note that
(cid:7) (cid:8)
1 n
(N −n) −1/2 ≈N −1/2 1+ , for n(cid:11)N, (4)
2N
that is 1.005N−1/2 for a small fraction n/N =1/100(1%) of failing processors.
Even though the probabilistic algorithm we derived and considered here is
scalable,naturallyfaulttolerant,andwellsuitedtogridandheterogeneouscom-
puting, it suffers for some weakness, due to the inherently poor accuracy of all
Monte Carlo methods. A considerable improvement, however, can be achieved
using sequences of“quasi-randomnumbers” [6,12]insteadofsequences ofpseu-
dorandom numbers. The pseudorandom numbers are those numbers obtained
in practice, when we try to generate truly random numbers, hence are approx-
imately characterized by a statistical distribution. The quasi-random numbers,
instead, are deterministic uniformly distributed numbers. Using the latter al-
lows to obtain an error (now deterministic) of order of O(N−1log d∗−1 N), d∗
representing a certain “effective” space dimension. It was shown in [3] that the
underlying system of SDEs can indeed be solved numerically in a very efficient
way. However, a reordering strategy is required at each step to break somehow
the inherent correlations of the sequence of numbers. This makes it difficult to
parallelizethealgorithm,andraisessomedoubtsonwhetherusingquasi-random
numbers can be useful in practice. But if this would be possible, the failure of
n(cid:11)N processors would imply the slightly larger error
(cid:9) (cid:10) (cid:11) (cid:9) (cid:10)(cid:12)
n −1 n
(N −n) −1 log(N −n)=N −1 1− logN +log 1−
N N
≈(1+α)N −1 [logN −α]. (5)
Here we assumed d∗ = 2 and set α := n/N. With α = 0.01, and considering
that N will be at least of the order of the thousands, hence logN (cid:12) α (e. g.,
logN =3 against α=0.01), we obtain
(N −n) −1 log(N −n)≈(1+α)N −1 logN =1.01N −1 logN. (6)
Moreover, due to the full uncoupling among the various subdomains, the
PDD algorithm exhibits fault-tolerance also when those processors working on
small fractions of subdomains fail. In this case, one can fully neglect (in the
firstinstance)thecorrespondingoutput,withouttheneedofresortingtorestart
procedures.
The various sources of numerical error which affect the evaluation of u(x,y)
by means of (2) include, besides the finite sample size mentioned above, (i)
the truncation error made in the numerical solution of the SDEs in (3), not to
mention the round-off errors, (ii) the uncertainty in estimating first exit times
(hitting times), and (iii) the numerical quadrature errors in (2). The latter is
missing whenever the potential term, c(x,y), and the source, f(x,y), in (1) are

6 Juan A. Acebro´n et al.
identicallyzero.Inparticular,estimatingaccuratelyfirstexittimesandfirstexit
points(whicharealsoneededwhenc(x,y)andf(x,y)donotvanishidentically),
hasbeenoftenoverlookedinthe literature.Anefficientwaytolocateaccurately
firstexittimesisadoptingexponentialtimesteppings,see[10].Thischoiceallows
infacttouseanexplicitanalyticformofthehittingprobability.Allthesesources
of error have been analyzed in [1,2], and we shall not do it here again.
3 Numerical examples
Some numerical examples are provided here to compare the performance of the
PDD algorithm described in §1 with that obtained by means of certain deter-
ministic DD algorithms.Despite the factthat “pivotal”values generatedby the
Monte Carlo method are poorly accurateand the Chebyshev interpolationadds
some further error,the total error inside of each subdomain is estimated by the
boundary errors. This is due to the maximum principle, and the error decays
rapidly going inside.
In [1,2,4], a comparison was made only with “parallel finite differences”,
hence a comparison with a true deterministic DD method was not made there.
Moreover,the codewasimplementedinOpenMP,andrunnedinasharedmem-
orycomputerarchitecture.InadditiontothefactthatthePDDmethodoutper-
forms the deterministic DD method, the former wins regarding to the issues of
scalability and fault-tolerance. These properties, not easily achieved by the DD
deterministic methods, should instead be considered at the present time if one
wants to exploit the forthcoming massively parallel supercomputers, equipped
withhundredsofthousandsorevenmillionsofprocessors.The numericalexam-
ples presented below concern, for the purpose of illustration, partial differential
equations on rather elementary domains, indeed, the unit square. Monte Carlo
methods, however, are expected to be useful even on domains having highly
complexgeometries.HereweonlystressthatourprobabilisticDDapproachcan
be easily applied, for instance, to polygonal domains with an arbitrary number
of sides. In fact, one of the most delicate points, which contributes significantly
to the overall numerical error, is given by the need of evaluating accurately the
firstexittimesandpoints,see[1,2].While suchataskmaybechallengingwhen
the boundaries are very irregular, it can be handled easily when the boundary
is piecewise linear. We do not enter into details in this paper.
Anotherrelatedissueis thatofhavingoneormore rathergeneralinterfaces,
insidethedomain.Theirshapemaybeprescribed,duetogeometricalorphysical
reasons. The idea is to “approximate” every (sufficiently smooth) interface by
a piecewise linear one, i.e., by a polygonal line, evaluating numerically on it
few values of the sought solution, to be used for interpolation. This can be
accomplished computing the solution by Monte Carlo methods at some more
pointsonsuchaline.Thesepointsshouldincludetheendpointsofeachsegment
ofthepolygonal,saythek−2internalpointsforapolygonallineofk segments,
and perhaps another point on each segment. The overall cost may therefore
increase, and load balancing become a little harder.

|     |     |     |     |     | A   | fully scalable | parallel algorithm | 7   |
| --- | --- | --- | --- | --- | --- | -------------- | ------------------ | --- |
0
0.01
0.1
|     |     |     |     | 0.2 |     |     | 0.009 |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | --- |
0.008
0.3
0.007
0.4
0.006
y 0.5
0.005
0.6
0.004
0.7
0.003
0.8
0.002
|     |     |     |     | 0.9   |         |     | 0.001 |     |
| --- | --- | --- | --- | ----- | ------- | --- | ----- | --- |
|     |     |     |     | 1     |         |     | 0     |     |
|     |     |     |     | 0 0.8 | 1.6 2.4 | 3.2 | 4     |     |
X
Fig.2.Example1.PointwisenumericalerrorinthePDDalgorithm for p=4.Param-
| eters | are N | =105, | Δx=Δy=1.25×10−3, |     | λ=102. |     |     |     |
| ----- | ----- | ----- | ---------------- | --- | ------ | --- | --- | --- |
Finally, we stress that, due to the full decoupling that the PDD method
realizes,arbitraryandpossibledifferentalgorithmscanbe implementedtosolve
the problem on each subdomain. In particular, serial solvers can be adopted,
taking into accountthatone will face smaller-sizeproblems oneachsubdomain.
However, the point in serious applications is not that to cope with small-size
| problems, |     | but, rather, |     | to be able | to solve | problems | that are much bigger. |     |
| --------- | --- | ------------ | --- | ---------- | -------- | -------- | --------------------- | --- |
A code in an MPI environment has been implemented and runned on the
MareNostrum supercomputer located at the Barcelona Supercomputing Center
(BSC).Below,inordertocomparetherelativeperformanceofthePDDmethod
against some deterministic method, we solved the same examples in both ways.
The chosen deterministic algorithm is extracted from the numerical package
pARMS, having chosen the overlapping Schwarz method with a FGMRES iter-
ative method preconditioned with ILUT as local solver, see [14]. We chose the
package pARMS for its wide and reliable usage, though better codes may ex-
ist for a comparison. The values of the parameters were chosen as follows: For
the outer iterations, the Krylov subspace dimension was 20 and the tolerance
| 10−5, |       |     |          |                |     |          | 10−3          |     |
| ----- | ----- | --- | -------- | -------------- | --- | -------- | ------------- | --- |
|       | while | for | the ILUT | preconditioner | the | dropping | threshold was | and |
the amount of fill in any row 20. The inner iterations were set equal to zero.
To make the comparison meaningful, we discretized the local problems within
the PDD algorithmby finite differences, and solvedthe ensuing linear algebraic
system by the same FGMRES iterative solver preconditioned with ILUT. Here
| are     | our numerical |             | examples. |               |           |                |     |     |
| ------- | ------------- | ----------- | --------- | ------------- | --------- | -------------- | --- | --- |
| Example |               | 1. Consider |           | the following | Dirichlet | problem,       |     |     |
|         |               |             | uxx+uyy   | =0            | in Ω      | :=(0,p)×(0,1), |     | (7) |

| 8 Juan | A. Acebro´n | et al. |     |     |
| ------ | ----------- | ------ | --- | --- |
u(x,y)|
∂Ω =g(x,y), (8)
|                | (cid:13)(cid:14) | (cid:15) (cid:16) |            |                 |
| -------------- | ---------------- | ----------------- | ---------- | --------------- |
|                | x2−y2            | /p2               |            |                 |
| where g(x,y):= |                  | , for the Laplace | equationin | two dimensions. |
∂Ω
Thesolutionofsuchaproblemisexplicitlyknown,andisu(x,y)=(x2−y2)/p2
[0,p]×[0,1].
| in Ω = |     | Note that the domain | was scaled along | the x dimension |
| ------ | --- | -------------------- | ---------------- | --------------- |
proportionally to the number of processors, p, involved. This has been done in
order to keep constant the computational load per processor, being the space
=1.25×10−3.
| discretization | fixed to | Δx=Δy |     |     |
| -------------- | -------- | ----- | --- | --- |
In Fig. 2, the pointwise numerical error made in the PDD method is de-
picted in a contourplot. Here only two nodes on each interface have been used.
Note that the maximum error made in each subdomain is indeed attained on
the corresponding boundary. The exponential timestepping used to solve the
underlying SDEs (3) was characterized by λ := (cid:13)Δt(cid:14)−1, Δt being the random
exponentially distributed time step used in solving the SDEs, and the bracket
denoting its average. Note that maximum error is of order 10−2, which corre-
sponds mainly to the statistical error obtained from the Monte Carlo method
at the nodal points. Increasing the accuracy can be attained by increasing the
sample size, or resorting to sequences of “quasi-random”numbers keeping fixed
| the sample | size, see [2]. |                      |         |     |
| ---------- | -------------- | -------------------- | ------- | --- |
|            |                | Table 1. CPU time in | seconds |     |
|            |                | Processors DD        | PDD     |     |
|            |                | 4 110.49             | 84.05   |     |
132.23 84.12
8
163.81 90.84
16
|     |     | 32 192.22 | 90.54 |     |
| --- | --- | --------- | ----- | --- |
|     |     | 64 335.20 | 88.89 |     |
14184.35 102.22
128
|     |     | 256 NA  | 132.15 |     |
| --- | --- | ------- | ------ | --- |
|     |     | 512 NA  | 129.35 |     |
|     |     | 1024 NA | 148.07 |     |
Table 1 shows the CPU time spent in solving the present problem by the
two algorithms. Clearly, the PDD outperforms the DD method for any number
of processors. This fact becomes more pronounced when the number of proces-
sors increases. This behavior can be explained by the high intercommunication
overheadexisting among processors,which affects strongly the deterministic al-
gorithm. Note that the CPU time for the PDD method remains bounded when
the number of processorsgrows.Testing scalability for larger number of proces-
sors (starting for p = 256) have been accomplished only for the PDD, because
CPU time for DD increasesunboundedly. For this reason,in table 1 CPU times
| are Not | Available (NA). |     |     |     |
| ------- | --------------- | --- | --- | --- |

|         |               |         | A fully | scalable | parallel algorithm |     | 9   |
| ------- | ------------- | ------- | ------- | -------- | ------------------ | --- | --- |
| Example | 2.            |         |         |          |                    |     |     |
|         | The Dirichlet | problem |         |          |                    |     |     |
2
|                   | uxx+(6x | +1)uyy =0 | in  | Ω =(0,p)×(0,1), |          |     | (9)  |
| ----------------- | ------- | --------- | --- | --------------- | -------- | --- | ---- |
| with the boundary | data    |           |     |                 |          |     |      |
|                   |         | (cid:13)  |     |                 | (cid:16) |     |      |
|                   | u(x,y)| | 4         | 2−y | 2 4             | 2        |     |      |
|                   |         | = (x +x   |     | )/2(p           | +p ) ,   |     | (10) |
|                   |         | ∂Ω        |     |                 | ∂Ω       |     |      |
u(x,y)=(x4+x2−y2)/2(p4+p2).
| has the solution |     |     |     |     | Again, the CPU | times | are |
| ---------------- | --- | --- | --- | --- | -------------- | ----- | --- |
reported in Table 2. The same comments made in the previous example can be
| repeated here. |     |              |      |            |     |     |     |
| -------------- | --- | ------------ | ---- | ---------- | --- | --- | --- |
|                |     | Table 2. CPU | time | in seconds |     |     |     |
|                |     | Processors   | DD   | PDD        |     |     |     |
115.94 69.38
4
|     |     | 8   | 110.80 | 70.06 |     |     |     |
| --- | --- | --- | ------ | ----- | --- | --- | --- |
|     |     | 16  | 113.41 | 70.61 |     |     |     |
133.09 70.12
32
255.07 72.19
64
|     |     | 128 | 25827.83 | 75.73 |     |     |     |
| --- | --- | --- | -------- | ----- | --- | --- | --- |
|     |     | 256 | NA       | 67.08 |     |     |     |
NA 65.67
512
|     |     | 1024 | NA  | 64.12 |     |     |     |
| --- | --- | ---- | --- | ----- | --- | --- | --- |
4 Conclusions
A probabilistic method, to accomplish domain decomposition for the numerical
solution of linear elliptic boundary-value problems in two dimensions, has been
described. The solution is generated by Monte Carlo simulations to solve the
associatedstochasticdifferentialequationsonlyatveryfewpointsinsidethedo-
main.AChebyshevinterpolationusingsuchpointsasnodesisthenconstructed,
andafullsplittingintoseveralsubdomains,tobehandledbyseparateprocessors
| acting concurrently, | is made. |     |     |     |     |     |     |
| -------------------- | -------- | --- | --- | --- | --- | --- | --- |
AcomparisonwithadeterministicDDalgorithmhasbeenmadehereforthe
first time. This has been done in an MPI environment. Working in an MPI en-
vironment also allows to test the effect of processor intercommunications which
beset all deterministic DD algorithms. Besides the competitive results observed
in the numericalexamples,the PDD method is expected to be competitive con-
cerningscalabilityandfault-tolerance.Thesearekeyissuesifoneintendstorun
codes on machines working with hundreds of thousands of processors or more.
Finally, we believe the PDD method could be applied, and likely more advan-
tageously, in three or more dimensions. In practice, some more work is needed,

| 10 Juan | A. Acebro´n |     | et al. |     |     |     |     |
| ------- | ----------- | --- | ------ | --- | --- | --- | --- |
especially concerning the important issue of accurately compute first exit times
of the trajectories of the underlying stochastic processes from high-dimensional
domains.
Acknowledgements.
This work was completed during a visit of J.A.A. at the Department of Math-
ematics, University “Roma Tre”, and was supported, in part, by the GNFM
of the Italian INdAM. J.A.A. also acknowledges support from the Ministerio
de Ciencia y Tecnolog´ıa (MEC) through the Ramo´n y Cajal programme. The
authorsthankfully acknowledgethe computer resources,technicalexpertise and
assistance provided by the Barcelona Supercomputing Center-Centro Nacional
de Supercomputacio´n.
References
1. Acebro´n,J.A.,Busico, M.P.,Lanucara,P.,andSpigler,R.,”Domain decomposition
solutionofellipticboundary-valueproblemsviaMonteCarloandquasi-MonteCarlo
| methods”, | SIAMJ. | Sci. | Comput., | 27, | 440–457 (2005). |     |     |
| --------- | ------ | ---- | -------- | --- | --------------- | --- | --- |
2. Acebro´n, J.A., Busico, M.P., Lanucara, P., and Spigler, R., “Probabilistically in-
duced domain decomposition methods for elliptic boundary-value problems”, J.
| Comput. | Phys., | 210, | 421–438 | (2005). |     |     |     |
| ------- | ------ | ---- | ------- | ------- | --- | --- | --- |
3. Acebro´n,J.A.,andSpigler,R.,“Fastsimulationsofstochasticdynamicalsystems”,
| J. Comput. | Phys., | 208, | 106–115 | (2005). |     |     |     |
| ---------- | ------ | ---- | ------- | ------- | --- | --- | --- |
4. Acebro´n,J.A.,andSpigler,R.,“Anewprobabilisticapproachtothedomaindecom-
position method”, Lect. Notes in Comput. Sci. and Eng., Vol. 55, 475–480 (2007)
5. Brenner, S.C., “ Lower bounds of two-level additive Schwarz preconditioners with
| small | overlap”, | SIAMJ. | Numer. | Anal., | 21, 1657–1669 | (2000). |     |
| ----- | --------- | ------ | ------ | ------ | ------------- | ------- | --- |
6. Caflisch, R.E., “Monte Carlo and quasi Monte Carlo methods”, Acta Numerica.
| Cambridge | University |     | Press, | 1–49. (1998). |     |     |     |
| --------- | ---------- | --- | ------ | ------------- | --- | --- | --- |
7. Dryja,M.,andWidlund,O.B.,“Domaindecompositionalgorithmswithsmallover-
| lap”, SIAMJ. |     | Sci. Comput., |     | 15, 604–620 | (1994). |     |     |
| ------------ | --- | ------------- | --- | ----------- | ------- | --- | --- |
8. Freidlin, M.: Functional integration and partial differential equations. Annals of
| Mathematics | Studies |     | no. 109, | Princeton | Univ.Press | (1985). |     |
| ----------- | ------- | --- | -------- | --------- | ---------- | ------- | --- |
9. Geist,G.A.,“ProgresstowardsPetascaleVirtualMachines”,LectureNotesinCom-
| puterScience, |     | 2840, | 10–14 (2003). |     |     |     |     |
| ------------- | --- | ----- | ------------- | --- | --- | --- | --- |
10. Jansons, K.M., and Lythe, G.D., “ Exponential timestepping with boundary test
for stochastic differential equations”, SIAMJ. Sci. Comput., 24 1809–1822 (2003).
11. Keyes,D.E.,“Howscalableisdomaindecompositioninpractice?”intheEleventh
International Conference on Domain Decomposition Methods (London, 1998), 286-
| 297 (electronic), |     | DDM.org, | Augsburg,(1999). |     |     |     |     |
| ----------------- | --- | -------- | ---------------- | --- | --- | --- | --- |
12. Niederreiter, H.: Random number generation and quasi Monte-Carlo methods.
SIAM(1992).
13. Quarteroni,A.,andValli,A.:Domaindecomposition methodsforpartialdifferen-
| tial equations. |     | Oxford | Science | Publications, | Clarendon | Press | (1999). |
| --------------- | --- | ------ | ------- | ------------- | --------- | ----- | ------- |
14. Li, Z., Saad, Y., and Sosonkina, M., “pARMS: a parallel version of the algebraic
recursive multilevel solver”, Numerical Linear Algebra with Applications, 10, 485–
509 (2003).
