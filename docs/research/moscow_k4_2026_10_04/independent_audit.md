# Independent audit of the weighted K4 argument

Date: 2026-10-04. This is an informal mathematical audit by a separately tasked Codex agent, not external human peer review or formal verification. The final argument is in [theorem.md](theorem.md).

## Decision and scope

**PASS** for the universal positive weighted $K_4$ statement with support factor $2+4\cos(\pi/9)$. No gap was found in the compactification, tree-selection dichotomy, Schur complement, or concavity argument. The theorem concerns graphic frames of weighted $K_4$, not arbitrary real $6\times3$ Parseval frames. This audit does not establish novelty or optimality.

## Mathematical checks

1. A maximum-sum spanning tree has the cycle exchange property: every off-tree edge is no heavier than any edge on its fundamental tree path. Replacing a lighter path edge would otherwise increase the sum. Maximum-product trees have the same property. Stars and paths exhaust the tree shapes on four vertices.

2. The star lemma is valid. In the layer-cake integral for $\min(s_i,s_j)$, a clique on $k\le3$ active leaves has Laplacian $kI-J\preceq3I$ on its active coordinates. Integrating proves the required bound by $3\operatorname{diag}(s_i)$ for arbitrary positive spoke weights.

3. For a maximum path with weights $x,y,z$ and chords $a,b,c$, the switch using $\rho=b/z$ has $0<\rho\le1$. In the star centered at the second vertex, the relevant bounds are $a\le\min(x,y)$, $c\le x$ and $c\le z=b/\rho$, and $z=b/\rho\le y/\rho$. Thus every off-tree weight is at most $1/\rho$ times both corresponding spoke weights. The $a/x$ switch is symmetric.

4. The compactification is sound. Normalize the middle path weight to one and write $A=x/y$, $B=z/y$. Increasing chord weights to their permitted maxima increases the nonnegative coefficient matrix entrywise. If $A$ is the smallest parameter below one, increasing it to $\min(B,1)$ keeps $a/A$ and $c/A$ constant and increases every other affected entry. If $A=B<1$, increase them together to one. The argument with $A,B$ interchanged covers the other case. Once $A,B\ge1$, the long chord weight is one. Reducing either parameter above $1/t$ to $1/t$ only increases the corresponding column entries. Intermediate auxiliary matrices need not retain the same maximum tree: they are used solely for entrywise upper bounds.

5. For the proposed squared off-tree norm bound $\lambda$, the leading Schur block is $E=(\lambda-t)I-vv^T$, where $v=(\sqrt p,\sqrt q)^T$. It is positive definite if $\lambda-t>2$. Independently expanding the Schur complement and multiplying by $\lambda-t$ gives

   $$F=\lambda(\lambda-1)-t(\lambda+3)-P-\lambda tR-\frac{(P+2t)^2}{\lambda-t-P},\qquad P=p+q,\quad R=1/p+1/q.$$

6. This $F$ is jointly concave. The reciprocal terms have negative coefficients, and

   $$\frac{d^2}{dP^2}\frac{(P+2t)^2}{\lambda-t-P}=\frac{2(\lambda+t)^2}{(\lambda-t-P)^3}>0.$$

   Therefore its minimum on the rectangle is bounded below by the minimum of its four vertex values. This is the direction required by the proof.

## Chronological parameter checks

The original argument used $t=3/5$, $\lambda=5$ and proved factor six. Its distinct Schur vertex values are $11/5$, $14/5$, and $44/15$.

The first sharpening used $t=5/8$, $\lambda=24/5$, giving the rational support factor $29/5$. Here $\lambda-t-2=87/40>0$, and

$$F(t,t)=\frac{8851}{23400},\qquad F(t,1)=F(1,t)=\frac{14251}{20400},\qquad F(1,1)=\frac{8851}{17400}.$$

All are positive. This remains a convenient rational fallback.

For the final sharpening, let $k$ be the unique root above three of $Q(k)=k^3-3k^2-9k+3$, set $\lambda=k$ and $t=3/k$. The support factor is $1+k=2+4\cos(\pi/9)$. A second reviewer supplied the following identities; this audit verified them independently by exact polynomial denominator clearing:

$$F(t,t)=\frac{(k^2-3)Q(k)}{k(k-3)(k+3)},$$

$$F(1,1)=\frac{(k^2-3)Q(k)}{k(k-3)(k+1)},$$

$$F(t,1)=\frac{(k^2-3)Q(k)}{k(k-3)(k+2)}+\frac{k-3}{k+2}.$$

The relevant root lies in $(19/4,24/5)$: $Q(19/4)=-17/64$, $Q(24/5)=159/125$, and $Q'>0$ for $k>3$. Every denominator and the leading Schur block are positive. The same-coordinate vertices have $F=0$; the mixed vertices have $F=(k-3)/(k+2)>0$. Concavity therefore proves positive semidefiniteness, not necessarily positive definiteness. The resulting path inequality is **non-strict**, as required. The switched-star factor is exactly $1+3/t=1+k$.

## Reproducibility and limits

[verify_analytic.py](verify_analytic.py) uses the Python standard library and exact `Fraction` arithmetic. It checks the rational vertices, 81 rational Schur-identity inputs, the displayed second-derivative polynomial identity, all 16 trees, and all principal minors of $(29/5)L_T-L$ for 40 rational fixtures. All 61 maximum-tree choices arising in those fixtures are checked, covering all four algorithm branches. Its output is [analytic_verification.json](analytic_verification.json).

[verify_sharp_identities.py](verify_sharp_identities.py) checks the three final rational-function identities as polynomial identities, the root-isolation arithmetic, and the cosine polynomial substitution. Its output is [sharp_identities_verification.json](sharp_identities_verification.json).

[exact_family.py](exact_family.py) checks all 16 tree pencils in the symmetric family, the three displayed spectral factorizations, and the identity relating the fourth type to the star polynomial. Its output is [exact_family.json](exact_family.json).

Finite fixture checks do not prove the universal theorem. That conclusion rests on the analytic argument in [theorem.md](theorem.md). The rational Schur grid is an implementation cross-check; the hand expansion establishes the general formula. The symmetric-family calculation and historical numerical exploration establish or suggest separate statements and are unnecessary for the universal proof. No formal verification was performed.
