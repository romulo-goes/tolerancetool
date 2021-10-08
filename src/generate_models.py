import os
import DESops as d
import sys
from itertools import combinations
import json
import tol_inv_property as t
#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'


def create_SMV_file(G, model_fname):
	with open(model_fname, "w") as f:

		print("MODULE control(state)\n\tVAR action:{a,b};", file=f)
		print("ASSIGN", file = f)
		print("init(action):=b;",file=f)
		print("next(action):=b;",file = f)
		print("MODULE main\n\tVAR", file=f)
		print("\tstate: 0..{0};".format(G.vcount()), file=f)
		print("\tctr: control(next(state));".format(G.vcount()), file=f)
		print("ASSIGN", file=f)
		print('\tinit(state):=0;',file=f)
		print("\tnext(state):= case",file=f)
		for st in G.vs:
			out = dict()
			for (tgt,ev) in st['out']:
				if ev not in out.keys():
					out[ev] = frozenset({tgt})
				else:
					out[ev] = frozenset.union(out[ev],frozenset({tgt}))
			for key in out.keys():
				print("\t\tstate={0} & ctr.action = {1}:{2};".format(st.index,key,set(out[key])),file=f)
		print("\t\tTRUE:{0};".format(G.vcount()),file=f)
		print("\tesac;",file=f)
		f.close()


Env = d.read_fsm(path_script[0:path_script.find('tolerancetool')]+"tolerancetool/examples/Comparison tools/T2.fsm")
all_edges = [(src,e, tgt) for src in range(Env.vcount()) for tgt in range(Env.vcount()) for e in Env.events if (tgt,e) not in Env.vs[src]['out']]
print(Env.vcount(),len(all_edges),all_edges)
n = 1
f = {'1':('b',),'2':tuple(),'3':('b',),'4':('b',)}
Unsafe = ['3']
Unsafe = {st.index for st in Env.vs if st['name'] in Unsafe}
print(Unsafe)
safe = []
for i in range(len(all_edges)):
	# print(i,len(all_edges))
	comb = combinations(all_edges, i)
	for it in comb:
		print(n)
		with open(path_script[0:path_script.find('tolerancetool')]+'tolerancetool/examples/Comparison tools/perturbations T2/d'+str(n)+'.json', 'w') as f:
			json.dump([(i[0],i[1].label,i[2]) for i in it], f)
		edges = [(i[0],i[2]) for i in it]
		labels = [(i[1]) for i in it]
		NG = d.NFA(Env)
		NG.add_edges(edges,labels,fill_out= True)
		# NGf = t.Control(NG,f)
		# inacc = d.basic_operations.unary.find_inacc(NGf)
		# if Unsafe.issubset(set(inacc)):
		# 	safe.append(it)
		create_SMV_file(NG,path_script[0:path_script.find('tolerancetool')]+'tolerancetool/examples/Comparison tools/models T2/T'+str(n)+'.smv')
		n+=1


