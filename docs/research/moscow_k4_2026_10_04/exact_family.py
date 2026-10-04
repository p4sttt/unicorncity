import itertools,json
from fractions import Fraction as Q
from pathlib import Path
# Sparse polynomials in lambda,t, exact rational coefficients.
def add(a,b):
 c=a.copy()
 for e,v in b.items():c[e]=c.get(e,Q(0))+v
 return {e:v for e,v in c.items() if v}
def mul(a,b):
 c={}
 for e,v in a.items():
  for f,w in b.items():g=(e[0]+f[0],e[1]+f[1]);c[g]=c.get(g,Q(0))+v*w
 return {e:v for e,v in c.items() if v}
def neg(a):return {e:-v for e,v in a.items()}
def det(M):
 if len(M)==1:return M[0][0]
 a={}
 for j in range(len(M)):
  z=mul(M[0][j],det([[M[i][k] for k in range(len(M)) if k!=j] for i in range(1,len(M))]))
  a=add(a,neg(z) if j%2 else z)
 return a
E=list(itertools.combinations(range(4),2));d={1,4}
B=[]
for a,b in E:B.append([(1 if a==i else -1 if b==i else 0) for i in range(3)])
def lap(T):
 return [[sum_poly([{(0,int(e in d)):Q(B[e][i]*B[e][j])} for e in T]) for j in range(3)] for i in range(3)]
def sum_poly(ps):
 a={}
 for p in ps:a=add(a,p)
 return a
L=lap(range(6));results={};orbit_polynomials={}
for T in itertools.combinations(range(6),3):
 LT=lap(T)
 if not det(LT):continue
 degree=[sum(v in E[e] for e in T) for v in range(4)]
 typ=('star' if max(degree)==3 else 'path')+'_'+str(len(set(T)&d))+'_diagonals'
 p=det([[add(mul({(1,0):Q(1)},LT[i][j]),neg(L[i][j])) for j in range(3)] for i in range(3)])
 if typ not in results:results[typ]={'tree':T,'poly':{str(e):str(v) for e,v in p.items()},'count':0}
 assert results[typ]['poly']=={str(e):str(v) for e,v in p.items()}
 results[typ]['count']+=1
 orbit_polynomials[typ]=p
# Explicit factorization assertions in the exact polynomial ring Q[lambda,t].
one={(0,0):Q(1)};lam={(1,0):Q(1)};tp={(0,1):Q(1)}
def scale(a,x):return {e:v*x for e,v in a.items()}
def sub(a,b):return add(a,neg(b))
star_factor=mul(mul(sub(lam,one),sub(lam,add(scale(one,2),scale(tp,2)))),sub(mul(tp,lam),add(scale(tp,2),scale(one,2))))
path0_factor=mul(sub(lam,add(one,tp)),add(sub(mul(lam,lam),mul(add(scale(one,5),scale(tp,3)),lam)),add(scale(one,4),scale(tp,4))))
path2_factor=mul(sub(mul(tp,lam),add(tp,one)),add(sub(mul(tp,mul(lam,lam)),mul(add(scale(tp,5),scale(one,3)),lam)),add(scale(tp,4),scale(one,4))))
assert orbit_polynomials['star_1_diagonals']==star_factor
assert orbit_polynomials['path_0_diagonals']==path0_factor
assert orbit_polynomials['path_2_diagonals']==path2_factor
assert orbit_polynomials['path_1_diagonals']==sub(star_factor,mul(tp,mul(lam,lam)))
assert len(results)==4 and all(v['count']==4 for v in results.values())
results['_verification']={'all_checks_passed':True,'tree_count':16,'orbit_count':4,'trees_per_orbit':4,'star_factorization':True,'path0_factorization':True,'path2_factorization':True,'path1_equals_star_minus_t_lambda_squared':True,'arithmetic':'exact rational sparse bivariate polynomials'}
print(json.dumps(results,indent=2))
Path(__file__).resolve().with_name('exact_family.json').write_text(json.dumps(results,indent=2)+'\n')
