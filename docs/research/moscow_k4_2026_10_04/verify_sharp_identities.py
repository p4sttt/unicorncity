"""Exact polynomial clearing checks for the optional sharper algebraic constant."""
from fractions import Fraction as Q
from pathlib import Path
import json

def add(a,b):
 c=a.copy()
 for e,v in b.items():c[e]=c.get(e,Q(0))+v
 return {e:v for e,v in c.items() if v}
def neg(a):return {e:-v for e,v in a.items()}
def mul(a,b):
 c={}
 for e,v in a.items():
  for f,w in b.items():c[e+f]=c.get(e+f,Q(0))+v*w
 return {e:v for e,v in c.items() if v}
class RF:
 def __init__(self,n,d=None):
  self.n=n if isinstance(n,dict) else ({0:Q(n)} if n else {})
  self.d={0:Q(1)} if d is None else d
 @staticmethod
 def co(x):return x if isinstance(x,RF) else RF(x)
 def __add__(self,x):
  x=self.co(x);return RF(add(mul(self.n,x.d),mul(x.n,self.d)),mul(self.d,x.d))
 __radd__=__add__
 def __neg__(self):return RF(neg(self.n),self.d)
 def __sub__(self,x):return self+-self.co(x)
 def __rsub__(self,x):return self.co(x)+-self
 def __mul__(self,x):
  x=self.co(x);return RF(mul(self.n,x.n),mul(self.d,x.d))
 __rmul__=__mul__
 def __truediv__(self,x):
  x=self.co(x);assert x.n;return RF(mul(self.n,x.d),mul(self.d,x.n))
 def __rtruediv__(self,x):return self.co(x)/self
 def __pow__(self,n):
  assert n>=0
  r=RF(1)
  for _ in range(n):r=r*self
  return r

def F(t,k,p,q):
 P=p+q;R=1/p+1/q
 return k*(k-1)-t*(k+3)-P-k*t*R-(P+2*t)**2/(k-t-P)
k=RF({1:Q(1)});t=3/k;poly=k**3-3*k**2-9*k+3
forms=[('tt',F(t,k,t,t),(k*k-3)*poly/(k*(k-3)*(k+3))),('11',F(t,k,RF(1),RF(1)),(k*k-3)*poly/(k*(k-3)*(k+1))),('t1',F(t,k,t,RF(1)),(k*k-3)*poly/(k*(k-3)*(k+2))+(k-3)/(k+2))]
checks=[]
for name,lhs,rhs in forms:
 residual=add(mul(lhs.n,rhs.d),neg(mul(rhs.n,lhs.d)))
 assert residual=={}
 checks.append({'vertex':name,'cleared_residual_zero':True})
def q(x):return x**3-3*x*x-9*x+3
lo,hi=Q(19,4),Q(24,5)
assert q(lo)<0<q(hi)
# Q'(k)=3((k-1)^2-4)>0 for k>3, so one root on this interval.
assert 3*((lo-1)**2-4)>0
assert lo-3/lo-2>0 and 0<3/hi<3/lo<1
# Identity Q(1+4c)=16(4c^3-3c)-8, so c=cos(pi/9) makes Q zero.
c=RF({1:Q(1)});v=1+4*c
res=(v**3-3*v*v-9*v+3)-(16*(4*c**3-3*c)-8)
assert res.n=={}
R={'scope':'Exact rational polynomial identities. Analytic proof supplies concavity and positive denominators.','all_checks_passed':True,'cleared_identities':checks,'root_isolation':{'lower':str(lo),'upper':str(hi),'Q_lower':str(q(lo)),'Q_upper':str(q(hi)),'derivative_positive_for_k_above_3':True},'cosine_polynomial_identity':True,'constant':'2+4*cos(pi/9)','parameter':'t=3/k, k=C-1','rational_fallback':'29/5; see verify_analytic.py'}
Path(__file__).with_name('sharp_identities_verification.json').write_text(json.dumps(R,indent=2)+'\n')
print(json.dumps(R,indent=2))
