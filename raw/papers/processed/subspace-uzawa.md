|     | Two–Grid |             |     | Preconditioning |           |          |            |          | on a Coarse | Subspace   |     |
| --- | -------- | ----------- | --- | --------------- | --------- | -------- | ---------- | -------- | ----------- | ---------- | --- |
|     |          | Generalized |     |                 | Uzawa:    | patches, |            | coarse   | functions,  | guarantees |     |
|     |          |             |     |                 | Numerical |          | Archeology |          | project     |            |     |
|     |          |             |     |                 |           |          | July       | 24, 2026 |             |            |     |
Abstract
A two–grid preconditioner determined by an SPD matrix given as a sum of local positive
semidefinite pieces, a family of overlapping patches, and a smoother. The coarse space is not
prescribed: itisgeneratedoneachpatchbyasmallgeneralizedeigenproblem,andthethreshold
at which that spectrum is truncated is the constant in the condition number bound. The ex-
act factorization is an A–orthogonal splitting whose complement has no local basis — which is
precisely why it is smoothed rather than solved; writing the resulting cycle symmetrically pro-
ducesthegeneralizedUzawaform,inwhichtheprolongationappearscorrectedbythesmoother.
Setup and iteration are local apart from the coarse solve, and the price of the construction is
|     | paid | in coarse–operator |     |     | density, | not in | locality. |     |     |     |     |
| --- | ---- | ------------------ | --- | --- | -------- | ------ | --------- | --- | --- | --- | --- |
Contents
| 1   | Data         |             |                |        |                |     |      |          |          |     | 1   |
| --- | ------------ | ----------- | -------------- | ------ | -------------- | --- | ---- | -------- | -------- | --- | --- |
| 2   | The          | exact       | factorization, |        | and            | why | half | of it is | unusable |     | 2   |
| 3   | The          | generalized |                | Uzawa  | preconditioner |     |      |          |          |     | 2   |
| 4   | Patches      |             |                |        |                |     |      |          |          |     | 3   |
| 5   | Constructing |             | the            | coarse | functions      |     |      |          |          |     | 4   |
| 6   | The          | guarantee   |                |        |                |     |      |          |          |     | 4   |
| 7   | What         | is local,   | and            | what   | is paid        |     |      |          |          |     | 6   |
| 8   | Summary      |             |                |        |                |     |      |          |          |     | 6   |
1 Data
Three objects, none of them referring to a mesh, an element type, or a dimension.
|     | • An | SPD matrix |     | presented | as  | an assembled |     | sum | of local pieces, |     |     |
| --- | ---- | ---------- | --- | --------- | --- | ------------ | --- | --- | ---------------- | --- | --- |
∑
⪰
|     |     |     |     | A = | A τ , |     | A τ | 0, supp(A | τ ) = the | nodes of τ. |     |
| --- | --- | --- | --- | --- | ----- | --- | --- | --------- | --------- | ----------- | --- |
τ
For a finite element or finite volume discretization the A τ are the element matrices and this
|     | costs | nothing; | it  | is the | only structural |     | input | the | theory needs. |     |     |
| --- | ----- | -------- | --- | ------ | --------------- | --- | ----- | --- | ------------- | --- | --- |
1

• A coarse space V
H
= range(P), P : RnH → Rn injective, whose columns have small supports.
How P is built is the subject of §4–§6; the preconditioner and its analysis do not depend on
the choice.
• A smoother M with K := M+MT −A ≻ 0 (any convergent relaxation), acting on the whole
space.
Write S := PTAP for the coarse operator. It is SPD: for v ̸= 0, injectivity gives Pv ̸= 0
H H H
and vTS v = ∥Pv ∥2 > 0.
H H H H A
2 The exact factorization, and why half of it is unusable
Lemma 1 (A–orthogonal splitting). Π := PS
−1PTA
is the A–orthogonal projector onto V , and
H H
Rn = V ⊕ ker(PTA), ∥v∥2 = ∥v ∥2 +∥w∥2 for v = Pv +w.
H A A H SH A H
Proof. The A–orthogonal complement of V is identified by moving A across the inner product:
H
w ⊥ range(P) ⇐⇒ (Pv )TAw = 0 ∀v ⇐⇒ PTAw = 0.
A H H
Next, Π2 = PS −1(PTAP)S −1PTA = Π, so Π is idempotent; Π(Pv ) = PS −1S v = Pv gives
H H H H H H H
range(Π) = V ; and Πv = 0 ⇐⇒ PTAv = 0 (cancel the injective P and the invertible S ), so
H H
kerΠ = ker(PTA). Idempotency gives the direct sum, the first display gives orthogonality of the
summands, and the cross term in ∥v∥2 therefore vanishes.
A
The splitting exhibits the inverse,
( )
A −1 = PS −1PT + exact solve on ker(PTA) ,
H
and with it the asymmetry that shapes every practical method. The coarse half is cheap: P is
local, S is a small assembled matrix. The other half is defined by the global constraint PTAw = 0
H
and has, in general, no local basis whatsoever — it cannot be assembled, so it is not solved. It is
smoothed. Everything below is the consequence of that single substitution.
3 The generalized Uzawa preconditioner
One application of B
−1
to a right–hand side b (from x = 0) is the symmetric inexact Uzawa sweep,
the coarse space in the role of the constraint block:
r = b−Ax; x += M −1r (pre–smooth)
( )
r = b−Ax; x += P S −1 PTr (coarse correction) (1)
H
r = b−Ax; x += M −Tr (post–smooth).
Proposition 1 (operator and block form). With the symmetrized smoother and the smoother–
corrected prolongation
( ) ( )
M¯−1 := M −T M +MT −A M −1 = M −1+M −T −M −TAM −1, P˜ := I −M −TA P,
the cycle (1) is the preconditioner
( )
M¯−1
0
B −1 = M¯−1+P˜S −1P˜T = L LT, L = [I, P˜]. (2)
H 0 S −1
H
2

|     |     |     |     |     |     |     | −M  | −TA)(I | −Π)(I | −M −1A), |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------ | ----- | -------- | --- | --- |
Proof. The error propagator of (1) is E = (I and B is defined by
−B −1A
| I   |     | = E. Expanding |     | the | smoothing | factors, |     |     |     |     |     |     |
| --- | --- | -------------- | --- | --- | --------- | -------- | --- | --- | --- | --- | --- | --- |
|     |     |                |     |     |           | [        |     |     |     | ]   |     |     |
(I −M −TA)(I −M −1A) = I − M −1+M −T −M −TAM −1 A = I −M¯−1A,
| and,         | using | A = AT  | so that | (I −M | −TA)T    | =     | I −AM | −1, |          |      |     |         |
| ------------ | ----- | ------- | ------- | ----- | -------- | ----- | ----- | --- | -------- | ---- | --- | ------- |
|              |       | −TA)Π(I |         | −1A)  |          |       | −TA)P |     | −1       | −1)A |     | −1P˜TA. |
|              | (I    | −M      |         | −M    | =        | (I −M |       | S   | PT(I −AM |      | =   | P˜S     |
|              |       |         |         |       |          |       |       |     | H        |      |     | H       |
|              |       |         |         | (     |          |       | )     |     |          |      |     |         |
|              |       |         | −1A     |       | M¯−1+P˜S | −1P˜T |       |     |          |      |     |         |
| Subtracting, |       | I −B    | =       | I −   |          |       | A.    |     |          |      |     |         |
H
The preconditioner is thus a block–diagonal solve — smoother on one block, coarse operator
on the other — conjugated by L. Two degenerate checks: if M = A then M¯−1 = A −1 and P˜ = 0,
|     | −1  | −1  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
so B = A and the coarse term switches itself off, there being nothing left to repair; and if AP
P˜
has no component along the smoothed directions, = P and no correction occurs.
Remark 1 (the prolongation is smoothed by the algebra). For damped Jacobi, M = 1D, the
ω
−1A)P
corrected prolongation is P˜ = (I −ωD — the smoothed–aggregation operator, arising here
as an identity rather than a device. Its columns keep the supports of P’s columns widened by the
|     |     | −TA: |     |     |     |     |     | P˜  |     |     |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
reach of M one ring for a point smoother, so remains local. (The correspondence is at the
level of this operator; (2) keeps S = PTAP, while smoothed aggregation forms its coarse operator
H
P˜.)
from
The analysis retains two independent channels: the smoother through t, and the coarse space
| through | the | stable–decomposition |     |       | constant |      |       |     |             |      |     |       |
| ------- | --- | -------------------- | --- | ----- | -------- | ---- | ----- | --- | ----------- | ---- | --- | ----- |
|         |     |                      |     | ∥v−Pv |          | ∥2   |       |     |             | (    |     | )     |
|         |     | C =                  | sup | min   | H        | M¯ , | κ(BA) |     | ≤ const·max | 1/t, | 1+C | . (3) |
|         |     | stab                 |     |       |          |      |       |     |             |      |     | stab  |
|         |     |                      |     | vH    | ∥v∥2     |      |       |     |             |      |     |       |
|         |     |                      | v   |       | A        |      |       |     |             |      |     |       |
The remainder of the note is about making C stab a quantity one sets rather than one that happens.
4 Patches
Definition 1 (admissible patch family). A family {ω }K of node sets is admissible if it covers
|     |     |     |     |     |     |     |     | k   | k=1 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
all nodes, each ω is a union of element supports, and the overlap multiplicity
k
|     |     |     |     |     |     |        | #{k |     | ∈ } |     |     |     |
| --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
|     |     |     |     |     | k   | := max |     | : i | ω   |     |     |     |
|     |     |     |     |     | 0   |        |     |     | k   |     |     |     |
i
∑
⪰
is bounded. Its local matrix is the Neumann assembly A k := τ⊆ω A τ 0.
k
The standard way to produce one, and the one to use: partition the elements into disjoint
aggregates by any means (a graph partitioner on the element adjacency, or geometry when it is
available), then grow each aggregate by δ ≥ 1 layers of elements. The result covers by construction,
is element–closed by construction, and on a shape–regular mesh has k = O(1) with a constant
0
| depending |        | on δ and | the     | mesh degree, |        | not on | the mesh |     | size. |     |     |     |
| --------- | ------ | -------- | ------- | ------------ | ------ | ------ | -------- | --- | ----- | --- | --- | --- |
| Two       | dials, | pulling  | against | each         | other: |        |          |     |       |     |     |     |
• aggregate size sets the coarsening ratio, hence how fast the hierarchy contracts;
• overlap δ raises k 0 (which enters the bound linearly, see Theorem 1) but improves the local
spectra, sinceawiderpatchseesmoreoftheoperator’slocalstructurebeforethecut–offacts.
3

What one does not need is a good guess. A patch family badly aligned with the operator —
cutting across a channel of large coeﬀicients, slicing an anisotropic direction — is still admissible,
andtheboundstillholds; themisalignmentsurfacesasanexcessofeigenvaluesabovethethreshold
in §5, i.e. as extra coarse functions on those patches, and it is visible patch by patch before any
solve. The local spectrum is the diagnostic for the patch choice, and it is cheap.
| 5 Constructing |     |     | the | coarse |     | functions |     |     |     |     |     |     |
| -------------- | --- | --- | --- | ------ | --- | --------- | --- | --- | --- | --- | --- | --- |
Fix a partition of unity subordinate to the patches: diagonal matrices D ⪰ 0 with
k
∑
⊆
|     |     |     |     |     | D k = | I,  | supp(D | k ) | ω k . |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | ------ | --- | ----- | --- | --- | --- |
k
The default is the equal share, (D ) = 1/#{j : i ∈ ω }; a taper that decays towards the patch
|     |     |     |     | k   | ii  |     |     | j   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
boundary is better, and the difference is exactly what the eigenproblem below will price.
The coarse space is then generated patch by patch, and the criterion is dictated by (3): a mode
must go to the coarse level exactly when the smoother cannot pay for it, i.e. when its localized
smoother–norm is large against its local energy. That ratio is a generalized eigenproblem on the
patch,
|     |     |     |     |     |     |     | ∥D  | x∥2 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
k
|     |     | D   | MD x = | λA  | x,  | λ(x) | =    | M,  | λk  | ≥ λk ≥ | ··· , | (4) |
| --- | --- | --- | ------ | --- | --- | ---- | ---- | --- | --- | ------ | ----- | --- |
|     |     | k   | k      | k   |     |      | ∥x∥2 |     |     | 1 2    |       |     |
A k
posed on the A k –complement of kerA k . The matrix D k MD k is as local as D k (diagonal for a
point smoother), so (4) is a small dense problem on the patch. Large λ marks the locally smooth,
low–energy modes — the ones relaxation leaves untouched; small λ marks the oscillatory ones,
which the smoother handles and which may be discarded. Note kerA is the local near–null space
k
— constants for diffusion, rigid body modes for elasticity — where λ = ∞; it is always selected.
| Definition | 2          | (the coarse | space         | at threshold |           | τ).      |      |     |     |         |       |     |
| ---------- | ---------- | ----------- | ------------- | ------------ | --------- | -------- | ---- | --- | --- | ------- | ----- | --- |
|            |            |             |               | {            |           |          |      | }   | {   |         | }     |     |
|            |            | V (τ)       | := span       |              | D z       | : z ∈    | kerA | ∪   | D   | xk : λk | > τ , |     |
|            |            | H           |               |              | k         |          |      | k   | k   | j j     |       |     |
| and P is   | the matrix |             | whose columns |              | are these | vectors. |      |     |     |         |       |     |
Each column is supported in one patch, so P is as local as the patches are; the number of
columns per patch is not chosen but read off the local spectrum, which is where the cost of a poor
| patch family | shows     | up. |     |     |     |     |     |     |     |     |     |     |
| ------------ | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 6 The        | guarantee |     |     |     |     |     |     |     |     |     |     |     |
By construction, every mode left to the smoother is cheap: if w is A –orthogonal to the selected
k
| modes on | patch | k, then |     |     |     |     |     |      |     |     |     |     |
| -------- | ----- | ------- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|          |       |         |     |     | ∥D  | w∥2 | ≤   | ∥w∥2 |     |     |     |     |
|          |       |         |     |     |     |     | τ   | ,    |     |     |     | (5) |
|          |       |         |     |     |     | k M |     | A k  |     |     |     |     |
M¯ ⪯
since the selected modes are exactly those with λ > τ. Because M, the same bound holds
M¯–norm
in the that (3) actually uses. This is the whole point of (4): the discarded part of the
| spectrum | is bounded |     | by the number |     | one | chose. |     |     |     |     |     |     |
| -------- | ---------- | --- | ------------- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
4

The bound is an identity. For the additive form (2) the abstract Schwarz theory gives more
| than an inequality: |     | λ max | (BA) = | 1 and λ | min (BA) | = 1/C | stab , so |     |     |     |     |
| ------------------- | --- | ----- | ------ | ------- | -------- | ----- | --------- | --- | --- | --- | --- |
|                     |     |       |        |         |          | (     | )         |     |     |     |     |
|                     |     |       |        | κ(BA)   | = max    | 1, C  | ,         |     |     |     | (6) |
stab
with no constant in front and no additive 1. This was verified to six digits over every configuration
of the calibration below — λ came out exactly 1 each time. So the design problem is precisely
max
| to make C | small, | and | τ is the | handle | on it. |     |     |     |     |     |     |
| --------- | ------ | --- | -------- | ------ | ------ | --- | --- | --- | --- | --- | --- |
stab
Theorem 1 (stable decomposition at a prescribed constant). For the coarse space of Definition 2
| on an admissible |     | patch | family with | multiplicity | k   | ,   |     |     |     |     |     |
| ---------------- | --- | ----- | ----------- | ------------ | --- | --- | --- | --- | --- | --- | --- |
0
|     |      |     |          |        |         |     |       |     | (   | )        |     |
| --- | ---- | --- | -------- | ------ | ------- | --- | ----- | --- | --- | -------- | --- |
|     |      | ≤   |          |        |         |     |       | ≤   |     |          |     |
|     | C    |     | C(k ) τ, | hence, | by (6), |     | κ(BA) | max | 1,  | C(k )τ , |     |
|     | stab |     | 0        |        |         |     |       |     |     | 0        |     |
with C(k ) depending only on the overlap multiplicity — not on the mesh size, the coeﬀicients, or
0
| the number | of patches. |     |     |     |     |     |     |     |     |     |     |
| ---------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∑
The mechanism is the standard one: decompose v by the partition of unity, v = D v;
k k
replace on each patch the selected modes by their coarse representative, which is exact; bound
what remains by (5); and pay k for the overlap when the local estimates are summed. This is the
0
GenEO argument (Spillane–Dolean–Nataf–Rixen–Scheichl) and the spectral AMGe construction
(Brezina–Vassilevski).
C(k 0 ), calibrated. CrudebookkeepingofthetwooverlapsummationssuggestsaquadraticC(k 0 ).
Measured, itislinear. Bilinearelementson25×25interiornodes, aggregatesof4×4cellsgrow(nby
M¯
δ layers, damped Jacobi;)τ swept over {1.5,1,0.6,0.3,0.15}; C computed sharply as λ −
|            |          |     |               |     |              |         | stab    |           |             | max      |     |
| ---------- | -------- | --- | ------------- | --- | ------------ | ------- | ------- | --------- | ----------- | -------- | --- |
| M¯P(PTM¯P) | −1PTM¯,  |     |               |     |              |         |         |           |             |          |     |
|            |          |     | A and divided | by  | the achieved |         | largest | discarded | eigenvalue: |          |     |
|            | operator |     |               | δ   | = 1 (k       | 0 =4) δ | = 2 (k  | 0 =9)     | δ = 3       | (k 0 =9) |     |
|            | Poisson  |     |               |     | 2.30         |         | 7.33    |           | 9.25        |          |     |
|            | rotated  |     | tensor ε =    | 0.1 | 2.19         |         | 5.14    |           |             | —        |     |
103
|     | jump |     |     |     | 2.35 |     | 7.13 |     |     | —   |     |
| --- | ---- | --- | --- | --- | ---- | --- | ---- | --- | --- | --- | --- |
(worst value over the τ sweep). Across every run C /τ ≤ k + 1, and the ratio is insensitive
|     |     |     |     |     |     | stab |     | 0   |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
to the operator: the mixed–derivative and the 103 jump behave like the Laplacian, which is the
coeﬀicient–robustnesstheconstructionisfor. Twohonestcaveats: thelinear–in–τ formisnotsharp
— C decays more slowly than τ, so the ratio drifts by about a factor of two across the sweep,
stab
and the table reports the worst case; and k saturates at 9 for δ ≥ 2 on this geometry, so the fit
0
| rests on two | distinct | multiplicities. |     |     |     |     |     |     |     |     |     |
| ------------ | -------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
What matters is the logical direction. One does not build a prolongation and then hope the
constant is small: one names τ, and the local eigenproblems answer with the number of coarse
functions required to honour it. Every ingredient of that answer is local and computable before
any solve — only C stab and κ themselves, used above as ground truth, are global.
The dial. Lowering τ improves the bound and admits more modes per patch; raising it does
the reverse. The coarse space grows monotonically as τ decreases, and so does the density of
PTAP
S = — which is the true cost, see §7. The near–null space is never subject to the dial: it
H
is always included, and omitting it is the one way to lose the bound outright.
5

| 7 What | is local, | and what | is paid |     |     |
| ------ | --------- | -------- | ------- | --- | --- |
Setup. Per patch, independently and in parallel: assemble A from the element pieces inside ω ;
k k
solve the small eigenproblem (4); form the columns D xk. Then assemble S = PTAP, a sparse
k H
j
triple product whose entries are gathered from overlapping patches. No global object is formed at
| any stage, | and the patch | tasks do       | not communicate. |               |          |
| ---------- | ------------- | -------------- | ---------------- | ------------- | -------- |
| Iteration. | In the cycle  | (1):           |                  |               |          |
|            | operation     | locality       |                  |               |          |
|            | Ax            | local (sparse  | product)         |               |          |
|            | M −1r, M      | −Tr local when | M is (Jacobi,    | block Jacobi, | a sweep) |
PTr, Pv local: each coarse function reads and writes its own patch
H
−1
|     | S   | not local | — the coarse | solve |     |
| --- | --- | --------- | ------------ | ----- | --- |
H
Everything is local except the coarse solve, which is removed as always: by recursion. Applying the
same construction to S turns the two–level method into a hierarchy, and an exact solve survives
H
| only at | the bottom, where | the problem | is small. |     |     |
| ------- | ----------------- | ----------- | --------- | --- | --- |
The cost. Generality is not paid for in locality but in sparsity. Several basis functions per patch,
P˜
overlapping supports, and the extra ring picked up by make S H denser than A, and the growth
compounds down a hierarchy; the threshold τ is the knob that trades guaranteed conditioning
against that density. This is the standing tension between a spectrally generated coarse space
and a cheap prolongation of fixed sparsity, and it is why the latter — whose constant must then
be measured rather than prescribed — remains the working default in practice. The complement
ker(PTA), by contrast, costs nothing at all: it is never formed, being exactly the part the smoother
| is responsible | for. |     |     |     |     |
| -------------- | ---- | --- | --- | --- | --- |
8 Summary
The construction runs in one direction, from data to guarantee. An admissible patch family and a
partition of unity are chosen freely; on each patch a small generalized eigenproblem measures how
badly localization inflates energy; the modes above a named threshold τ, together with the local
near–null space, are localized and become the coarse basis. The resulting coarse space satisfies a
stabledecompositionwithconstantC(k )τ,sotheconditionnumberofthepreconditionedoperator
0
is bounded by a number fixed in advance, uniformly in mesh size and coeﬀicients. The precondi-
tioner itself is the symmetric inexact Uzawa cycle (1), whose operator form (2) is a block–diagonal
|     |     | P˜] P˜ | −M −TA)P: |     |     |
| --- | --- | ------ | --------- | --- | --- |
solve conjugated by [I, with = (I the prolongation corrected by the smoother,
the correction being what the smoother must repair. Setup and application are local except for the
coarse solve, and the price of the whole arrangement is the density of the coarse operator, governed
by τ.
Companion. The fixed–sparsity branch — a prescribed cheap prolongation whose constant is
measured by a local certificate, with numerical validation: two-grid-primer.
6
