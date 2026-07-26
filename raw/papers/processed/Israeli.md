Thirteenth International Conference on Domain Decomposition Methods
Editors: N. Debit, M.Garbey, R. Hoppe, J. P´eriaux, D. Keyes, Y. Kuznetsov

c

2001 DDM.org

40 A Hierarchical Domain Decomposition Method with Low
Communication Overhead

M. Israeli1, E. Braverman2, A. Averbuch3

1 Introduction

We present a low communication, non-iterative algorithm for a high order (spectral) solution
of the Poisson equation. The domain is decomposed into nonoverlapping subdomains. Par-
ticular solutions are found in subdomains and subsequently hierarchically matched, such that
only the solution in the adjacent subdomains are coupled at each matching step, then these
steps we
joint subdomains are matched etc. If originally we had (cid:1)(cid:3)(cid:2)(cid:5)(cid:4)
obtain a smooth global solution.

subdomains, after (cid:6)

Implicit discretization of time dependent problems in computational physics, semicon-
ductor device simulation, electromigration and ﬂuid dynamics often gives rise to equations of
Poisson and modiﬁed Helmholtz type. Thus, fast and accurate methods for elliptic equations
are important for such applications.

We solve the Poisson equation

(cid:7)(cid:9)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)

in (cid:24)

or the modiﬁed Helmholtz equation

(cid:7)(cid:25)(cid:8)(cid:27)(cid:26)(cid:29)(cid:28)

(cid:8)(cid:30)(cid:10)(cid:13)(cid:12)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)

in (cid:24)

(cid:10)"!

#$(cid:18)(cid:21)%’&)(*!

#(cid:23)(cid:18)(cid:5)+,&

in the rectangular/square domain (cid:24)

with Dirichlet

(cid:8)(cid:11)(cid:10)(cid:13)-.(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)

on /0(cid:24)

(1)

(2)

(3)

boundary conditions by the Domain Decomposition (DD) methods.

An algorithm for a fast solution of the Poisson equation by decomposition of the domain
into square domains and the subsequent matching of these solutions by the fast multipole
method was developed in [GL96]. Previously [ABI00] we adopted a DD method where the
equation was solved in each subdomain with assumed boundary conditions, resulting in jumps
in function or derivative on subdomain boundaries. The solution in each rectangular domain
is fast and accurate and is based on the algorithm developed in [AIV97, AIV98]. The jumps
at the interfaces were removed by the introduction of singularity layers. In order to account
for the global effect of these layers we had to compute the inﬂuence of each layer on each
subdomain boundary. In order to alleviate this heavy computational task we took into account
the decay or smoothing out of the inﬂuence as a function of the distance from the layer. To

1Technion, Computer Science Dept., Haifa 32000, Israel, israeli@cs.technion.ac.il. The research of the ﬁrst

author was supported by the VPR fund for promotion of research at the Technion.

2Technion, Computer Science Dept., Haifa 32000, Israel, maelena@csd.technion.ac.il; now on leave in Yale

University, Dept. of Math., 10 Hillhouse Ave., New Haven, CT 06520, USA, braverm@cyndra.cs.yale.edu

3Tel Aviv University, School of Math. Sciences, Tel Aviv 69978,Israel, amir@math.tau.ac.il

(cid:0)
(cid:2)
394

ISRAELI,BRAVERMAN,AVERBUCH

reduce the communication load, compression in a multiwavelet basis was applied. Neverthe-
less, this part of the procedure can become expensive as the number of subdomains grows
considerably.

The algorithm developed in [ABI00] consists of the following steps:

(cid:0)(cid:2)(cid:1)(cid:4)(cid:3)

1. In each subdomain a particular solution

of the non-homogeneous equation with

arbitrary Neumann (Dirichlet) boundary conditions is found.

(cid:0)(cid:6)(cid:1)(cid:4)(cid:3)

(cid:18)(cid:8)(cid:7).(cid:10)(cid:10)(cid:9)

(cid:18)(cid:12)(cid:11)(cid:13)(cid:11)(cid:12)(cid:11)

(cid:18)(cid:15)(cid:14)

2. The collection of particular solutions

usually have discontinuities (or
discontinuities in the derivatives) on the boundaries of the subdomains. We introduce
double (single) layers on the boundaries to match the solutions from different domains
to have continuous global solution. The effect of these layers on other boundaries is
calculated.

3. With the boundary conditions that were computed in the previous step, the solutions

(cid:18)(cid:13)(cid:11)(cid:12)(cid:11)(cid:13)(cid:11)

(cid:10)(cid:18)(cid:9)

(cid:18)(cid:19)(cid:14) (cid:18)

(cid:0)(cid:2)(cid:1)(cid:16)(cid:3)

(cid:0)(cid:2)(cid:1)(cid:16)(cid:3)

(cid:18)(cid:17)(cid:7)

are patched by adding the solutions

of the Laplace equation.

4. An additional solution of the Laplace equation is added to satisfy the boundary con-
of the homogeneous

. Namely, for the Dirichlet case the solution

(cid:8)(cid:21)(cid:20)

ditions on /0(cid:24)
equation on the boundary /0(cid:24)

is derived by

(cid:8)(cid:22)(cid:20)

(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)’(cid:10)(cid:13)-.(cid:14)

(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)

(cid:16)(cid:19)(cid:18) (cid:20)(cid:23)(cid:22)(cid:15)(cid:26)*(cid:8)

(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)

(4)

(cid:8)(cid:11)(cid:10)

(cid:5)(cid:8)(cid:23)

(the case with Neumann boundary conditions is treated similarly). Thus

is the solution of the non-homogeneous equation with the initial non-homogeneous

boundary conditions.

The interface jump removal can become cheaper if only adjacent boxes are matched,
which is a basis of the hierarchical approach which is proposed in the present paper. The
present hierarchical approach matching only two adjacent boxes at each level requires only
local corrections at the boundaries of these boxes. The result is a much more efﬁcient com-
putation.

2 Outline of the Algorithm

(cid:2) subdomains; ﬁrst (see
In the new hierarchical approach the domain is decomposed into (cid:6)
Fig. 1) the smallest domains 1,2,3,4 are matched, then they are matched with larger blocks
5,6,7, and, ﬁnally, the resulting box is matched with 8,9,10.

The “elementary step” of the hierarchical algorithm is the following.

1. First, in each of four subdomains some smooth boundary conditions are deﬁned. These
conditions should not contradict the given right hand side, at the junctions. The Poisson
equation is solved with these boundary conditions by a fast spectral algorithm which
takes (cid:24)

is a number of points in each direction).

operations (

(cid:2)(cid:28)(cid:27)(cid:30)(cid:29) (cid:31)

(cid:14)(cid:26)(cid:25)

2. The solutions have a discontinuity in the ﬁrst derivative. We match the subdomains by
adding certain discontinuous functions. In fact we only evaluate these functions at the
boundaries of four adjacent subdomains and then solve homogeneous equations in each
subdomain with the cumulative boundary conditions.

(cid:8)
(cid:5)
(cid:8)
(cid:5)
(cid:18)
(cid:8)
(cid:5)
(cid:8)
(cid:2)
(cid:22)
(cid:26)
(cid:8)
(cid:5)
(cid:14)
(cid:2)
(cid:8)
(cid:8)
(cid:2)
(cid:23)
(cid:8)
(cid:20)
(cid:25)
(cid:22)
(cid:25)
HIERARCHICALDOMAINDECOMPOSITIONMETHOD

395

3. The global homogeneous equation is solved in such a way that it satisﬁes the assumed

conditions at the “global boundaries” of the merged subdomains.

This step is repeated (cid:27)(cid:2)(cid:29)

times, for a smalled number of larger subdomains each time.

8

9

5

3

1

4

2

6

7

10

Figure 1: The domain is decomposed into (cid:6)$(cid:2) subdomains; ﬁrst the smallest domains 1,2,3,4
are matched, then they are matched with larger blocks 5,6,7, and, ﬁnally, the obtained box is
matched with 8,9,10.

The algorithm can be also implemented on parallel multiprocessors. The parallelization of
the serial algorithm is achieved by decomposition of the computational domain into smaller
domains. Each domain is assigned to a processor. The information transmitted between
the processors is the inﬂuences of a function/derivative jumps at the interfaces. of a func-
tion/derivative jumps at the interfaces. The low communication is achieved due to the fast
decay of these inﬂuences and their efﬁcient representation in multiwavelet bases.

For instance, when computing the inﬂuence of the derivative jump in the form of the sum

of random Gaussians

(cid:14) (cid:14)

(cid:26)*(cid:16)

(cid:14)(cid:17)(cid:20)(cid:25)(cid:26)*(cid:20)

(cid:12)(cid:11)

(cid:2)(cid:13)

(cid:15)(cid:14)

(cid:14)(cid:17)(cid:16)

(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)(cid:10)(cid:9)

(cid:2)(cid:1)

at distance 3 we have only 4 (of 256) multiwavelet coefﬁcients above
above

.

(cid:4)(cid:18)

(cid:24)(cid:23)

(cid:19)(cid:18)(cid:21)(cid:20)

(cid:4)(cid:18)(cid:21)(cid:22)

, 7 above

, 15

3 Matching step of the algorithm

The fast and efﬁcient solution of the Poisson/modiﬁed Helmholtz and their homogeneous
analogs was in detail described in [AIV97, AIV98]. Thus we focus here on the matching step
of the algorithm.

(cid:31)
(cid:6)
(cid:5)
(cid:2)
(cid:0)
(cid:4)
(cid:5)
(cid:26)
(cid:4)
(cid:16)
(cid:4)
(cid:22)
(cid:2)
(cid:23)
(cid:4)
(cid:22)
(cid:2)
(cid:22)
(cid:18)
#
(cid:11)
(cid:1)
(cid:11)
(cid:4)
(cid:18)
(cid:9)
#
(cid:9)
#
(cid:9)
#
(cid:5)
396

ISRAELI,BRAVERMAN,AVERBUCH

Let us consider the simplest (“linear”) geometry of the 2-D problem (see Fig. 2) and
present the corresponding steps concerned either with the choice of the initial boundary con-
ditions or with patching jumps between the subdomains.

y

1

0

Box 1

Box 2

Box 3

Box L

1

2

3

L-1

L

x

Figure 2: The domain is decomposed into

subdomains.

Step 1. At the boundary of the global domain we assume the original boundary conditions,

(cid:16)(cid:11)(cid:10)

to avoid singularities at the corners. At the interfaces

we assume

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)

(cid:22)’(cid:10)

(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)

(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)

where

(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)

(cid:22)’(cid:10)

-.(cid:14)(cid:17)(cid:16)

(cid:18)(cid:5)#

-.(cid:14)

(cid:18)(cid:12)(cid:9)

(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:11)(cid:7)

(cid:2)(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:2)(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:28)(cid:19)(cid:14)

(cid:20)(cid:23)(cid:22)(cid:21)(cid:22)

(cid:28)(cid:23)(cid:20)(cid:23)(cid:22)

matches the values at the interfaces with the value at the boundary and

(cid:13)(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)

(cid:22)’(cid:10)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:11)(cid:7)

(cid:12)(cid:15)(cid:14)(cid:17)(cid:16)

(cid:18)(cid:5)#

(cid:22)(cid:15)(cid:26)

-.(cid:14)(cid:17)(cid:16)

(cid:18)(cid:5)#

(cid:22) (cid:28)

(cid:20)(cid:23)(cid:22) (cid:22)

(cid:20)(cid:23)(cid:22)(cid:21)(cid:22)

(cid:12)(cid:15)(cid:14)

(cid:18)(cid:13)(cid:9)

-.(cid:14)(cid:17)(cid:16)

(cid:18)(cid:13)(cid:9)

(cid:22) (cid:28)

(cid:20)(cid:23)(cid:22)

(cid:20)(cid:23)(cid:22)

(cid:1)(cid:9)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:13)(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:26)(cid:29)(cid:28)

(5)

(6)

(7)

to satisfy the Poisson equation at the corners of the interfaces. The latter function vanishes at

#(cid:23)(cid:18)(cid:13)(cid:9)

(cid:16)(cid:11)(cid:10)

(cid:18) (cid:20)

.

Step 2. We solve the Poisson equation with the prescribed (at the ﬁrst step) boundary

conditions. There is a jump of the ﬁrst derivative at the interfaces

(cid:16)(cid:15)

(cid:14)(cid:17)(cid:16)

(cid:18)(cid:21)(cid:20)

(cid:18) (cid:20)(cid:23)(cid:22)’(cid:10)

(cid:31)(cid:14)(cid:17)(cid:20)(cid:23)(cid:22)

Since the original boundary conditions are smooth, then
a function

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:15)(cid:11)(cid:18)

(cid:19)(cid:1)(cid:9)(cid:3)(cid:6)(cid:5)

(cid:13)(cid:15)

(cid:31)(cid:14)

#(cid:3)(cid:22)

(cid:31)(cid:14)(cid:16)(cid:9)

(8)

. After subtracting

(cid:14)(cid:16)(cid:9)

(cid:20)(cid:23)(cid:22)

(cid:20)(cid:23)(cid:22)

(cid:20)(cid:14)

(cid:22)’(cid:10)

(cid:1)(cid:9)(cid:3)(cid:6)(cid:5)

(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)

(cid:26)(cid:29)(cid:28)

(9)

%
(cid:16)
(cid:23)
(cid:18)
#
(cid:0)
(cid:20)
(cid:0)
(cid:9)
(cid:23)
(cid:8)
(cid:5)
(cid:23)
(cid:22)
(cid:23)
(cid:8)
(cid:2)
(cid:23)
(cid:18)
(cid:8)
(cid:5)
(cid:23)
(cid:23)
(cid:22)
(cid:14)
(cid:9)
(cid:26)
(cid:14)
(cid:28)
(cid:22)
(cid:23)
(cid:16)
(cid:23)
(cid:22)
(cid:14)
(cid:14)
(cid:28)
(cid:22)
(cid:8)
(cid:2)
(cid:23)
(cid:23)
(cid:23)
(cid:2)
(cid:28)
(cid:2)
(cid:5)
(cid:26)
(cid:28)
(cid:2)
(cid:2)
(cid:22)
(cid:12)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:9)
(cid:26)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:14)
(cid:9)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:22)
(cid:14)
(cid:23)
(cid:16)
(cid:23)
(cid:22)
(cid:26)
(cid:23)
(cid:2)
(cid:28)
(cid:2)
(cid:5)
(cid:2)
(cid:2)
(cid:22)
(cid:12)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:14)
(cid:28)
(cid:2)
(cid:22)
(cid:14)
(cid:16)
(cid:23)
(cid:10)
/
(cid:8)
/
(cid:16)
(cid:23)
(cid:23)
(cid:22)
(cid:26)
/
(cid:8)
/
(cid:16)
(cid:14)
(cid:16)
(cid:23)
(cid:26)
(cid:11)
(cid:15)
(cid:10)
(cid:22)
(cid:10)
#
(cid:17)
(cid:14)
(cid:20)
(cid:18)
(cid:22)
(cid:28)
(cid:2)
(cid:5)
(cid:2)
(cid:2)
(cid:12)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:14)
(cid:28)
(cid:2)
(cid:22)
HIERARCHICALDOMAINDECOMPOSITIONMETHOD

397

(cid:31)(cid:14)(cid:17)(cid:20)(cid:23)(cid:22)

vanishes at

for
the fourth and higher even derivatives can be also eliminated by an analogous procedure)

together with its second derivative. A similar function is subtracted
can be accurately expanded into the sine series (in fact,

. Then the remaining part

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:31)(cid:14)(cid:17)(cid:20)(cid:23)(cid:22)

(cid:20)(cid:23)(cid:22)

(cid:3)(cid:2)

Then, after adding to the solution to the left of

(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)

(cid:1)(cid:4)(cid:7)

(cid:16)(cid:11)(cid:10)

(cid:19)(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:11)(cid:7)

the following function

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:14)(cid:16)(cid:9)

(cid:5)(cid:4)

(cid:14)(cid:17)(cid:16)(cid:27)(cid:26)

(cid:22) (cid:22)

(cid:26)*(cid:16)

(cid:22)(cid:21)(cid:22)

(cid:20)(cid:23)(cid:22)

(cid:1)(cid:4)(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:1)(cid:9)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:6)(cid:5)

(cid:1)(cid:9)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:5)(cid:4)

(cid:16)(cid:27)(cid:26)*(cid:16)

(cid:22)(cid:21)(cid:22)

(cid:14)(cid:16)(cid:9)

(cid:26)*(cid:20)(cid:23)(cid:22) (cid:22)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:8)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:26)(cid:29)(cid:28)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)(cid:11)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:26)*(cid:16)

(cid:22)(cid:21)(cid:22)

(cid:14)(cid:16)(cid:9)

(cid:26)*(cid:20)(cid:23)(cid:22) (cid:22)

(cid:1)(cid:9)(cid:7)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:1)(cid:9)(cid:3)(cid:10)(cid:5)

(cid:1)(cid:4)(cid:7)

(cid:6)(cid:2)

(cid:3)(cid:2)

(cid:20)(cid:23)(cid:22)

%(cid:29)(cid:26)*(cid:16)

(cid:22) (cid:22)

(cid:1)(cid:4)(cid:7)

(cid:6)(cid:2)

(cid:16)*(cid:10)

(10)

(11)

(cid:23) ) to the right of this axis, we obtain a function
and a symmetric (with respect to axis
which is smooth together with its ﬁrst derivative. Besides, the function which we add decays
exponentially with the growth of the distance from

(cid:23) .

(cid:16)(cid:11)(cid:10)

4 Numerical Results

Assume that
use the following measures to estimate the errors:

is the exact solution and

is the computed solution. In the examples we will

(cid:7)(cid:9)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:14)(cid:16)(cid:15)

0(cid:26)*(cid:8)

(cid:7)(cid:9)(cid:8)(cid:20)(cid:19)(cid:22)(cid:21)

(cid:7)&%

 (cid:31)"!

(cid:3)#

(cid:24)(cid:11)(cid:25)

(cid:26)(cid:28)(cid:27)(cid:30)(cid:29)

 (cid:31)"!

(cid:26)(cid:28)(cid:27)(cid:30)(cid:29)

(cid:24)(cid:11)(cid:25)

(cid:26) (cid:27)((cid:29)

4.1 Linear geometry

We assume the geometry of Fig. 2 where the domain is decomposed in one dimension only.

(cid:7)(cid:25)(cid:8)

Example 1. We solve the Poisson equation

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)0(cid:18)

*)

(cid:22)’(cid:10)

#(cid:23)(cid:18)(cid:12)(cid:9)

conditions corresponding to the exact solution
which is divided into three equal boxes.

with the boundary

&(cid:19)(

#$(cid:18)

*+

in the domain

-,

-.

(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

/+

in each box

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

4.1e-7
2.9e-8
2.0e-9
1.3e-10
8.5e-12

1.2e-7
8.2e-9
5.4e-10
3.5e-11
2.2e-12

2.1e-7
1.4e-8
9.2e-10
5.9e-11
3.8e-12

46587

(cid:22)(cid:15)(cid:10)

, MSQ and 9

(cid:2) errors for the Poisson equation with the exact solution

for three boxes

Table 1:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)0(cid:18)

*)

(cid:15)
(cid:20)
(cid:10)
(cid:9)
(cid:20)
(cid:10)
#
(cid:0)
(cid:15)
(cid:0)
(cid:15)
(cid:10)
(cid:0)
(cid:1)
(cid:4)
(cid:14)
(cid:6)
(cid:16)
(cid:23)
(cid:15)
(cid:18)
(cid:18)
(cid:22)
(cid:1)
(cid:14)
(cid:28)
(cid:2)
(cid:5)
(cid:26)
(cid:28)
(cid:2)
(cid:2)
(cid:22)
(cid:12)
(cid:29)
(cid:14)
(cid:28)
(cid:5)
(cid:16)
(cid:23)
(cid:23)
%
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
%
(cid:22)
(cid:14)
(cid:28)
(cid:5)
(cid:20)
(cid:22)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:14)
(cid:16)
(cid:23)
(cid:23)
%
(cid:4)
(cid:29)
(cid:14)
(cid:28)
(cid:2)
%
(cid:22)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:14)
(cid:23)
(cid:15)
(cid:18)
(cid:18)
(cid:14)
#
(cid:22)
(cid:1)
(cid:14)
(cid:28)
(cid:2)
(cid:5)
(cid:2)
(cid:2)
(cid:22)
(cid:12)
(cid:29)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:23)
(cid:23)
%
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
%
(cid:22)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:26)
(cid:14)
(cid:28)
(cid:2)
(cid:14)
(cid:16)
(cid:23)
(cid:23)
%
(cid:4)
(cid:29)
(cid:14)
(cid:28)
(cid:2)
%
(cid:22)
(cid:14)
(cid:28)
(cid:5)
(cid:14)
(cid:28)
(cid:5)
(cid:22)
(cid:14)
(cid:23)
(cid:9)
(cid:1)
(cid:2)
(cid:6)
(cid:4)
(cid:29)
(cid:14)
(cid:6)
%
(cid:22)
(cid:0)
(cid:1)
(cid:4)
(cid:14)
(cid:6)
(cid:4)
(cid:29)
(cid:14)
(cid:6)
(cid:14)
(cid:23)
(cid:23)
(cid:16)
(cid:16)
(cid:16)
(cid:8)
(cid:8)
(cid:18)
(cid:10)
(cid:5)
(cid:17)
(cid:8)
(cid:18)
(cid:18)
(cid:18)
(cid:17)
(cid:10)
(cid:23)
(cid:0)
(cid:26)
(cid:18)
(cid:31)
(cid:26)
(cid:3)
$
#
(cid:10)
’
(cid:24)
(cid:25)
(cid:0)
(cid:26)
(cid:18)
(cid:31)
(cid:26)
(cid:3)
#
(cid:31)
#
(cid:26)
(cid:10)
(cid:26)
(cid:1)
(cid:4)
(cid:29)
(cid:1)
(cid:16)
(cid:4)
(cid:29)
(cid:1)
(cid:20)
(cid:4)
(cid:29)
(cid:1)
(cid:16)
(cid:4)
(cid:29)
(cid:1)
(cid:20)
!
!
&
(cid:25)
(
(cid:25)
(cid:7)
(cid:7)
#
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
3
(cid:9)
(cid:1)
(
3
(cid:9)
(cid:1)
(cid:4)
(cid:29)
(cid:1)
(cid:16)
(cid:4)
(cid:29)
(cid:1)
(cid:20)
398

ISRAELI,BRAVERMAN,AVERBUCH

Example 2. We solve the Poisson equation with boundary conditions corresponding to the
exact solution

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)’(cid:10)

(cid:26)*(cid:16)

(cid:5)(cid:14)

(cid:14)(cid:17)(cid:20)

(cid:12)(cid:11)

(cid:10)(cid:18)(cid:9)

(cid:18))(cid:20)

(cid:29)(cid:10)

#$(cid:18)

#$(cid:18)(cid:12)(cid:9)

(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

*+

(cid:2)(cid:1)

(cid:4)(cid:3)(cid:6)(cid:5)

3 ,

in the domain

which is divided into three equal

with
boxes.

/+

in each box

(cid:7)(cid:9)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:7)(cid:9)(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

6.8e-6
3.9e-7
2.3e-8
1.4e-9
8.7e-11

2.0e-6
1.1e-7
6.6e-9
4.0e-10
2.4e-11

4.4e-6
2.4e-7
1.4e-8
8.5e-10
5.2e-11

Table 2:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)’(cid:10)

46587

, MSQ and 9

(cid:9) (cid:11)

(cid:2) errors for the Poisson equation with the exact solution

 (cid:11)

4.2 Hierarchical subdomains matching

3

1

4

2

Figure 3: The domain is decomposed into four subdomains

In examples 3, 4 the global subdomain was decomposed into four subdomains (see Fig. 3).
In the practical implementation ﬁrst two pairs of adjacent subdomains were matched: box 1
and 2, box 3 and 4. Afterwards the two resulting boxes were patched. This is also valid for
examples 5,6 with 16 subdomains, where each four subdomains were matched in the same
way.

Example 3. We solve the Poisson equation with boundary conditions corresponding to the
exact solution

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)’(cid:10)

(cid:26)*(cid:16)

(cid:14)(cid:17)(cid:20)

(cid:12)(cid:11)

(cid:18))(cid:20)

#$(cid:18)(cid:12)(cid:9)

&(cid:31)(*!

#(cid:23)(cid:18)(cid:13)(cid:9)

(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:4)(cid:3)(cid:6)(cid:5)

with

3 ,

in the domain

divided into four equal boxes.

(cid:0)
(cid:26)
(cid:16)
(cid:23)
(cid:22)
(cid:2)
(cid:23)
(cid:26)
(cid:20)
(cid:23)
(cid:22)
(cid:2)
(cid:18)
(cid:16)
(cid:23)
(cid:11)
3
(cid:23)
(cid:10)
#
(cid:11)
(cid:11)
(cid:1)
!
&
(
!
&
(cid:25)
,
(
(cid:25)
.
#
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
3
(cid:9)
(cid:1)
(
3
(cid:9)
(cid:1)
(cid:3)
(cid:5)
(cid:7)
(cid:9)
(cid:26)
(cid:1)
(cid:14)
(cid:16)
(cid:26)
3
(cid:22)
(cid:2)
(cid:23)
(cid:1)
(cid:14)
(cid:20)
(cid:26)
#
(cid:11)
3
(cid:22)
(cid:2)
(cid:13)
(cid:0)
(cid:26)
(cid:1)
(cid:14)
(cid:16)
(cid:23)
(cid:22)
(cid:2)
(cid:23)
(cid:26)
(cid:20)
(cid:23)
(cid:22)
(cid:2)
(cid:18)
(cid:16)
(cid:23)
(cid:10)
#
(cid:11)
3
(cid:23)
(cid:10)
#
(cid:11)
(cid:11)
(cid:10)
(cid:1)
!
&
HIERARCHICALDOMAINDECOMPOSITIONMETHOD

399

in each subdomain

(cid:7)(cid:22)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:7)(cid:9)(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

1.7e-4
1.3e-5
1.2e-6
1.0e-7
8.0e-9
6.1e-10

5.1e-5
3.6e-6
3.5e-7
2.8e-8
2.0e-9
1.4e-10

7.1e-5
4.9e-6
4.7e-7
3.7e-8
2.7e-9
1.9e-10

/+

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

Table 3:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)’(cid:10)

46587

, MSQ and 9

(cid:26)(cid:29)#

(cid:14)(cid:21)(cid:14)(cid:17)(cid:16)

(cid:2) errors for the Poisson equation with the exact solution

(cid:14)(cid:17)(cid:20)(cid:25)(cid:26)(cid:29)#

&)((cid:29)!

#$(cid:18)(cid:12)(cid:9)

#(cid:23)(cid:18)(cid:12)(cid:9)

 (cid:11)

(cid:2)(cid:13)

in the domain

Table 4 presents the results for the same exact solution when the Dirichlet problem is

&(cid:19)((cid:29)!

#$(cid:18)

#(cid:23)(cid:18)

solved in the square

.

in each subdomain

(cid:7)(cid:22)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:7)(cid:9)(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

3.5e-3
1.7e-4
8.3e-6
4.4e-7
2.5e-8
1.5e-9

1.2e-3
5.7e-5
2.5e-6
1.2e-7
6.5e-9
3.8e-10

3.1e-3
1.4e-4
6.1e-6
2.9e-7
1.6e-8
9.4e-10

/+

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

Table 4:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)’(cid:10)

46587

, MSQ and 9

(cid:26)(cid:29)#

(cid:14)(cid:21)(cid:14)(cid:17)(cid:16)

(cid:2) errors for the Poisson equation with the exact solution

(cid:14)(cid:17)(cid:20)(cid:25)(cid:26)(cid:29)#

&(cid:19)(*!

#$(cid:18)

#(cid:23)(cid:18)

in the domain

Example 4. The exact solution is a steep Gaussian

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)’(cid:10)

(cid:26)(cid:29)#

(cid:14)(cid:17)(cid:20)(cid:9)(cid:26)*#

(cid:3)(cid:22)

(cid:3)(cid:6)(cid:5)(cid:8)(cid:7)

(cid:4)(cid:3)(cid:6)(cid:5)

Table 5 presents the numerical errors.

-,

-.

(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

in each subdomain

/+

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

1.9e-2
4.9e-4
1.1e-5
3.0e-7
1.1e-8
4.7e-10

4.4e-3
9.1e-5
2.1e-6
6.0e-8
1.9e-9
6.4e-11

2.4e-2
4.9e-4
1.1e-5
3.2e-7
1.0e-8
3.5e-10

Table 5:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)’(cid:10)

46587

, MSQ and 9

(cid:26)(cid:29)#

(cid:14) (cid:14)

(cid:2) errors for the Poisson equation with the exact solution

(cid:14)(cid:17)(cid:20)(cid:9)(cid:26)*#

&)(*!

#$(cid:18)

#(cid:23)(cid:18)

(cid:3)(cid:22)

 (cid:11)

(cid:2)(cid:13)

in the domain

(cid:25)
,
(
(cid:25)
.
#
2
(
2
(cid:9)
0
(
(cid:9)
0
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
(cid:3)
(cid:5)
(cid:7)
(cid:9)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:23)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:22)
!
&
!
(cid:1)
(cid:1)
&
(cid:25)
,
(
(cid:25)
.
#
2
(
2
(cid:9)
0
(
(cid:9)
0
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
(cid:3)
(cid:5)
(cid:7)
(cid:9)
(cid:26)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:23)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:22)
(cid:13)
!
(cid:1)
(cid:1)
&
(cid:0)
(cid:26)
(cid:9)
#
(cid:1)
(cid:14)
(cid:16)
(cid:11)
(cid:1)
(cid:22)
(cid:2)
(cid:23)
(cid:11)
+
(cid:2)
(cid:11)
(cid:25)
(
(cid:25)
(cid:7)
(cid:7)
#
2
(
2
(cid:9)
0
(
(cid:9)
0
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
(cid:3)
(cid:5)
(cid:7)
(cid:9)
(cid:26)
(cid:9)
#
(cid:16)
(cid:11)
(cid:1)
(cid:22)
(cid:2)
(cid:23)
(cid:1)
(cid:11)
+
(cid:2)
(cid:22)
!
(cid:1)
(cid:1)
&
400

ISRAELI,BRAVERMAN,AVERBUCH

3c

3d

4c

4d

3a

1c

1a

3b

4a

4b

1d

1b

2c

2d

2a

2b

Figure 4: The domain is decomposed into sixteen subdomains

The domain is decomposed into sixteen subdomains which are hierarchically matched
(see Fig. 4): ﬁrst each four small boxes and then the resulting four “big” (joint) boxes. Such
domain decomposition was implemented in Example 5.

Example 5. We solve the Poisson equation with the boundary conditions corresponding to
the exact solution

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:31)(cid:18) (cid:20)(cid:23)(cid:22)

(cid:21)(cid:14)(cid:17)(cid:16)

(cid:26)(cid:29)#

(cid:14)(cid:17)(cid:20)(cid:25)(cid:26)(cid:29)#

#$(cid:18)(cid:12)(cid:9)

&(cid:19)(*!

#(cid:23)(cid:18)(cid:13)(cid:9)

(cid:5)(cid:8)(cid:7)

in the domain

divided into sixteen equal boxes (Table 6).

in each subdomain

(cid:7)(cid:22)(cid:8)(cid:11)(cid:10)(cid:13)(cid:12)

(cid:7)(cid:9)(cid:8)(cid:20)(cid:19)((cid:21)

(cid:7)&%

/+

0&1

0(cid:9)1

&2

(cid:9)2

(cid:9)3

(cid:9)3

3.6e-4
2.4e-5
2.3e-6
1.9e-7
1.5e-8
1.1e-9
8.3e-11

1.6e-4
1.0e-5
9.6e-7
8.0e-8
6.1e-9
4.5e-10
3.3e-11

2.2e-4
1.4e-5
1.3e-6
1.1e-7
8.2e-9
6.0e-10
4.4e-11

Table 6:

(cid:8)(cid:15)(cid:14)(cid:17)(cid:16)(cid:19)(cid:18)(cid:21)(cid:20)(cid:23)(cid:22)’(cid:10)

46587

, MSQ and 9

(cid:26)(cid:29)#

(cid:14)(cid:21)(cid:14)(cid:17)(cid:16)

(cid:2) errors for the Poisson equation with the exact solution

(cid:14)(cid:17)(cid:20)(cid:25)(cid:26)(cid:29)#

&(cid:19)(*!

#$(cid:18)(cid:12)(cid:9)

#(cid:23)(cid:18)(cid:13)(cid:9)

in the domain

5 Summary

1. The procedure developed here reduces drastically (by a factor of (cid:24)

times)
the number of computations as compared to our previous algorithm where inﬂuences of
the layers at interfaces are evaluated.

(cid:27)(cid:2)(cid:29)

(cid:10)
(cid:3)
(cid:0)
(cid:26)
(cid:1)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:23)
(cid:11)
3
(cid:22)
(cid:2)
(cid:3)
(cid:5)
!
&
(cid:25)
,
(
(cid:25)
.
#
1
(
1
2
(
2
(cid:9)
0
(
(cid:9)
0
+
(cid:1)
(
(cid:1)
(
(cid:9)
(cid:1)
(
(cid:9)
(cid:1)
(cid:1)
0
(
(cid:1)
0
(cid:3)
(cid:5)
(cid:7)
(cid:9)
(cid:26)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:23)
(cid:1)
(cid:11)
3
(cid:22)
(cid:2)
(cid:22)
(cid:13)
!
&
(cid:14)
(cid:6)
(cid:2)
(cid:0)
(cid:31)
(cid:6)
(cid:22)
HIERARCHICALDOMAINDECOMPOSITIONMETHOD

401

2. The algorithm has an adaptive DD version and also achieves high accuracy (

0(cid:9)1

0(cid:9)1

(cid:8)(cid:18)(cid:21)(cid:22)

for

points in the smallest subdomains).

3. The algorithm is applicable for parallel implementation as its previous version devel-

oped in [ABI00].

4. This algorithm can be used as a preconditioner for the solution of elliptic equations with
nonconstant coefﬁcients by solving local constant coefﬁcient problems in subdomains.

5. The present algorithm is close to a multigrid strategy, where the discretization points
are replaced by the small boxes in where the equation is satisﬁed with spectral accuracy
which is preserved in the ﬁnal solution.

References

[ABI00]Amir Averbuch, Elena Braverman, and Moshe Israeli. Parallel adaptive solution of a

Poisson equation with multiwavelets. SIAM J. Sci. Comput., 22(3):1053–1086, 2000.

[AIV97]Amir Averbuch, Moshe Israeli, and Lev Vozovoi. On fast direct elliptic solver by

modiﬁed Fourier method. Numer. Algorithms, 15:287–313, 1997.

[AIV98]Amir Averbuch, Moshe Israeli, and Lev Vozovoi. A fast Poisson solver of arbitrary

order accuracy in rectangular regions. SIAM J. Sci. Comput., 19:933–952, 1998.

[GL96]Leslie Greengard and June-Yub Lee. A direct adaptive Poisson solver of arbitrary

order accuracy. J. Comput. Phys., 125:415–424, 1996.

(cid:9)
#
(cid:18)
(cid:0)
(cid:26)
(cid:9)
#
(

