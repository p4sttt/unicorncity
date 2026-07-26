|     |     | Streaming |     | Tensor-Train |     |     | Dynamic | Mode | Decomposition: |     |     |
| --- | --- | --------- | --- | ------------ | --- | --- | ------- | ---- | -------------- | --- | --- |
Error Bounds, Break-Even Analysis, and Drift-Matched Forgetting
Abstract
We propose a streaming formulation of tensor-train dynamic mode decomposition (TT-DMD) in which the spatial
subspace is tracked online by TT-FOA—a fixed-rank, recursive-least-squares tensor-train tracker with an exponential
forgetting factor λ—and the reduced DMD operator is updated slice-by-slice. The proposal is theory-led: the central
object is a per-step error recursion linking the TT truncation tolerance and the tracking error to the perturbation
of the DMD eigenvalues, together with a criterion that ties the optimal forgetting factor to the spectral drift rate
of a time-varying system. Experiments on synthetic time-varying linear systems and the two-dimensional cylinder
wake are designed to confirm the predicted scalings rather than merely to demonstrate feasibility. We position the
work against the recent online TT-DMD of Ma, Liu and Wei [19], whose updating scheme differs from an off-the-shelf
|     | streaming-TT | tracker. |     |     |     |     |     |     |     |     |     |
| --- | ------------ | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1 Thesis
Setup. Let x ∈Rn be a snapshot at time t, reshaped (tensorized) into a d-way array X ∈Rn1×···×nd with n= ∏︁ n .
|     |     | t   |     |     |     |     |     |     |     | t   | i i |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Batch TT-DMD [8] replaces the SVD in standard DMD [22, 25] by a tensor-train decomposition [21] of the snapshot
data and forms the reduced operator A˜=U∗X′VΣ−1 in TT format, where U is an orthonormal basis of the (tensorized)
|     |     | X↦→X′ |     |     |     |     |     |     | A˜  |     |     |
| --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
spatial subspace and is the temporal shift. The eigenvalues of approximate the system (Koopman) spectrum.
Claim. We maintain U online using TT-FOA [13], a fixed-rank tensor-train tracker that updates the TT-cores by an
exponentially weighted least-squares fit with forgetting factor λ∈(0,1], and we update A˜ from each incoming snapshot
pair. (TT-FOA models the stream as a (d+1)-way tensor growing along a temporal mode, with the d spatial cores
shared across slices—exactly the “tensorized spatial subspace × temporal coefficients” split that TT-DMD needs, which
is why it is the natural tracker here.) Three properties of TT-FOA shape the entire proposal:
A˜
1. Fixed TT-rank. keeps a constant size, so eigenvalues are trackable frame-to-frame; the rank-jump problem of
|     | adaptive-rank | trackers | (e.g. TT-ICE |     | [1]) is | avoided | by construction. |     |     |     |     |
| --- | ------------- | -------- | ------------ | --- | ------- | ------- | ---------------- | --- | --- | --- | --- |
2. Forgetting factor λ. The effective window length is W ≈1/(1−λ), which turns “optimal window length” into
| “optimal |     | λ” and connects | directly | to  | time-varying |     | online DMD | [26]. |     |     |     |
| -------- | --- | --------------- | -------- | --- | ------------ | --- | ---------- | ----- | --- | --- | --- |
3. RLS structure. Recursive-least-squares error dynamics are analyzable, giving access to a per-step error recursion
A˜.
for
Framework view. AlthoughTT-FOAistheprimaryinstantiation, theproposalisbestreadasamodulararchitecture
with three exchangeable slots: (spatial subspace tracker) × (reduced-operator update) × (forgetting mechanism). The
error analysis of Conjecture 1.1 should therefore be stated against abstract tracker properties—per-step residual η t ,
orthogonality defect, and rank behavior—so that any streaming-TT tracker can be dropped into the first slot: TT-
FOA [13] (fixed rank, exponential forgetting; the default), ATT [14] (same RLS family, adds incomplete observations),
TT-ICE[1], andthesketch-basedstreamingapproximationof[10]. Thisframinghastwopayoffs: anysingleinstantiation
published elsewhere (including [19]) becomes a point in our design space rather than a competing method, and the
systematic tracker comparison is itself a deliverable no existing work provides. A caveat on TT-ICE: it is append-
only—adaptive rank, no forgetting factor—so the “effective window length” notion central to the λ⋆ analysis has no
analogue there, past data are never down-weighted (bad for time-varying spectra), and rank jumps change the size of A˜
mid-stream, breaking eigenpair continuity. TT-ICE therefore enters only as a stationary-regime baseline and as the foil
motivating fixed-rank forgetting trackers; the λ⋆ theory is scoped to the RLS family.
Conjecture 1.1 (Sharpened thesis, revised after M0.5). With TT-FOA as the spatial tracker, streaming TT-DMD
| admits | a per-step | subspace | error | bound | of the | form |      |     |             |     |     |
| ------ | ---------- | -------- | ----- | ----- | ------ | ---- | ---- | --- | ----------- | --- | --- |
|        |            |          |       | (︁    | )︁     |      |      |     | δ √         |     |     |
|        |            |          | sinθ  | U ,   | U(t) ≤ | C ε  | +C η | +C  | t +C σ 1−λ, |     |     |
|        |            |          |       | t     | true   | 1 tt | 2 t  | 3   | 4           |     |     |
1−λ
where ε is the TT truncation tolerance, η the (noise-free) tracker residual, δ the subspace/spectral drift per step, and
|     | tt  |     |     |     | t   |     |     |     | t   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
σ the measurement-noise level. The last two terms are the tracking bias and the estimation variance: the drift term
1

| Algorithm | 1:       | Streaming | TT-DMD |            | (TT-FOA | tracker)     |                |     |        |     |     |     |
| --------- | -------- | --------- | ------ | ---------- | ------- | ------------ | -------------- | --- | ------ | --- | --- | --- |
| Input:    | snapshot | stream    | {x     | }; TT-rank |         | r; tolerance | ε ; forgetting |     | factor | λ   |     |     |
|           |          |           |        | t          |         |              | tt             |     |        |     |     |     |
(λˆ(t),ϕ(t))
| Output:    | running  | DMD | eigenpairs |         |         |       |     |     |     |     |     |     |
| ---------- | -------- | --- | ---------- | ------- | ------- | ----- | --- | --- | --- | --- | --- | --- |
|            |          |     |            |         | k       | k     |     |     |     |     |     |     |
| initialize | TT-cores |     | of U from  | a short | warm-up | batch |     |     |     |     |     |     |
1
| for each    | new | snapshot | x do |     |     |     |     |     |     |     |     |     |
| ----------- | --- | -------- | ---- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2           |     |          | t    |     |     |     |     |     |     |     |     |     |
| 3 tensorize |     | x →X     |      |     |     |     |     |     |     |     |     |     |
t t
| TT-FOA |     | step: | update | TT-cores | of  | U with weight | λ   |     |     |     |     |     |
| ------ | --- | ----- | ------ | -------- | --- | ------------- | --- | --- | --- | --- | --- | --- |
4
| 5 re-orthogonalize |         |     | cores if | canonical | form        | drifted |     |     |     |     |     |     |
| ------------------ | ------- | --- | -------- | --------- | ----------- | ------- | --- | --- | --- | --- | --- | --- |
| update             | reduced |     | operator | A˜ via    | the shifted | pair    |     |     |     |     |     |     |
6
eigendecompose A˜; match eigenpairs to step t−1 (e.g. greedy assignment on |λˆ(t)−λˆ(t−1)| or mode overlap
| 7   |     |     |     |     |     |     |     |     |     | k   | k   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|⟨ϕ(t),ϕ(t−1)⟩|)
k k
| report | (λˆ(t),ϕ(t)) |     |     |     |     |     |     |     |     |     |     |     |
| ------ | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 8      | k            | k   |     |     |     |     |     |     |     |     |     |     |
9 end
grows as λ→1 (long memory averages over a moving subspace) while the noise term grows as λ→0 (RLS estimate
|     |     | (1−λ)σ2). |     |     |     |     |     |     |     |     | λ⋆  | (︁ )︁2/3 |
| --- | --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- |
variance scales like Balancing them yields a drift-matched optimum of the form ≈1− cδ t /σ , the
usable tuning rule targeted by open question 4. The eigenvalue error is then a corollary, not the primary object:
|     |     |     |     | |λ(t)−λˆ(t)| |     | (︁ )︁[︂ | (︁      | )︁ ]︂ |     |          |     |     |
| --- | --- | --- | --- | ------------ | --- | ------- | ------- | ----- | --- | -------- | --- | --- |
|     |     |     |     |              |     | ≲ κ W   | σg sinθ | +δ ,  | W   | =U+B(t), |     |     |
|     |     |     |     | k            | k   |         |         | t     |     | t        |     |     |
reflecting a structural fact confirmed empirically at M0.5: for noise-free data confined to a K-dimensional invariant
subspace with basis B, any injective rank-≥K projection preserves the reduced operator’s eigenvalues exactly (the reduced
U+B).
dynamics are similar to the true K ×K dynamics via Subspace quality therefore enters the eigenvalue error
only through noise amplification, i.e. through the conditioning κ(U+B(t)), which is why eigenvalue error alone barely
t
separates good trackers from bad ones and sinθ must be the headline metric (and bound).
| Algorithm | 1 states  |     | the loop | whose | analysis | Conjecture | 1.1 | targets. |     |     |     |     |
| --------- | --------- | --- | -------- | ----- | -------- | ---------- | --- | -------- | --- | --- | --- | --- |
| 2 Open    | questions |     |          |       |          |            |     |          |     |     |     |     |
The proposal stands or falls on the following, ordered by how much they gate the main result.
1. Incremental TT pseudoinverse. Matrix streaming DMD updates Σ−1 by rank-1 (Sherman–Morrison) steps;
there is no clean TT analogue because TT-rank grows under addition. Is there a bounded-cost incremental TT
pseudoinverse whose error is controllable per step? This is the genuine kernel. Fallback: the pseudoinverse can be
pushed into the small reduced space—project each pair, y =U∗x , y′ =U∗x , and run matrix online DMD [26] on
|     |     |     |     |     |     |     | t   | t t | t t | t+1 |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
the r-dimensional stream via λ-weighted correlation matrices P =λP +y′y∗, Q =λQ +y y∗, A˜ =P Q−1, so
|     |     |     |     |     |     |     |     | t   | t−1 | t t t | t−1 t | t t t t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ------- |
no TT pseudoinverse is ever formed. Status after M0.5: the fallback is the method. The anticipated subspace-rotation
error floor (past y projected with old bases U ) did not materialize: the explicit rotation correction G =U+U
|     |     | s   |     |     |     | s   |     |     |     |     |     | t t t−1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
applied to (P,Q) changed results by <5% across all tested regimes, because (i) TT-FOA’s first-order core updates
move the basis very little per step (∥G −I∥ ∼ 10−5–10−3), and (ii) rotating P and Q together is a similarity
t
transform on A˜ = PQ−1 and hence cannot move its eigenvalues except through the interleaving of new updates.
The correction is dropped from the critical path; the residual mismatch enters the bound as a second-order term.
One implementation caveat survives and matters: between re-orthogonalization sweeps U is not orthonormal, and
t
|     |     |     |     |     |     |     |     | U+, | U∗—the |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- |
any projection must use the Gram-corrected pseudoinverse not latter inflates (P,Q) along near-null
|            |     |              |     |            |     |          |          | t   | t   |     |     |     |
| ---------- | --- | ------------ | --- | ---------- | --- | -------- | -------- | --- | --- | --- | --- | --- |
| directions | and | was measured |     | to degrade |     | accuracy | by ∼40×. |     |     |     |     |     |
2. Error accumulation vs. bounded drift. Does the per-step bound of Conjecture 1.1 accumulate over the stream
or stay bounded under a forgetting factor? A stability (non-accumulation) statement is the theoretical headline.
A˜ U∗X′VΣ−1
3. Orthogonality maintenance. = assumes left-orthogonal cores; TT-FOA updates degrade this.
What is the cost/frequency of re-orthogonalization needed to keep the bound valid?
|     |     | λ⋆. | λ⋆  |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
4. Drift-matched Can be expressed in terms of a measurable spectral drift rate and noise level, giving a usable
| tuning | rule rather | than | a grid | search? |     |     |     |     |     |     |     |     |
| ------ | ----------- | ---- | ------ | ------- | --- | --- | --- | --- | --- | --- | --- | --- |
5. When do tensors actually help? Characterize the system class (low-TT-rank / approximately separable fields) for
which streaming TT-DMD beats matrix streaming DMD [7, 26] in memory/compute at fixed accuracy. Status after
M0.5: the form of the answer is measured. With K modes of individual mode-TT-rank ρ, the tracked bond rank
1282
must reach the joint unfolding rank ≈Kρ; the tensor route wins iff Kρ ≪ n i (measured crossover on a grid,
K=8: dominant win at ρ=1, marginal at ρ=4, dominated at ρ=16). This yields the promised a-priori test: estimate
Kρ from a TT-SVD of a warm-up batch before committing to the tensor route. Two refinements remain open: (a)
2

Benchmark Role Primary metric
B1 synthetic validate bounds eigenvalue-error scaling
B2 cylinder demonstrate mem/compute vs. accuracy
B3 PDE scalability wall-clock, TT-rank growth
Table 1: Benchmarks and the job each one does.
sharpen and prove the Kρ rule; (b) the win at small ρ was not only memory (∼14×) but accuracy (∼4×), driven
by sample efficiency—fewer parameters overfit less noise—so the characterization should be stated as a statistical
(estimation-variance) advantage, not merely a compression one. No compute advantage is claimed: at equal rank
the TT step is currently slower (the O(nR2) least-squares for the temporal coefficients dominates); the sketched LS
variant of TT-FOA is the untested lever.
6. Delta vs. Ma–Liu–Wei [19]. Their online TT-DMD appears to use a bespoke update rather than a principled
streaming-TT tracker; confirming this pins down exactly what is novel here.
3 Benchmarks
Benchmarksservetwodistinctjobs: validatingthebounds(controlled,ground-truthspectra)anddemonstratingusefulness
(realistic fields).
Baselines (mandatory in every benchmark). Matrix online DMD with forgetting factor [26] is the primary
baseline—it is the exact matrix analogue of the proposed method, and the central empirical question is when the TT
version beats it in memory/compute at fixed accuracy (open question 5). Secondary baselines: streaming DMD [7], batch
TT-DMD [8] recomputed on a sliding window (accuracy oracle at prohibitive cost), and the online TT-DMD of [19]
wherereproducible. Theproof-of-concept gate (milestoneM0.5)hasbeencompleted with a GO at sharply bounded
scope: at mode-TT-rank ρ=1 the TT frontier dominates the matrix one on memory (∼14×) and accuracy (∼4×);
at ρ=16 the matrix frontier dominates everywhere; no per-step compute advantage exists yet (see open question 5).
Caveats carried forward: single seed per configuration, PAST as the only matrix tracker (an incremental-SVD tracker
may narrow the accuracy gap; the memory gap is structural), synthetic d=2 data only.
Metrics (prescribed by M0.5). The headline metric is the subspace error sinθ between the tracked and true
(or batch-reference) mode span; DMD eigenvalue error is reported but is nearly insensitive to subspace quality (see
Conjecture 1.1) and must never be the sole ranking criterion. Every sweep includes a random-subspace control—a fixed,
untracked injective projection—whose eigenvalue error pins the floor that any eigenvalue-based claim has to clear.
B1 — Synthetic time-varying linear systems (validation). Construct x =A x +w with a known slowly
t+1 t t t
drifting spectrum, so δ and the true λ(t) are exact. Sweep ε , tracker rank r, drift δ , noise, and λ; check that measured
t k tt t
eigenvalue error follows the three-term scaling of Conjecture 1.1 and that the empirical λ⋆ matches the drift-matched
prediction. This is the primary theory-confirmation harness.
B2 — Two-dimensional cylinder wake (demonstration). The von Kármán vortex street is the standard DMD
testbed and was used in the original TT-DMD paper [8]. Step zero, dictated by M0.5: measure the data’s effective
mode-TT-rank ρ (TT-SVD of a batch of snapshots / of the leading POD modes at several tolerances) before anything
else—the PoC shows the tensor route wins only when Kρ ≪ n , so this single number predicts whether B2 is a
i
demonstration or a negative result, and either outcome feeds open question 5. Then two regimes: (i) stationary periodic
shedding, to confirm streaming eigenvalues converge to batch TT-DMD and to plot the memory/compute vs. accuracy
frontier against matrix streaming DMD; (ii) non-stationary (ramped Reynolds number or transient onset of shedding),
to exercise λ and show tracking of a moving spectrum.
B3 — High-dimensional PDE / control (stretch). A reaction–diffusion or advection field on a fine grid where
the tensorized state is plausibly low-TT-rank, echoing the control setting of [19]; used only to probe scalability, not for
tuned accuracy claims.
4 Milestones
Remark 4.1. IfM0revealsthat[19]alreadycontainsanerror/stabilityanalysis, pivotthenoveltytotheTT-FOA-specific
λ⋆ criterion and the low-rank “win” characterization, and position the bound as a comparison rather than a first result.
3

| Wk  | Milestone |     |     |     |     |     |     |     |     |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- |
M0 Verify what [19] already proves/does (read full text); freeze the novelty statement.
M0.5 [DONE — GO at bounded scope.] PoC: TT-FOA + projected-space A˜update vs. matrix online DMD.
Win only atlow mode-TT-rank (Kρ≪n ); sinθ adopted asheadline metric; rotation correction dropped; λ⋆
i
|     | U-shape | confirmed | to move | with | drift. |     |     |     |     |
| --- | ------- | --------- | ------- | ---- | ------ | --- | --- | --- | --- |
M1 Harden the PoC: multiple seeds + error bars (esp. the ρ=4/16 boundary); add an incremental-SVD matrix
|     | baseline; | 3D case; | measure | effective |     | ρ of the | B2 cylinder | data. |     |
| --- | --------- | -------- | ------- | --------- | --- | -------- | ----------- | ----- | --- |
M2 Compute arm: benchmark the sketched-LS variant of TT-FOA (only route to a per-step compute win);
|     | re-orthogonalization |     | period | sweep. |     |     |     |     |     |
| --- | -------------------- | --- | ------ | ------ | --- | --- | --- | --- | --- |
κ(U+B)
M3 Theory: per-step subspace bound + eigenvalue corollary via (Conj. 1.1), then the non-
|     | accumulation/stability |               |                | statement.    |              |     |     |     |     |
| --- | ---------------------- | ------------- | -------------- | ------------- | ------------ | --- | --- | --- | --- |
| M4  | Theory:                | drift-matched |                | λ⋆ criterion. |              |     |     |     |     |
| M5  | B1 validation          |               | sweeps confirm |               | the scalings | and | λ⋆. |     |     |
M6 B2 non-stationary demonstration; mem/compute frontier vs. matrix streaming DMD.
M7 Characterize the low-TT-rank “win” regime (open question 5); write-up.
|     |     | Table | 2:  | Milestones. |     | M3–M4 | are the | spine; | M0 de-risks scooping. |
| --- | --- | ----- | --- | ----------- | --- | ----- | ------- | ------ | --------------------- |
5 Additional directions (brainstorm, not on the critical path)
Streaming TT-SINDy. The same tracker–operator–forgetting framework should transfer to sparse identification
of nonlinear dynamics (SINDy) [3]. SINDy’s bottleneck is the candidate-function library matrix Θ(X), which grows
combinatoriallywiththenumberofcandidateterms;MANDy[4]showedthatstandardlibraries(monomials,trigonometric
dictionaries) admit an exact low-rank TT representation, making TT the natural format for the library. A streaming
version—track the tensorized library with an RLS-type TT tracker and run online sparse regression (e.g. sequential
thresholded least squares with the same forgetting factor λ) on top—appears to be unoccupied territory. Two genuine
research problems distinguish it from a mechanical port and are why it is staged as a follow-up, not folded in here:
(i) the tensorization is structural (function library over state variables) rather than spatial reshaping of a field, so the
low-TT-rankassumptionhasadifferentjustification;and(ii)thesparsitypatterninteractsnontriviallywithforgetting—a
thresholdedsupportthatflickersasλ-weightedcoefficientsdriftisitsownstabilityproblem,arguablytheSINDyanalogue
ofoureigenpair-continuityissue. TheDMDprojectcomesfirstbecauseitsfailuremodesarediagnosablebyeye(spectra);
if the framework and the λ⋆ machinery survive contact with DMD, streaming TT-SINDy is the natural second paper.
| 6 What           | to    | read      | / cite  |     |                   |     |     |     |     |
| ---------------- | ----- | --------- | ------- | --- | ----------------- | --- | --- | --- | --- |
| A staged reading | list; | citations | resolve | in  | the bibliography. |     |     |     |     |
Start here (foundations). DMD theory and the exact-DMD formulation [22, 25] and the textbook [11]; the TT
format [21]; and the paper this whole idea extends, TT-DMD [8]. The recent variants survey [23] gives the lay of the
land.
The streaming/online axis (matrix side). Streaming DMD [7] and, most importantly, time-varying online DMD
with rank-1 updates and a weighting factor [26]—the direct matrix analogue of what we do in TT form—plus the
| incremental | variant | [2]. |     |     |     |     |     |     |     |
| ----------- | ------- | ---- | --- | --- | --- | --- | --- | --- | --- |
The anchor and its neighbours (streaming TT). TT-FOA [13] is the tracker we build on; read alongside its
missing-dataRLSsuccessorATT[14], theadaptive-rankalternativeTT-ICE[1], thestreamingTTapproximationof[10],
the incremental iTTD [18], and the streaming-tensor survey [15] for the full landscape.
Closest prior work (read critically at M0). The online TT-DMD of Ma, Liu and Wei [19] and TT-based
HODMD [17, 16]; the recent tensor-DMD preprint [6] should be checked at M0 for overlap as well. Also EDMD in TT
| form [20] | and HODMD | [12] | for the | higher-order |     | framing. |     |     |     |
| --------- | --------- | ---- | ------- | ------------ | --- | -------- | --- | --- | --- |
For the SINDy follow-up (Section 5). Original SINDy [3] and its TT-format library, MANDy [4]; skim only until
| the DMD | project clears | M0.5. |     |     |     |     |     |     |     |
| ------- | -------------- | ----- | --- | --- | --- | --- | --- | --- | --- |
For the theorems. Convergence of (E)DMD to the Koopman operator [9] for the estimator-consistency side, and
matrix perturbation theory [24] (Bauer–Fike) for propagating operator error to eigenvalue error.
4

| 7 The | M1  | empirical |     | battery: | what |     | was measured |     |     |     |
| ----- | --- | --------- | --- | -------- | ---- | --- | ------------ | --- | --- | --- |
The proof-of-concept gate M0.5 has since been followed by a full multi-seed battery (milestone M1). This section records
its findings; §8 extracts the results that admit proof, and §9 revises the paper’s aims accordingly. The reading that
survives contact with the data is a regime map for streaming TT-DMD, not a claim of TT-FOA supremacy — our own
| numbers | contradict | the latter, | and saying |     | so is one | of the | contributions. |     |     |     |
| ------- | ---------- | ----------- | ---------- | --- | --------- | ------ | -------------- | --- | --- | --- |
Corpus and provenance. 31,659 runs, every one terminating finished (zero failures; the safe_svd gesvd fallback
held across the battery). 55 seeds, 8 grid sizes n∈{4096,...,4194304} (i.e. 642 →20482 plus 323/643/1283), mode-TT-
rank ρ∈{1,2,4,8,16}, and DMD rank points {4,8,16,32,48}. All comparisons below are memory-normalised for the
reason made precise in Proposition 8.2: the raw metric favours whichever tracker carries the larger latent dimension.
The metric is sinθ =sin (︁∠ (U,V) )︁ , the sine of the largest principal angle between the tracked basis U ∈Rn×R and
max
∈Rn×K,
| the true | mode basis | V   | K =8. |     |     |     |     |     |     |     |
| -------- | ---------- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
7.1 Tensor versus matrix baselines: a decisive but bounded win
Best achievable sinθ (min over rank points, median over seeds), by field separability ρ:
|     |     | ρ   | tt-foa  | tt-ice  |         | past | inc-svd | grouse  |     | random-ctrl |
| --- | --- | --- | ------- | ------- | ------- | ---- | ------- | ------- | --- | ----------- |
|     |     | 1   | 1.02e−4 | 6.65e−5 | 2.58e−3 |      | 1.89e−3 | 1.84e−3 |     | 1.00        |
|     |     | 2   | 1.70e−4 | 1.13e−4 | 2.91e−3 |      | 1.98e−3 | 1.85e−3 |     | 1.00        |
|     |     | 4   | 2.66e−4 | 2.05e−4 | 2.75e−3 |      | 1.94e−3 | 1.78e−3 |     | 1.00        |
|     |     | 8   | 4.47e−2 | 4.32e−2 | 2.95e−3 |      | 1.96e−3 | 1.84e−3 |     | 1.00        |
|     |     | 16  | 8.41e−2 | 8.25e−2 | 2.48e−3 |      | 1.94e−3 | 1.80e−3 |     | 1.00        |
The matrix baselines are flat in ρ (≈1.8–2.9e−3 everywhere): they never exploit the separable structure, so they never
lose it. All the ρ-dependence lives on the tensor side. The memory advantage of the smallest TT that still matches the
| best matrix | accuracy | is large | and, crucially, |     | grows with | n:    |      |     |      |     |
| ----------- | -------- | -------- | --------------- | --- | ---------- | ----- | ---- | --- | ---- | --- |
|             |          |          | n               |     | ρ=1        | ρ=2   | ρ=4  | ρ=8 | ρ=16 |     |
|             |          |          | 4,096           |     | 43×        | 21×   | —    | —   | —    |     |
|             |          |          | 16,384          |     | 85×        | 43×   | 21×  | —   | —    |     |
|             |          |          | 65,536          |     | 171×       | 85×   | 43×  | —   | —    |     |
|             |          |          | 262,144         |     | 341×       | 171×  | 85×  | —   | —    |     |
|             |          |          | 1,048,576       |     | 455×       | 341×  | 114× | —   | —    |     |
|             |          |          | 2,097,152       |     | 5783×      | 1966× | 599× | —   | —    |     |
|             |          |          | 4,194,304       |     | 1365×      | 683×  | 341× | —   | —    |     |
For ρ≤4 the tensor route is simultaneously 7–28× more accurate and 21–5783× cheaper in memory, at no wall-clock
cost (§7.4). The “—” entries are the substance of the next subsection: past ρ≈4 the TT cannot reach the target at any
swept rank.
ρ⋆
7.2 The observed break-even ≈ 4, and why it is a budget, not a law
The tensor advantage does not merely shrink with ρ; it inverts. At ρ=8 the TT methods are ≈24× worse than the
best matrix baseline, and at ρ=16, ≈46× worse. The cliff sits between ρ=4 and ρ=8 at every grid size from 4×103
to 4×106 (Fig. 3). It is tempting — and an earlier draft did so — to read this apparent n-independence as a law of the
field’s separability. It is not: the deployed bond-rank sweep is capped at r =48, and since representing the K-mode
rank-ρ subspace needs bond r ≳Kρ (Prop. 8.3(b)), with K =8 the cliff lands at ρ=48/8=6 — which is exactly the
observed split {1,2,4} win vs. {8,16} loss, and it does not move with n only because the cap does not move with n.
Underthematched-memoryprotocolthispaperotherwiseinsistson, theaffordablebondgrowswithn, sothebreak-even
ρ⋆(n) should grow like n(1−1/d)/2: the tensor route’s applicability widens with problem size. The current battery cannot
tell these apart; the decisive experiment (extend the bond sweep at the two largest grids) is prepared but unrun. The
honest headline is thus the growing memory advantage of §7.1, not a fixed cliff.
7.3 TT-FOA versus TT-ICE: the intended headline does not hold
At matched memory the ratio sinθ /sinθ (>1 means TT-FOA wins):
|     |     |     | tt-ice |          | tt-foa |        |          |         |     |     |
| --- | --- | --- | ------ | -------- | ------ | ------ | -------- | ------- | --- | --- |
|     |     |     |        | ρ median | ratio  | TT-FOA | win-rate | budgets |     |     |
|     |     |     |        | 1        | 0.75   |        | 0%       |         | 31  |     |
|     |     |     |        | 2        | 0.85   |        | 25%      |         | 28  |     |
|     |     |     |        | 4        | 1.53   |        | 71%      |         | 31  |     |
|     |     |     |        | 8        | 1.52   |        | 75%      |         | 28  |     |
|     |     |     |        | 16       | 1.37   |        | 77%      |         | 31  |     |
5

Figure 1: Frontier: accuracy versus memory across trackers, grids, and ρ. Tensor methods occupy the low-memory/high-
| accuracy corner | for small ρ | and vacate it | as ρ grows. |
| --------------- | ----------- | ------------- | ----------- |
Figure 2: Memory advantage of the tensor representation at matched accuracy, versus n. The advantage grows with grid
| size, as predicted | by the storage | count of | Proposition 8.3(a). |
| ------------------ | -------------- | -------- | ------------------- |
6

Figure 3: The ρ⋆ break-even. Whether the smallest accurate TT beats the best matrix method flips between ρ=4 and
| ρ=8 at | all eight grid | sizes; the crossover | does | not move with n. |
| ------ | -------------- | -------------------- | ---- | ---------------- |
In the regime where tensors are most useful (ρ∈{1,2}), TT-ICE is the better tensor tracker at essentially every budget,
and it has better peak accuracy at every ρ (previous table). TT-FOA leads only near ρ≈4; its nominal wins at ρ≥8
are hollow, since both TT methods are then an order of magnitude worse than the matrix baselines. TT-FOA’s one
genuine, reproducible edge is reaching a loose target (matrix-baseline accuracy, ≈2e−3) with 1–3.7× less memory than
TT-ICE, because it decouples the bond rank r 1 from the latent R=K. The operating rule is “good enough, as small as
| possible” | → TT-FOA; | “as accurate | as possible” | → TT-ICE. |
| --------- | --------- | ------------ | ------------ | --------- |
Figure 4: TT-FOA vs TT-ICE at matched memory. TT-ICE dominates at low ρ; TT-FOA leads only in a narrow band
near ρ=4.
7.4 Compute: the memory win is free, but there is no compute win
Median per-step time sits within ≈1.3× across all methods at every n (at n=4.19M, ρ=1: grouse 0.75, inc-svd 0.72,
past 0.63, tt-foa 0.61, tt-ice 0.80 ms). The tensor memory advantage therefore costs no wall-clock, but no FLOP-level
advantage exists for any tensor method; any paper text claiming one would be unsupported (Fig. 5).
| 7.5 Where | TT-FOA             | fails:        | mode drift |     |
| --------- | ------------------ | ------------- | ---------- | --- |
| Median    | sinθ by drift type | (2,160 runs): |            |     |
7

Figure 5: Per-step wall-clock across trackers and n. All methods are within a small constant factor; the memory saving
| does not translate | into a compute | saving. |                 |         |                 |
| ------------------ | -------------- | ------- | --------------- | ------- | --------------- |
|                    | drift          | tt-foa  | tt-ice ittd     | past    | inc-svd grouse  |
|                    | eigenvalue     | 7.11e−4 | 4.15e−3 4.15e−3 | 2.71e−3 | 4.34e−3 2.20e−3 |
|                    | mode           | 4.14e−1 | 5.79e−1 1.87e−2 | 1.58e−1 | 8.82e−2 3.11e−1 |
|                    | both           | 4.14e−1 | 5.78e−1 1.94e−2 | 1.58e−1 | 8.81e−2 3.09e−1 |
Under eigenvalue drift TT-FOA is the best method in the battery (3.8× better than PAST): the forgetting factor does
exactly its job. Under mode drift — a rotating spatial subspace — TT-FOA is among the worst, and the adaptive-rank
iTTD beats it by ≈ 22×. The mechanism is structural: a fixed-rank TT basis cannot follow a subspace whose TT
structure is itself moving, and the bond rank that sufficed at t=0 stops sufficing; iTTD’s rank growth is what absorbs
this. The corroborating fixed-rank collapse (exp_consistency, r =R=K) is visible in Fig. 7: at ρ=4 with rank pinned
1
at K, tt-foa, tt-ice and sliding-TT all collapse (≈4.7e−1) while iTTD grows its memory 15× and holds 1.56e−2. Any
| claim for TT-FOA | must be scoped | to stationary | or eigen-drifting | bases. |     |
| ---------------- | -------------- | ------------- | ----------------- | ------ | --- |
Figure 6: Drift battery. Fixed-rank TT trackers track eigenvalue drift well but fail under mode (subspace) drift, where
| adaptive-rank | iTTD dominates. |     |     |     |     |
| ------------- | --------------- | --- | --- | --- | --- |
8

Figure 7: Fixed-rank fragility. At ρ = 4 with the rank pinned at K, fixed-rank TT methods fall off a cliff while the
| adaptive-rank | method | degrades | gracefully. |     |     |     |     |     |
| ------------- | ------ | -------- | ----------- | --- | --- | --- | --- | --- |
7.6 The forgetting factor: a clean U-shape, an unconfirmed law
The error-versus-λ curve is a clean U-shape for both RLS-family trackers, with a robust minimiser (argmin of the
seed-median curve) λ⋆ =0.8 and λ⋆ =0.9 at both deployed drift rates (Fig. 8). TT-FOA is better at its optimum
|     |     | tt-foa |     | past |     |     |       |       |
| --- | --- | ------ | --- | ---- | --- | --- | ----- | ----- |
|     |     |        |     | λ⋆   |     |     | =10−4 | 10−3: |
and prefers a shorter memory. However, did not move between δ and with only two rates and a floor
that is flat over λ∈[0.8,0.9], the “λ⋆ moves with drift” law is not demonstrated. Proposition 8.4 derives the law that
| ought to hold; | the dedicated |     | δ×σ sweep | (E14, | below) | is built | to test it. |     |
| -------------- | ------------- | --- | --------- | ----- | ------ | -------- | ----------- | --- |
Figure 8: Forgetting-factor U-shape. The minimiser is well defined but did not shift measurably between the two
λ⋆(δ/σ)
| deployed drift | rates;         | resolving | the       | law | needs | the finer | E14 grid. |     |
| -------------- | -------------- | --------- | --------- | --- | ----- | --------- | --------- | --- |
| 7.7 A          | methodological |           | confound: |     | the   | warm-up   | budget    |     |
A separate, reusable finding concerns how streaming trackers are compared. Scoring noise amplification at a fixed short
warm-up T 0 =5K conflates the tracker’s transient with its steady state. On the frontier subset (fixed n, ρ, rank), the
apparent ≈6× gap in noise-amplification constant between TT-FOA and TT-ICE at T =5K disappears once warm-up
0
is adequate: the ratio C /C is 1.09 at T =160 and 0.82 at T =240 (at T =40 even PAST is unconverged,
|     |     | tt-ice | tt-foa |     | 0   |     | 0   | 0   |
| --- | --- | ------ | ------ | --- | --- | --- | --- | --- |
C ≈20). The “6× lower noise amplification” reading is thus a warm-up artefact, not a steady-state property; the two
RLS trackers are within ±20% at convergence. The practical consequence — baked into E14 — is that any steady-state
(λ⋆
quantity included) must be measured past the transient, with a bond-adequate warm-up, or ranking conclusions can
invert.
| 8 Theoretical |     | analysis |     |     |     |     |     |     |
| ------------- | --- | -------- | --- | --- | --- | --- | --- | --- |
We use throughout: snapshots X =[x ,...,x ]∈Rn×T and their one-step images Y =[Ax ,...,Ax ] under a linear
|     |     |     |     | 1   | T   |     |     | 1 T |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
operator A; P the orthogonal projector onto a subspace U; M† the Moore–Penrose pseudo-inverse; ∠ the largest
U max
principal angle. “PROVEN” marks a complete argument; “DERIVED” a result contingent on a stated conjecture; each
| carries an | explicit gap | note | where one | remains. |     |     |     |     |
| ---------- | ------------ | ---- | --------- | -------- | --- | --- | --- | --- |
9

| 8.1 | Why | the | eigenvalue |     | metric | is near-vacuous |     | (PROVEN) |     |     |     |     |
| --- | --- | --- | ---------- | --- | ------ | --------------- | --- | -------- | --- | --- | --- | --- |
Proposition 8.1 (Eigenvalue invariance under any injective reduction). Let the snapshots lie in a K-dimensional
A-invariant subspace S =range(B), B ∈Rn×K of full column rank, and set M :=B†AB (the true reduced dynamics).
∈Rn×r,
Assumepersistentexcitation, rank(B†X)=K. LetU r ≥K, be anymatrixforwhichG:=U†B hasfullcolumn
rank K (the generic case: no direction of S lies in kerU†), and form the projected-DMD operator A˜:=(U†Y)(U†X)†.
A˜
Then has exactly K nonzero eigenvalues, equal to those of M; the remaining r−K are zero. In particular the DMD
spectrum is independent of U — and hence of sinθ(U,S): no containment S ⊆range(U) is required.
Proof. Since range(X) ⊆ S = range(B), write X = BC with C = B†X ∈ RK×T; persistent excitation makes C
|     |     |     |     |     |     |     | X   | X   |     |     |     | X   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
full row rank. Invariance gives AB = BM, so Y = AX = BMC . Writing G := U†B, we get U†X = GC and
|     |     |     |     |     |     |     |     | X   |     |     |     | X         |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- |
| U†Y |     |     |     |     |     |     |     |     |     |     |     | )† =C† G† |
=GMC . BecauseG has full column rankK and C has full rowrank K, the reverse-order law (GC
|        |     | X    |         |     |     |     | X   |     |     |     | X   | X   |
| ------ | --- | ---- | ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| holds, | and | C C† | =I , so |     |     |     |     |     |     |     |     |     |
|        |     | X    | K       |     |     |     |     |     |     |     |     |     |
X
|     |     |     |     | A˜=(U†Y)(U†X)† |     | =(GMC  | )(GC     | )† =GMC | C† G† =GMG†. |     |     |              |
| --- | --- | --- | --- | -------------- | --- | ------ | -------- | ------- | ------------ | --- | --- | ------------ |
|     |     |     |     |                |     |        | X X      |         | X X          |     |     |              |
|     |     |     |     | G†G            |     | A˜(Gv) | GM(G†G)v |         |              |     |     | A˜-invariant |
Full column rank of G gives = I K , hence = = G(Mv) for every v: range(G) is
|     | A˜| |     |     |     |     |     |     |     | rank(A˜)≤K, |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- |
and is similar to M via G, so its K eigenvalues are exactly spec(M). As the remaining r−K
range(G)
G=U†B
vanish. The argument never used S ⊆range(U), only that is injective — and U was not assumed orthonormal,
so the statement survives the QR sweeps that leave U non-orthonormal between re-orthogonalisations.
t
Remark 8.1 (Consequence: subspace quality is invisible to the spectrum). In the noise-free, persistently-excited setting
the eigenvalue error is therefore identically zero for every injective reduction — including a random subspace at sinθ =1.
Subspace quality per se does not enter. This corrects a tempting but false explanation (that the random control scores
wellonlybecausethetrueeigenvaluesclusterneartheunitcircleandthemetrichaslittledynamicrange): Proposition8.1
makes the noise-free random control exact even for eigenvalues placed far from the unit circle, so clustering is not the
mechanism. What does enter, once Y =AX is perturbed by noise or drift, is the conditioning κ(G)=κ(U†B), which
amplifies that perturbation into the recovered spectrum. Empirically the random control attains a small-but-nonzero
κ(U†B)=O(1)
eigenvalue error because the runs carry noise σ >0 while for a random U in high dimension (a random
K-frame is near-orthogonal to S yet well-conditioned onto it), so amplification is modest. This is the rigorous basis
for treating sinθ, not eigenvalue error, as the primary object (Conjecture 1.1), and it sharpens Contribution 2: the
| eigenvalue-blindness |     |     | is exact, | not approximate. |                      |     |     |          |     |     |     |     |
| -------------------- | --- | --- | --------- | ---------------- | -------------------- | --- | --- | -------- | --- | --- | --- | --- |
| 8.2                  | Why | raw | sinθ      | must             | be memory-normalised |     |     | (PROVEN) |     |     |     |     |
Proposition 8.2 (Monotonicity of the largest principal angle). Fix a K-dimensional subspace V and two subspaces
U ⊆U′ with dimU ≥K. Then ∠ (U′,V)≤∠ (U,V); equivalently, sinθ is non-increasing as the tracked basis is
|     |     |     |     | max |     | max |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
enlarged.
sin∠
Proof. When dimU ≥ dimV = K, the largest principal angle admits the variational form (U,V) =
max
max ∥(I − P )v∥ (the worst-covered direction of V; see [5]). Nesting U ⊆ U′ gives P ⪰ P , hence
|     | v∈V,∥v∥=1 |     | U   |     |     |     |     |     |     |     | U′  | U   |
| --- | --------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(I−P U′ )⪯(I−P U ) and ∥(I−P U′ )v∥≤∥(I−P U )v∥ for every v. Taking the maximum over unit v ∈V preserves the
inequality.
Because TT-FOA fixes R = K and sweeps only the bond rank, while TT-ICE, iTTD and the matrix trackers take
R=p up to 48, Proposition 8.2 shows the raw metric mechanically favours the large-R methods. Comparing at matched
| memory | removes |     | exactly | this artefact, | which | is why §7 | does so | uniformly. |     |     |     |     |
| ------ | ------- | --- | ------- | -------------- | ----- | --------- | ------- | ---------- | --- | --- | --- | --- |
8.3 Two thresholds: a growing memory win and a budget-dependent break-even
|     | (PROVEN, |     | with | a stated |     | model) |     |     |     |     |     |     |
| --- | -------- | --- | ---- | -------- | --- | ------ | --- | --- | --- | --- | --- | --- |
∏︁d
Proposition 8.3 (Storage growth and the representability break-even). Consider a d-way grid n = n with
|     |     |     |     |     |     |     |     |     |     |     |     | k=1 k |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- |
≍n1/d,
| n k |     | tracking | R modes. |     |     |     |     |     |     |     |     |     |
| --- | --- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
(a) Storage. A dense subspace tracker costs Θ(Rn) scalars. A TT tracker stores all R modes in a single train (the
|     |     |     |     |     |     | (︁  |     | )︁  |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
latent index occupying one core), costing Θ dr2n1/d+r2R at bond ≤r — not Θ(Rn); for large n the spatial term
|     |     |     |     |     |     |     | (︁ Rn1−1/d/(dr2) |     | )︁  |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------- | --- | --- | --- | --- | --- |
dominates. Hence the memory ratio dense:TT is Θ , which diverges as n→∞ for fixed (d,r,R);
√
|     | for d=2 | it  | grows like | R n/(dr2). |     |     |     |     |     |     |     |     |
| --- | ------- | --- | ---------- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
(b) Break-even. Suppose the field has exact mode-TT-rank ρ, so the K-mode basis has TT-rank Θ(Kρ); a bond-r
tracker reaches accuracy target ε only if r ≳Kρ. Two regimes. (i) Fixed budget: if the bond is capped at a constant
r , the break-even is ρ⋆ =Θ(r /K), independent of n — but this is a statement about the sweep budget, not
|     | max |     |     |     | max |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
about the field. (ii) Matched memory (the protocol of §7.1): at a budget equal to the dense Θ(Rn), the affordable
|     |     |     | √︁  |     |     |     |     |     |     | (︁√︁ |     | )︁  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
bond is r ≍ Rn1−1/d/d, which grows with n, so the representability break-even ρ⋆(n)=Θ n1−1/d/(dK) grows
like n(1−1/d)/2. The tensor route’s applicability therefore widens with problem size; there is no fixed cliff.
10

Proof. (a) A tensor train of d cores with external sizes n and bond ranks ≤r stores ∑︁d r n r ≤dr2max n =
|            |     |     |     |     |     | k   |         |     | k=1 k−1 | k k | k k |
| ---------- | --- | --- | --- | --- | --- | --- | ------- | --- | ------- | --- | --- |
| Θ(dr2n1/d) |     |     |     |     |     |     | Θ(r2R); |     |         |     |     |
for the shared spatial cores, plus one latent core of size the R modes share the spatial cores rather
than multiplying them. The dense basis stores Rn. Dividing (spatial term dominating) gives the stated ratio, and
n1−1/d →∞. (b) A tensor of exact TT-rank ρ has exactly ρ nonzero singular values on the unfolding whose rank equals
ρ; a K-mode basis is a sum of K such objects, of TT-rank ≤ Kρ, and truncating below rank Kρ incurs an error at
least the discarded σ (Eckart–Young on that unfolding), a fixed positive constant in n for a generic field. A constant
r+1
cap r max then makes ρ>r max /K unreachable at every n — regime (i). Under matched memory, setting the TT cost
√︁
Θ(dr2n1/d) equal to the dense Θ(Rn) gives the affordable bond r ≍ Rn1−1/d/d, and representability r ≳Kρ yields
√︁
| ρ≲r/K | =Θ( | n1−1/d/(dK)) | —   | regime | (ii). |     |     |     |     |     |     |
| ----- | --- | ------------ | --- | ------ | ----- | --- | --- | --- | --- | --- | --- |
Remark 8.2 (Match to data, and a correction). Part (a) is the measured monotone growth of the memory advantage
(§7.1, Fig. 2); if anything it understates the model, since an earlier count multiplied TT storage by R. Part (b) carries a
ρ⋆
correction the earlier draft got wrong: the measured flat ≈4 was read as an n-independent law, but it is regime (i) in
disguise — the deployed bond sweep is capped at r =48 (FRONT_RANKS), and with K =8 the threshold r ≳Kρ puts
the cliff at ρ = 48/8 = 6, reproducing the observed {1,2,4}-win / {8,16}-loss split at every n precisely because the
cap does not grow with n. The battery therefore cannot distinguish regime (i) from the growing break-even of regime
(ii). Decisive experiment (prepared, not yet run): extend the bond sweep to r ∈{64,96,128} at the two largest
≳64)
grids; regime (ii) predicts ρ=8 (needing r becomes representable and winning, more readily at larger n. Gap to
close. (b) still assumes an exactly rank-ρ field (real fields only approximately so — open question R2, milestone E13)
and a generic unfolding spectrum; the quantitative version replaces the Eckart–Young floor with the field’s actual TT
| singular-value |     | decay.           |     |     |             |     |            |      |     |     |     |
| -------------- | --- | ---------------- | --- | --- | ----------- | --- | ---------- | ---- | --- | --- | --- |
| 8.4            | The | λ⋆ law (DERIVED, |     |     | conditional | on  | Conjecture | 1.1) |     |     |     |
Proposition 8.4 (Drift-matched forgetting). Assume the two λ-dependent terms of the bound in Conjecture 1.1 are
|     |     |     |     |     |     | δ   | √   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
tight, so that near the optimum sinθ(λ) ≃ C + C σ 1−λ, with the drift rate δ and noise level σ; the
|     |     |     |     |     | 3   |     | 4   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
1−λ
λ-independent terms C ε +C η shift the floor but not the minimiser. Then the minimiser is
|     |           | 1 tt | 2   |     |         |       |         |       |     |     |     |
| --- | --------- | ---- | --- | --- | ------- | ----- | ------- | ----- | --- | --- | --- |
|     |           |      |     |     | (︂      | )︂2/3 | (︁      | )︁2/3 |     |     |     |
|     |           |      |     | λ⋆  | = 1 − c | δ     | , c= 2C | /C    |     |     |     |
|     |           |      |     |     |         | σ     |         | 3 4   |     |     |     |
|     | c(δ/σ)2/3 |      |     |     |         |       |         | λ⋆    |     |     |     |
valid while ≤ 1 (otherwise the constraint λ ≥ 0 binds and → 0). Two falsifiable predictions follow: the
exponent is 2/3, and λ⋆ depends on (δ,σ) only through the ratio δ/σ (a data collapse).
√
|     |     |     |     |     |     |     | f′(u) | δu−2+ | 1C σu−1/2, |     |     |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ---------- | --- | --- |
Proof. Put u = 1−λ ∈ (0,1] and f(u) = C 3 δ/u+C 4 σ u. Then = −C 3 4 which vanishes iff
2
u3/2 =2C δ/(C σ), i.e. u⋆ =(2C /C )2/3(δ/σ)2/3; f′′(u)=2C δu−3−1C σu−3/2 >0 at u⋆, so it is the unique interior
|     | 3   | 4   | 3     | 4   |     |     | 3   | 4 4 |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |     | λ⋆  | =1−u⋆ |     |     |     | u⋆  |     |     |     |     |
minimiser. Substituting givestheboxed form; if >1 theobjectiveis monotoneon (0,1] andtheboundary
| u=1 | (λ=0) | is optimal. |     |     |     |     |     |     |     |     |     |
| --- | ----- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Remark 8.3 (Status and test). This is the “usable tuning rule” targeted by open question 4, now written explicitly.
Empirical status: not yet confirmed, arguably in mild tension. The law predicts that lowering δ from 10−3 to
| 10−4 |     | 1−λ⋆ | 102/3 |     | λ⋆  |     |     |     |     | λ⋆  |     |
| ---- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
should raise by ≈4.6, i.e. :0.8→≈0.96; the deployed two-rate slice instead held flat at 0.8–0.9
(§7.6), consistent only within the flat-floor resolution. The dedicated experiment exp_lstar (E14) sweeps five drift rates
against five noise levels on a fine λ grid, with the bond-adequate warm-up mandated by §7.7, and its fit routine reports
the exponent against 2/3 and tests the δ/σ collapse directly. Gap to close. The derivation is exact given the bound
form; establishing that form — the per-step subspace bound of Conjecture 1.1, with the δ/(1−λ) bias term and the
√
σ 1−λ variance term — is the outstanding theorem (milestone M3) and is not proven here.
| 9   | Revised | aims | for | the | SISC submission |     |     |     |     |     |     |
| --- | ------- | ---- | --- | --- | --------------- | --- | --- | --- | --- | --- | --- |
The battery changes what this paper should claim. The original framing implicitly leaned on TT-FOA out-performing
the incremental-TT competitors; §7.3 and §7.5 show that is false as a general statement (TT-ICE wins at ρ∈{1,2} and
on peak accuracy; iTTD wins by ≈22× under mode drift). What survives is stronger and more honest.
Contribution 1 — a regime map for streaming TT-DMD. The load-bearing, proven part is the memory
advantage growing as n1−1/d (Prop. 8.3(a)); the break-even is stated budget-conditionally — ρ⋆ =Θ(r /K) for a fixed
max
sweep, but ρ⋆(n)∼n(1−1/d)/2 under matched memory (Prop. 8.3(b)), so applicability widens with n rather than sitting
ρ⋆
at a fixed cliff (the earlier “n-independent ≈4” claim was a sweep-cap artefact, §7.2). This is decided by the prepared
bond-extension experiment. On top sits a tracker-selection rule stated as a theorem-backed decision, not a benchmark
ranking: TT-FOA for stationary or eigen-drifting low-ρ fields under a memory budget; TT-ICE when accuracy is the
objective; iTTD whenever the spatial basis moves or the rank is unknown a priori. The most conspicuous hole is the
missing iTTD sweep on the accuracy–memory frontier — after §7.5, iTTD is the method a practitioner would default to,
| so its | absence | must be closed | before | submission. |     |     |     |     |     |     |     |
| ------ | ------- | -------------- | ------ | ----------- | --- | --- | --- | --- | --- | --- | --- |
11

Contribution 2 — two evaluation results that invert conclusions. Proposition 8.1 (the eigenvalue metric is
provably blind to subspace quality) and Proposition 8.2 (raw sinθ is provably biased toward large latent R), together
with the warm-up confound of §7.7 (which erased an apparent 6× separation), constitute a compact, rigorous protocol
for comparing streaming decompositions. This is a genuine methodological contribution: three named traps, two of
them proven, each capable of reversing a ranking.
Contribution 3 — the λ⋆ tuning law. Proposition 8.4 gives the explicit λ⋆ =1−c(δ/σ)2/3; E14 decides it. This is
the gate the whole program hinges on — the proposal stages streaming TT-SINDy (§5) as the second paper precisely on
the condition that “the framework and the λ⋆ machinery survive contact with DMD.” If E14 confirms the 2/3 collapse,
the machinery has survived and TT-SINDy is unlocked; if λ⋆ depends on δ and σ separately, that is itself a publishable
characterisation and redirects the theory in M3–M4.
What remains open (and is deliberately staged). The per-step subspace bound (Conjecture 1.1, M3) and the
drift-matched criterion (M4) are the outstanding theorems; Contribution 3 is conditional on the former. The decisive
missing experiment is iTTD on the accuracy–memory frontier (it is the strongest competitor yet was never swept over
rank/memory), followed by the real-data ρ measurement (E13) on which Proposition 8.3(b)’s exact-rank assumption —
and hence the entire tensor case — ultimately rests. The recommended target is SIAM Journal on Scientific Computing:
the combination of an algorithmic regime map, a memory/representability complexity analysis, and a validated tuning
rule is squarely in its scope.
References
[1] Doruk Aksoy, David J. Gorsich, Shravan Veerapaneni, and Alex A. Gorodetsky. “An incremental tensor train
decomposition algorithm”. In: SIAM Journal on Scientific Computing 46.2 (2024), A1047–A1075. doi: 10.1137/
22M1537734.
[2] Mustaffa Alfatlawi and Vaibhav Srivastava. “An incremental approach to online dynamic mode decomposition
for time-varying systems with applications to EEG data modeling”. In: Journal of Computational Dynamics 7.2
(2020), pp. 209–241. doi: 10.3934/jcd.2020009.
[3] Steven L. Brunton, Joshua L. Proctor, and J. Nathan Kutz. “Discovering governing equations from data by sparse
identification of nonlinear dynamical systems”. In: Proceedings of the National Academy of Sciences 113.15 (2016),
pp. 3932–3937. doi: 10.1073/pnas.1517729113.
[4] Patrick Gelß, Stefan Klus, Jens Eisert, and Christof Schütte. “Multidimensional approximation of nonlinear
dynamical systems”. In: Journal of Computational and Nonlinear Dynamics 14.6 (2019), p. 061006. doi: 10.1115/
1.4043148.
[5] Gene H. Golub and Charles F. Van Loan. Matrix Computations. 4th ed. Baltimore: Johns Hopkins University
Press, 2013.
[6] Ziqin He, Mengqi Hu, Yifei Lou, and Can Chen. Tensor dynamic mode decomposition. 2025. doi: 10.48550/arXiv.
2508.02627. arXiv: 2508.02627.
[7] Maziar S. Hemati, Matthew O. Williams, and Clarence W. Rowley. “Dynamic mode decomposition for large and
streaming datasets”. In: Physics of Fluids 26.11 (2014), p. 111701. doi: 10.1063/1.4901016.
[8] Stefan Klus, Patrick Gelß, Sebastian Peitz, and Christof Schütte. “Tensor-based dynamic mode decomposition”.
In: Nonlinearity 31.7 (2018), pp. 3359–3380. doi: 10.1088/1361-6544/aabc8f.
[9] MilanKordaandIgorMezić.“OnconvergenceofextendeddynamicmodedecompositiontotheKoopmanoperator”.
In: Journal of Nonlinear Science 28.2 (2018), pp. 687–710. doi: 10.1007/s00332-017-9423-0.
[10] DanielKressner,BartVandereycken,andRikVoorhaar.“Streamingtensortrainapproximation”.In:SIAM Journal
on Scientific Computing 45.5 (2023), A2610–A2631. doi: 10.1137/22M1515045.
[11] J. Nathan Kutz, Steven L. Brunton, Bingni W. Brunton, and Joshua L. Proctor. Dynamic Mode Decomposition:
Data-Driven Modeling of Complex Systems. Philadelphia, PA: Society for Industrial and Applied Mathematics
(SIAM), 2016. doi: 10.1137/1.9781611974508.
[12] SoledadLeClaincheandJoséM.Vega.“Higherorderdynamicmodedecomposition”.In:SIAM Journal on Applied
Dynamical Systems 16.2 (2017), pp. 882–925. doi: 10.1137/15M1054924.
[13] Thanh Le Trung, Karim Abed-Meraim, Nguyen Linh-Trung, and Rémy Boyer. “Adaptive algorithms for tracking
tensor-traindecompositionofstreamingtensors”.In:Proceedingsofthe28thEuropeanSignalProcessingConference
(EUSIPCO). 2020, pp. 995–999. doi: 10.23919/Eusipco47968.2020.9287780.
[14] Thanh Le Trung, Karim Abed-Meraim, Nguyen Linh-Trung, and Adel Hafiane. “A novel recursive least-squares
adaptive method for streaming tensor-train decomposition with incomplete observations”. In: Signal Processing
216 (2024), p. 109297. doi: 10.1016/j.sigpro.2023.109297.
12

[15] ThanhLeTrung,KarimAbed-Meraim,NguyenLinh-Trung,VietNguyenDuc,andAdelHafiane.“Acontemporary
and comprehensive survey on streaming tensor decomposition”. In: IEEE Transactions on Knowledge and Data
Engineering 35.11 (2023), pp. 10897–10921. doi: 10.1109/TKDE.2022.3230874.
[16] Keqi Li. “Tensor Train Based Higher-Order Dynamic Mode Decomposition: A New Big Data Mining Algorithm in
Energy Networks”. PhD thesis. United Kingdom: The University of Manchester, 2023.
[17] Keqi Li and Sergey Utyuzhnikov. “Tensor train-based higher-order dynamic mode decomposition for dynamical
systems”. In: Mathematics 11.8 (2023), p. 1809. doi: 10.3390/math11081809.
[18] HuazhongLiu,LaurenceT.Yang,YimuGuo,XiaXie,andJianhuaMa.“Anincrementaltensor-traindecomposition
for cyber-physical-social big data”. In: IEEE Transactions on Big Data 7.2 (2021), pp. 341–354. doi: 10.1109/
TBDATA.2018.2867485.
[19] Wei Ma, Chang Liu, and Yimin Wei. “Online Tensor-Based Dynamic Mode Decomposition for Time-Varying
System”. In: Journal of Scientific Computing 108.1 (2026), p. 3. doi: 10.1007/s10915-026-03301-z.
[20] Feliks Nüske, Patrick Gelß, Stefan Klus, and Cecilia Clementi. “Tensor-based computation of metastable and
coherent sets”. In: Physica D: Nonlinear Phenomena 427 (2021), p. 133018. doi: 10.1016/j.physd.2021.133018.
[21] Ivan V. Oseledets. “Tensor-train decomposition”. In: SIAM Journal on Scientific Computing 33.5 (2011), pp. 2295–
2317. doi: 10.1137/090752286.
[22] Peter J. Schmid. “Dynamic mode decomposition of numerical and experimental data”. In: Journal of Fluid
Mechanics 656 (2010), pp. 5–28. doi: 10.1017/S0022112010001217.
[23] PeterJ.Schmid.“Dynamicmodedecompositionanditsvariants”.In:Annual Review of Fluid Mechanics 54(2022),
pp. 225–254. doi: 10.1146/annurev-fluid-030121-015835.
[24] G. W. Stewart and Ji-guang Sun. Matrix Perturbation Theory. Boston: Academic Press, 1990.
[25] JonathanH.Tu,ClarenceW.Rowley,DirkM.Luchtenburg,StevenL.Brunton,andJ.NathanKutz.“Ondynamic
mode decomposition: Theory and applications”. In: Journal of Computational Dynamics 1.2 (2014), pp. 391–421.
doi: 10.3934/jcd.2014.1.391.
[26] Hao Zhang, Clarence W. Rowley, Eric A. Deem, and Louis N. Cattafesta. “Online dynamic mode decomposition
for time-varying systems”. In: SIAM Journal on Applied Dynamical Systems 18.3 (2019), pp. 1586–1609. doi:
10.1137/18M1192329.
13
