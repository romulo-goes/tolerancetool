import json
import os
import DESops as d
import sys
import time
from DESops.automata.automata import State_or_StateSet
from itertools import combinations
from DESops.basic_operations.construct_complement import construct_complement
from collections import deque


#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
#
import tol_inv_property as t

def parallel(*automata: d.DFA) -> d.DFA:
	"""
	Computes the parallel composition of 2 (or more) Automata in a BFS manner, and returns the resulting composition as a new Automata.
	"""

	G1 = automata[0]
	input_list = automata[1:]

	if any(i.vcount() == 0 for i in automata):
		# if any inputs are empty, return empty automata
		return d.DFA()

	for G2 in input_list:
		G_out = d.NFA()
		
		G1_x0 = G1.vs[0]
		G2_x0 = G2.vs[0]
		G_out_vertices = [{
				"name": (G1_x["name"], G2_x["name"]),
				"marked": G1_x["marked"] and G2_x["marked"],
			} for G1_x in G1.vs for G2_x in G2.vs]
		# print(G_out_vertices)
		G_out_vertices = [
		    {
		        "name": (G1_x0["name"], G2_x0["name"]),
		        "marked": G1_x0["marked"] and G2_x0["marked"],
		    }
		]
		G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		G_out_edges = []  # type: List[Dict[str, Any]]

		# queue = deque([(G1_x, G2_x) for G1_x in G1.vs for G2_x in G2.vs])
		queue = deque([(G1_x0, G2_x0)])
		private_G1 = G1.events - G2.events
		private_G2 = G2.events - G1.events

		while len(queue) > 0:
			x1, x2 = queue.popleft()
			active_x1 = {e[1]: e[0] for e in x1["out"]}
			active_x2 = {e[1]: e[0] for e in x2["out"]}
			active_both = set(active_x1.keys()) & set(active_x2.keys())
			cur_name = (x1["name"], x2["name"])
			src_index = G_out_names[cur_name]

			for e in set(active_x1.keys()) | set(active_x2.keys()):
				st1 = st2 = []
				if e in active_both:
					st1 = [st for (st,ev) in x1['out'] if ev == e]
					st2 = [st for (st,ev) in x2['out'] if ev == e]
					for x1_d_id in st1:
						for x2_d_id in st2:
							x1_dst = G1.vs[x1_d_id]
							x2_dst = G2.vs[x2_d_id]
							dst_name = (x1_dst["name"], x2_dst["name"])
							dst_index = G_out_names.get(dst_name)

							if dst_index is None:
								G_out_vertices.append(
									{
										"name": dst_name,
										"marked": x1_dst["marked"] and x2_dst["marked"],
									}
								)
								dst_index = len(G_out_vertices) - 1
								G_out_names[dst_name] = dst_index
								queue.append((x1_dst, x2_dst))

							G_out_edges.append({"pair": (src_index, dst_index), "label": e})
					
				elif e in private_G1:
					st1 = [st for (st,ev) in x1['out'] if ev == e]
					x2_dst = x2
					for x1_d_id in st1:
						x1_dst = G1.vs[x1_d_id]
						dst_name = (x1_dst["name"], x2_dst["name"])
						dst_index = G_out_names.get(dst_name)

						if dst_index is None:
							G_out_vertices.append(
								{
									"name": dst_name,
									"marked": x1_dst["marked"] and x2_dst["marked"],
								}
							)
							dst_index = len(G_out_vertices) - 1
							G_out_names[dst_name] = dst_index
							queue.append((x1_dst, x2_dst))

						G_out_edges.append({"pair": (src_index, dst_index), "label": e})	
				elif e in private_G2:
					x1_dst = x1
					st2 = [st for (st,ev) in x2['out'] if ev == e]
					
					for x2_d_id in st2:
						x2_dst = G2.vs[x2_d_id]
						dst_name = (x1_dst["name"], x2_dst["name"])
						dst_index = G_out_names.get(dst_name)

						if dst_index is None:
							G_out_vertices.append(
								{
									"name": dst_name,
									"marked": x1_dst["marked"] and x2_dst["marked"],
								}
							)
							dst_index = len(G_out_vertices) - 1
							G_out_names[dst_name] = dst_index
							queue.append((x1_dst, x2_dst))

						G_out_edges.append({"pair": (src_index, dst_index), "label": e})
				else:
					continue
				

		G_out.add_vertices(
			len(G_out_vertices),
			[v["name"] for v in G_out_vertices],
			[v["marked"] for v in G_out_vertices],
		)
		G_out.add_edges(
			[e["pair"] for e in G_out_edges],
			[e["label"] for e in G_out_edges],
			fill_out=True,
		)
		G_out.events = G1.events | G2.events
		G_out.Euc.update(G1.Euc | G2.Euc)
		G_out.Euo.update(G1.Euo | G2.Euo)

		G1 = G_out

	return G_out


# Env = d.read_fsm(path_script+"/protocol.fsm")

ch1 = d.read_fsm(path_script+"/ch1.fsm")
ch2 = d.read_fsm(path_script+"/ch2.fsm")
ch3 = d.read_fsm(path_script+"/ch3.fsm")
ch4 = d.read_fsm(path_script+"/ch4.fsm")
N = d.read_fsm(path_script+"/network.fsm")
A = d.read_fsm(path_script+"/peerA.fsm")
B = d.read_fsm(path_script+"/peerB.fsm")

C = parallel(A,B,N,ch2,ch3,ch4)

d.write_fsm(path_script+"/comp.fsm",C)

# Unsafe = ['err']
all_edges_1 = [(src.index,e,tgt.index,0) for src in ch1.vs for tgt in ch1.vs for e in ch1.events if (tgt.index,e) not in src['out']]
# all_edges_2 = [(src.index,e,tgt.index,1) for src in ch2.vs for tgt in ch2.vs for e in ch2.events if (tgt.index,e) not in src['out']]
all_edges = list(all_edges_1)
# all_edges.extend(all_edges_2)
# print(len(all_edges))
sat = []
stack = deque()
stack.append(all_edges)
while stack:
	print(len(stack),len(sat))
	it = stack.popleft()
	if any(set(it).issubset(set(e)) for e in sat):
		print('already checked')
	else:
		edges_1 = [(i[0],i[2]) for i in it if i[3]==0]
		labels_1 = [(i[1]) for i in it if i[3]==0]
		# edges_2 = [(i[0],i[2]) for i in it if i[3]==1]
		# labels_2 = [(i[1]) for i in it if i[3]==1]
		NG1 = d.NFA(ch1)
		NG1.add_edges(edges_1,labels_1,fill_out= True)
		# NG2 = d.NFA(ch2)
		# NG2.add_edges(edges_2,labels_2,fill_out= True)
		ctr_env = parallel(C,NG1)
		unsafe = {st.index for st in ctr_env.vs if 'closed'==st['name'][0][0][0][0][0][0] and 'Estab'==st['name'][0][0][0][0][0][1]}
		# print(ctr_env)
		# inacc = d.basic_operations.unary.find_inacc(ctr_env)
		# print(inacc)
		# print(unsafe)
		if not unsafe:
			sat.append(it)
		else:
			# start = time.time()
			comb = list(combinations(it, len(it)-1))
			[stack.append(ed) for ed in comb if ed not in stack]
			# print(time.time()-start)

# for i,it in enumerate(sat):
# 	edges_S = [(i[0],i[2]) for i in it if i[3]==0]
# 	labels_S = [(i[1]) for i in it if i[3]==0]
# 	edges_A = [(i[0],i[2]) for i in it if i[3]==1]
# 	labels_A = [(i[1]) for i in it if i[3]==1]
# 	NG = d.NFA(S)
# 	NG.add_edges(edges_S,labels_S,fill_out= True)
# 	d.write_fsm(path_script+'/satS'+str(i)+'.fsm',NG)
# 	NGA = d.NFA(A)
# 	NGA.add_edges(edges_A,labels_A,fill_out= True)
# 	d.write_fsm(path_script+'/satA'+str(i)+'.fsm',NGA)
# 	ctr_env = parallel(NG,NGA,P,controller)
# 	inacc = d.basic_operations.unary.find_inacc(ctr_env)
# 	print(inacc)
# 	d.write_fsm(path_script+'/ctr'+str(i)+'.fsm',ctr_env)

	



# BOTTOM UP APPROACH
# Unsafe = ['err']
# Unsafe = {st.index for st in Env.vs if st['name'] in Unsafe}

# sat = []
# unsat = []
# events = [d.Event('s')]
# states = ['E','S','A','SA']
# states_ids = []
# for st in states:
# 	vertex = Env.vs.select(name_in = [st+'I',st+'O'])
# 	id = []
# 	for v in vertex:
# 		id.append(v.index)
# 	print(id)
# 	states_ids.append(id)
# print(states_ids)
# all_edges = []
# for src in states_ids:
# 	for tgt in states_ids:
		
# 		for e in events:
# 			li = []
# 			if (tgt[0],e) not in Env.vs[src[0]]['out']:
# 				li.append((src[0],e,tgt[0]))
# 			if (tgt[0],e) not in Env.vs[src[1]]['out']:
# 				li.append((src[1],e,tgt[0]))
# 			if (tgt[1],e) not in Env.vs[src[0]]['out']:
# 				li.append((src[0],e,tgt[1]))
# 			if (tgt[1],e) not in Env.vs[src[1]]['out']:
# 				li.append((src[1],e,tgt[1]))
# 			if li:
# 				all_edges.append(li)
# print(len(all_edges))
# print(all_edges)
# states = [st.index for st in Env.vs if st['name']+'I' or st['name']+'O' in states]


# # all_edges = [(src,e,tgt) for src in states for tgt in states for e in events if (tgt,e) not in Env.vs[src]['out']]
# print(len(all_edges))

# for n_edges in range(len(all_edges)):	
# 	comb_edges = list(combinations(all_edges, n_edges))
# 	print(n_edges,len(comb_edges))
# 	level_all_unsat = 0
# 	for it in comb_edges:
# 		it = [item for sublist in it for item in sublist]
# 		if any(set(e).issubset(set(it)) for e in unsat):
# 			# print('already unsat')
# 			level_all_unsat +=1
# 		else:
# 			edges = [(i[0],i[2]) for i in it]
# 			labels = [(i[1]) for i in it]
# 			NG = d.NFA(Env)
# 			NG.add_edges(edges,labels,fill_out= True)
# 			ctr_env = parallel(NG,controller)
# 			unsafe = {st.index for st in ctr_env.vs if 'err' in st['name']}
# 			# print(ctr_env)
# 			inacc = d.basic_operations.unary.find_inacc(ctr_env)
# 			# print(inacc)
# 			# print(unsafe)
# 			if unsafe.issubset(set(inacc)):
# 				sat.append(it)
# 			else:
# 				unsat.append(it)
# 				level_all_unsat +=1
# 	if level_all_unsat == len(comb_edges):
# 		print('reached an unsat level',n_edges,len(all_edges))
# 		break
# print(len(sat))
# unique = []
# for j in range(len(sat)):
# 	# comp = []
# 	# print(comp,not any(comp))
# 	if not any(set(sat[j]).issubset(set(sat[i])) for i in range(j+1,len(sat))):
# 		unique.append(sat[j])
# print(len(unique))		
# for i,it in enumerate(unique):
# 	edges = [(i[0],i[2]) for i in it]
# 	labels = [(i[1]) for i in it]
# 	NG = d.NFA(Env)
# 	NG.add_edges(edges,labels,fill_out= True)
# 	d.write_fsm(path_script+'/sat'+str(i)+'.fsm',NG)


#STACK METHOD TOP DOWN
# stack = deque()
# stack.append(all_edges)
# while stack:
# 	print(len(stack),len(sat))
# 	it = stack.popleft()
# 	if any(set(it).issubset(set(e)) for e in sat):
# 		print('already checked')
# 	else:
# 		edges = [(i[0],i[2]) for i in it]
# 		labels = [(i[1]) for i in it]
# 		NG = d.NFA(Env)
# 		NG.add_edges(edges,labels,fill_out= True)
# 		ctr_env = parallel(NG,controller)
# 		unsafe = {st.index for st in ctr_env.vs if 'err' in st['name']}
# 		# print(ctr_env)
# 		inacc = d.basic_operations.unary.find_inacc(ctr_env)
# 		# print(inacc)
# 		# print(unsafe)
# 		if unsafe.issubset(set(inacc)):
# 			sat.append(it)
# 		else:
# 			start = time.time()
# 			comb = list(combinations(it, len(it)-1))
# 			[stack.append(ed) for ed in comb if ed not in stack]
# 			print(time.time()-start)