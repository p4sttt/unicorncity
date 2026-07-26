| An  | Entrywise |     |     | Certificate |     | for | the | Two–Grid |     | Condition |
| --- | --------- | --- | --- | ----------- | --- | --- | --- | -------- | --- | --------- |
Number
|     |     |     |     | Numerical |      | Archeology |      | project |     |     |
| --- | --- | --- | --- | --------- | ---- | ---------- | ---- | ------- | --- | --- |
|     |     |     |     |           | July | 22,        | 2026 |         |     |     |
Abstract
Asinglecomputableboundonκ(BA)forthefactorized(inexactUzawa)two–gridprecondi-
tioner, with every input read from the matrix entries, the interpolation weights, and one scalar
characterizing the smoother. No spectral computation, no geometric information, and no inte-
rior/boundarycasedistinctions: thematrixclassistreateduniformlyasagroundedgraphLapla-
cian, so the certificate applies verbatim to unstructured meshes, scattered Dirichlet nodes, and
shifted operators. Proofs of the underlying spectral theorem are in uzawa-spectral-theory;
| this  | note   | records | only the | certificate. |     |            |     |     |     |     |
| ----- | ------ | ------- | -------- | ------------ | --- | ---------- | --- | --- | --- | --- |
| 1 The | class: |         | grounded | graph        |     | Laplacians |     |     |     |     |
∈ RN×N
| Throughout, |     | A   | is  | SPD with |     |     |     |     |     |     |
| ----------- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- |
∑
|     |     |     |     | ≤   | ̸=   |     |     | ≥   |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
|     |     |     |     | a   | 0 (i | j), | s = | a   | 0.  |     |
|     |     |     |     | ij  |      |     | i   | ij  |     |     |
j
Bothconditionsarereadofftheentries. Thisclassisexactlytheclassof groundedgraphLaplacians:
introduce one extra node g (“ground”), held at value 0, and a weighted graph on {1,...,N}∪{g}
with
|     |     |     |     |     | |a | | ≤    |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | ---- | --- | --- | --- | --- |
|     |     |     |     | w = |      | (i,j | N), | w = | s . |     |
|     |     |     |     | ij  | ij   |      |     | ig  | i   |     |
∑
−v
Then vTAv = w (v )2 with v = 0 — every term is an edge term; there are no “vertex
|     |     | edges | xy  | x y | g   |     |     |     |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
terms” and no interior/boundary distinction. A Dirichlet row, a reaction term, a shift +σI are all
the same object: an edge into the ground, of weight s (resp. s +σ), wherever it happens to sit.
|       |       |           |     |            |     |        | i     | i          |       |     |
| ----- | ----- | --------- | --- | ---------- | --- | ------ | ----- | ---------- | ----- | --- |
| Given | a C/F | splitting | of  | {1,...,N}, | the | ground | joins | the coarse | side: |     |
|       |       |           |     | C¯         |     | ∪{g},  |       | ≡          |       |     |
|       |       |           |     |            | = C |        |       | u 0.       |       |     |
g
C¯
| All quantities |     | below | live on | uniformly. |     |     |     |     |     |     |
| -------------- | --- | ----- | ------- | ---------- | --- | --- | --- | --- | --- | --- |
2 Inputs
1. The matrix A (equivalently, the grounded graph) and the C/F splitting.
|                  |     |         |     | C¯:       |     |             |     | ≥      | ∈ C¯, |     |
| ---------------- | --- | ------- | --- | --------- | --- | ----------- | --- | ------ | ----- | --- |
| 2. Interpolation |     | weights |     | over each | F   | row carries |     | ω 0, c | with  |     |
fc
∑
|     |     |     |     | ω   | = 1 | —   | always, | no exceptions. |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------- | -------------- | --- | --- |
fc
c∈C¯
1

Interpolatingfromthegroundcontributesthevalue0. Thecanonical(lumped)choicesatisfies
| this | identically: |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
| ---- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|      |              |     |     |     | ∑   |     |     | |a  | |   |     |     |     |     |     |     |     |
s
|     |     |     |     | d = | |a |+s | ,   | ω   | = fc | ,   | ω   | = f . |     |     |     |     |     |
| --- | --- | --- | --- | --- | ------ | --- | --- | ---- | --- | --- | ----- | --- | --- | --- | --- | --- |
|     |     |     |     | f   | fc     | f   | fc  |      |     | fg  |       |     |     |     |     |     |
|     |     |     |     |     |        |     |     | d    |     |     | d     |     |     |     |     |     |
|     |     |     |     |     | c∈C    |     |     |      | f   |     | f     |     |     |     |     |     |
(Foraninteriorrows = 0thisistheusuallumpedinterpolation; forarownexttoaDirichlet
f
node it automatically interpolates partly from the boundary zero. One formula covers both.)
|     |     | M¯  |     | M¯  | ⪰   |     |     |     |     |     |     |     | (M¯−1A |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
3. A smoother f (SPD, f A ff ), entering through the single scalar t = λ min ff ).
f
|     |     |     | M¯  |     |     |     |     |     |     | ≥   | 1−ρ |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
For damped Jacobi = (1+ρ)diag(a ) the certified value is t with ρ from Table 1.
|         |          |     |            | f      |       | ff  |     |       |     |     | 1+ρ |     |     |     |     |     |
| ------- | -------- | --- | ---------- | ------ | ----- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 The   | estimate |     |            |        |       |     |     |       |     |     |     |     |     |     |     |     |
| Theorem | 1. With  |     | the inputs | above, |       |     |     |       |     |     |     |     |     |     |     |     |
|         |          |     |            | (      |       | )   |     |       |     |     |     |     |     |     |     |     |
|         |          |     |            |        |       |     |     |       |     |     |     | |Q  | |   |     |     |     |
|         |          |     |            |        | 1     |     |     | 1+1/t |     |     |     |     |     |     |     |     |
|         | κ(BA)    |     | ≤ 4max     |        | , 1+Θ | ,   | Θ = |       | µ,  | µ = | max | xy  |     |     |     |     |
1−ρ
|     |     |     |     |     | t   |     |     |     |     |     | x̸=y∈C¯ | β   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- |
xy
Qxy ̸=0
|     |     | √   |     |     |     |     |     |     | [   | (   | )   | ]   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
and #PCG ≤ κ ln(2/tol). The spectrum satisfies σ(BA) ⊆ 1 min t, 1 , 2 ; the upper end-
|         |                   |     |     |     |     |     |     |     | 2   |     | 1+Θ |     |     |     |     |     |
| ------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| point 2 | is unconditional. |     |     |     |     |     |     |     |     |     |     |     |     |     |     |     |
Table 1: The inputs of Theorem 1. All indices x,y range over C¯ = C ∪{g}; w are the grounded–
| graph edge | weights |        | of Section | 1.         |     |     |     |     |          |     |     |         |     |     |            |          |
| ---------- | ------- | ------ | ---------- | ---------- | --- | --- | --- | --- | -------- | --- | --- | ------- | --- | --- | ---------- | -------- |
| quantity   | formula |        |            |            |     |     |     |     | meaning  |     |     |         |     |     | source     |          |
|            |         | (M¯−1A |            |            | 1−ρ |     |     |     |          |     |     |         |     |     |            |          |
| t          | λ       |        |            | ); Jacobi: | ≥   |     |     |     | smoother |     | vs. | F–block |     |     | smoother’s | passport |
|            | min∑f   |        | ff         |            | 1+ρ |     |     |     |          |     |     |         |     |     |            |          |
|            |         |        | |a         | |          |     |     |     |     |          |     |     |         |     |     |            |          |
f′∈F ff′
| ρ   | max |     |     |     |     |     |     |     | F   | rows | anchored | in  | C¯  |     | rows of | A   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | -------- | --- | --- | --- | ------- | --- |
ff
|     | f∈F |     | a   |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     |     | ff  |     |     |     | ∑   |     |     |     |     |     |     |     |     |     |
(APˆ)
η w–weighted residual row: , x∈C¯ η = 0 weight residual at f A + weights
| fx  |     |     |     |     |     | fx  |     | fx  |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
∑
|      |     | η   | η   |     |     |     |     |     |          |     |      |         |     |             |               |     |
| ---- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | ---- | ------- | --- | ----------- | ------------- | --- |
|      |     | fx  | fy  |     |     |     |     |     |          |     |      |         |     |             |               |     |
| Q xy |     |     |     |     |     |     |     |     | residual |     | Gram | (“Schur | of  | the error”) | sparse matmul |     |
a
ff
f ∑
w w
| β   | w   | +   | xf  | fy  |     |     |     |     | certified |     | stiffness | between |     | x and y | rows of | A   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --------- | ------- | --- | ------- | ------- | --- |
| xy  | xy  |     |     |     |     |     |     |     |           |     |           |         |     |         |         |     |
a
f ff
C¯
Both Q and the Schur complement of the grounded ∑ Laplacian are grounded Laplacians on with
zero row sums (for Q this is the identity η = (APˆ1 ) = 0, a direct consequence of
| ∑   |     |     |     |     |     | x∈C¯ | fx  |     | C¯  | f   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ω = 1), so both quadratic forms are sums of the same squares (u −u )2, u = 0, and the
| x fx       |            |      |     |           |            |       |         |       |       |      | x      | y   | g   |     |     |     |
| ---------- | ---------- | ---- | --- | --------- | ---------- | ----- | ------- | ----- | ----- | ---- | ------ | --- | --- | --- | --- | --- |
| form ratio | is bounded |      | by  | the worst | coeﬀicient |       | ratio µ | — one | line: |      |        |     |     |     |     |     |
|            |            |      |     | ∑         |            |       | ∑       |       |       |      |        |     |     |     |     |     |
|            |            | uTQu | ≤   | |Q        | |(u        | −u )2 | ≤ µ     | β (u  | −u    | )2 ≤ | µ∥u∥2. |     |     |     |     |     |
|            |            |      |     |           | xy x       | y     |         | xy    | x     | y    | S      |     |     |     |     |     |
|            |            |      |     | x<y       |            |       | x<y     |       |       |      |        |     |     |     |     |     |
The last inequality is the entrywise Schur bound: the true Schur complement dominates, edge by
|     |     |     |     |     | −1 ≥ | −1  |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
edge, its first Neumann term (A D entrywise, valid in this sign class), which is the formula
|     |     |     |     |     | ff  | F   |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
for β . Pairs x,y with Q ̸= 0 but β = 0 signal a coverage gap; see Remark 1.
| xy  |     |     |     | xy  | xy  |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2

Remark 1 (coverage depth). Q couples pairs within distance k+1 of the F–graph, where k is the
reach of the weights (k = 1 for nearest–neighbor weights). If the splitting satisfies the Ruge–Stüben
axiom (every strongly connected F–F pair has a common C¯–neighbor), the one–term β above covers
all such pairs at the cost of a factor 2 in µ. Otherwise replace β by the (k+1)–term Neumann
∑
|     |     | |(AC¯ | −AC¯ | AC¯ | |,  |     | −1N)jD | −1: |
| --- | --- | ----- | ---- | --- | --- | --- | ------ | --- |
truncation β xy = Y ) xy Y m = (D every truncation is a valid
|     |     | cc   | cf  | k+1 fc |     | j<m | F   | F   |
| --- | --- | ---- | --- | ------ | --- | --- | --- | --- |
|     |     | ↑ −1 |     |        |     |     |     |     |
lower bound (Y A entrywise) and depth k+1 guarantees coverage by construction.
|           |     | m ff |             |     |     |     |     |     |
| --------- | --- | ---- | ----------- | --- | --- | --- | --- | --- |
| 4 Reading |     | the  | certificate |     |     |     |     |     |
C¯
• ρ < 1 is the go/no–go check of the splitting: every F row must be anchored in (a C point
| or  | the ground). |     |     |     |     |     |     |     |
| --- | ------------ | --- | --- | --- | --- | --- | --- | --- |
• µ is the single substantive number: the worst elementwise ratio of the error–Schur ∑ Q to the
stiffness–Schur bound β. Ideal weights give Q = 0 and κ ≤ 4/t; injection breaks ω = 1,
x fx
so Q acquires ground edges of size ∼ a against β = 0 at interior nodes — the certificate
|          |            |     |     |     |     | ff  | cg  |     |
| -------- | ---------- | --- | --- | --- | --- | --- | --- | --- |
| refuses, | correctly. |     |     |     |     |     |     |     |
∑
• The condition ω = 1 is what aligns the two Laplacians: it forces Q to have edges
|     |     |     | x∈C¯ fx |     |     |     |     |     |
| --- | --- | --- | ------- | --- | --- | --- | --- | --- |
only where the Schur complement has certified stiffness. It is a single unconditional identity
— the interior/boundary distinction of earlier drafts is absorbed by the ground node.
• Everything is one pass over the sparse matrix; no eigenvalue problem is solved anywhere.
Roles are separated: the smoother enters only through t, the matrix through ρ,β, the weights
| through  |     | Q.       |     |              |     |     |     |     |
| -------- | --- | -------- | --- | ------------ | --- | --- | --- | --- |
| 5 Scope, |     | and what |     | lies outside |     |     |     |     |
The certificate is stated for the grounded–Laplacian class of Section 1. Outside it (positive off–
diagonal entries) exactly one step fails: the entrywise lower bound β on the Schur energy. Two
| precise | facts delimit | what | can | be done. |     |     |     |     |
| ------- | ------------- | ---- | --- | -------- | --- | --- | --- | --- |
Aˇ
Lemma 1 (Schur monotonicity). If ⪯ A then the Schur energies satisfy σ (u) ≥ σ (u) for all
A Aˇ
|          |       | ∥(v   | ;u)∥2 ≥ |     | ∥(v ;u)∥2 |             |     |     |
| -------- | ----- | ----- | ------- | --- | --------- | ----------- | --- | --- |
| u: σ (u) | = min |       |         | min |           | = σ Aˇ (u). |     |     |
| A        |       | v f f | A       | v f | f         | Aˇ          |     |     |
Consequently β may be computed from any grounded–Laplacian minorant Aˇ ⪯ A; the matrix,
the preconditioner and the Schur complement of A are untouched — the minorant exists only in
the denominator of the analysis. Whether a useful minorant exists is problem–specific and is not
treated here.
Remark 2 (animpossibility). Noentrywisecertificatecanavoidsomesuchstructure: twosymmet-
2I±adj(K
ric matrices with identical entry moduli can differ in λ min by an arbitrary factor (e.g. 3 )),
so lower bounds of quadratic forms are not certifiable from moduli alone. When no minorant is
−1A
available, Θ is measured instead: a short Lanczos run on the sparse pencil (Q, A −A D ),
cc cf F fc
| at the cost | of  | a few sparse | products. |     |     |     |     |     |
| ----------- | --- | ------------ | --------- | --- | --- | --- | --- | --- |
| 6 Worked    |     | example      |           |     |     |     |     |     |
−2tridiag(−1,2,−1)
1D Poisson, A = h with Dirichlet ends (so the two extreme rows carry ground
edges s = 1/h2), C = even points, interior weights (1 +θ, 1 −θ); the lumped formula gives the
|     |     |     |     |     |     | 2   | 2   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
3

(1, 1)
extreme F points weights split between their C neighbor and the ground. Then ρ = 0, t = 1,
2 2
| and | on interior | positions |     |          |     |       |       |      |      |
| --- | ----------- | --------- | --- | -------- | --- | ----- | ----- | ---- | ---- |
|     |             | 2θ        |     | (2θ/h2)2 | 2θ2 |       | 1     |      |      |
|     |             | ±         | |Q  | |        |     |       |       | 4θ2, | 8θ2, |
|     | η fc =      | ,         | cc′ | =        | = , | β cc′ | = , µ | =    | Θ =  |
|     |             | h2        |     | 2/h2     | h2  |       | 2h2   |      |      |
whichcoincideswiththeexactlycomputedvalue: thecertificateissharphere. Idealweights(θ = 0)
| give | κ ≤ 4, | i.e. at most | 13 PCG | iterations | to 10 −8. |     |     |     |     |
| ---- | ------ | ------------ | ------ | ---------- | --------- | --- | --- | --- | --- |
Provenance. The spectral theorem behind Theorem 1 (λ ≤ 2 unconditionally; the lower end
max
sandwichedbytandΘwithinafactoroftwo)isprovedinuzawa-spectral-theory. Theentrywise
layer adds three tools, each used once: Gershgorin (for ρ and the residual norm), the entrywise
monotonicity of the Neumann series (for β), and the grounded zero–row–sum decomposition that
| reduces | the | form ratio | Θ to | the elementwise | ratio | µ.  |     |     |     |
| ------- | --- | ---------- | ---- | --------------- | ----- | --- | --- | --- | --- |
4
