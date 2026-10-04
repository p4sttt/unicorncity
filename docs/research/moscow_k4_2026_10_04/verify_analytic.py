"""Exact rational arithmetic checks; universal proof still requires the written reasoning.
Standard-library-only. Verifies algebraic identities at rational inputs, stated
vertex values, spanning-tree enumeration and the construction on finite fixtures.
"""
from fractions import Fraction as Q
from itertools import combinations
from pathlib import Path
import json, random
ROOT=Path(__file__).resolve().parent
EDGES=list(combinations(range(4),2)); IDX={e:i for i,e in enumerate(EDGES)}
def edge(a,b):return IDX[tuple(sorted((a,b)))]
def det(M):
 if not M:return Q(1)
 return sum(((-1)**j*M[0][j]*det([[M[i][k] for k in range(len(M)) if k!=j] for i in range(1,len(M))]) for j in range(len(M))),Q(0))
def lap(w,T):
 L=[[Q(0) for j in range(3)] for i in range(3)]
 for e in T:
  a,b=EDGES[e];v=[Q(int(a==i)-int(b==i)) for i in range(3)]
  for i in range(3):
   for j in range(3):L[i][j]+=w[e]*v[i]*v[j]
 return L
TREES=[T for T in combinations(range(6),3) if det(lap([Q(1)]*6,T))]
assert len(TREES)==16
THRESHOLD=Q(5,8); LAMBDA=Q(24,5); FACTOR=Q(29,5)
def F(t,l,p,q):
 P=p+q;R=1/p+1/q
 return l*(l-1)-t*(l+3)-P-l*t*R-(P+2*t)**2/(l-t-P)
def schur_exact(t,l,p,q):
 # Congruence by diag(sqrt(p),sqrt(q),1) removes radicals.
 E=[[(l-t)*p-p*p,-p*q],[-p*q,(l-t)*q-q*q]]
 d=[p+t,q+t];gamma=l-1-t/p-t/q
 de=det(E);assert E[0][0]>0 and de>0
 inv_quad=(E[1][1]*d[0]**2-2*E[0][1]*d[0]*d[1]+E[0][0]*d[1]**2)/de
 return (l-t)*(gamma-inv_quad)
vertices=[]
for p,q in [(THRESHOLD,THRESHOLD),(THRESHOLD,Q(1)),(Q(1),THRESHOLD),(Q(1),Q(1))]:
 z=F(THRESHOLD,LAMBDA,p,q)
 assert z==schur_exact(THRESHOLD,LAMBDA,p,q)>0
 vertices.append({'p':str(p),'q':str(q),'F':str(z)})
assert [v['F'] for v in vertices]==['8851/23400','14251/20400','14251/20400','8851/17400']
assert 1+3/THRESHOLD==FACTOR and 1+LAMBDA==FACTOR
assert LAMBDA-THRESHOLD-2==Q(87,40)>0
checks=0
for i in range(9):
 for j in range(9):
  p=THRESHOLD+(1-THRESHOLD)*Q(i,8);q=THRESHOLD+(1-THRESHOLD)*Q(j,8)
  assert F(THRESHOLD,LAMBDA,p,q)==schur_exact(THRESHOLD,LAMBDA,p,q)
  checks+=1
# Concavity rational identity: ((P+2t)^2/(l-t-P))''=2(l+t)^2/(l-t-P)^3>0.
# This formula is checked symbolically by polynomial coefficients below.
def poly_add(a,b):
 c=a.copy()
 for e,v in b.items():c[e]=c.get(e,Q(0))+v
 return {e:v for e,v in c.items() if v}
def poly_mul(a,b):
 c={}
 for e,v in a.items():
  for f,w in b.items():c[e+f]=c.get(e+f,Q(0))+v*w
 return {e:v for e,v in c.items() if v}
# q'' numerator: 2D^2+4ND+2N^2=2(D+N)^2=2(l+t)^2, N=P+2t,D=l-t-P.
N={1:Q(1),0:2*THRESHOLD};D={1:Q(-1),0:LAMBDA-THRESHOLD}
num=poly_add(poly_add({e:2*v for e,v in poly_mul(D,D).items()},{e:4*v for e,v in poly_mul(N,D).items()}),{e:2*v for e,v in poly_mul(N,N).items()})
assert num=={0:2*(LAMBDA+THRESHOLD)**2}
def path_edges(T,start,goal):
 def dfs(v,prev,path):
  if v==goal:return path
  for e in T:
   if v in EDGES[e]:
    other=EDGES[e][0]+EDGES[e][1]-v
    if other!=prev:
     r=dfs(other,v,path+[e])
     if r is not None:return r
 return dfs(start,-1,[])
def choose(w,T):
 degree=[sum(v in EDGES[e] for e in T) for v in range(4)]
 if max(degree)==3:return T,'maximum_star'
 v=[degree.index(1)];prev=-1
 while len(v)<4:
  neighbors=[EDGES[e][0]+EDGES[e][1]-v[-1] for e in T if v[-1] in EDGES[e] and EDGES[e][0]+EDGES[e][1]-v[-1]!=prev]
  prev=v[-1];v.append(neighbors[0])
 x,y,z=[w[edge(v[i],v[i+1])] for i in range(3)]
 a,b,c=[w[edge(v[i],v[j])] for i,j in [(0,2),(1,3),(0,3)]]
 assert a<=min(x,y) and b<=min(y,z) and c<=min(x,y,z)
 if b/z>=THRESHOLD:center=v[1];branch='switch_b'
 elif a/x>=THRESHOLD:center=v[2];branch='switch_a'
 else:return T,'retain_path'
 return tuple(sorted(edge(center,j) for j in range(4) if j!=center)),branch
def verify_fixture(name,w):
 w=list(map(Q,w));G=lap(w,range(6));score=[sum(w[e] for e in T) for T in TREES]
 maxscore=max(score);records=[]
 for T,s in zip(TREES,score):
  if s!=maxscore:continue
  for e in range(6):
   if e not in T:assert w[e]<=min(w[f] for f in path_edges(T,*EDGES[e]))
  S,branch=choose(w,T);LT=lap(w,S)
  M=[[FACTOR*LT[i][j]-G[i][j] for j in range(3)] for i in range(3)]
  minors=[]
  for k in [1,2,3]:
   for J in combinations(range(3),k):
    z=det([[M[i][j] for j in J] for i in J]);assert z>=0;minors.append(str(z))
  records.append({'maximum_tree':list(T),'chosen_tree':list(S),'branch':branch,'all_principal_minors':minors})
 return {'name':name,'weights':list(map(str,w)),'checks':records}
fixtures=[('uniform',[1]*6),('maximum_star',[10,10,10,1,1,1]),('switch_b',[10,1,1,10,7,10]),('switch_a',[10,7,1,10,1,10]),('retain_path',[10,1,1,10,1,10]),('unique_maximum_product_path',[Q(11,10),1,1,Q(11,10),1,Q(11,10)]),('symmetric_near_hard',[1,Q(5,9),1,1,Q(5,9),1]),('five_edge_limit',[Q(2,3),1,1,1,1,Q(1,1000000)])]
rng=random.Random(20261004)
fixtures += [('rational_'+str(i),[Q(rng.randint(1,30),rng.randint(1,9)) for _ in range(6)]) for i in range(32)]
R={'scope':'Exact finite arithmetic checks, not a replacement for the universal analytic proof.','threshold':str(THRESHOLD),'off_tree_norm_squared_bound':str(LAMBDA),'support_factor':str(FACTOR),'vertices':vertices,'schur_identity_rational_grid_checks':checks,'concavity_polynomial_identity':True,'tree_count':len(TREES),'trees':[list(t) for t in TREES],'fixtures':[verify_fixture(*f) for f in fixtures]}
R['all_checks_passed']=True
(ROOT/'analytic_verification.json').write_text(json.dumps(R,indent=2)+'\n')
branches=sorted({c['branch'] for f in R['fixtures'] for c in f['checks']})
print(json.dumps({'all_checks_passed':True,'vertices':vertices,'fixture_count':len(fixtures),'all_maximum_tree_choices_checked':sum(len(f['checks']) for f in R['fixtures']),'branches_covered':branches,'rational_schur_checks':checks},indent=2))
