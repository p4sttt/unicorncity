import json
from pathlib import Path
import numpy as np
from explore import record, vals, nelder
out=Path(__file__).resolve().parent

def main():
 R2={'families':{},'counterexamples':{}}
 def add(name,w):R2['families'][name]=record(np.array(w,dtype=float))
 t=(np.sqrt(17)-3)/2
 for x in [0.000001,.1,t,.9,1,1/t,10]:add('cycle_diagonal_'+str(x),[1,x,1,1,x,1])
 R2['counterexamples']['unique_maximum_product_path']=record(np.array([1.1,1,1,1.1,1,1.1]))
 for x in [.1,.5,1,2,10,100]:add('five_edge_shared_'+str(x),[x,1,1,1,1,1e-12])
 def fun5(x):return -vals(np.r_[np.exp(np.r_[x,0.]),1e-12]).min()
 rng=np.random.default_rng(913)
 starts=rng.uniform(-8,8,(2000,4)); starts=starts[np.argsort([fun5(x) for x in starts])[:6]]
 cs=[nelder(fun5,x,niter=1000) for x in starts]
 x=min(cs,key=fun5)
 R2['five_edge_optimized']=record(np.r_[np.exp(np.r_[x,0.]),1e-12])
 R2['five_edge_sharp_fixture']=record(np.array([2/3,1,1,1,1,1e-12]))
 R2['counterexamples']['unique_maximum_product_path']['maximum_product_path_factor']=(41+20*np.sqrt(2))/11
 print(json.dumps({key:{k:({'best':v['best'],'best_stars':v['best_stars'],'weights':v['weights']} if 'best' in v else v) for k,v in value.items()} if key!='five_edge_optimized' else value for key,value in R2.items()},indent=2))
 (out/'followup.json').write_text(json.dumps(R2,indent=2)+'\n')

if __name__=='__main__':
 main()
