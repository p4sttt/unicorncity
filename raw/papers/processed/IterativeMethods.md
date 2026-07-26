Classic Iterative Methods
Dmitry Scherbakov∗ Damir Rakhimov∗
Moscow State University Moscow State University
scherbakovdv@my.msu.ru s02240257@gse.cs.msu.ru
Abstract
Wepresentacomprehensiveanalysisofclassiciterativedomaindecompositionmethods: Dirichlet-
Neumann, Neumann-Neumann (https://gitlab.com/josephofthebread/im); Alternating Schwarz,
Multiplicative Schwarz, Restricted Schwarz, Schur complement (https://gitlab.com/pig-ai/dd
m-framework). Wealsopresentbasictheoreticalfoundationsandbenchmarks(https://wandb.ai/p
ig-ai/IterativeMethods/) with empirical studies.
1 Notations
Throughout the text, we use the following typographical conventions. Lowercase italic letters (x, n, τ)
denote scalars, while boldface lowercase letters (x, n) denote vectors (e.g. x ∈ Rd). Italic uppercase
letters (A, S, R) denote matrices. A superscript n (e.g. un, un) denotes the iteration index, and a
k Γ
subscript k (e.g. Ω , un) denotes the subdomain index.
k k
2 Method properties
What is being iterated. DN, NN and Schur act purely on the interface unknown u ; the volume
Γ
unknownsu areeliminatedalgebraicallyandrecoveredonceattheend. AS,MSandRASiterateonthe
I
fullvectoruoverthewholedomain,withnodistinguishedinterfacevariable–convergenceisastatement
about A, not about a reduced Schur system.
Exact vs. iterative. Schur-complement solution is exact up to rounding: assembling S and solving
Su =g directly requires no tolerance ε or iteration count at all. Its cost is what motivates every other
Γ
row of the table: assembling S explicitly is only possible when local Schur complements S are small
i
enough to form and factor, which fails once a subdomain’s interface is not tiny. DN, NN, AS, MS and
RAS all exist to approximate the action of S−1 (or A−1) without ever forming it.
Symmetry and the choice of Krylov accelerator. NN’s preconditioner P−1 is symmetric positive
definitewhencomposedwithS,soitisusabledirectlyasaRichardsoniterationoracceleratedwithplain
CG. DN’s P−1 is non-symmetric – and needs GMRES. Among the Schwarz methods, AS is symmetric
when A is (making CG available), MS is not symmetric even for symmetric A because the sequential
pass breaks the symmetry between subdomains, and RAS trades the symmetry of AS for a cheaper
communication pattern (only one of the two crossings, R or RTD , is applied at each end) and is used
i i i
with GMRES.
Coloring requirement. DN is the one method in the table that requires an auxiliary combinatorial
object: a proper 2-coloring of the subdomain adjacency graph, separating dirichlet from neumann roles.
Such a coloring need not exist (odd cycles in the adjacency graph), which alone rules DN out for generic
unstructured partitions. NN, AS, MS and RAS treat all subdomains identically and impose no such
constraint.
∗Equalcontribution.
1

Parallelism. Schur, NN,ASandRASareparallelacrosssubdomainswithinoneiteration/application;
onlyaglobalreduction(assemblingS orsummingcorrectionsonΓ)isasynchronizationpoint. DN’stwo
color classes and MS’s Gauss-Seidel pass are both inherently sequential across (at least) that dimension,
which is the practical price of the extra convergence speed MS gets from using freshly updated data
immediately.
Overlapandgeometriclocality. AS,MSandRASrelyonoverlapbetweensubdomainstopropagate
information; the size of the overlap controls the condition number, with condition estimates such as
cond(P−1A) = O(H−2) degrading as the overlap shrinks relative to H, exactly mirroring the non-
overlapping estimates for DN/NN. DN, NN and Schur have no overlap parameter – they instead depend
on the interface geometry and the subdomain diameter H relative to the mesh size h.
Cost per application. Measuredinlocalsubdomainsolves,Schur,NN,ASandRASallcostonelocal
(dirichlet, or dirichlet+neumann for NN) solve per subdomain per application, executed concurrently;
NN’s cost is roughly twice that of AS/RAS per application because it solves both a dirichlet and a
neumannproblemoneverysubdomain,andDNinheritsNN’stwo-problems-per-subdomaincostwithout
NN’s parallelism, since the two colors execute one after the other. MS’s per-pass cost matches AS’s, but
apasstoucheseverysubdomainsequentially,sowall-clockcostperouteriterationscaleswiththenumber
of subdomains rather than staying constant.
Sensitivity to coefficient discontinuities. All six methods are sensitive to jumps in α, but not
equallyso,andnotinthesameway. Ajumpstrictlyinsideasubdomainisabsorbedbythelocal(dirichlet
orneumann)solveonthatsubdomainandbarelydisturbsS orthepreconditioner. Ajumpsittingonthe
interface or overlap region is a different matter: the two sides now carry local operators differing by the
contrast, and any coefficient-blind weighting (uniform multiplicity scaling D for NN, uniform partition-
i
of-unityweightsforRAS)mis-weightsthecorrectionbyexactlythatcontrast,degradingtheconvergence
factor as the jump grows. The standard remedy in all cases is a coefficient-dependent weighting, which
none of the six methods apply by default.
3 Method applications
The classification in table 1 groups the same six methods by where they are actually deployed: the reg-
ularity of the coefficient α they tolerate well, the mesh and partition regime they are built for, how they
scaleunderrefinement,thetypicalusecasethatfollowsfromthoseconstraints,whethertheresultingpre-
conditionerissymmetric,whichKrylovacceleratoritispairedwith,andhowparallelasingleapplication
is.
2

α continuity Mesh / Refinement Typical use Symmetric Accelerator Granularity
|     |     |     | partition |     |     | case |     |     |     |     |     |     |
| --- | --- | --- | --------- | --- | --- | ---- | --- | --- | --- | --- | --- | --- |
no(P−1S
| DN  | tolerates |     | bipartite/ |     | coarser | onlywhena |     |     | GMRES |     | sequential |     |
| --- | --------- | --- | ---------- | --- | ------- | --------- | --- | --- | ----- | --- | ---------- | --- |
interiordis- striped/ meshes, 2-coloringexists non- acrossthe
continuities checkerboard- wherean andischeapto symmetric) twocolors
|     | well;        |     | colorable |     | extrafactor  | build |     |     |     |     |     |     |
| --- | ------------ | --- | --------- | --- | ------------ | ----- | --- | --- | --- | --- | --- | --- |
|     | interface-   |     | adjacency |     | fromthe      |       |     |     |     |     |     |     |
|     | alignedjumps |     | graph     |     | missing      |       |     |     |     |     |     |     |
|     | hurtasmuch   |     |           |     | coarsespace  |       |     |     |     |     |     |     |
|     | asforNN      |     |           |     | isaffordable |       |     |     |     |     |     |     |
NN robustto arbitrary, finemeshes defaultchoicefor yes(SPD, CG fullyparallel
|     | interiordis-  |     | unstructured |     | andmany      | FEM             |     | admitsCG) |     |     |     |     |
| --- | ------------- | --- | ------------ | --- | ------------ | --------------- | --- | --------- | --- | --- | --- | --- |
|     | continuities; |     | partitions,  |     | subdomains,  | substructuring; |     |           |     |     |     |     |
|     | needs         |     | any          |     | providedthe  | CG-compatible   |     |           |     |     |     |     |
|     | coefficient-  |     | subdomain    |     | two-level    |                 |     |           |     |     |     |     |
|     | awareDi       |     | count        |     | (coarse)     |                 |     |           |     |     |     |     |
|     | onceajump     |     |              |     | correctionis |                 |     |           |     |     |     |     |
|     | sitsonΓ       |     |              |     | enabled      |                 |     |           |     |     |     |     |
Schur continuousor few any,aslong referencesolver N/A(direct) none(direct fullyparallel,
discontinuous, subdomains, asSi stays formeasuring solve) onepass
|     | eitherisfine |     | smalllocal |     | factorable | DN/NN/Schwarz   |     |     |     |     |     |     |
| --- | ------------ | --- | ---------- | --- | ---------- | --------------- | --- | --- | --- | --- | --- | --- |
|     |              |     | interfaces |     |            | iterationcounts |     |     |     |     |     |     |
AS robustto unstructured, benefitsfrom general-purpose, yesifASPD CG fullyparallel
|     | interiordis-   |     | overlapping  |     | acoarse    | symmetric-A     |     |     |     |     |     |     |
| --- | -------------- | --- | ------------ | --- | ---------- | --------------- | --- | --- | --- | --- | --- | --- |
|     | continuities;  |     | partitions   |     | spaceas    | Krylov          |     |     |     |     |     |     |
|     | overlap-region |     | withgenerous |     | subdomain  | preconditioning |     |     |     |     |     |     |
|     | jumpsbehave    |     | overlap      |     | countgrows |                 |     |     |     |     |     |     |
likeNN’s
interfacecase
MS same small any; serialorcoarse- no(evenfor GMRESor sequential
toleranceas subdomain convergence grained-parallel SPDA) Richardson pass
|     | AS  |     | counts,or   |     | perpassis     | settings, |     |     |     |     |     |     |
| --- | --- | --- | ----------- | --- | ------------- | --------- | --- | --- | --- | --- | --- | --- |
|     |     |     | usedasa     |     | largely       | multigrid |     |     |     |     |     |     |
|     |     |     | local       |     | refinement-   | smoothing |     |     |     |     |     |     |
|     |     |     | smoother    |     | insensitiveat |           |     |     |     |     |     |     |
|     |     |     | ratherthana |     | fixedH/h      |           |     |     |     |     |     |     |
globalsolver
RAS same unstructured, benefitsfrom preferredover no GMRES fullyparallel
|     | toleranceas |     | overlapping |     | acoarse    | ASwhen        |     | (asymmetric |     |     |     |     |
| --- | ----------- | --- | ----------- | --- | ---------- | ------------- | --- | ----------- | --- | --- | --- | --- |
|     | AS          |     | partitions, |     | spaceas    | communication |     | byconstruc- |     |     |     |     |
|     |             |     | larger      |     | subdomain  | volumeisthe   |     | tion)       |     |     |     |     |
|     |             |     | subdomain   |     | countgrows | bottleneck    |     |             |     |     |     |     |
countsthan
ASis
comfortable
with
Table 1: Applications: coefficient regularity, mesh and partition assumptions, refinement behavior, typi-
calusecase,symmetry,Krylovacceleratorandparallelgranularity. Bluemarksnon-overlappingmethods
(Ω ∩Ω =∅), orange marks overlapping (Schwarz-type) methods, and gray marks the Schur comple-
i j
| ment,                                  | a direct | method | with      | no        | decomposition | topology  | to classify. |     |     |     |     |     |
| -------------------------------------- | -------- | ------ | --------- | --------- | ------------- | --------- | ------------ | --- | --- | --- | --- | --- |
| 4                                      | Problem  |        | statement |           |               |           |              |     |     |     |     |     |
| Figure1denotestwosubdomains(opensets)Ω |          |        |           |           |               | andΩ      | ofΩ,         |     |     |     |     |     |
|                                        |          |        |           |           |               | 1 2       |              |     |     |     |     |     |
| where                                  | Ω =      | Ω ∪Ω   | . ∂Ω      | is called | a physical    | boundary, | while        |     |     |     |     |     |
|                                        |          | 1      | 2         |           |               |           |              |     |     |     |     |     |
| Γ :=                                   | (∂Ω      | ∪∂Ω    | )\∂Ω      | is called | an interface. | We also   | use          |     |     |     |     | Ω   |
1 2
:=
| Γ i | Γ∩Ω | i denoting | an  | interface, | relative | to a subdomain |     |     |     | n   |     |     |
| --- | --- | ---------- | --- | ---------- | -------- | -------------- | --- | --- | --- | --- | --- | --- |
1
| Ω .                                             | AteverypointofΓwedenotebyn |     |     |                            | theoutwardunitnor- |     |       |     |     |     |     |     |
| ----------------------------------------------- | -------------------------- | --- | --- | -------------------------- | ------------------ | --- | ----- | --- | --- | --- | --- | --- |
| i                                               |                            |     |     |                            | i                  |     |       |     |     | Γ   |     |     |
| malofΩ                                          | ,sothatn                   |     | =−n | onΓ;thesearethenormalsused |                    |     |       |     | Ω 1 |     | Ω 2 |     |
|                                                 | i                          |     | 1   | 2                          |                    |     |       |     |     |     |     |     |
| throughoutwhenmatchingfluxesacrosstheinterface. |                            |     |     |                            |                    |     | These |     |     |     |     |     |
n
definitions naturally extend to d-dimensional case. We then 2
| consider | the | following | elliptic |     | problem | with (only, for | sim- |        |        |           |       |     |
| -------- | --- | --------- | -------- | --- | ------- | --------------- | ---- | ------ | ------ | --------- | ----- | --- |
|          |     |           |          |     |         |                 |      | Figure | 1: Two | subdomain | case. |     |
3

| plicity) dirichlet | boundary | conditions on | physical boundary: |     |     |
| ------------------ | -------- | ------------- | ------------------ | --- | --- |
(cid:40)
|     | −∇·(α∇u)=f, | x∈Ω⊂Rd, |     |     |     |
| --- | ----------- | ------- | --- | --- | --- |
(cid:12)
|     | u(cid:12) =u . |     |     |     |     |
| --- | -------------- | --- | --- | --- | --- |
0
∂Ω
In all cases, we assume finite-element method (FEM) discretization (Brenner and Scott, 2008), that
assembles a linear system with banded n×n matrix, where n denotes the number of approximation
points.
| 5 Dirichlet-Neumann |     | and | Neumann-Neumann |     | iterations |
| ------------------- | --- | --- | --------------- | --- | ---------- |
Dirichlet-Neumann(DN)andNeumann-Neumann(NN)iterationsarenon-overlapping domaindecompo-
sition methods, which involve repeatedly solving dirichlet and neumann problems on each of the subdo-
mainΩ . Westartwithasimplecaseofa(good,i.e. smooth)2Ddomain,partitionedinto2subdomains
k
in section 5.1 and extend derived results to multidimensional case in section 5.2.
| 5.1 Simple | case |     |     |     |     |
| ---------- | ---- | --- | --- | --- | --- |
This section aims togive practical intuition, rather than hardtheory. Westart with a simple 2Dcase, as
denotedinfigure1. Bothalgorithmsareeasy-enoughtounderstandrightaway. Convergenceestimations
| derivation | and practical tweaks | for generic | case live in section | 5.2. |     |
| ---------- | -------------------- | ----------- | -------------------- | ---- | --- |
The key thing to keep in mind throughout both algorithms below is what they are not doing: at no
pointdowesolveforthefullsolutionuonallofΩatonce. Alloftheiterating,relaxingandflux-matching
happens exclusively on the interface Γ, which is a much smaller unknown than u itself. Once un has
Γ
converged to the correct boundary values, recovering the actual solution is a single, final dirichlet solve
on each subdomain Ω . And, since these final solves only depend on the (now fixed and shared) values
k
| on Γ, they | can be carried | out independently | and in parallel. |     |     |
| ---------- | -------------- | ----------------- | ---------------- | --- | --- |
Dirichlet-Neumann iteration. Wefixaguessun fortheboundaryvaluesonΓandsolveanordinary
Γ
Dirichlet problem on Ω , treating un as a dirichlet boundary condition on Γ. This produces a solution
|     | 1   | Γ   |     |     |     |
| --- | --- | --- | --- | --- | --- |
on Ω , from which we read off the flux it induces on Γ. That flux is then used on Ω as a Neumann
| 1   |     |     |     |     | 2   |
| --- | --- | --- | --- | --- | --- |
condition on Γ (while keeping u 0 on physical boundary), and solving this mixed problem produces a new
boundary value on Γ. Relaxation between the old and new boundary values gives un+1, and the process
Γ
repeats until the two subdomains agree closely enough. The pseudocode is summarized in algorithm 1.
Neumann-Neumanniteration. NNis“moresymmetric”,comparedtoDN,treatingbothsubdomains
identically. Both Ω and Ω independently solve a Dirichlet problem using the current guess un on Γ,
|     | 1   | 2   |     |     | Γ   |
| --- | --- | --- | --- | --- | --- |
producing two solutions that (in general) disagree with each other in terms of flux across Γ. This flux
mismatch is exactly the residual we want to minimize. Both subdomains then solve a Neumann problem
driven by that mismatch (zero on physical boundary and flux on Γ), and the resulting corrections are
used to update un towards un+1. The pseudocode is summarized in algorithm 2.
|     | Γ   | Γ   |     |     |     |
| --- | --- | --- | --- | --- | --- |
4

Algorithm 1 Dirichlet-Neumann iteration Algorithm 2 Neumann-Neumann iteration
Require: initial guess u0 on Γ, relaxation τ ∈ Require: initial guess u0 on Γ, relaxation τ ∈
Γ Γ
(0,1), tolerance ε (0,1), tolerance ε, scaling operators D on Γ
k
1: n←0 with D 1 +D 2 =I
2: repeat 1: n←0
3: Solve Dirichlet problem: 2: repeat
−∇·(α∇un 1 )=f in Ω 1 , 3: for k =1,2 do
un 1 =u 0 on ∂Ω 1 \Γ, un 1 =un Γ on Γ 4: Solve Dirichlet problem:
∂un −∇·(α∇un)=f in Ω ,
4: Compute flux φn =α 1 on Γ k k
∂n un =u on ∂Ω \Γ, un =un on Γ
1 k 0 k k Γ
5: Solve mixed problem: 5: end for
−∇·(α∇un)=f in Ω , ∂un ∂un
2 2 ∂un 6: Compute flux gn =α ∂n 1 +α ∂n 2 on Γ
un =u on ∂Ω \Γ, α 2 =−φn on Γ 1 2
2 0 2 ∂n 7: for k =1,2 do
6: un+1 ←τun (cid:12) (cid:12) +(1−τ)un 2 8: Solve Neumann problem:
7: n Γ ←n+1 2 Γ Γ −∇·(α∇un k )=0 in Ω k ,
8: until ∥un Γ −un Γ −1∥<ε un k =0 on ∂Ω k \Γ, α ∂ ∂ n un k =gn on Γ
k
9: end for
10: un+1 ←un−τ (cid:0) un (cid:12) (cid:12) +un (cid:12) (cid:12) (cid:1)
Γ Γ 1 Γ 2 Γ
11: n←n+1
12: until ∥un−un−1∥<ε
Γ Γ
Our writings on both DN and NN follow the theory presented in (Quarteroni and Valli, 1991; Quar-
teroni and Valli, 1999) and, for NN specifically, in (Bourgat et al., 1989) as well; we highly encourage
readers to review the theory and proofs, presented in these materials.
5.2 Generic case
After discretization, we end up with a linear system Ax=f, which, without the loss of generality can be
rewritten as follows:
(cid:20) (cid:21)(cid:20) (cid:21) (cid:20) (cid:21) (cid:40)
A A u f A u +A u =f
II IΓ I = I ⇐⇒ II I IΓ Γ I . (1)
A ΓI A ΓΓ u Γ f Γ +ϕ A ΓI u I +A ΓΓ u Γ =f Γ +ϕ
Here, we split all points in a triangulation in two sets: those, which are either on the physical boundary
or on the interface (denoted as Γ), and the rest (denoted as I); so A is a submatrix of A, which is
II
formed by elements that lie on the intersection of rows and columns of A, corresponding to I points;
submatrices A , A and A are defined similarly; ϕ is a flux on boundary (not zero, due to the way
IΓ ΓI ΓΓ
we define basis functions in FEM – they don’t come from H (Ω), which is a contradiction, in general):
0
(cid:82)
ϕ= α∂ udx. Duringiteration, theunknownthingin(1)isu ; derivingitfromthefirstequationand
Γ n I
substituting in second, we get
ϕ=A A−1(f −A u )+A u −f =(A −A A−1A )u +A A−1f −f =Su −g.
ΓI II I IΓ Γ ΓΓ Γ Γ ΓΓ ΓI II IΓ Γ ΓI II I Γ Γ
(cid:124) (cid:123)(cid:122) (cid:125) (cid:124) (cid:123)(cid:122) (cid:125)
S g
The resulting expression clearly separates into two parts: that depends on a boundary value u (first),
Γ
and that depends on the source term f (second). Here, S is a Poincaré-Steklov operator, which evaluates
a flux, given values on boundary. Recall that total flux on interface, ϕ, is zero, when u is a solution
function. That is, when u is correct, Su −g=0, and we can derive a fixed point iteration on u :
Γ Γ Γ
un+1 =un−τP−1(Sun−g), (2)
Γ Γ Γ
where P−1 is an operator, that maps flux back to u . In theory, we could just write P−1 = S−1, but
Γ
when working with a fine mesh we not only can’t assemble A – we can’t assemble S and, obviously, S−1
(that’s not even a domain decomposition to begin with).
Remark 1 (A few words on S matrix). As it was mentioned before, it is a discrete approximation of
(cid:20) (cid:21)
A B
Poincaré-Steklovoperator, whichiscalledtheSchurcomplement. ConsiderM = , thentheSchur
C D
5

|     |     |     |     |     |     | :=D−CA−1B, |     |     |     | :=A−BD−1C. |     |
| --- | --- | --- | --- | --- | --- | ---------- | --- | --- | --- | ---------- | --- |
complement of the block A in M is called M/A or, for block D, M/D
| This originates |     | from gaussian |          | elimination |     | process: |          |     |          |     |     |
| --------------- | --- | ------------- | -------- | ----------- | --- | -------- | -------- | --- | -------- | --- | --- |
|                 |     |               | (cid:20) |             |     | (cid:21) | (cid:20) |     | (cid:21) |     |     |
|                 |     |               |          | A           | B   |          | A−BD−1C  |     | 0        |     |     |
|                 |     | M             | ∼        |             |     | or M     | ∼        |     |          | .   |     |
|                 |     |               |          | 0 D−CA−1B   |     |          |          | C   | D        |     |     |
P−1Su
Remark 2. Formula (2) is exact formula for Richardson iterative method, but for solving Γ =
P−1g, which is just a preconditioned system. But we have other better methods for solving Su = g:
Γ
preconditioned conjugate gradients (PCG) or preconditioned GMRES, which, essentially, choose iteration
| parameter | τ adaptively. |     |     |     |     |     |     |     |     |     |     |
| --------- | ------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The obvious next step would be decompose (2) to avoid constructing giant matrices. This is where
differences between two method are introduced. The problem is that 2-domain (but not necessarily
2D) DN iteration, described in section 5.1 doesn’t naturally generalize to multi-domain case, while NN
iteration does. One huge disadvantage DN suffers from is that we have to decide which domain do
dirichletsolveandwhichdomixed-neumannsolve,whichrequiresaconsistent2-coloringofthesubdomain
adjacency graph, and such coloring is not even guaranteed to exist for an arbitrary subdomain partition
(e.g. if adjacency graph contains odd cycles). We therefore first provide NN explanations.
| 5.2.1 NN | iteration |     |     |     |     |     |     |     |     |     |     |
| -------- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Calculating a flux ϕ on entire Γ is equivalent to solving a local dirichlet problems on all domains and
summing up the flux (which, by the means of physics, is an additive metric). This is, essentially, what is
done on practice, for each subdomain: (1) assemble a linear system with dirichlet boundary conditions,
(2) solve this system locally (CG or simple gaussian elimination), (3) calculate flux. Theoretically this is
equivalent to doing exactly S u −g , where S is a simply local Poincaré-Steklov operator.
|     |     |     |     | i Γi | i   | i   |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- |
Since the partition into subdomains is arbitrary, the only thing left to do is to map local vertex
numbers to global ones and back – an index remap. This is done using remap matrices R :R|Γi| →R|Γ|,
i
| containing      | only | ones and   | zeroes. | Then           |          |           |          |          |       |      |     |
| --------------- | ---- | ---------- | ------- | -------------- | -------- | --------- | -------- | -------- | ----- | ---- | --- |
|                 |      | p          |         |                | p        |           |          | p        |       |      |     |
|                 |      | (cid:88)   |         |                | (cid:88) |           | (cid:88) |          |       |      |     |
|                 | S    | = RTS      | R       | ,              | g=       | RTg , and |          | RT [S (R | u )−g | ]=0, | (3) |
|                 |      |            | i i     | i              |          | i i       |          | i i      | i Γ   | i    |     |
|                 |      | i=1        |         |                | i=1      |           | i=1      |          |       |      |     |
| where p denotes |      | the number |         | of subdomains. |          |           |          |          |       |      |     |
As it was mentioned before, P−1 operator maps flux back to boundary values, which is exactly
equivalent to solving neumann problems locally, on each subdomain: given a flux residual R (Su −g)
|                 |     |           |     |         |           |         |        |     |     | i   | Γ   |
| --------------- | --- | --------- | --- | ------- | --------- | ------- | ------ | --- | --- | --- | --- |
| on Γ , applying |     | S−1 leads | to  | solving | a Neumann | problem | on Ω . |     |     |     |     |
| i               |     | i         |     |         |           |         | i      |     |     |     |     |
P−1
| Assembling |     | from | these | local | pieces | is now straightforward: |     |     |     |     |     |
| ---------- | --- | ---- | ----- | ----- | ------ | ----------------------- | --- | --- | --- | --- | --- |
p
(cid:88)
|     |     |     |     |     |     | P−1 = RTS−1R | .   |     |     |     | (4) |
| --- | --- | --- | --- | --- | --- | ------------ | --- | --- | --- | --- | --- |
|     |     |     |     |     |     | i            | i i |     |     |     |     |
i=1
|     |     |     |     |     |     |     |     | S−1 |     |     | S−1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Formulas (3) and (4) prove constructively, that we never form S or explicitly – each term is
i
applied to a small, local vector supported on Γ , and RT simply scatters the result back into the global
|     |     |     |     |     |     | i i |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
interface vector. This is the base method. Next, we discuss practical tweaks.
Scaling matrices. So far, formula (4) silently assumes that each point of Γ belongs to exactly two
subdomains. This is not true in general: whenever three or more subdomains meet at a single ver-
tex, summing RTS†R over all subdomains touching that vertex would add its contribution once per
i i i
subdomain, i.e. overcount the flux there. To fix this, we introduce diagonal scaling matrices D i :
|     |     |     |     | p        |     |           | p   |         |     |     |     |
| --- | --- | --- | --- | -------- | --- | --------- | --- | ------- | --- | --- | --- |
|     |     |     |     | (cid:88) |     | (cid:88)  |     |         |     |     |     |
|     |     |     |     | RTD      | R   | =I, P−1 = | RTD | S†D R   | .   |     | (5) |
|     |     |     |     | i        | i i |           | i   | i i i i |     |     |     |
|     |     |     |     | i=1      |     | i=1       |     |         |     |     |     |
Other variations of D are also common, but multiplicity scaling is the simplest.
i
Adaptive step size. As mentioned in remark remark 2, plain Richardson iteration with constant τ
can be improved with Krylov methods or even Chebyshev τ selection method. In case of NN iteration,
P−1S matrixisSPD,regardlessofwhetherP−1 isone-ortwo-levelpreconditioner,whichmeanswecan
| leverage PCJ | method. |     |     |     |     |     |     |     |     |     |     |
| ------------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
6

Floating domains and convergence. Note that if Ω i subdomain’s boundary ∂Ω i has no common
points with physical boundary ∂Ω, the neumann problem is singular. Such domains are called floating
domains. This means that S−1 is not defined, because it is singular. Obvious solution is a pseudoinverse
S†
matrix (but, say, Tikhonov regularization can work out as well). Intuitively, this introduces a prob-
lem of different constants being picked up on different floating subdomains, because solutions of such
neumann problems form a one-dimensional linear subspace (i.e. u Γi and u Γi +c both are solutions),
and pseudoinverse operator chooses a solution with minimal length. This arbitrary constant choose can
slow down completely or even cause solver to diverge. Obviously, if iteration converges, we have “some”
H1(Ω))oninterface,duetodifferentconstants,which
| solution,whichisnotguaranteedtobe“good” |     |     |     | (i.e. |     |     |     |
| --------------------------------------- | --- | --- | --- | ----- | --- | --- | --- |
is not what we need. This is why we want these constants to be adjusted, which is what is done with a
| two-level | preconditioner: |     |     |     |     |     |     |
| --------- | --------------- | --- | --- | --- | --- | --- | --- |
:=P−1+P−1.
P−1
|     |     |     |     | c   | f   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
Here,P−1 isafinemeshpreconditioner,exactlyasdefinedin(5);andP−1 isacoarsegridpreconditioner,
| f   |     |     |     |     |     | c   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
application of which’s on a subdomain is equivalent to solving of minimization problem
∥Za−e∥2
|     |     |     |     |     | (cid:55)→min. |     | (6) |
| --- | --- | --- | --- | --- | ------------- | --- | --- |
|     |     |     |     | S   | a             |     |     |
Rn×q
where Z ∈ is a matrix, assembled by combining kernel vectors (i.e. vectors of all ones) of S i
on each subdomain, projected to a global domain with R matrices; a is a vector of q constants on q
i
floating subdomains; and e is an absolute convergence error. S-norm is used here, because P−1S is
P−1
symmetric in S, and applications of P−1 and don’t mess with each other. Problem (6) is equivalent
|                  |     |        | c               | f       |     |     |     |
| ---------------- | --- | ------ | --------------- | ------- | --- | --- | --- |
| to ZTSZ(−a)=ZTr, |     | with a | small dense q×q | matrix. |     |     |     |
Condition number estimations. For the one-level NN preconditioner of (5) the estimate is
|     |     |     |     |     | (cid:18) | (cid:19)2 |     |
| --- | --- | --- | --- | --- | -------- | --------- | --- |
H
|     |     |     | cond(P−1S)≤CH−2 |     | 1+log | ,   | (7) |
| --- | --- | --- | --------------- | --- | ----- | --- | --- |
h
whereH =max ρ(x,y)isasubdomaindiameter(growsdownasrefinementincreases,H =O(1)),
x,y∈Ωk
n
h is a max diameter of simplex in triangulation and C is a constant. The H−2 factor is exactly the price
of having no coarse, global coupling between subdomains – information can only travel one subdomain
at a time per iteration. Adding the coarse-grid correction of (6) removes it, giving the two-level NN
| preconditioner | the | better estimate: |     |     |            |           |     |
| -------------- | --- | ---------------- | --- | --- | ---------- | --------- | --- |
|                |     |                  |     |     | (cid:18) H | (cid:19)2 |     |
cond(P−1S)≤C
|     |     |     |     |     | 1+log | ,   | (8) |
| --- | --- | --- | --- | --- | ----- | --- | --- |
h
whichisindependentofH (andhenceofthenumberofsubdomains)aswell(QuarteroniandValli,1999).
| 5.2.2 DN | iteration |     |     |     |     |     |     |
| -------- | --------- | --- | --- | --- | --- | --- | --- |
As it was mentioned already, DN requires a proper subdomain coloring, which can be relatively com-
plicated (or not exist at all). Given such a coloring, generic DN iteration proceeds exactly as in the
2-domain case, just applied class-by-class: (1) solve a dirichlet problem using un on Γ and computes
Γ i
the induced flux on dirichlet domains, (2) solve a mixed problem using previously computed flux values,
| (3) relax | the resulting | boundary | values. |     |     |     |     |
| --------- | ------------- | -------- | ------- | --- | --- | --- | --- |
Schur-complementcompatibleconstruction. RatherthantreatingDNasaseparatealgorithm,we
buildP−1
fromexactlythesameper-subdomainbuildingblocksS i ,R i andD i ,usedforNNinequations
(3)and(4). LetP−1 andP−1 denotethatverysameconstruction,eachrestrictedtooneofthetwocolor
|     | D   | N   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
classes fixed by the 2-coloring (D for dirichlet subdomains, N for neumann ones); both are symmetric,
for the same reason P−1 itself is in (4). Method then corrects the two roles in sequence within a single
application:
|     | un+1/2 |                 |     |      | =un+1/2−P−1(Sun+1/2−g), |     |     |
| --- | ------ | --------------- | --- | ---- | ----------------------- | --- | --- |
|     |        | =un−P−1(Sun−g), |     | un+1 |                         |     | (9) |
|     |        | Γ Γ             | D Γ | Γ    | Γ                       | N Γ |     |
which is already visibly different from NN’s single simultaneous update in (4): D and N never see the
same residual. Since Sun+1/2−g = (I −SP−1)rn, substituting into (9) and collecting terms gives the
|            |          | Γ    |            | D   |                    |     |     |
| ---------- | -------- | ---- | ---------- | --- | ------------------ | --- | --- |
| equivalent | one-shot | form |            |     |                    |     |     |
|            |          | un+1 | =un−P−1rn, | P−1 | :=P−1+P−1−P−1SP−1. |     |     |
(10)
|     |     | Γ   | Γ   |     | D   | N N D |     |
| --- | --- | --- | --- | --- | --- | ----- | --- |
7

| TransposingP−1 |     | from(10)(usingthefactthatP−1, |     |     |     |     | P−1,                                  |     |     |     |
| -------------- | --- | ----------------------------- | --- | --- | --- | --- | ------------------------------------- | --- | --- | --- |
|                |     |                               |     |     |     |     | andS areeachsymmetricontheirown)gives |     |     |     |
|                |     |                               |     |     |     |     | D N                                   |     |     |     |
P−1+P−1−P−1SP−1, whichcorrespondstocorrectingN beforeD instead, andisgenerallyadifferent
| D   | N   | D   | N   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
operator from P−1 itself. This is the price of processing the two roles in sequence, as in (9), instead of
| applying | a single | simultaneous |     | sum, | as  | NN does | in (4). |     |     |     |
| -------- | -------- | ------------ | --- | ---- | --- | ------- | ------- | --- | --- | --- |
Adaptive step size. BecauseDN’sP−1S isnotsymmetric, adaptivestepsizeselectioncannotrelyon
| plain PCG | the | way | NN does; | GMRES |     | is required | instead. |     |     |     |
| --------- | --- | --- | -------- | ----- | --- | ----------- | -------- | --- | --- | --- |
Condition number estimations. In the 2-subdomain setting of section 5.1, both the DN and the
cond(P−1S)
NN preconditioner are optimal: is bounded by a constant independent of h. This mesh-
independenceislostoncewemovetomanysubdomains,andtheconditionnumberpicksupadependence
onthesubdomainsizeH aswell. DNadmitsnocomparablycleanbound,sinceitsP−1Sisnotsymmetric,
so (7) and (8) do not directly apply to it; empirically it behaves like one-level NN or worse, consistent
| with the    | iteration | counts       | reported |           | in the     | benchmarks | below.     |     |     |     |
| ----------- | --------- | ------------ | -------- | --------- | ---------- | ---------- | ---------- | --- | --- | --- |
| 6 Schwarz   |           |              | and      | Schur     | complement |            | iterations |     |     |     |
| We consider |           | the same     | elliptic | model     | problem    | with       | dirichlet  |     |     |     |
| conditions  | on        | the physical |          | boundary: |            |            |            |     |     | Γ   |
|             |           | (cid:40)     |          |           | x∈Ω⊂Rd,    |            |            |     |     |     |
−∇·(α∇u)=f,
|     |     | (cid:12)   |        |     |     |     |     | Ω Ω  | Ω   |     |
| --- | --- | ---------- | ------ | --- | --- | --- | --- | ---- | --- | --- |
|     |     | u (cid:12) | =u 0 , |     |     |     |     | 1 12 | 2   |     |
∂Ω
| and four | domain          | decomposition |         | methods |        | for it:  | three mem- |     |     |     |
| -------- | --------------- | ------------- | ------- | ------- | ------ | -------- | ---------- | --- | --- | --- |
| bers of  | the overlapping |               | Schwarz |         | family | – damped | additive   |     |     |     |
Schwarz (AS), multiplicative Schwarz (MS) and restricted Figure 2: Two overlapping subdomains.
| additive   | Schwarz          | (RAS) |     | – and   | the non-overlapping |          | Schur       |     |     |     |
| ---------- | ---------------- | ----- | --- | ------- | ------------------- | -------- | ----------- | --- | --- | --- |
| complement | (substructuring) |       |     | method. |                     | Figure 2 | denotes the |     |     |     |
overlappingsetting: subdomainsΩ 1 andΩ 2 coverΩ=Ω 1 ∪Ω 2 andsharetheoverlapregionΩ 12 =Ω 1 ∩Ω 2 .
The part of ∂Ω that lies strictly inside Ω is called the artificial boundary of Ω ; unlike the interface Γ
|     |     | i   |     |     |     |     |     | i   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of non-overlapping methods, it carries no unknowns of its own – it is simply where one subdomain reads
| values off | its    | neighbours. |     |     |     |     |     |     |     |     |
| ---------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6.1        | Simple | case        |     |     |     |     |     |     |     |     |
As before, this section aims for practical intuition on the two-subdomain case of figure 2; the algebraic
| multi-domain |     | machinery | lives | in  | section | 6.2. |     |     |     |     |
| ------------ | --- | --------- | ----- | --- | ------- | ---- | --- | --- | --- | --- |
Thekeycontrastwiththeinterface-basedDNandNNiterationsiswhattheSchwarzmethodsdonot
have: there is no separate interface unknown, no flux matching and no interface operator. The iterate
un
is the full field on all of Ω, and every step improves it by re-solving the equation locally, using the
current values of un as artificial dirichlet data. Information propagates from one subdomain to the other
only through the overlap Ω , which is why the convergence rate of every Schwarz method improves as
12
| the overlap | widens. |     |     |     |     |     |     |     |     |     |
| ----------- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Multiplicative Schwarz. This is the original alternating method of H.A. Schwarz (1870). Solve the
problem on Ω with un supplying the dirichlet data on the artificial boundary; update the iterate there;
1
then solve on Ω 2 , whose artificial data already sees the fresh Ω 1 values; repeat. The subdomains are
| processed | sequentially, |     | in  | a Gauss–Seidel |     | fashion. |     |     |     |     |
| --------- | ------------- | --- | --- | -------------- | --- | -------- | --- | --- | --- | --- |
Additive Schwarz. Both subdomains solve their local problems simultaneously, each using the same,
un
old iterate for its artificial data, and the two corrections are added at once, in a Jacobi fashion. This
makes the sweep embarrassingly parallel, but in the overlap both corrections target the same error, so
| their plain | sum | overshoots |     | and the | update | must | be damped. |     |     |     |
| ----------- | --- | ---------- | --- | ------- | ------ | ---- | ---------- | --- | --- | --- |
RestrictedadditiveSchwarz. RAS(CaiandSarkis,1999)removestheovercountinginsteadofdamp-
ingit: thelocalproblemsarestillsolvedonthefulloverlappingsubdomains,buteachpointoftheoverlap
accepts the correction from exactly one, fixed owner subdomain. Every point is then updated exactly
once per sweep, no damping is needed, and the parallelism of the additive variant is retained.
8

| 6.2 | Generic |     | case |     |     |     |     |     |     |     |     |     |     |
| --- | ------- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
After discretization the subdomains become index sets: subdomain Ω collects the degrees of freedom of
i
∈{0,1}ni×n
allverticesitcontains,andtheindex remap matricesR i (exactlyasintheNNconstruction)
gather local values out of a global vector. The local operator is the principal submatrix
|     |     |     |     |     |     |     | A =R | ART, |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | --- | --- | --- | --- | --- |
|     |     |     |     |     |     |     | i    | i i  |     |     |     |     |     |
and solving A i δ i = R i r is the discrete analogue of the local dirichlet solve of section 6.1: the rows of A
are restricted to the subdomain, which is equivalent to imposing zero dirichlet data on the first ring of
vertices outside it. For RAS we additionally fix diagonal 0/1 partition-of-unity masks D , marking for
i
| every | subdomain | the | degrees | of  | freedom | it owns, | so  | that |     |     |     |     |     |
| ----- | --------- | --- | ------- | --- | ------- | -------- | --- | ---- | --- | --- | --- | --- | --- |
p
(cid:88)
RTD
|     |     |     |     |     |     |     |     | i R i =I, |     |     |     |     | (11) |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | --- | ---- |
i
i=1
where p denotes the number of subdomains. The three sweeps are summarized in algorithms 3 to 5.
Algorithm 3 Additive Schwarz Algorithm 4 Multiplicative Schwarz
Require: restrictions R , local matrices A = Require: restrictions R , local matrices A =
|     |               |         |           | i        |           |     | i   |         |               |           | i            |     | i   |
| --- | ------------- | ------- | --------- | -------- | --------- | --- | --- | ------- | ------------- | --------- | ------------ | --- | --- |
|     | ART,          |         |           |          |           |     |     |         | ART,          |           |              |     |     |
|     | R i           | damping | θ ∈(0,1], |          | tolerance | ε   |     | R i     |               | tolerance | ε            |     |     |
|     | i             |         |           |          |           |     |     |         | i             |           |              |     |     |
| 1:  | u0 ←0,        | n←0     |           |          |           |     |     | 1: u←0, | n←0           |           |              |     |     |
|     | repeat        |         |           |          |           |     |     | repeat  |               |           |              |     |     |
| 2:  |               |         |           |          |           |     |     | 2:      |               |           |              |     |     |
| 3:  | rn ←b−Aun     |         |           |          |           |     |     | 3:      | for i=1,...,p |           | sequentially | do  |     |
|     | for i=1,...,p |         | in        | parallel | do        |     |     |         | r←b−Au        |           |              |     |     |
| 4:  |               |         |           |          |           |     |     | 4:      |               |           |              |     |     |
|     |               |         | n         | rn       |           |     |     |         |               |           |              |     |     |
| 5:  | Solve         | A       | i δ =R    | i        |           |     |     | 5:      | Solve         | A i       | δ i =R i r   |     |     |
i
| 6:  | end | for |     |     |     |     |     | 6:  | u←u+R |     | Tδ  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
i i
|     |      |       | p        |      |     |     |     |     | end | for |     |     |     |
| --- | ---- | ----- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | un+1 | ←un+θ | (cid:88) | RTδn |     |     |     | 7:  |     |     |     |     |     |
7:
|     |     |     |     | i   | i   |     |     | 8:  | n←n+1 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
i=1
until ∥b−Au∥<ε
| 8:        | n←n+1        |                    |     |          |          |      |       | 9:  |     |     |     |     |     |
| --------- | ------------ | ------------------ | --- | -------- | -------- | ---- | ----- | --- | --- | --- | --- | --- | --- |
| 9:        | until ∥rn∥<ε |                    |     |          |          |      |       |     |     |     |     |     |     |
| Algorithm |              | 5 Restricted       |     | Additive | Schwarz  |      |       |     |     |     |     |     |     |
| Require:  | restrictions |                    | R   | , local  | matrices |      | A =   |     |     |     |     |     |     |
|           |              |                    |     | i        |          |      | i     |     |     |     |     |     |     |
|           | R ART,       | partition-of-unity |     |          | masks    | D of | (11), |     |     |     |     |     |     |
|           | i i          |                    |     |          |          | i    |       |     |     |     |     |     |     |
|           | tolerance    | ε                  |     |          |          |      |       |     |     |     |     |     |     |
| 1:        | u0 ←0,       | n←0                |     |          |          |      |       |     |     |     |     |     |     |
2: repeat
| 3:  | rn ←b−Aun     |     |     |          |     |     |     |     |     |     |     |     |     |
| --- | ------------- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     | for i=1,...,p |     | in  | parallel | do  |     |     |     |     |     |     |     |     |
4:
|     |       |     | n      | rn  |     |     |     |     |     |     |     |     |     |
| --- | ----- | --- | ------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 5:  | Solve | A   | i δ =R | i   |     |     |     |     |     |     |     |     |     |
i
| 6:  | end | for |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
p
|     | un+1 | ←un+ | (cid:88) | TD  | n   |     |     |     |     |     |     |     |     |
| --- | ---- | ---- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 7:  |      |      |          | R i | δ   |     |     |     |     |     |     |     |     |
|     |      |      |          | i   | i   |     |     |     |     |     |     |     |     |
i=1
8: n←n+1
| 9:  | until ∥rn∥<ε |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The implementation utilized the domain decomposition algorithms described in Toselli and Widlund,
2005. Specifically, these methods were used to efficiently parallelize the solver across subdomains.
|                |           |                  |     |          |          | AllthreesweepsareRichardsoniterationsun+1 |     |     |              |      |     | =un+M−1rn |      |
| -------------- | --------- | ---------------- | --- | -------- | -------- | ----------------------------------------- | --- | --- | ------------ | ---- | --- | --------- | ---- |
| Preconditioner |           | form             | and | damping. |          |                                           |     |     |              |      |     |           |      |
| with           | different | preconditioners: |     |          |          |                                           |     |     |              |      |     |           |      |
|                |           |                  |     |          | p        |                                           |     |     | p            |      |     |           |      |
|                |           |                  | M−1 |          | (cid:88) | RTA−1R                                    |     | M−1 | (cid:88) RTD | A−1R |     |           |      |
|                |           |                  |     | =θ       |          |                                           | ,   | =   |              |      | ,   |           | (12) |
|                |           |                  |     | AS       |          | i i                                       | i   | RAS |              | i i  | i i |           |      |
|                |           |                  |     |          | i=1      |                                           |     |     | i=1          |      |     |           |      |
whileonemultiplicativesweepistheerrorpropagationE =(I−P )···(I−P )withP =RTA−1R A.
|     |     |     |     |     |     |     |     | MS  |     | p   | 1   | i i | i i |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
A point of the overlap belongs to m subdomains and receives m corrections per additive sweep, so the
9

undamped iteration generally diverges; θ ≤ 1/m restores convergence, where m is the maximal overlap
multiplicity (m = 2 for strip decompositions and m = 2d for box decompositions in d dimensions,
attainedintheboxcorners). Thisexponential-in-ddampingisthepracticalweaknessofplainAS,clearly
M−1
visible in the benchmarks below. RAS avoids it entirely at the price of a nonsymmetric (so plain
RAS
CG acceleration is unavailable), and MS avoids it by sequencing, at the price of losing subdomain-level
parallelism. OurwritingsontheSchwarzfamilyfollow(QuarteroniandValli,1999);wehighlyencourage
| readers | to    | review     | the theory | and | proofs | presented | there. |     |     |     |     |
| ------- | ----- | ---------- | ---------- | --- | ------ | --------- | ------ | --- | --- | --- | --- |
| 6.3     | Schur | complement |            |     | method |           |        |     |     |     |     |
The fourth method works on a non-overlapping partition and is the direct constructive counterpart of
the interface formulation used by the DN and NN iterations. Number the degrees of freedom of each
subdomain interior-first, with the interface Γ (vertices shared by two or more subdomains) last. Because
the elements of the triangulation are split between subdomains without repetition, each subdomain can
assemble its own local system completely independently, and the global matrix is never formed – only
| the | local blocks |     |     |     |      |          |          |          |          |     |     |
| --- | ------------ | --- | --- | --- | ---- | -------- | -------- | -------- | -------- | --- | --- |
|     |              |     |     |     |      | (cid:34) | (cid:35) | (cid:34) | (cid:35) |     |     |
|     |              |     |     |     |      | A(i)     | A(i)     |          | b(i)     |     |     |
|     |              |     |     |     | A(i) |          |          | b(i)     |          |     |     |
|     |              |     |     |     |      | = II     | IΓ ,     | =        | I .      |     |     |
|     |              |     |     |     |      | A(i)     | A(i)     |          | b(i)     |     |     |
|     |              |     |     |     |      | ΓI       | ΓΓ       |          | Γ        |     |     |
Eliminating the interior unknowns of every subdomain produces the local Schur complements, which are
subassembled on Γ with interface remaps R :R|Γ| →R|Γi|, exactly as in (3):
Γ,i
|     |     |     |     |     |     | p   |     |     | p        |     |          |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | -------- |
|     |     |     |     |     |     |     |     |     | (cid:16) |     | (cid:17) |
=A(i) −A(i)(cid:0) A(i)(cid:1)−1 A(i), (cid:88) RT (cid:88) RT b(i)−A(i)(cid:0) A(i)(cid:1)−1 b(i)
| S   | i   |     |     |     | S   | =   | S i R Γ,i , | g=  |       |       | . (13) |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ----- | ----- | ------ |
|     | ΓΓ  | ΓI  | II  | IΓ  |     |     | Γ,i         |     | Γ,i Γ | ΓI II | I      |
|     |     |     |     |     |     | i=1 |             | i=1 |       |       |        |
S is SPD whenever A is, so the interface problem Su Γ = g is solved by plain conjugate gradients –
this is the only iteration of the method; there is no stationary sweep over subdomains and no relaxation
parameter to tune. Once u has converged, the interiors are recovered by one final, independent and
Γ
parallel back substitution per subdomain. The whole procedure is summarized in algorithm 6. Note the
contrastwiththeNNpreconditionerof(4): there,theS areneverformedandonlytheir(pseudo)inverses
i
are applied; here, the subdomains are small enough that every S i is formed explicitly as a dense matrix,
| turning   | the     | interface       | solve      | into      | ordinary    | dense | linear algebra. |     |     |     |     |
| --------- | ------- | --------------- | ---------- | --------- | ----------- | ----- | --------------- | --- | --- | --- | --- |
| Algorithm |         | 6 Schur         | complement |           | method      |       |                 |     |     |     |     |
| Require:  |         | non-overlapping |            | partition |             | with  | inter-          |     |     |     |     |
|           | face Γ, | interface       | remaps     | R         | , tolerance |       | ε               |     |     |     |     |
Γ,i
| 1:  | for i=1,...,p |     | in parallel |     | do                 |     |     |     |     |     |     |
| --- | ------------- | --- | ----------- | --- | ------------------ | --- | --- | --- | --- | --- | --- |
| 2:  | Assemble      |     | A(i), b(i)  | on  | Ω , interior-first |     |     |     |     |     |     |
i
|     | ←A( | i ) | −A( i )(cid:0) | A( i )(cid:1)−1 | A( i ) |     |     |     |     |     |     |
| --- | --- | --- | -------------- | --------------- | ------ | --- | --- | --- | --- | --- | --- |
3: S i
|     |     | Γ Γ   | Γ I        | I I             | I Γ   |     |     |     |     |     |     |
| --- | --- | ----- | ---------- | --------------- | ----- | --- | --- | --- | --- | --- | --- |
|     | ←b( | i)−A( | i )(cid:0) | A( i )(cid:1)−1 | b( i) |     |     |     |     |     |     |
4: g i
|     |     | Γ   | Γ I | I I | I   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
5: end for
|     | Subassemble | S   | and | g by (13) |     |     |     |     |     |     |     |
| --- | ----------- | --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- |
6:
| 7:  | Solve Su | =g  | by CG | to tolerance |     | ε   |     |     |     |     |     |
| --- | -------- | --- | ----- | ------------ | --- | --- | --- | --- | --- | --- | --- |
Γ
|     | for i=1,...,p |     | in parallel |     | do  |     |     |     |     |     |     |
| --- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
8:
|     | u( i) | (cid:0) A( | i )(cid:1)−1(cid:0) | b( i)−A( | i )R | (cid:1) |     |     |     |     |     |
| --- | ----- | ---------- | ------------------- | -------- | ---- | ------- | --- | --- | --- | --- | --- |
| 9:  |       | ←          |                     |          |      | u       |     |     |     |     |     |
|     | I     |            | I I                 | I        | I Γ  | Γ,i Γ   |     |     |     |     |     |
end for
10:
6.4 Implementation
AllfourmethodsareimplementedinasingleJAXframework,builtaroundoneideaborrowedfromgraph-
ics APIs: the expensive preparation (mesh decomposition, FEM assembly, tracing and XLA compilation
ofthewholeiterationgraph)isperformedonce, afterwhichthecompiledpipelinemesh→decompose→
assemble→solve runs repeatedly on the device with no host round-trips. Every stage is a pure function
overimmutabledata,andeveryentityisexplicitlyclassifiedaseitherstatic (problemcallables,tolerances,
decomposition layout – fixed at compile time) or traced (vertex coordinates, matrices, right-hand sides –
free to change between calls). This design is what makes the methods fast, but it is also the source of
| most | implementation |     | difficulties, |     | which | we describe | next. |     |     |     |     |
| ---- | -------------- | --- | ------------- | --- | ----- | ----------- | ----- | --- | --- | --- | --- |
10

Choosing the additive damping. The damping bound θ ≤ 1/m of section 6.2 is easy to state
and easy to underestimate. For strip decompositions m = 2 and θ = 1/2 behaves acceptably; for box
decompositions in d = 3 the corner regions push m to 23 = 8, and the safe θ = 1/8 slows the iteration
down by almost the same factor. An adaptive or spectrum-based choice of θ (or CG acceleration of
the symmetric AS preconditioner) would remove this, but with plain Richardson the exponential-in-d
damping is unavoidable, and the benchmarks below show exactly this failure mode.
Constructing the partition of unity. RAS needs the ownership masks D of (11), and they must
i
formanexact partitionofunity: avertexownedtwiceisovercorrected(andtheiterationmaydiverge),a
vertexownedzerotimesisnevercorrected(andtheiterationstalls). Thesubtletyisentirelycombinatorial
and lives on the boundaries between boxes: we assign ownership by half-open cell ranges [start,end) per
axis,withtheclosingboxalongeachaxisadditionallyowningitshighface. Anearlyversionofthesolver
re-derivedthesemasksfromthestriplayoutinsidetheRASsolveritself,whichsilentlycoupledthesolver
to one particular decomposer; the masks are now produced by the decomposer, next to the index remaps
they belong with.
Dirichlet conditions on interface degrees of freedom. The Schur complement method assembles
each subdomain independently, including the physical boundary conditions – and a dirichlet vertex can
lieexactlyontheinterfaceΓ(e.g.wheretheinterfaceplanemeetsthephysicalboundary,oraboxcorner
shared by up to 2d subdomains). Each touching subdomain then eliminates that vertex symmetrically
on its own: zeroing its row and column, placing a unit diagonal and moving the known value to the
right-hand side. After subassembly (13) the diagonal of S at such a vertex equals its multiplicity κ
and the right-hand side equals κ times the boundary value, so the interface solve still reproduces the
boundary value exactly – but only because the elimination is symmetric and performed identically by
every subdomain. Zeroing only the rows (the cheaper, nonsymmetric variant) would break both the
consistency of the subassembled system and the SPD property CG relies on. This is the single most
fragileinvariantoftheimplementation,andweverifyitbycomparingeverysolveragainstadirectglobal
solve.
Consistency of local and global assembly. The subassembly identity A= (cid:80) R¯TA(i)R¯ (with full-
i i i
subdomain remaps R¯ ) holds only if the union of local triangulations is exactly the global one: every
i
simplex must appear in exactly one subdomain, with the same geometry. With a structured Kuhn
triangulation (d! simplices per cell) this reduces to sharing one canonical layout routine between the
global mesher, the decomposers and the solvers that need static block sizes – any second, hand-rolled
triangulation of the subdomains is an opportunity for the two to drift apart. The same routine also
fixes the interior-first ordering, so the block sizes of A(i) are known at compile time, as the static/traced
contract requires.
Dense local algebra. The local matrices A and the blocks of A(i) are extracted and stored dense,
i
and the local solves are dense factorizations. At the benchmark sizes below this is not a bottleneck (the
framework targets method comparison, not peak scale), but it bounds the subdomain size; sparse local
representations are the natural next step and nothing in the interfaces precludes them.
7 Benchmarks
7.1 Problems
Webenchmarkonfourproblems, inincreasingorderofdifficultyfortheinterfaceoperator. Thefirsttwo
fix α≡1 and vary only the data (f and u ); the last two fix trivial data and vary only α.
0
High-dimensional oscillatory Poisson.
(cid:40)
−∆u=
(cid:81)d
k=1 sin(πx k ), with the closed form u= 1 (cid:89)
d
sin(πx ).
u (cid:12) (cid:12) =0, dπ2 k
∂Ω k=1
This is the only problem with a known analytical solution, which lets us verify that the decomposition
converges to the right thing.
11

L2 L∞
Method Runs
min max mean min max mean
NN 12 1.5020 1.5024 1.5022 4.3212 4.3223 4.3217
DN 9 1.5020 1.5025 1.5023 4.3212 4.3227 4.3221
Table 2: Aggregated error values.
Poisson with polynomial source.
(cid:40)
−∆u=d,
no closed form.
u (cid:12) (cid:12) = (cid:80)d x2,
∂Ω k=1 k
Same operator as above, but with a constant source and inhomogeneous dirichlet data.
Checkerboard diffusion.
(cid:40)
−∇·(α(x)∇u)=1,
(cid:40)
1,
(cid:80)d
⌊mx ⌋=0 (mod 2),
α(x)= k=1 k ε∈{10,102,103}.
u
(cid:12)
(cid:12) ∂Ω =0, ε,
(cid:80)d
k=1 ⌊mx k ⌋=1 (mod 2),
Layered material.
(cid:40) (cid:40)
−∇·(α(x)∇u)=1, 1, x <0.5,
α(x)= 1 ε∈{102,103,104}.
(cid:12)
u(cid:12)
∂Ω
=0, ε, x
1
≥0.5,
Why only making α discontinuous matters. It is worth being explicit about why we pass ε inside
α and never inside f or u . Recall the two objects of (1):
0
S =A −A A−1A , g=A A−1f −f .
ΓΓ ΓI II IΓ ΓI II I Γ
The matrix A depends only on α, so A – and hence S, and hence the preconditioner P−1 of (4) – all
have the same and only dependency. The data f and u enter only through g. Since the asymptotic
0
convergencerateofanyoftheiterationsweconsiderisgovernedbythespectrumofP−1S,changingf or
u can move the starting residual ∥g∥, but it cannot move the rate. Oscillations in the source are, from
0
the interface operator’s point of view, invisible.
7.2 Dirichlet-Neumann and Neumann-Neumann iterations
All benchmarks solve the same model problem family on the unit cube Ω = [0,1]3; the discretization is
obtained by refining each axis into 32 equal intervals. This yields n = 32,768 approximation points and
178,746 simplexes. The cube is then cut into p3 cubic subdomains for p∈{8,10,12}, i.e. 512, 1000 and
1728 subdomains respectively. Every subdomain solve is a dense local problem, floating subdomains are
handled by the pseudoinverse S† of section 5.2, and D is used for multiplicity scaling. All iterations
i i
start from u0 =0 and stop once ∥Sun−g∥<10−9, an absolute tolerance. PCG and GMRES (Krylov)
Γ Γ
solvers are capped at 2048 iterations and Richardson at 16,384. We run over 120 one-shot benchmarks
in total. We keep GMRES solver un-restarted.
High-dimensionaloscillatoryPoisson. Wemeasuretheerroragainstuatthemeshnodes,reporting
the L2 and the L∞ errors. Per-run values are reported in the last two columns of table 3, and table 2
aggregates them by method.
Checkerboard diffusion. Here, α isadiscontinuouscoefficientwithfixedprimem=41cellsperaxis
(when considering unit cube). Since 41 is coprime to 8, 10 and 12, the coefficient jump in theory should
never land on a boundary: discontinuities live strictly inside the subdomains.
Layered material. A discontinuity here is subject to a single jump of size (ε−1) across the plane
x =0.5 (because refinement levels are equal across all axes).
1
12

|     | p   | Method | Solver     | τ     |        | n t     | , s ∥Su        | −g∥ |             | L2          | L∞  |
| --- | --- | ------ | ---------- | ----- | ------ | ------- | -------------- | --- | ----------- | ----------- | --- |
|     |     |        |            |       |        | it it   |                | Γ   |             |             |     |
|     |     | NN     | CG         | —     |        | 52      | 3.7 9.43×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
|     |     | NN     | GMRES      | —     |        | 59 26.3 | 9.15×10−10     |     | 1.5020×10−5 | 4.3212×10−5 |     |
|     |     |        |            |       | 16384∗ |         | 1.01×10−3      |     | 3.7242×10−3 | 1.0646×10−2 |     |
|     |     | NN     | Richardson | 0.001 |        | 1135.6  |                |     |             |             |     |
|     |     |        |            |       | 16384∗ |         | 4.87×10−8      |     | 1.5193×10−5 | 4.3715×10−5 |     |
|     |     | NN     | Richardson | 0.01  |        | 1136.3  |                |     |             |             |     |
NN Richardson 0.05 4425 307.0 9.98×10−10 1.5024×10−5 4.3222×10−5
8 NN Richardson 0.06 3686 256.1 9.99×10−10 1.5024×10−5 4.3222×10−5
|     |     | DN  | GMRES      | —     |        | 120 103.4 | 9.32×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
| --- | --- | --- | ---------- | ----- | ------ | --------- | ---------- | --- | ----------- | ----------- | --- |
|     |     |     |            |       | 16384∗ |           | 1.01×10−3  |     | 4.5191×10−3 | 1.3774×10−2 |     |
|     |     | DN  | Richardson | 0.001 |        | 1104.4    |            |     |             |             |     |
|     |     |     |            |       | 16384∗ |           | 2.64×10−7  |     | 1.6167×10−5 | 4.6815×10−5 |     |
|     |     | DN  | Richardson | 0.01  |        | 1104.1    |            |     |             |             |     |
DN Richardson 0.05 5266 354.7 9.97×10−10 1.5024×10−5 4.3225×10−5
DN Richardson 0.06 4387 295.4 9.98×10−10 1.5024×10−5 4.3225×10−5
|     |     | NN  | CG         | —     |        | 57      | 2.5 8.77×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
| --- | --- | --- | ---------- | ----- | ------ | ------- | -------------- | --- | ----------- | ----------- | --- |
|     |     | NN  | GMRES      | —     |        | 66 28.3 | 9.80×10−10     |     | 1.5020×10−5 | 4.3212×10−5 |     |
|     |     |     |            |       | 16384∗ |         | 1.15×10−3      |     | 4.6218×10−3 | 1.3241×10−2 |     |
|     |     | NN  | Richardson | 0.001 |        | 724.4   |                |     |             |             |     |
NN Richardson 0.01 16384∗ 720.5 3.64×10−7 1.6432×10−5 4.7345×10−5
NN Richardson 0.05 5430 238.8 9.98×10−10 1.5024×10−5 4.3223×10−5
10 NN Richardson 0.06 4524 199.1 9.98×10−10 1.5024×10−5 4.3223×10−5
|     |     | DN  | GMRES      | —     |        | 130 106.5 | 9.76×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
| --- | --- | --- | ---------- | ----- | ------ | --------- | ---------- | --- | ----------- | ----------- | --- |
|     |     |     |            |       | 16384∗ |           | 1.12×10−3  |     | 5.4414×10−3 | 1.6752×10−2 |     |
|     |     | DN  | Richardson | 0.001 |        | 641.9     |            |     |             |             |     |
DN Richardson 0.01 16384∗ 641.8 1.52×10−6 2.2214×10−5 6.5882×10−5
DN Richardson 0.05 6545 256.4 9.98×10−10 1.5025×10−5 4.3227×10−5
DN Richardson 0.06 5453 213.8 9.98×10−10 1.5025×10−5 4.3227×10−5
|     |     | NN  | CG         | —     |        | 62      | 3.6 9.45×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
| --- | --- | --- | ---------- | ----- | ------ | ------- | -------------- | --- | ----------- | ----------- | --- |
|     |     |     |            |       |        |         | 8.24×10−10     |     | 1.5020×10−5 | 4.3212×10−5 |     |
|     |     | NN  | GMRES      | —     |        | 71 31.0 |                |     |             |             |     |
|     |     |     |            |       | 16384∗ |         | 1.55×10−3      |     | 5.8098×10−3 | 1.7428×10−2 |     |
|     |     | NN  | Richardson | 0.001 |        | 957.8   |                |     |             |             |     |
NN Richardson 0.01 16384∗ 958.1 3.99×10−6 2.9605×10−5 8.7666×10−5
NN Richardson 0.05 7371 430.9 9.99×10−10 1.5024×10−5 4.3223×10−5
12 NN Richardson 0.06 6142 360.0 9.98×10−10 1.5024×10−5 4.3223×10−5
|     |     |     |            |       |        |           | 9.58×10−10 |     | 1.5020×10−5 | 4.3212×10−5 |     |
| --- | --- | --- | ---------- | ----- | ------ | --------- | ---------- | --- | ----------- | ----------- | --- |
|     |     | DN  | GMRES      | —     |        | 134 106.6 |            |     |             |             |     |
|     |     |     |            |       | 16384∗ |           | 1.24×10−3  |     | 6.0288×10−3 | 1.8690×10−2 |     |
|     |     | DN  | Richardson | 0.001 |        | 813.8     |            |     |             |             |     |
DN Richardson 0.01 16384∗ 814.1 4.15×10−6 3.4968×10−5 1.0613×10−4
DN Richardson 0.05 7585 376.9 9.98×10−10 1.5025×10−5 4.3227×10−5
DN Richardson 0.06 6320 313.9 9.98×10−10 1.5025×10−5 4.3227×10−5
|     |     |     | Table | 3: High-dimensional |     |     | oscillatory | Poisson | results. |     |     |
| --- | --- | --- | ----- | ------------------- | --- | --- | ----------- | ------- | -------- | --- | --- |
Why only making α discontinuous matters. The first two problems confirm this. They share
α≡1 but differ in both f and u . For, say, p=8 and NN-CG iteration, average convergence factors are
0
| 0.750 | and 0.725, | while | iteration | counts | are | 52 and 70. |     |     |     |     |     |
| ----- | ---------- | ----- | --------- | ------ | --- | ---------- | --- | --- | --- | --- | --- |
7.2.1 Results
Tables 3 to 6 report, for each problem, partition p, method and solver: the iteration count n , the
it
iteration-only wall-clock time t it , and the final residual ∥Su Γ −g∥. An asterisk (∗) marks runs that
exhausted their iteration budget without reaching the tolerance. DN is never paired with CG, since, as
noted in section 5.2, its preconditioned operator P−1S is not symmetric. n counts residual evaluations,
it
so for CG and GMRES it includes the initial residual and the number of Krylov steps is one less.
7.2.2 Discussion
NN vs. DN. On every problem and every partition, NN converges in roughly half the iterations of
DN: on the oscillatory problem under GMRES, 59 against 120 at p=8, 66 against 130 at p=10, and 71
against 134 at p=12. DN is also the more expensive iteration in absolute terms, its step costing about
twice that of NN-GMRES. Combined with the coloring requirement of section 5.2 and the loss of CG,
| this | leaves | DN with | no advantage | in  | our experiments. |     |     |     |     |     |     |
| ---- | ------ | ------- | ------------ | --- | ---------------- | --- | --- | --- | --- | --- | --- |
CG vs. GMRES. Where CG is possible it is decisively the better choice, and the reason is per-
iteration cost rather than iteration count: the two need comparable numbers of steps (52 against 59 on
13

| p Method |     | Solver     | τ            | n t , s ∥Su          | −g∥ |
| -------- | --- | ---------- | ------------ | -------------------- | --- |
|          |     |            |              | it it                | Γ   |
|          | NN  | CG         | —            | 70 5.0 7.84×10−10    |     |
|          | NN  | GMRES      | —            | 77 39.1 6.84×10−10   |     |
|          | NN  | Richardson | 0.001 16384∗ | 1183.2 7.44×10−2     |     |
|          |     |            | 16384∗       | 3.39×10−6            |     |
|          | NN  | Richardson | 0.01         | 1182.9               |     |
|          | NN  | Richardson | 0.05 5681    | 409.6 9.99×10−10     |     |
| 8        | NN  | Richardson | 0.06 4733    | 341.7 9.98×10−10     |     |
|          | DN  | GMRES      | —            | 151 139.1 9.02×10−10 |     |
|          | DN  | Richardson | 0.001 16384∗ | 1148.4 6.77×10−2     |     |
|          |     |            | 16384∗       | 1.68×10−5            |     |
|          | DN  | Richardson | 0.01         | 1148.1               |     |
|          | DN  | Richardson | 0.05 6751    | 472.8 9.97×10−10     |     |
|          | DN  | Richardson | 0.06 5624    | 394.7 9.99×10−10     |     |
7.60×10−10
|     | NN  | CG         | —            | 81 3.5             |     |
| --- | --- | ---------- | ------------ | ------------------ | --- |
|     | NN  | GMRES      | —            | 88 50.2 8.33×10−10 |     |
|     | NN  | Richardson | 0.001 16384∗ | 721.7 9.29×10−2    |     |
|     | NN  | Richardson | 0.01 16384∗  | 720.4 2.64×10−5    |     |
|     | NN  | Richardson | 0.05 6995    | 307.8 9.97×10−10   |     |
1.00×10−9
| 10  | NN  | Richardson | 0.06 5827    | 256.4                |     |
| --- | --- | ---------- | ------------ | -------------------- | --- |
|     | DN  | GMRES      | —            | 167 173.1 8.38×10−10 |     |
|     | DN  | Richardson | 0.001 16384∗ | 639.1 8.00×10−2      |     |
|     | DN  | Richardson | 0.01 16384∗  | 638.7 9.97×10−5      |     |
|     | DN  | Richardson | 0.05 8412    | 328.1 9.99×10−10     |     |
9.97×10−10
|     | DN  | Richardson | 0.06 7009    | 273.5              |     |
| --- | --- | ---------- | ------------ | ------------------ | --- |
|     | NN  | CG         | —            | 89 5.3 6.87×10−10  |     |
|     | NN  | GMRES      | —            | 96 54.5 9.22×10−10 |     |
|     | NN  | Richardson | 0.001 16384∗ | 983.9 1.26×10−1    |     |
|     | NN  | Richardson | 0.01 16384∗  | 984.4 2.89×10−4    |     |
9.99×10−10
|     | NN  | Richardson | 0.05 9486    | 570.1                |     |
| --- | --- | ---------- | ------------ | -------------------- | --- |
| 12  | NN  | Richardson | 0.06 7904    | 474.6 9.98×10−10     |     |
|     | DN  | GMRES      | —            | 174 175.1 8.46×10−10 |     |
|     | DN  | Richardson | 0.001 16384∗ | 827.8 9.38×10−2      |     |
|     | DN  | Richardson | 0.01 16384∗  | 828.2 2.79×10−4      |     |
9.99×10−10
|     | DN    | Richardson | 0.05 9761       | 493.3            |     |
| --- | ----- | ---------- | --------------- | ---------------- | --- |
|     | DN    | Richardson | 0.06 8133       | 411.1 9.98×10−10 |     |
|     | Table | 4: Poisson | with polynomial | source results.  |     |
14

| p   | Method | Solver          | ε   | n         | t , s    | ∥Su −g∥    |
| --- | ------ | --------------- | --- | --------- | -------- | ---------- |
|     |        |                 |     | it        | it       | Γ          |
|     |        |                 | 101 |           |          | 7.83×10−10 |
|     | NN     | CG              |     | 59        | 4.1      |            |
|     | NN     | CG              | 102 | 61        | 4.2      | 7.59×10−10 |
|     | NN     | CG              | 103 | 61        | 4.2      | 8.02×10−10 |
|     | NN     | GMRES           | 101 | 62        | 26.4     | 8.65×10−10 |
| 8   | NN     | GMRES           | 102 | 58        | 23.9     | 8.49×10−10 |
|     |        |                 | 103 |           |          | 6.59×10−10 |
|     | NN     | GMRES           |     | 53        | 20.1     |            |
|     | DN     | GMRES           | 101 | 126       | 103.0    | 9.59×10−10 |
|     | DN     | GMRES           | 102 | 115       | 83.5     | 9.36×10−10 |
|     |        |                 | 103 |           |          | 8.57×10−10 |
|     | DN     | GMRES           |     | 104       | 68.4     |            |
|     | NN     | CG              | 101 | 65        | 3.5      | 8.58×10−10 |
|     | NN     | CG              | 102 | 65        | 3.7      | 9.94×10−10 |
|     | NN     | CG              | 103 | 66        | 3.5      | 8.17×10−10 |
|     | NN     | GMRES           | 101 | 68        | 28.4     | 9.48×10−10 |
|     |        |                 | 102 |           |          | 7.70×10−10 |
| 10  | NN     | GMRES           |     | 62        | 23.7     |            |
|     | NN     | GMRES           | 103 | 54        | 18.4     | 8.64×10−10 |
|     | DN     | GMRES           | 101 | 137       | 114.4    | 8.59×10−10 |
|     | DN     | GMRES           | 102 | 127       | 93.7     | 8.38×10−10 |
|     | DN     | GMRES           | 103 | 113       | 73.6     | 9.81×10−10 |
|     |        |                 | 101 |           |          | 9.11×10−10 |
|     | NN     | CG              |     | 74        | 4.9      |            |
|     | NN     | CG              | 102 | 77        | 5.1      | 9.24×10−10 |
|     | NN     | CG              | 103 | 78        | 5.2      | 8.53×10−10 |
|     | NN     | GMRES           | 101 | 78        | 39.3     | 8.07×10−10 |
| 12  | NN     | GMRES           | 102 | 74        | 33.4     | 8.20×10−10 |
|     |        |                 | 103 |           |          | 9.71×10−10 |
|     | NN     | GMRES           |     | 65        | 26.0     |            |
|     | DN     | GMRES           | 101 | 147       | 134.7    | 9.75×10−10 |
|     | DN     | GMRES           | 102 | 139       | 115.6    | 9.01×10−10 |
|     | DN     | GMRES           | 103 | 123       | 91.0     | 9.17×10−10 |
|     | Table  | 5: Checkerboard |     | diffusion | results. |            |
15

| p Method | Solver   | ε       | n        | t ,      | s ∥Su −g∥  |
| -------- | -------- | ------- | -------- | -------- | ---------- |
|          |          |         | it       | it       | Γ          |
|          |          | 102     |          |          | 9.35×10−10 |
| NN       | CG       |         | 233      | 16.4     |            |
| NN       | CG       | 103     | 539      | 38.0     | 9.64×10−10 |
| NN       | CG       | 104     | 847      | 60.2     | 9.73×10−10 |
| NN       | GMRES    | 102     | 217      | 316.8    | 9.14×10−10 |
| 8 NN     | GMRES    | 103     | 273      | 503.9    | 8.35×10−10 |
|          |          | 104     |          |          | 8.74×10−10 |
| NN       | GMRES    |         | 276      | 514.0    |            |
| DN       | GMRES    | 102     | 281      | 498.0    | 9.46×10−10 |
| DN       | GMRES    | 103     | 301      | 593.0    | 8.74×10−10 |
|          |          | 104     |          |          | 8.99×10−10 |
| DN       | GMRES    |         | 303      | 588.6    |            |
| NN       | CG       | 102     | 242      | 10.8     | 9.92×10−10 |
| NN       | CG       | 103     | 565      | 25.2     | 9.51×10−10 |
| NN       | CG       | 104     | 925      | 41.4     | 8.31×10−10 |
| NN       | GMRES    | 102     | 233      | 335.8    | 9.42×10−10 |
|          |          | 103     |          |          | 8.54×10−10 |
| 10 NN    | GMRES    |         | 362      | 832.4    |            |
| NN       | GMRES    | 104     | 363      | 824.2    | 8.30×10−10 |
| DN       | GMRES    | 102     | 310      | 586.6    | 9.62×10−10 |
| DN       | GMRES    | 103     | 348      | 731.3    | 9.58×10−10 |
| DN       | GMRES    | 104     | 338      | 697.8    | 9.98×10−10 |
|          |          | 102     |          |          | 9.95×10−10 |
| NN       | CG       |         | 263      | 15.6     |            |
| NN       | CG       | 103     | 645      | 38.4     | 9.99×10−10 |
| NN       | CG       | 104     | 1108     | 66.0     | 9.35×10−10 |
| NN       | GMRES    | 102     | 242      | 358.6    | 9.89×10−10 |
| 12 NN    | GMRES    | 103     | 411      | 1022.2   | 9.04×10−10 |
|          |          | 104     |          |          | 9.07×10−10 |
| NN       | GMRES    |         | 426      | 1117.9   |            |
| DN       | GMRES    | 102     | 317      | 612.8    | 9.14×10−10 |
| DN       | GMRES    | 103     | 371      | 827.9    | 9.97×10−10 |
| DN       | GMRES    | 104     | 364      | 808.8    | 9.26×10−10 |
|          | Table 6: | Layered | material | results. |            |
16

|     |     |     |     | Method | n   | ∥r∥ |     | L∞ error |
| --- | --- | --- | --- | ------ | --- | --- | --- | -------- |
it
|     |     |       |     | AS          | 200∗     | 4.1×10−6      | 1.128×10−4 |                     |
| --- | --- | ----- | --- | ----------- | -------- | ------------- | ---------- | ------------------- |
|     |     |       |     |             |          | 6.1×10−9      | 7.460×10−5 |                     |
|     |     |       |     | MS          | 23       |               |            |                     |
|     |     |       |     | RAS         | 51       | 9.0×10−9      | 7.463×10−5 |                     |
|     |     |       |     |             |          | 9.2×10−9      | 7.456×10−5 |                     |
|     |     |       |     | Schur-CG    | 29       |               |            |                     |
|     |     | Table | 7:  | Oscillatory | Poisson: | error against |            | the exact solution. |
the oscillatory problem at p = 8), but NN-CG’s iteration costs 0.068 against GMRES’s 0.458. This is
the expected consequence of un-restarted GMRES (on the other hand, GMRES with restarts might not
converge at all). The effect is worst exactly where iteration counts are highest – on the layered problem
at ε = 104, p = 12, GMRES’s step reaches 2.57 against CG’s 0.059. Both the memory and the time
P−1S
argument favour CG, and, since is SPD for NN, nothing prevents its use.
The difficulty of choosing τ. The Richardson runs are included in full because they illustrate how
“difficult” the choice of τ can be. At τ =10−3 the iteration is still eight orders of magnitude away from
|     |     |     |     | =10−2 | itgetswithin10−7 |     |     |     |
| --- | --- | --- | --- | ----- | ---------------- | --- | --- | --- |
thetoleranceafter16,384steps;atτ butstillfailstoconverge. Thetwolarger
| values succeed, | and | comparing |     | them | isolates the | mechanism. |     |     |
| --------------- | --- | --------- | --- | ---- | ------------ | ---------- | --- | --- |
Coefficient jumps. The two variable-coefficient problems behave completely differently, and the dif-
raisingεfrom10to103
ferenceisnotthesizeofthejump. Onthecheckerboardproblem, movesNN-CG
from 59 to 61 iterations at p=8, with the average convergence factor stirring only from 0.760 to 0.767.
Three orders of magnitude of contrast cost two iterations. On the layered problem, raising ε from 102 to
104 movesNN-CGfrom233to847iterations,withtheconvergencefactordegradingfrom0.935to0.982.
The distinction is where the discontinuity sits. The checkerboard’s jumps (m=41, coprime to every
p) fall strictly inside subdomains, where they are controlled by the local Dirichlet solves and never reach
S. Thelayeredjumpsitson asubdomainfaceforeverypweuse,sothetwosubdomainsmeetingatthat
face have local operators S differing by a factor ε. Multiplicity scaling, which sets D from the number
i i
ofsubdomainssharingavertexandisblindtoα,thenaveragesthetwosideswithequalweight,andP−1
mis-weights the correction by exactly the contrast. This is the price of the simplest choice of D , flagged
i
in section 5.2: a coefficient-dependent scaling, weighting each side by its local α, is the standard remedy
| for such cases. | We  | did | not test | it. |     |     |     |     |
| --------------- | --- | --- | -------- | --- | --- | --- | --- | --- |
Scalability in the number of subdomains. Iteration counts grow slowly and predictably with p.
NN-CG on the oscillatory problem needs 52, 57 and 62 iterations for p = 8,10,12, a 19% increase for a
3.4× increase in the number of subdomains, consistent with the (poly-logarithmic) growth of a two-level
Neumann-Neumann preconditioner at fixed subdomain size. Wall-clock time, by contrast, grows much
faster, because the local solves are dense and |Γ| itself grows. The growth in n it is also visibly worse for
the harder problems – NN-CG on the layered material at ε=104 goes 847→925→1108.
| 7.3 Schwarz |     | and | Schur | complement |     | iterations |     |     |
| ----------- | --- | --- | ----- | ---------- | --- | ---------- | --- | --- |
All benchmarks solve the same model problem family on the unit cube Ω = [0,1]3; the discretization
is obtained by refining each axis into 32 equal intervals and applying the Kuhn triangulation (d! = 6
tetrahedra per cell). This yields n = 333 = 35,937 approximation points and 196,608 simplexes. The
cubeisthencutinto23 =8boxsubdomains. TheSchwarz-familymethodsextendeveryboxbyanoverlap
of one cell layer; the Schur complement method uses the non-overlapping partition. Every subdomain
solve is a dense local problem. All iterations start from u0 = 0 and stop once ∥b−Aun∥ < 10−8 (for
Schur-CG—oncetheinterfaceresidual∥Sun−g∥<10−8),anabsolute
tolerance. Allsolversarecapped
Γ
at 200 iterations, where one iteration is one sweep over all subdomains for the Schwarz family and one
Krylov step for Schur-CG. The additive Schwarz update is damped by θ = 1/23 = 0.125, the maximal
multiplicity of the box overlap, as discussed in section 6.4. We run 44 one-shot benchmarks in total (11
| problem instances |     | × 4 | methods). |     |     |     |     |     |
| ----------------- | --- | --- | --------- | --- | --- | --- | --- | --- |
High-dimensionaloscillatoryPoisson. Wemeasuretheerroragainstuatthemeshnodes,reporting
the L∞ error; table 7 lists it per method together with the iteration count and the final residual.
17

|     |     | Problem     |     |     |     | AS   | MS  | RAS Schur-CG |     |
| --- | --- | ----------- | --- | --- | --- | ---- | --- | ------------ | --- |
|     |     | oscillatory |     |     |     | 200∗ | 23  | 51           | 29  |
200∗
|     |     | polynomial    |     |      |      |      | 30  | 66  | 60  |
| --- | --- | ------------- | --- | ---- | ---- | ---- | --- | --- | --- |
|     |     | checkerboard, |     | m=2, | ε=10 | 200∗ | 14  | 36  | 37  |
ε=102
|     |     | checkerboard, |       | m=2,         |        | 180         | 10  | 27          | 37   |
| --- | --- | ------------- | ----- | ------------ | ------ | ----------- | --- | ----------- | ---- |
|     |     | checkerboard, |       | m=2,         | ε=103  | 171         | 9   | 25          | 37   |
|     |     | checkerboard, |       | m=4,         | ε=10   | 200∗        | 18  | 45          | 37   |
|     |     |               |       |              | ε=102  | 200∗        |     |             |      |
|     |     | checkerboard, |       | m=4,         |        |             | 15  | 39          | 38   |
|     |     | checkerboard, |       | m=4,         | ε=103  | 200∗        | 15  | 38          | 38   |
|     |     | layered,      | ε=102 |              |        | 200∗        | 19  | 42          | 200∗ |
|     |     | layered,      | ε=103 |              |        | 200∗        | 19  | 42          | 200∗ |
|     |     | layered,      | ε=104 |              |        | 200∗        | 19  | 42          | 200∗ |
|     |     |               | Table | 8: Iteration | counts | per problem |     | and method. |      |
Checkerboard diffusion. Here α is a discontinuous coefficient with m∈{2,4} blocks per axis. Both
values of m are aligned with the 23 box partition: for m = 2 every coefficient jump lies exactly on a
subdomain boundary, while for m = 4 the mid-plane jumps lie on the subdomain boundaries and the
| quarter-plane | jumps | live | strictly | inside the | subdomains. |     |     |     |     |
| ------------- | ----- | ---- | -------- | ---------- | ----------- | --- | --- | --- | --- |
Layered material. A discontinuity here is subject to a single jump of size (ε−1) across the plane
x 1 =0.5, which is precisely the boundary plane between the left and right boxes.
Why only making α discontinuous matters. The first two problems confirm this: they share
α ≡ 1 but differ in both f and u , and the stationary Schwarz iterations barely notice (MS takes 23 vs
0
30iterations, RAS51vs66). Schur-CGismoresensitive(29vs60): CGisnotastationarymethod, and
its practical iteration count depends on how the right-hand side is distributed over the spectrum of S,
| even though | the | worst-case | rate | bound depends |     | on the spectrum |     | alone. |     |
| ----------- | --- | ---------- | ---- | ------------- | --- | --------------- | --- | ------ | --- |
7.3.1 Results
Table8reportstheiterationcountn foreachprobleminstanceandmethod. Anasterisk(∗)marksruns
it
| that exhausted | the | 200-iteration |     | budget | without | reaching | the tolerance. |     |     |
| -------------- | --- | ------------- | --- | ------ | ------- | -------- | -------------- | --- | --- |
References
Bourgat,Jean-Frédéricetal.(1989).“Variationalformulationandalgorithmfortraceoperatorindomain
decomposition calculations”. In: Domain Decomposition Methods. Ed. by Roland Glowinski et al.
| Philadelphia: |     | SIAM, | pp. 3–16. |     |     |     |     |     |     |
| ------------- | --- | ----- | --------- | --- | --- | --- | --- | --- | --- |
Brenner,SusanneC.andL.RidgwayScott(2008).The Mathematical Theory of Finite Element Methods.
3rd.Vol.15.TextsinAppliedMathematics.NewYork:Springer.doi:10.1007/978-0-387-75934-0.
Quarteroni, Alfio and Alberto Valli (1991). “Theory and applications of Steklov–Poincaré operators for
boundary-valueproblems”.In:AppliedandIndustrialMathematics.Ed.byRenatoSpigler.Dordrecht:
| Kluwer, | pp. 179–203. |     |     |     |     |     |     |     |     |
| ------- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- |
— (1999). Domain Decomposition Methods for Partial Differential Equations. Numerical Mathematics
and Scientific Computation. Oxford: Oxford University Press. isbn: 978-0-19-850178-7.
Toselli,AndreaandOlofB.Widlund(2005).Domain Decomposition Methods — Algorithms and Theory.
isbn:
Vol. 34. Springer Series in Computational Mathematics. Berlin, Heidelberg: Springer-Verlag.
| 978-3-540-20696-5. |     | doi: | 10.1007/3-540-26908-X. |     |     |     |     |     |     |
| ------------------ | --- | ---- | ---------------------- | --- | --- | --- | --- | --- | --- |
18
