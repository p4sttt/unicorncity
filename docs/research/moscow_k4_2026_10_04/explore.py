import json,itertools,time
import numpy as np
from pathlib import Path
out=Path(__file__).resolve().parent
E=list(itertools.combinations(range(4),2))
B=np.zeros((3,6))
for j,(a,b) in enumerate(E):
 if a<3:B[a,j]=1
 if b<3:B[b,j]=-1
T=np.array([t for t in itertools.combinations(range(6),3) if abs(np.linalg.det(B[:,t]))>.5])
C=np.array([np.linalg.solve(B[:,t],B) for t in T])
star=np.array([max(np.bincount(np.array([E[e] for e in t]).ravel(),minlength=4))==3 for t in T])
def vals(w):
 wt=w[T]
 K=np.einsum('tik,k,tjk->tij',C,w,C)/np.sqrt(wt[:,:,None]*wt[:,None,:])
 ev=np.linalg.eigvalsh(K)
 return ev[:,-1]
def record(w):
 v=vals(w); best=np.min(v); active=np.flatnonzero(v<best+1e-5*max(1,best))
 return {'weights':w.tolist(),'best':float(best),'best_stars':float(v[star].min()),'active_trees':[T[i].tolist() for i in active], 'all_values':v.tolist()}
def f(x):return -vals(np.exp(np.r_[x,0.])).min()
def nelder(fun,x,step=.6,niter=1200):
 S=np.vstack([x,x+np.eye(len(x))*step]); y=np.array([fun(z) for z in S])
 for it in range(niter):
  order=np.argsort(y);S=S[order];y=y[order];c=S[:-1].mean(axis=0)
  if np.ptp(y)<1e-11 and np.max(abs(S-S[0]))<1e-7:break
  xr=2*c-S[-1];yr=fun(xr)
  if yr<y[0]:
   xe=3*c-2*S[-1];ye=fun(xe)
   S[-1],y[-1]=(xe,ye) if ye<yr else (xr,yr)
  elif yr<y[-2]: S[-1],y[-1]=xr,yr
  else:
   xc=c+.5*((xr if yr<y[-1] else S[-1])-c);yc=fun(xc)
   if yc<min(yr,y[-1]):S[-1],y[-1]=xc,yc
   else:
    S[1:]=S[0]+.5*(S[1:]-S[0]);y[1:]=[fun(z) for z in S[1:]]
 return S[np.argmin(y)]

def main():
 R={'edges':E,'trees':T.tolist(),'star_indices':np.flatnonzero(star).tolist(),'cases':{}}
 R['cases']['uniform']=record(np.ones(6))
 for eps in [1e-2,1e-6]:
  w=np.ones(6); w[-1]=eps
  R['cases']['five_edges_equal_eps'+str(eps)]=record(w)
 print(json.dumps(R['cases'],indent=2),flush=True)
 R['search']=[]
 rng=np.random.default_rng(17029)
 for bound in [3,8,14]:
  start=time.time()
  starts=rng.uniform(-bound,bound,(3000,5)); scores=np.array([f(x) for x in starts])
  starts=starts[np.argsort(scores)[:8]]
  def bounded(x):
   if np.max(abs(x))>30:return 100+np.max(abs(x))
   return f(x)
  candidates=[nelder(bounded,x) for x in starts]
  x=min(candidates,key=f)
  row=record(np.exp(np.r_[x,0.]))
  row.update({'bound':bound,'seed':17029,'seconds':time.time()-start,'logweights':x.tolist()})
  R['search'].append(row)
  print(json.dumps({'bound':bound,'best':row['best'],'weights':row['weights'],'best_stars':row['best_stars'],'active_trees':row['active_trees'],'seconds':row['seconds']}),flush=True)
 (out/'results.json').write_text(json.dumps(R,indent=2)+'\n')

if __name__=='__main__':
 main()
