ThirteenthInternationalConferenceonDomainDecompositionMethods
Editors:N.Debit,M.Garbey,R.Hoppe,J.Pe´riaux,D.Keyes,Y.Kuznetsov c
(cid:0)
2001DDM.org
6 Domain decomposition and fictitious domain methods
with distributed Lagrange multipliers
Yu.A.Kuznetsov1
Introduction
InthispaperweconsiderthreeapplicationsofthedistributedLagrangemultipliertechnique
[DGH
(cid:1)
92,GHJ
(cid:1)
97,GK98]todesignnewdomaindecompositionandfictitiousdomainmeth-
odsforthediffusionequation
(cid:2)(cid:4) (cid:3)(cid:6) (cid:5)(cid:8) (cid:7)(cid:9) (cid:3)(cid:11) (cid:10)(cid:13) (cid:12)(cid:15) (cid:14)(cid:17) (cid:16)(cid:19) (cid:18) (cid:20)(cid:22) (cid:21)(cid:24) (cid:23)(cid:25) (cid:18)
(1)
inabounded2D/3DpolygonaldomainwiththehomogeneousDirichletboundarycondition
(cid:10)(cid:6) (cid:14)(cid:27) (cid:26)(cid:28) (cid:18) (cid:20)(cid:22) (cid:21)(cid:30) (cid:29)(cid:13) (cid:23)(cid:25) (cid:18)
(2)
andapiece-wiseconstantdiffusioncoefficient
(cid:7)
.
Theaboverestrictionsareimposedforthesakeofsimplicity. Thegeneralizationsofthe
algorithms and theoretical results to more complicated equations, domains, and boundary
conditionsareobvious.
Let
(cid:23) (cid:31)
be a triangular/tetrahedralpartitioning of
(cid:23)
, and
! (cid:31)
be thecorresponding piece-
wiselinearfiniteelementsubspaceof
"$ %# (cid:5)(cid:8) (cid:23) (cid:12)
. Weshallalwaysassumeinthispaperthat
(cid:23)(cid:4) (cid:31)
isashape-regularmesh. Thentheclassicalfiniteelementmethod
(cid:10)
(cid:31)
(cid:21) ! (cid:31)(cid:15) & (cid:7)’ (cid:5)( (cid:10)(cid:13) (cid:31)(cid:28) (cid:18)(cid:28) )(cid:9) (cid:12)(cid:15) (cid:14)(cid:27) *+ (cid:5)( )(cid:9) (cid:12) ,(cid:19) )- (cid:21) ! (cid:31)
(3)
where (cid:7)’ (cid:5)( (cid:10). (cid:18)(cid:9) )(cid:9) (cid:12)/ (cid:14)(cid:27) 0
1
(cid:7)2 (cid:3)3 (cid:10)- 45 (cid:3)3 )7 6(cid:9) (cid:20)
and
*8 (cid:5)( )(cid:9) (cid:12)(cid:15) (cid:14)9 0
1
(cid:16)(cid:19) )/ 6(cid:9) (cid:20): (cid:18)
resultsinthesystemoflinearalgebraicequations
;= <
(cid:10)(cid:30) (cid:14)
<
(cid:16)
(4)
withasymmetricpositivedefinitematrix
;
(cid:21)(cid:22) >@ ?B A(cid:28) ?
,
C (cid:14)D 6(cid:9) EGF ! (cid:31)
,andavector
<
(cid:16)H (cid:21)I >J ?
. We
alsodenoteby
K
themassmatrixandby
K L
thelumpedmassmatrix,i.e.
K L
isdiagonaland K
<
M (cid:14) K L
<
M
,
<
M5 N (cid:14)O (cid:5)Q PR (cid:18)T SU ST SV (cid:18)U PW (cid:12)
,
<
M (cid:21)(cid:24) >J ?
.
For
(cid:23)
#Y
(cid:31)
X
and
(cid:23) Z (cid:31)
X
beingnon-overlappingsubdomainsof
(cid:23)(cid:4) (cid:31)
suchthat
(cid:23) (cid:31)(cid:11) (cid:14)D (cid:23)
#Y
(cid:31)/
X
[\ (cid:23)J Z (cid:31)
X
,
wedenoteby
;
#
and
;
Z
thecorrespondingstiffnessmatricesandby
K
#
(cid:5) K L
#
(cid:12)
and
K Z] (cid:5) K L ZU (cid:12)
thecorrespondingmass(lumpedmass)matrices.Thematrices
;
,
K
and
K L
canbeintroduced
bysubassemblingofmatrices
;(cid:25) ^
,
K
^
,
K L
^
withthesamesubassemblingmatrices
_
^
,
‘ (cid:14)a P] (cid:18)c b
,
respectively.Forinstance,
K
;
L
(cid:14)
(cid:14)
_
_
#
#
;
K L
#
#
_
_
N
#
N
#
d
d
_
_
Z
Z
;
K L
Z
Z
_
_
NZ
NZ
(cid:18)
S
1DepartmentofMathematics,UniversityofHouston,Houston,TX,77204-3008,USA,e-mail:kuz@math.uh.edu

| 68  |     |     |     |     |     |     | KUZNETSOV |
| --- | --- | --- | --- | --- | --- | --- | --------- |
^
| Domain   | decomposition |     |     | for                  | composite | materials |     |
| -------- | ------------- | --- | --- | -------------------- | --------- | --------- | --- |
|          |               | ^   |     |                      | ^         |           |     |
| (cid:23) |               |     |     | (cid:14) P] (cid:18) | P         |           |     |
‘
|     |     |     | (cid:0) | (cid:2) | (cid:1) ^ (cid:1)(cid:4) (cid:3) |     | ^   |
| --- | --- | --- | ------- | ------- | -------------------------------- | --- | --- |
Let be (cid:23) a rectangle [ and (cid:14) , ‘ (cid:14) , (cid:29) , be (cid:29)(cid:13) open (cid:23) (cid:14) non-overlappingpolygonalsubdo- ‘ (cid:18) (cid:22) (cid:14) PR (cid:18) (cid:23)
|     | ^   | (cid:0) (cid:0)(cid:6) | (cid:5) |     | (cid:0) (cid:13) |     |     |
| --- | --- | ---------------------- | ------- | --- | ---------------- | --- | --- |
mainsof , i.e. (cid:8) (cid:7) for (cid:10) (cid:12)(cid:9) (cid:11) and (cid:14) (cid:7) , (cid:15) (cid:11) 6(cid:9) E] (cid:16) F (cid:1) . An W (cid:5) exampleof (cid:12) Z
|     |     |     |     | ^   |     | ^ (cid:18)(cid:20) (cid:19) | (cid:19) (cid:18) |
| --- | --- | --- | --- | --- | --- | --------------------------- | ----------------- |
isgivenin 6(cid:9) E R (cid:5) Figure1. (cid:18)B (cid:29)’ (cid:23)  (cid:12) We assumethat (cid:0) are shape-regular, # (cid:22)(cid:21) (cid:10) (cid:23)(cid:25) (cid:24)(cid:2) (cid:23)(cid:27) (cid:26) (cid:0) and
|     |         |     |          |     |     | (cid:17) Z | (cid:26) (cid:17) |
| --- | ------- | --- | -------- | --- | --- | ---------- | ----------------- |
|     | (cid:0) |     | (cid:18) |     |     | #          | (cid:18)( ’       |
(cid:29)(cid:28)(cid:30) (cid:24)(cid:31) (cid:21)!  # "$ (cid:23) % (cid:3) (cid:7) (cid:17)(cid:25) (cid:14)O & P with # somepositiveconstants 5 C (cid:21)$ (cid:5)(cid:8) (cid:26)(cid:28) (cid:18)V P (cid:17) , (cid:17) ‘ (cid:14) , and P] (cid:18) (cid:17)$ & where (cid:7) P is given.
Wealsoassumethat (cid:23) d )+ * , - $ 2 in (cid:0) , (cid:2) (cid:1) ,and - intherestof
|     |     |     |     | ,   | (cid:17)(cid:25) . 0 /(cid:27) 1 |     |     |
| --- | --- | --- | --- | --- | -------------------------------- | --- | --- |
. Weshallcallthismodelexamplea“compositematerial”.
;
|                    |     |     |                                    | Figure1: | Thecomputationalgrid. |     |     |
| ------------------ | --- | --- | ---------------------------------- | -------- | --------------------- | --- | --- |
| Thestiffnessmatrix |     |     | ofsystem(4)canbepresentedintheform | ;        | ;                     | ^   |     |
|                    |     |     |                                    |          | ^                     | P ^ |     |
3
|     |     |     |     |     | (cid:14) % | 7 6 |     |
| --- | --- | --- | --- | --- | ---------- | --- | --- |
4
d (5)
#
|     |     |     |     |     | 5   | ,   |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
^Y < <
where
|     |     | (cid:5) 6 | )(cid:19) (cid:18) | (cid:12)7 (cid:14)(cid:27) 0 | (cid:3)3 )] (cid:31) 4W (cid:3) (cid:31)(cid:15) 6(cid:9) (cid:20) | ,(cid:19) )] (cid:31)(cid:28) (cid:18) (cid:31)= (cid:21) ! (cid:31)(cid:28) (cid:18) |     |
| --- | --- | --------- | ------------------ | ---------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------- | --- |
|     |     |           | 8                  |                              | 8                                                                  | 8                                                                                     |     |
*
|     |     | ;   | < < | 9   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
and
|     |     | (cid:5) | % )(cid:19) (cid:18) | (cid:12)(cid:15) (cid:14) 0 | (cid:3)3 ) (cid:31) 4U (cid:3) (cid:31) 6(cid:9) (cid:20) | ,(cid:19) ) (cid:31) (cid:18) (cid:31) (cid:21) ! (cid:31) S |     |
| --- | --- | ------- | -------------------- | --------------------------- | --------------------------------------------------------- | ------------------------------------------------------------ | --- |
|     |     |         | 8                    | 1                           | 8                                                         | ^ 8                                                          |     |
; ^
| Itisobviousthatwithanappropriatepermutationmatrix |     |     |     |     | ^ ^ | : wehave |     |
| ------------------------------------------------- | --- | --- | --- | --- | --- | -------- | --- |
^
(cid:26)
N
|     |     |     |     |     | 6 (cid:14) |          |     |
| --- | --- | --- | --- | --- | ---------- | -------- | --- |
|     |     |     |     |     | (cid:26)   | (cid:26) |     |
|     |     |     |     | :   | : < ;      |          |     |
> =

| ; ^                                           |     |     |     |     |     |     | ^   |     |
| --------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOMAINDECOMPOSITIONANDFICTITIOUSDOMAINMETHODS |     |     |     |     |     |     |     | 69  |
;
| (cid:2) |     |     |     |     |     |     | P ‘ |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- |
(cid:19) (cid:19)
where isthestiffnessmatrixoftheLaplacianforthesubdomain (cid:0) , (cid:1) .
|     |     |     | <   | ;   |     | <   | <   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
In[Kuz00]wasproposedtoreplacesystem(4)with in(5)byasaddlepointsystem
|      |     |                | <                      |                      | N                              | <                               |                            |     |
| ---- | --- | -------------- | ---------------------- | -------------------- | ------------------------------ | ------------------------------- | -------------------------- | --- |
|      |     | (cid:0)(cid:2) | (cid:1) (cid:10)       | (cid:1) %            | 6 (cid:1)                      | (cid:10)                        | (cid:1) (cid:16)           |     |
|      |     |                |                        | (cid:14)             |                                | (cid:3)(cid:5) (cid:4) (cid:14) | (cid:4)                    |     |
|      |     |                | (cid:3)(cid:5) (cid:4) |                      | (cid:7)(cid:2) (cid:6) (cid:4) |                                 |                            |     |
|      |     |                |                        | 6                    |                                |                                 | (cid:26)                   | (6) |
| with |     |                | 6 N (cid:14)O          | (cid:5) 6 6 ZI ST ST | S 6 (cid:12)                   | (cid:21)(cid:24) > ?B (cid:9)A  | (cid:8) (cid:11)? (cid:10) |     |
|      |     |                |                        | #                    |                                |                                 | 3                          |     |
3
andtheblockdiagonalmatrix
(cid:16)(cid:18) (cid:17)
(cid:17)
6
|     |     |     | #   | #   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
,
|     |     | (cid:6) (cid:13)(cid:14) | (cid:12)(cid:14) |     |          | (cid:21) > (cid:8) | (cid:11)? (cid:10)8 (cid:9)A (cid:8) (cid:20)? (cid:10) S |     |
| --- | --- | ------------------------ | ---------------- | --- | -------- | ------------------ | --------------------------------------------------------- | --- |
|     |     |                          | (cid:14)(cid:15) |     | (cid:19) | 3                  | 3                                                         |     |
...
6
<
, 3 3
<
(cid:10)
System(6)isequivalenttosystem(4)inthesensethatthesolutionvector to(4)coin-
(cid:10)
|                               |     |     |     | < ^ <              |     | ^         |     |     |
| ----------------------------- | --- | --- | --- | ------------------ | --- | --------- | --- | --- |
| cideswiththesolutionsubvector |     |     |     | to(6)andviceversa. |     | Moreover, |     |     |
P ^
(cid:3)
|     |     |     |     | (cid:2) (cid:10)(cid:22) | (cid:22)(cid:21) (cid:21) | 6   |     |     |
| --- | --- | --- | --- | ------------------------ | ------------------------- | --- | --- | --- |
<
|     |     |         | ^   |     | (cid:23)$ (cid:26) |     |                    |     |
| --- | --- | ------- | --- | --- | ------------------ | --- | ------------------ | --- |
|     |     | (cid:3) |     | ,   |                    |     | (cid:26); (cid:25) |     |
(cid:14) P] (cid:18)
‘
|                         |           | N                                    |                               | (cid:2) (cid:1)         |                             |                |                                    |     |
| ----------------------- | --------- | ------------------------------------ | ----------------------------- | ----------------------- | --------------------------- | -------------- | ---------------------------------- | --- |
| foranysolutionsubvector | (cid:24)" | (cid:23) (cid:14) " (cid:23)         | to(6), (cid:26)               | .                       |                             |                | % #                                |     |
|                         |           | <                                    | ’ <                           | ; (cid:25) < <          |                             | < <            | <                                  |     |
| Letamatrix              |           |                                      | bespectrallyequivalentto      |                         |                             |                | ,i.e                               |     |
|                         |           | (cid:5) )’ (cid:18)                  | )(cid:28) (cid:12) (cid:5)    | )’ (cid:18) )2 (cid:12) | (cid:5)                     | )B (cid:18) )2 | (cid:12) , )= (cid:21)(cid:24) > ? |     |
|                         |           | (cid:28) (cid:27) (cid:29)" (cid:23) |                               | % #                     | (cid:31) (cid:30) (cid:24)" | (cid:23)       |                                    |     |
|                         |           |                                      | (cid:19)                      |                         | (cid:19)                    |                |                                    |     |
|                         |           | (cid:17)                             |                               |                         | (cid:17)                    |                |                                    |     |
|                         |           | (cid:27)                             | (cid:30)                      |                         |                             | (cid:23)@      | (cid:31)                           |     |
| withpositiveconstants   |           | (cid:17) and                         | (cid:17) independentofthemesh |                         |                             |                | . Thenthematrix                    |     |
(cid:26)
|     |     |     |     |   (cid:1)(cid:28) (cid:24)" | (cid:23) |         |     |     |
| --- | --- | --- | --- | --------------------------- | -------- | ------- | --- | --- |
|     |     |     |     | (cid:14)                    |          | (cid:4) |     |     |
|     |     |     |     | (cid:26)                    | ""       | !       |     |     |
(7)
| with ^    |     |     | " ! (cid:14) | 6(cid:28) (cid:11)E #(cid:5) $ 6 (cid:1) | (cid:18) 6 Z(cid:1) ^ (cid:18)(cid:13) | ST ST S (cid:18) 6   | (cid:26)(cid:1) % (cid:18) |     |
| --------- | --- | --- | ------------ | ---------------------------------------- | -------------------------------------- | -------------------- | -------------------------- | --- |
|           |     |     |              | (cid:22)(cid:21) #                       |                                        |                      | 3                          |     |
| 6 (cid:1) |     |     |              |                                          | 6 ‘                                    | (cid:14) PR (cid:18) |                            |     |
(cid:0)
where denotes the generalized inverse to , (cid:16) (cid:1) , was proposed in [Kuz00] as
|     |     | (cid:0)   |     |     |     | (cid:0) |     |     |
| --- | --- | --------- | --- | --- | --- | ------- | --- | --- |
an effective preconditioner for the matrix in (6). To justify the latter statement we have
‘
to consider the matrix in its invariant & subspace (cid:1) supplied with the scalar product
| generatedbythematrix |     |     |     |           | (cid:26) |                  |     |     |
| -------------------- | --- | --- | --- | --------- | -------- | ---------------- | --- | --- |
|                      |     |     |     | (cid:1) " | (cid:23) |                  |     |     |
|                      |     |     |     | (cid:14)  |          | (cid:4) (cid:18) |     |     |
|                      |     |     |     | (cid:26)  | ’ !      |                  |     |     |
where ’ (cid:14)(cid:17) 6(cid:9) (cid:20)E #( $ 6 (cid:18) 6 Z (cid:18)V SU ST SV (cid:18) 6 % S &
!
|     |     |     |           | (cid:29)(cid:21) # |     |     |           |     |
| --- | --- | --- | --------- | ------------------ | --- | --- | --------- | --- |
|     |     |     | (cid:0)   |                    |     |     | 3 (cid:0) |     |
|     |     |     | (cid:0)   | (cid:0)            |     |     | ‘         |     |
It can be easily shown that (cid:14) is a (cid:5) symmetric (cid:12) operator in (cid:1) with respect to the -
|           |     |     | ‘       | ‘       |     |     |     |     |
| --------- | --- | --- | ------- | ------- | --- | --- | --- | --- |
| (cid:0)   |     |     | (cid:1) | (cid:1) |     |     |     |     |
scalar product. Moreover, . To ) this Z end, all ) non-zero (cid:27) eigenvalues of the
|        |                               |     |     |                       | (cid:18) +# * | (cid:18) | (cid:18) * (cid:18) |     |
| ------ | ----------------------------- | --- | --- | --------------------- | ------------- | -------- | ------------------- | --- |
| matrix | belongtotheunionoftwosegments |     |     |                       |               | 2 and    | & 2 withendpoints   |     |
|        |                               |     |     | -Z , (cid:29)(cid:26) | ,             | S        |                     |     |
(cid:27)
|     |     |     | (cid:18) | # (cid:19) (cid:18) | (cid:18) | (cid:19) (cid:18) |     |     |
| --- | --- | --- | -------- | ------------------- | -------- | ----------------- | --- | --- |
&

&
| 70  |     |     |           |     |     |     |         | KUZNETSOV |     |
| --- | --- | --- | --------- | --- | --- | --- | ------- | --------- | --- |
|     |     |     | (cid:0)   |     |     |     | (cid:0) |           |     |
‘
Theconditionnumberof withrespecttothesubspace (cid:1) andthe -scalarproductis
( $
| definedby |     |     |                          | (cid:0)            |   F                       | (cid:27)     | %                        |     |     |
| --------- | --- | --- | ------------------------ | ------------------ | ------------------------- | ------------ | ------------------------ | --- | --- |
|           |     |     |                          | 6 (cid:25) (cid:5) | (cid:12)(cid:15) (cid:14) | (cid:18) *   | (cid:18) # S             |     |     |
|           |     |     |                          |                    | F (cid:21)E(cid:6)        | (cid:5) $    | (cid:7) Z (cid:7)        |     |     |
|           |     |     | (cid:0)(cid:2) (cid:1)   |                    |                           |              | %                        |     |     |
|           |     |     |                          | (cid:4) (cid:3)    |                           |   (cid:18) * | (cid:7) (cid:18) (cid:7) |     |     |
&
Underalltheaboveassumptionsthefollowingresultwasprovedin[Kuz00].
Proposition1
(cid:0)
|     |     |     |     |     | 6 (cid:5) (cid:12) | (cid:18) |     |     |     |
| --- | --- | --- | --- | --- | ------------------ | -------- | --- | --- | --- |
(cid:19)
(cid:0)(cid:2) (cid:1)
|     |     |     |     |     | (cid:4) (cid:3) | (cid:17) |     |     | (8) |
| --- | --- | --- | --- | --- | --------------- | -------- | --- | --- | --- |
(cid:9) (cid:8)
|     |     |     |     |     |     |     | (cid:18) Z (cid:18)V | SU ST S(cid:13) (cid:18) | (cid:23)  (cid:31) |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | ------------------------ | ------------------ |
|     |     |     |     |     |     |     | #                    | ^                        |                    |
where (cid:17) isapositiveconstantindependentofthevalues , , , 3 andthemesh .
(cid:9) (cid:8)
|                               |     |     |     |                                |     |     |     | ‘ (cid:14) P] (cid:18)         |     |
| ----------------------------- | --- | --- | --- | ------------------------------ | --- | --- | --- | ------------------------------ | --- |
| Remark1 Ingeneral,theconstant |     |     |     | (cid:17) dependsontheconstants |     |     |     | (cid:17) , (cid:11) (cid:10) . |     |
|                               |     |     |     | (cid:8)                        |     |     |     |                                |     |
Theimplementationprocedureofthepreconditioner ^ isbasedonasimpleobservation
| that |     |     |     | ^   | ^                         |          |     |     |     |
| ---- | --- | --- | --- | --- | ------------------------- | -------- | --- | --- | --- |
|      |     |     |     |     | (cid:1)                   | (cid:26) |     |     |     |
|      |     |     |     | 6 6 | (cid:14)                  |          |     |     |     |
|      |     |     |     |     | (cid:1)                   | (cid:4)  |     |     |     |
|      |     |     |     |     | (cid:13) (cid:26)(cid:12) | (cid:26) |     |     |     |
(9)
|     |     |     |     |     | ^ ; ^(cid:8) ; | ^   |     |     |     |
| --- | --- | --- | --- | --- | -------------- | --- | --- | --- | --- |
where
(cid:1) S
-
(cid:12)
The results of numerical experiments (cid:23) for the geometry given in Fig. 1 are presented in
"
Table1. Fornumericalexperiments waschosentobetheBPX-preconditioner[BPX90].
|     |     |     | Table1. P H | P ThenumberofPCGiterations. |     |     | P R | (cid:26) $ P R (cid:26) |     |
| --- | --- | --- | ----------- | --------------------------- | --- | --- | --- | ----------------------- | --- |
(cid:25)
|     |     | P,  | (cid:15) (cid:14)(cid:17) (cid:16) | (cid:15) (cid:14) (cid:14)(cid:6) | (cid:18)(cid:17) (cid:16)(cid:19) (cid:14)(cid:6) (cid:18) | (cid:20)(cid:6) (cid:21)(cid:22) (cid:16)(cid:23) | (cid:20)(cid:6) (cid:21) (cid:24) (cid:21) | (cid:25) (cid:16) (cid:24) (cid:21) |     |
| --- | --- | --- | ---------------------------------- | --------------------------------- | ---------------------------------------------------------- | ------------------------------------------------- | ------------------------------------------ | ----------------------------------- | --- |
(cid:25)
|     |     | PU (cid:26) | 15  |     | 16  | 18  |     | 18  |     |
| --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
(cid:25) #
Z
|     |     | PU (cid:26) | 17  |     | 22  | 25  |     | 27  |     |
| --- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- |
(cid:25)
|     |     | PU (cid:26)            | 19  |     | 23  | 27  |     | 29  |     |
| --- | --- | ---------------------- | --- | --- | --- | --- | --- | --- | --- |
|     |     | PU (cid:26) (cid:27) & | 19  |     | 23  | 27  |     | 29  |     |
|     |     |                        | 19  |     | 23  | 27  |     | 29  |     |
^
(cid:3)
‘ (cid:14) PR (cid:18)
Thevectors , (cid:16) (cid:1) ,in(6)canbecalledthediscretedistributedLagrangemultipliers.
|     |     |     |     |     | ^   | ^   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
They have a very simple connection with the continuous/differential distributed Lagrange
(cid:3)
| multiplier. System(6)canbeobtainedbythestraightforwardfiniteelementdiscretizationof |     |     | (cid:10)(cid:22) (cid:21) | "$ %# (cid:5)(cid:8) (cid:23)  (cid:12) | (cid:21) "$ | # (cid:5) (cid:12) | ‘ (cid:14) P] (cid:18) |     |     |
| ----------------------------------------------------------------------------------- | --- | --- | ------------------------- | --------------------------------------- | ----------- | ------------------ | ---------------------- | --- | --- |
(cid:0)
| thevariationalproblem:find |     |     |     |     | , ^ | ,   | (cid:2) (cid:1) | ,suchthat |     |
| -------------------------- | --- | --- | --- | --- | --- | --- | --------------- | --------- | --- |
^
|     |     |                                |                      | 3   | (cid:3)                    |                                      |                       |                             |     |
| --- | --- | ------------------------------ | -------------------- | --- | -------------------------- | ------------------------------------ | --------------------- | --------------------------- | --- |
|     | 0   | (cid:3)3 (cid:10)- 4U (cid:3)3 | )J 6(cid:9) (cid:20) | 0   | (cid:3) 4W (cid:3)(cid:11) | )J 6(cid:9) (cid:20)(cid:6) (cid:14) | 0 (cid:16)(cid:19) )/ | 6(cid:28) (cid:20) (cid:18) |     |
4
|     | 1   |     | ^ d | ^   | ^   | ^   | 1   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
5 # *
|     |     |                               |                     | 9         | (cid:3)            |                                    |                   |                                   |      |
| --- | --- | ----------------------------- | ------------------- | --------- | ------------------ | ---------------------------------- | ----------------- | --------------------------------- | ---- |
|     | 0   | (cid:3)3 (cid:10)- 4U (cid:3) | 6(cid:28) (cid:20)- | (cid:2) 0 | (cid:3) 45 (cid:3) | 6(cid:9) (cid:20)(cid:30) (cid:14) | (cid:26) (cid:18) | ‘ (cid:14) PR (cid:18) $ (cid:18) | (10) |
(cid:16) (cid:1)
|     |     | (cid:25) | (cid:26) | ,   | (cid:27) | (cid:26) |     |     |     |
| --- | --- | -------- | -------- | --- | -------- | -------- | --- | --- | --- |
^ ^
|                                                            | 9 *        |         |                      | 9 *              |     |     |     |     |     |
| ---------------------------------------------------------- | ---------- | ------- | -------------------- | ---------------- | --- | --- | --- | --- | --- |
| ,(cid:19) )= (cid:21) %# (cid:5)(cid:8) (cid:23)  (cid:12) | (cid:21)   | (cid:5) | (cid:12) (cid:14) PR | (cid:18)         |     |     |     |     |     |
| "H                                                         |            | "H #    | ‘                    |                  |     |     |     |     |     |
|                                                            |            | (cid:0) |                      | (cid:16) (cid:1) |     |     |     |     |     |
|                                                            | , (cid:26) |         | ,                    | .                |     |     |     |     |     |

| DOMAINDECOMPOSITIONANDFICTITIOUSDOMAINMETHODS |     |        |        |     |     |     |     |     |     | 71  |
| --------------------------------------------- | --- | ------ | ------ | --- | --- | --- | --- | --- | --- | --- |
| Fictitious                                    |     | domain | method |     |     |     |     |     |     |     |
The name“fictitious domainmethod”was originallysuggested by V.K. Saul’evin [Sau63].
TheSaul’ev’sideaistoreplacedifferentialproblem(1)–(2)bytheproblem
|     |     |     | (cid:2)(cid:4) | (cid:3)(cid:30) (cid:5) (cid:7) (cid:3)3 | (cid:10) (cid:12) (cid:14) | (cid:16)          | (cid:18) (cid:20)(cid:24) | (cid:21) (cid:18)                  |     |     |
| --- | --- | --- | -------------- | ---------------------------------------- | -------------------------- | ----------------- | ------------------------- | ---------------------------------- | --- | --- |
|     |     |     |                | )                                        | )                          | )                 |                           |                                    |     |     |
|     |     |     |                |                                          | (cid:10) (cid:14)          | (cid:26) (cid:18) | (cid:20)(cid:22)          | (cid:21) (cid:29) (cid:0) (cid:18) |     |     |
(11)
)
(cid:0)
(cid:23)
| where | (cid:0) isarectanglecontainingtheoriginalsimply-connecteddomain |                  |                          |                                   |                           |     |                   |                           | ,                                                           |     |
| ----- | --------------------------------------------------------------- | ---------------- | ------------------------ | --------------------------------- | ------------------------- | --- | ----------------- | ------------------------- | ----------------------------------------------------------- | --- |
|       |                                                                 |                  |                          |                                   | <                         |     |                   |                           | <                                                           |     |
|       |                                                                 |                  | (cid:7)(cid:19) (cid:18) | (cid:20)(cid:22) (cid:21)(cid:24) | (cid:23)(cid:25) (cid:18) |     |                   | (cid:16)(cid:19) (cid:18) | (cid:20)(cid:24) (cid:21)(cid:24) (cid:23)(cid:25) (cid:18) |     |
|       |                                                                 | (cid:7) (cid:14) |                          |                                   |                           |     | (cid:16) (cid:14) |                           |                                                             |     |
|       |                                                                 |                  | (cid:1) P                |                                   |                           |     |                   | (cid:1)                   |                                                             |     |
|       |                                                                 | )                | # (cid:18)               | (cid:20)(cid:22) (cid:21)         | (cid:23)(cid:25) (cid:18) |     | )                 | (cid:26)(cid:28) (cid:18) | (cid:20)(cid:24) (cid:21) (cid:23)(cid:4) S                 |     |
d
|                 |     |          | )                |                  | (cid:0)(cid:3) (cid:2) |          |     |     | (cid:0)(cid:4) (cid:2) |     |
| --------------- | --- | -------- | ---------------- | ---------------- | ---------------------- | -------- | --- | --- | ---------------------- | --- |
|                 |     | (cid:10) | (cid:2) (cid:10) | 1                | (cid:26)               | (cid:26) |     |     |                        |     |
|                 |     |          | L                | (cid:8) (cid:10) |                        |          |     |     |                        |     |
| Itwasprovedthat |     |          | )                |                  | as                     | where    |     |     |                        |     |
,
|     |     | (cid:5) | (cid:5)(cid:7) (cid:6)(cid:9) (cid:8)(cid:10) |                   |                             |                    | <                         |     |     |     |
| --- | --- | ------- | --------------------------------------------- | ----------------- | --------------------------- | ------------------ | ------------------------- | --- | --- | --- |
|     |     |         |                                               | (cid:12) (cid:11) | (cid:10): (cid:18) (cid:11) | (cid:20)I (cid:21) | (cid:23)(cid:25) (cid:18) |     |     |     |
|     |     |         |                                               | (cid:10) (cid:14) |                             |                    |                           |     |     |     |
|     |     |         |                                               | L                 | (cid:1)                     |                    |                           |     |     |     |
|     |     |         |                                               |                   | (cid:26)(cid:28) (cid:18)   | (cid:20)I (cid:21) | (cid:23)(cid:25)          | S   |     |     |
|     |     |         |                                               |                   |                             |                    | (cid:0)(cid:3) (cid:2)    |     |     |     |
Theformoftheequationin(1)remindsusthesituationconsideredintheprevioussection.
IfweintroducethedistributedLagrangemultiplierby
P
(cid:3)
|     |     |     |     |     |     | (cid:14) (cid:10) |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ----------------- | --- | --- | --- | --- |
<
(12)
,
|         | (cid:14) (cid:23) |     |     |     |     |     |     |     | (cid:10)D (cid:21) | " %# (cid:5) (cid:12) |
| ------- | ----------------- | --- | --- | --- | --- | --- | --- | --- | ------------------ | --------------------- |
| (cid:3) | (cid:3)           |     |     |     |     |     |     |     |                    |                       |
in (cid:21) (cid:0) (cid:5) (cid:0)(cid:13) (cid:12) (cid:2) , (cid:14)(cid:27) then (cid:26) the (cid:29) weak (cid:29) saddle point formulation reads as follows: find (cid:0) ,
"H #
|     | (cid:0) |     | (cid:0) (cid:13) |           |     |     |     |     |     |     |
| --- | ------- | --- | ---------------- | --------- | --- | --- | --- | --- | --- | --- |
|     | ,       | on  | (cid:0)          | ,suchthat |     |     |     |     |     |     |
(cid:3)
|     |     |     | 0 (cid:3)3 (cid:10)(cid:6)         | 4U (cid:3)3 )7 6(cid:9) (cid:20) | 0 (cid:3) | 4W (cid:3)3 | )7 6(cid:9) (cid:20) (cid:14)     | 0 (cid:16) )7                                      | 6(cid:9) (cid:20): (cid:18) |      |
| --- | --- | --- | ---------------------------------- | -------------------------------- | --------- | ----------- | --------------------------------- | -------------------------------------------------- | --------------------------- | ---- |
|     |     |     |                                    |                                  | d         |             |                                   | )                                                  |                             |      |
|     |     |     |                                    |                                  | 9         | (cid:3)     |                                   |                                                    |                             |      |
|     |     |     | 0(cid:14) (cid:3)3 (cid:10)(cid:6) | 4U (cid:3) 6(cid:28) (cid:20)-   | (cid:2) 0 | (cid:3) 4U  | (cid:3) 6(cid:9) (cid:20)(cid:30) | (cid:14)(cid:27)(cid:14) (cid:26)(cid:28) (cid:18) |                             | (13) |
,
|                       |                        |               |                                              | (cid:25) (cid:26) |                  |                     | (cid:25) (cid:26) |     |     |     |
| --------------------- | ---------------------- | ------------- | -------------------------------------------- | ----------------- | ---------------- | ------------------- | ----------------- | --- | --- | --- |
|                       |                        |               | 9                                            |                   | 9                |                     |                   |     |     |     |
| ,(cid:19) )= (cid:21) | "H %# (cid:5) (cid:12) | $ (cid:21) "H | # (cid:5) (cid:12) (cid:22) (cid:14)(cid:27) | (cid:26) (cid:29) | (cid:29)         |                     |                   |     |     |     |
|                       |                        |               | (cid:0)                                      |                   | (cid:0) (cid:13) |                     |                   |     |     |     |
|                       | (cid:0) ,              |               | ,                                            | on                | (cid:0)          | . (cid:14) (cid:26) |                   |     |     |     |
|                       |                        | (cid:26)      | (cid:26)                                     |                   |                  |                     |                   |     |     |     |
The interesting observation is that with formulation (13) coincides with the dis-
|     |     |     |     |     |     | ,   |     |     |     | (cid:1) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- |
tributedLagrangemultiplierfictitiousdomainmethodinventedbyR.Glowinski(see[DGH (cid:1) 92,
GHJ 97]). Thus,theGlowinski’smethodistheclosurewithrespecttotheparameter ofthe
,
| Saul’ev’smethod. |     |     |     |     |     |     |     |     | <   |     |
| ---------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                  |     |     | <   | ;   | ;   |     |     | <   |     |     |
Thefiniteelementdiscretizationto(13)resultsinthealgebraicsystem
|     |     |         | (cid:16)(cid:18) (cid:17)         |                          |        |           | (cid:16)(cid:18) (cid:17) | (cid:16)(cid:18) (cid:17)         | < (cid:16)(cid:18) (cid:17)       |      |
| --- | --- | ------- | --------------------------------- | ------------------------ | ------ | --------- | ------------------------- | --------------------------------- | --------------------------------- | ---- |
|     |     |         | <(cid:10)                         | ;                        | ; Z    | (cid:26)  |                           | <(cid:10)                         | (cid:16)                          |      |
|     |     | (cid:0) | < #                               | #c #                     | #      |           |                           | < #                               | #                                 |      |
|     |     |         | (cid:10)(cid:19) Z                | Z                        | Zc Z   | 6 Zc      | Z                         | (cid:10)(cid:19) Z (cid:14)       | (cid:16) Z                        |      |
|     |     |         | (cid:12)(cid:14)(cid:15) (cid:19) | (cid:12)(cid:14)(cid:15) |        |           | (cid:19)                  | (cid:12)(cid:14)(cid:15) (cid:19) | (cid:12)(cid:14)(cid:15) (cid:19) |      |
|     |     |         | (cid:3) -                         | #                        |        |           |                           | (cid:3)                           |                                   |      |
|     |     |         |                                   | (cid:26)                 | 6 Z8 Z | (cid:2) 6 | Z8 Z                      |                                   | (cid:26)                          | (14) |
,
6 Zc Z
|       |                                       |     |     |     |            | ; ;  | (cid:0) |     |     |     |
| ----- | ------------------------------------- | --- | --- | --- | ---------- | ---- | ------- | --- | --- | --- |
| where | staysforthestiffnessmatrixinsubdomain |     |     | ;   |            |      | ,and    |     |     |     |
|       |                                       |     |     |     |            | ; ;  | Z       |     |     |     |
|       |                                       |     |     |     | % (cid:14) | #c # | #       |     |     |     |
|       |                                       |     |     |     |            | Z    | Z8 Z    |     |     |     |
< ;
|     |     |     |     |     |     | #   | =   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

72 KUZNETSOV
(cid:0)
;
staysforthestiffnessmatrixintherectangle (cid:0) . Ifwepresent inadifferentblockform:
|     |     | %        | 6 N             |                          |     |
| --- | --- | -------- | --------------- | ------------------------ | --- |
|     |     | (cid:0)  |                 | (cid:6)                  |     |
|     |     | (cid:14) | (cid:18)        | (cid:14) 6 Zc Z (cid:18) |     |
|     |     | 6        | (cid:2) (cid:6) |                          |     |
|     |     | ;        |                 | ; (cid:25)               |     |
=
,
(cid:0)
|     |     | "" (cid:23) |     | % # |     |
| --- | --- | ----------- | --- | --- | --- |
andassumethat amatrix isspectrallyequivalentto , thenthepreconditionerfor
canbeproposedintheformoftheblockdiagonalmatrix
(cid:26)
|     |     |     | " (cid:23) |     |     |
| --- | --- | --- | ---------- | --- | --- |
(cid:14)
(cid:26)
|     | (cid:25) |     | ; "" ! |     | (15) |
| --- | -------- | --- | ------ | --- | ---- |
=
| " !   | (cid:14) 6 Zc Z# |     |     |     |     |
| ----- | ---------------- | --- | --- | --- | --- |
| where | .                |     |     |     |     |
(cid:0)
Assumethat the norm preserving finite elementextensiontheorem for the subdomain
| withrespecttotherectangle |     | (cid:0) holds.Then, |     |     |     |
| ------------------------- | --- | ------------------- | --- | --- | --- |
(cid:0)
6 (cid:5) (cid:12)
(cid:19)
|     |     | (cid:0)(cid:2) (cid:1) |     | (cid:17) |     |
| --- | --- | ---------------------- | --- | -------- | --- |
(cid:0)
|     |     |     |     | (cid:2) (cid:1) (cid:31) (cid:21) (cid:26)) P |     |
| --- | --- | --- | --- | --------------------------------------------- | --- |
*
where (cid:14) (cid:17) (cid:26) is a positiveconstant independentof the mesh (cid:0) (cid:26) andvalue of , (cid:25) 2 . In the
’
case (cid:3) (cid:1) theresultwasprovedin[GK98].Forthecase onehastousetechniquefrom
| ,   |     |     |     | ,   |     |
| --- | --- | --- | --- | --- | --- |
[Kuz00].
| Overlapping | domain | decomposition |     |     |     |
| ----------- | ------ | ------------- | --- | --- | --- |
(cid:14) (cid:23) (cid:23)
(cid:23) (cid:31) (cid:23) (cid:31) (cid:23) Z (cid:31) (cid:31) (cid:31) Z (cid:31)
|     |     |     | # X | X # X (cid:13) | X   |
| --- | --- | --- | --- | -------------- | --- |
Let be partitioned into two F subdomains U (cid:5) (cid:29) (cid:31) (cid:29)(cid:13) (cid:23)  (cid:12) and 5 C (cid:26) such that (cid:4) is
|     |     |     | (cid:13) | ’   |     |
| --- | --- | --- | -------- | --- | --- |
nonempty. We assumethat (cid:23)7 (cid:21) (cid:28) (cid:31) (cid:4) (cid:23) (cid:31) (cid:3) (cid:23) Z (cid:31) ,andthenormpreservingfinite
|     |     |     | (cid:17)$ . 0 | /$ 1 |     |
| --- | --- | --- | ------------- | ---- | --- |
# X X
elementextensionresultsfrom (cid:4) into and hold[Wid87]. Laterweshallgivethe
| algebraicinterpretationofthisassumption. | (cid:7)’ | (cid:5)( (cid:10). (cid:18)(cid:9) )(cid:9) (cid:12)                            |                                                        |                                                                |      |
| ---------------------------------------- | -------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ | -------------------------------------------------------------- | ---- |
| Letthebilinearform                       |          | besplitintotwobilinearforms[Kuz97]:                                             |                                                        |                                                                |      |
|                                          |          | (cid:7)’ (cid:5)( (cid:10). (cid:18)(cid:9) )(cid:9) (cid:12)/ (cid:14)(cid:17) | (cid:7) (cid:5)( (cid:10). (cid:18)(cid:9) )2 (cid:12) | (cid:7) Z (cid:5) (cid:10): (cid:18)(cid:28) )(cid:9) (cid:12) |      |
|                                          |          |                                                                                 | # d                                                    |                                                                | (16) |
*8 (cid:5)( )(cid:9) (cid:12)
| andthelinearform | bealsosplittedintotwolinearforms: |                                       |                                                  |                            |      |
| ---------------- | --------------------------------- | ------------------------------------- | ------------------------------------------------ | -------------------------- | ---- |
|                  |                                   | *8 (cid:5)( )(cid:9) (cid:12)(cid:15) | (cid:14)(cid:17) * (cid:5)( )(cid:9) (cid:12) *Z | (cid:5)( )(cid:9) (cid:12) |      |
|                  |                                   |                                       | # d                                              |                            | (17) |
|                  |                                   | ^                                     | ^                                                |                            |      |
where
|     |     | (cid:7) (cid:5)( (cid:10). (cid:18)(cid:28) )(cid:9) | (cid:12)(cid:15) (cid:14)D 0 (cid:7) (cid:3)3 (cid:10)- 4W | (cid:3)3 )7 6(cid:28) (cid:20) |     |
| --- | --- | ---------------------------------------------------- | ---------------------------------------------------------- | ------------------------------ | --- |
1
^
*
^
| with |     |     | (cid:7)B (cid:18) (cid:20)(cid:24) (cid:21)(cid:22) (cid:23) | (cid:18) |     |
| ---- | --- | --- | ------------------------------------------------------------ | -------- | --- |
(cid:7) (cid:14)
|     |     | (cid:1) |                                                       | (cid:2) (cid:4) |     |
| --- | --- | ------- | ----------------------------------------------------- | --------------- | --- |
|     |     |         | (cid:7) ] b(cid:9) (cid:18) (cid:20)(cid:24) (cid:21) | (cid:18)        |     |
|     |     | ^       | ^ (cid:4)                                             |                 |     |
|     |     |         | (cid:6) (cid:5)                                       |                 |     |
and
|     |     | * (cid:5) )2 | (cid:12)7 (cid:14) 0 (cid:16)(cid:19) )7 | 6(cid:9) (cid:20) |     |
| --- | --- | ------------ | ---------------------------------------- | ----------------- | --- |
1
(cid:7)
^
*
^
| with |     |     | P] (cid:18) (cid:20)(cid:22) (cid:21)(cid:24) (cid:23) | (cid:18) |     |
| ---- | --- | --- | ------------------------------------------------------ | -------- | --- |
(cid:14)
|     |     | (cid:1) |                                                 | (cid:2) (cid:4) |     |
| --- | --- | ------- | ----------------------------------------------- | --------------- | --- |
|     |     |         | P ] b(cid:9) (cid:18) (cid:20)(cid:22) (cid:21) | (cid:18)        |     |
(cid:7)
(cid:4)
|     |     |     | (cid:8) (cid:5) |     |     |
| --- | --- | --- | --------------- | --- | --- |

DOMAINDECOMPOSITIONANDFICTITIOUSDOMAINMETHODS 73
‘ (cid:14)O P] (cid:18)Y b
. Then,letusdefinetwonewbilinearandlinearformsby
(cid:7)(cid:19)
L
(cid:0)
(cid:5)
(cid:5)
<
(cid:10):
(cid:3)
(cid:18)
(cid:18)
*Q (cid:5) L
<
)(cid:28)<
)(cid:28)
<
)(cid:28)
(cid:12)
(cid:12)
(cid:12)
(cid:14)
(cid:14)
(cid:14)
(cid:7) (cid:5)( (cid:10)
#
0 (cid:3)
(cid:1)
* (cid:5) )
# #
#
(cid:3)
(cid:12)
(cid:18)(cid:9) )
45
d
(cid:12) (cid:7)2
# d
(cid:3)(cid:6) (cid:5) ) (cid:2)$
#
*Z] (cid:5) ) ZW (cid:12)
Z] (cid:5)( (cid:10)’
) ZW
Z
(cid:12)(cid:9)
(cid:18)
6(cid:28)
)
(cid:20)
ZU (cid:12)
(cid:18)
(cid:18)
(18)
where
<
) (cid:14)
(cid:1) )
) # Z
(cid:18)
(cid:4) (cid:18) )
^
(cid:21) !
^
(cid:14) (cid:3) (cid:2) )7 & )- (cid:21) " # (cid:5) (cid:23)
^
(cid:12) (cid:18): ) (cid:14)(cid:17) (cid:26)
on
(cid:29)(cid:13) (cid:23) (cid:13) (cid:29)(cid:13) (cid:23)
^
(cid:5) (cid:4)
(cid:18) ‘ (cid:14)O P] (cid:18)c b(cid:28) (cid:18)
and
(cid:3)
(cid:21) (! ! (cid:14) (cid:6) (cid:2)
(cid:3)
&
(cid:3)
(cid:21) " # (cid:5)
(cid:4)
(cid:12) (cid:18)
(cid:3)
(cid:14)(cid:17) (cid:26)
on
(cid:29)(cid:13) (cid:23) (cid:13) (cid:29)
(cid:4)
(cid:4)
S
Then, the weak formulation of (1) based on the aboveoverlappingdecompositionwith dis-
tributedLagrangemultiplierscanbegivenby: find
<
(cid:10)(cid:22) (cid:21) L! (cid:14) !
#
(cid:16)
! Z
,
(cid:3)
(cid:21) ! !
suchthat (cid:7)(cid:19)
L
(cid:0)
<
< (cid:5) (cid:10):
(cid:5) (cid:10).
(cid:18)
(cid:18)
(cid:4)
<
)2
(cid:26)
(cid:12)
(cid:12)
d
(cid:0) (cid:5) (cid:3) (cid:18)
<
)(cid:9) (cid:12) (cid:14)
(cid:14)
*QL
(cid:26)
(cid:5)( )(cid:9) (cid:12) (cid:18)
(19)
,
<
)= (cid:21) L!
,
H
(cid:26)
(cid:21) (cid:9)! !
.
The finite element discretization of (19) can be suggested with the same formulae by
replacing
L!
and
! !
by
L! (cid:31)
and
! ! (cid:31)
X
whicharethetracesofthefiniteelementspace
! (cid:31)
onto (cid:23)
#
(cid:31)
X
,
(cid:23) Z (cid:31)
X
and (cid:4)
(cid:31)
,respectively.Thefiniteelementdiscretizationof(19)resultsinthesystem
ofalgebraicequations
(cid:0)
;
<
<
(cid:10) (cid:3)
=
-
(cid:14)(cid:12)(cid:15)
;
6
(cid:26) #
#
;
6
(cid:26)
Z
Z
6
6
N
# NZ
(cid:26)
(cid:16)
(cid:19)
(cid:17)
(cid:14)(cid:12)(cid:15)
<
<(cid:10)
# < (cid:10)’ Z
(cid:3)
(cid:16)
(cid:19)
(cid:17)
(cid:14) (cid:14)(cid:12)(cid:15)
<
< (cid:16)
# (cid:16) Z
(cid:26)
(cid:16)
(cid:19)
(cid:17)
(cid:18)
(20)
where
;
6
#
N
#
(cid:14)
<
(cid:14)
;
(cid:1)
;
;
6
#8
(cid:1)
(cid:26)
(cid:1)
#
#
(cid:4)
;
;
(cid:18)
(cid:1) #
(cid:8) (cid:10) # (cid:1)(cid:7) (cid:1) =
;
6
Z
NZ
(cid:14)
(cid:14)
;
(cid:1)
;
;
6
Z
(cid:8) (cid:10) (cid:1)(cid:7) (cid:1)
Z (cid:1)
(cid:1) (cid:4)
(cid:26)
S
;
; (cid:1)
Zc
Z
Z =
(cid:18)
Here
6
(cid:1)
isdefinedby
(cid:5) 6 (cid:1)
<
(cid:3)
(cid:18)
<
(cid:26)
(cid:12)(cid:15) (cid:14) 0
(cid:1)
(cid:3)
(cid:3)
(cid:31) 4U (cid:3)
(cid:25) (cid:26)
(cid:31) 6(cid:9) (cid:20): (cid:18) ,
(cid:3)
(cid:31) (cid:18)
(cid:26)
(cid:31) (cid:21) ! ! (cid:31)
X
(cid:18)
(21)
i.e.
(cid:2) 6
(cid:1)
isthestiffnessmatrixfortheLaplacianinthesubdomain (cid:4)
(cid:31)
.
Weintroduceapreconditioner for
(cid:0)
intheformofablockdiagonalmatrix:
(cid:14) (cid:15) (cid:12)
"
(cid:26)
(cid:26)
#
"
(cid:26)
(cid:26)
Z
(cid:24)"
(cid:26)
(cid:26)
!
(cid:16)
(cid:19) (cid:18)
(22)

|     | ^   |     |     | ; (cid:25)^ |                         |     | (cid:25) |           |
| --- | --- | --- | --- | ----------- | ----------------------- | --- | -------- | --------- |
| 74  |     |     |     |             |                         |     |          | KUZNETSOV |
|     | "   |     |     | #           | ‘ (cid:14) P] (cid:18)Y | b   | " #      |           |
!
where is spectrally equivalentto , , and is spectrallyequivalentto the
|     |     |     |     | ; (cid:25) |     | ; (cid:25) |     |     |
| --- | --- | --- | --- | ---------- | --- | ---------- | --- | --- |
Schurcomplementmatrix
|     |     |     |              |     | N           |       | N       |      |
| --- | --- | --- | ------------ | --- | ----------- | ----- | ------- | ---- |
|     |     |     | ! (cid:14) 6 | #   | 6           | 6 Z Z | # 6 Z S |      |
|     |     |     |              | #   | #(cid:24) d |       |         |      |
|     |     |     | (cid:0)      | #   |             |       |         | (23) |
Z
|     |     |     | "   | "   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
#
Wehaveplentyofchoicesfor " ! and ,forinstance,multigridpreconditioner.Thequestion
| isonlyaboutachoicefor |     |     | .   |     |     |     |     |     |
| --------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
The assumption about the norm preserving finite element extension results 6 (in the con-
(cid:1)
text of the above method) ^ is equivalent ^ to the assumption that the matrix is spectrally
|     |     |     | ;   | ;   | ^ ; (cid:25)^G^ ; | ^   |     |     |
| --- | --- | --- | --- | --- | ----------------- | --- | --- | --- |
equivalenttomatrices
|     |     |     | (cid:8) (cid:10) (cid:8) (cid:10) |                 |     |                  |                                     |     |
| --- | --- | --- | --------------------------------- | --------------- | --- | ---------------- | ----------------------------------- | --- |
|     |     |     | (cid:14)                          | (cid:2) (cid:1) | #   | (cid:1) (cid:18) | ‘ (cid:14)a P] (cid:18)Y b(cid:9) S |     |
(cid:1) (cid:1)
(cid:0)
!
In this 6 case simple transformations show that the matrix is spectrally equivalent to the
|        | (cid:1)                                 |     |     |             | (cid:25)   |     | (cid:0) |     |
| ------ | --------------------------------------- | --- | --- | ----------- | ---------- | --- | ------- | --- |
| matrix | . Theconclusionisobvious:wehavetochoose |     |     |             |            |     |         |     |
|        |                                         |     |     | (cid:24)" ! | (cid:14) 6 | # S |         |     |
(cid:1)
|                            |     |           | " !                                        |          |                   | ;                                 |                       |     |
| -------------------------- | --- | --------- | ------------------------------------------ | -------- | ----------------- | --------------------------------- | --------------------- | --- |
| Implementationprocedurefor |     |           | isverysimpleduetotheformulae               |          | (cid:16) (cid:17) |                                   | (cid:16) (cid:17)     |     |
|                            |     |           |                                            |          |                   |                                   | ; N                   |     |
|                            |     |           | "                                          | (cid:26) | (cid:26)          |                                   | (cid:26) 6            |     |
|                            |     |           | #                                          |          |                   | #                                 |                       |     |
|                            |     |   (cid:0) |                                            |          |                   |                                   | NZ #                  |     |
|                            |     |           | (cid:14) (cid:14)(cid:12)(cid:15) (cid:26) | " Z      | (cid:26) (cid:19) | (cid:14)(cid:12)(cid:15) (cid:26) | Z 6 (cid:19) (cid:18) |     |
|                            |     |           | (cid:26)                                   | (cid:26) | !                 | 6                                 | 6 Z (cid:26)          |     |
#
|     |     |     |     |     |     | (cid:2) | (cid:2) |     |
| --- | --- | --- | --- | --- | --- | ------- | ------- | --- |
(cid:1)
where
|     |     |     | 6 (cid:14)O | (cid:5) (cid:26) ! (cid:12) |     | 6 Z (cid:14)a | (cid:5) ! (cid:26) (cid:12)’ S |     |
| --- | --- | --- | ----------- | --------------------------- | --- | ------------- | ------------------------------ | --- |
#
|     |     |     | (cid:2) |                 | and | (cid:2) |                 |           |
| --- | --- | --- | ------- | --------------- | --- | ------- | --------------- | --------- |
|     |     |     |         | (cid:3) (cid:1) |     |         | (cid:4) (cid:1) |   (cid:0) |
, ,
Proposition2 Under the assumptions ) Z ) made, (cid:27) the eigenvalues of the matrix Z (cid:26) belong to (cid:27)
|     |     |     | (cid:18) # * (cid:18) | (cid:18) * (cid:18) |     |     | (cid:18) # (cid:19) (cid:18) | (cid:18) (cid:19) (cid:18) |
| --- | --- | --- | --------------------- | ------------------- | --- | --- | ---------------------------- | -------------------------- |
the union of two segments (cid:23) (cid:31) 2 , & 2 with the end points &
| independentofthemesh |     |     | .   |     |     | ^   |     |     |
| -------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
^ ; ^ Z
(cid:27)
|     |     |     | (cid:18) # (cid:18) (cid:18) | (cid:18) |     |     |     |     |
| --- | --- | --- | ---------------------------- | -------- | --- | --- | --- | --- |
Remark2 The values of , , & and 6 from Proposition (cid:8) (cid:10) (cid:14)a P] (cid:18)c 2 b depend on the constants of
|                     |     | "   |           |     | (cid:1) | (cid:1)   | ‘   |     |
| ------------------- | --- | --- | --------- | --- | ------- | --------- | --- | --- |
| spectralequivalence |     | and | ,aswellas |     | and     | (cid:0) , | .   |     |
Acknowledgments: This work was partially supported by NSF (grant CCR-9902035)
andbyLosAlamosComputerScienceInstitute(LASCI).TheauthorthanksK.Lipnikovfor
providingthenumericalexperimentsandtechnicalassistance.
References
[BPX90]JamesH.Bramble,JosephE.Pasciak,andJinchaoXu. Parallelmultilevelprecondi-
|     | tioners. (cid:1) Math.Comp.,55:1–22,1990. |     |     |     |     |     |     |     |
| --- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
[DGH 92]Q.V.Dihn,R.Glowinski,J.He,V.Kwock,T.W.Pan,andJ.Pe´riaux. Lagrange
multiplierapproachtofictitiousdomainmethods: Applicationtofluiddynamicsandelec-
tromagnetics. In David E. Keyes, Tony F. Chan, Ge´rard A. Meurant, Jeffrey S. Scroggs,
and Robert G. Voigt, editors, Fifth International Symposium on Domain Decomposition
MethodsforPartialDifferentialEquations,pages151–194,Philadelphia,PA,1992.SIAM.

DOMAINDECOMPOSITIONANDFICTITIOUSDOMAINMETHODS 75
[GHJ
(cid:1)
97]R.Glowinski,T.I.Hesla,D.D.Joseph,T.W.Pan,andJ.Periaux. DistributedLa-
grangemultipliermethodsforparticulateflows. InM.O.Bristeau,G.J.Etgen,W.Fitzgib-
bon,J.L.Lions,J.Periaux,andM.F.Wheeler,editors,ComputationalScienceforthe21st
Century,pages270–279,Chichester,1997.Wiley.
[GK98]RolandGlowinskiandYuriKuznetsov. OnthesolutionoftheDirichletproblemfor
linearellipticoperatorsbyadistributedLagrangemultipliermethod. C.R.Acad.Sci.Paris
Se´r.IMath.,327(7):693–698,1998.
[Kuz97]Yuri. A. Kuznetsov. Overlapping domain decomposition with non matching grids.
In Petter E. Bjørstad, Magne Espedal, and David Keyes, editors, Domain Decomposition
MethodsinSciencesandEngineering.J.Wiley,1997. ProceedingsfromtheNinthInterna-
tionalConference,June1996,Bergen,Norway.
[Kuz00]Yuri A. Kuznetsov. New iterative methods for singular perturbed positive definite
matrices. RussianJ.Numer.Anal.Math.Modelling,15:65–71,2000.
[Sau63]Valerij K. Saul’ev. On solution of some boundary value problems on high perfor-
mancecomputersbyfictitiousdomainmethod. SiberianMath.J.,4(4):912–925,1963. (in
Russian).
[Wid87]Olof B. Widlund. An extension theorem for finite elementspaces with three appli-
cations. In Wolfgang Hackbusch and Kristian Witsch, editors, Numerical Techniques in
ContinuumMechanics,pages110–122,Braunschweig/Wiesbaden,1987.NotesonNumer-
icalFluidMechanics,v.16,Friedr.ViewegundSohn. ProceedingsoftheSecondGAMM-
Seminar,Kiel,January,1986.
