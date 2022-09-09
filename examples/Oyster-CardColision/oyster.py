import json
import os

from igraph.datatypes import TriadCensus
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

def parallel(*automata: d.NFA) -> d.NFA:
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
		# G_out_vertices = [{
		#         "name": (G1_x["name"], G2_x["name"]),
		#         "marked": G1_x["marked"] and G2_x["marked"],
		#     } for G1_x in G1.vs for G2_x in G2.vs]
		# G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		# G_out_edges = []  # type: List[Dict[str, Any]]

		# queue = deque([(G1_x, G2_x) for G1_x in G1.vs for G2_x in G2.vs])
		# G_out_vertices = [{
		# 		"name": (G1_x["name"], G2_x["name"]),
		# 		"marked": G1_x["marked"] and G2_x["marked"],
		# 	} for G1_x in G1.vs for G2_x in G2.vs]
		# print(G_out_vertices)
		G_out_vertices = [
		    {
		        "name": (G1_x0["name"], G2_x0["name"]),
		        "marked": G1_x0["marked"] and G2_x0["marked"],
		    }
		]
		G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		G_out_edges = []  # type: List[Dict[str, Any]]

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
	G_out.vs[0]['init'] = True
	return G_out


def parallel_error(*automata: d.NFA) -> d.NFA:
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
		# G_out_vertices = [{
		#         "name": (G1_x["name"], G2_x["name"]),
		#         "marked": G1_x["marked"] and G2_x["marked"],
		#     } for G1_x in G1.vs for G2_x in G2.vs]
		# G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		# G_out_edges = []  # type: List[Dict[str, Any]]

		# queue = deque([(G1_x, G2_x) for G1_x in G1.vs for G2_x in G2.vs])
		# G_out_vertices = [{
		# 		"name": (G1_x["name"], G2_x["name"]),
		# 		"marked": G1_x["marked"] and G2_x["marked"],
		# 	} for G1_x in G1.vs for G2_x in G2.vs]
		# print(G_out_vertices)
		G_out_vertices = [
		    {
		        "name": (G1_x0["name"], G2_x0["name"]),
		        "marked": G1_x0["marked"] and G2_x0["marked"],
		    },
			{
		        "name": 'err',
		        "marked": 1,
		    }
		]
		G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		G_out_edges = []  # type: List[Dict[str, Any]]

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
							if x2_dst['name'] == 'err':
								dst_name = 'err'
							else:
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
						if x2_dst['name'] == 'err':
							dst_name = 'err'
						else:
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
	G_out.vs[0]['init'] = True
	return G_out

def backward_error(A: d.NFA) -> d.NFA:
	error_states = [st.index for st in A.vs if 'err'in st['name']]
	transitions_to_del = []
	transitions = []
	check = True
	while check:
		check = False
		for st in A.vs:
			if st.index not in error_states:
				for (tgt, ev) in st['out']:
					if tgt in error_states and ev in A.Euc:
						error_states.append(st.index)
						check=True
					elif tgt in error_states:
						if (st.index,ev,tgt) not in transitions:
							l = A.es.select(_source_eq=st.index,_target_eq=tgt,label_eq=ev)
							# print(l[0])
							transitions.append((st.index,ev,tgt))
							transitions_to_del.append(l[0].index)
	
	# print(error_states)
	# print(transitions_to_del)
	# A.delete_edges(A.es.select())
	A.delete_edges(transitions_to_del)
	# print(d.unary.find_inacc(A).issubset(set(error_states)))
	A.delete_vertices(error_states)
	return A

def project(A: d.NFA,O: d.NFA) -> d.NFA:
	names = O.vs['name']
	# print(names)
	transitions_to_del = []
	for st in O.vs:
		states = [(s,s['name'].index(st['name'])) for s in A.vs if st['name'] in s['name']]
		# print(states)
		t = dict()
		for (s,i) in states:
			for (tgt, ev) in s['out']:
				if (A.vs[tgt]['name'][i],ev) not in t.keys():
					t[(A.vs[tgt]['name'][i],ev)]=1
				else:
					t[(A.vs[tgt]['name'][i],ev)]+=1
		
		remaining_trans = [i for i,j in t.items() if j == len(states)]
		# print(remaining_trans)
		for (tgt,ev) in st['out']:
			if (O.vs[tgt]['name'],ev) not in remaining_trans:
				l = O.es.select(_source_eq=st.index,_target_eq=tgt,label_eq=ev)
				# print(l[0])
				transitions_to_del.append(l[0].index)
	O.delete_edges(transitions_to_del)
	return O
def backward_error_prop(A):
	error_states = [st.index for st in A.vs if 'err'==st['name']]
	error_state = error_states[0]
	transitions_to_del = []
	transitions = []
	transitions_to_add = []
	check = True
	while check:
		check = False
		for st in A.vs:
			if st.index not in error_states:
				for (tgt, ev) in st['out']:
					if tgt in error_states and ev in A.Euo:
						error_states.append(st.index)
						# transitions_to_add.append((st.index,ev,))
						check=True
					# elif tgt in error_states:
					# 	if (st.index,ev,tgt) not in transitions:
					# 		l = A.es.select(_source_eq=st.index,_target_eq=tgt,label_eq=ev)
					# 		print(l[0])
					# 		transitions.append((st.index,ev,tgt))
					# 		transitions_to_del.append(l[0].index)
	
	# print(error_states)
	# print(transitions_to_del)
	# A.delete_edges(A.es.select())
	error_states.pop(0)
	l = A.es.select(_target_in=error_states)
	transitions_to_add = []
	labels = []
	for edge in l:
		# print(edge.source)
		transitions_to_add.append((edge.source,error_state))
		labels.append(edge["label"])
	A.add_edges(transitions_to_add,labels)
	A.delete_vertices(error_states)
	# print(A)
	return A

def min_error(A):
	A = d.NFA(A)
	error_states = [st.index for st in A.vs if st['marked']]
	l = A.es.select(_target_in=error_states)
	transitions_to_add = []
	labels = []
	for edge in l:
		print(edge.source,len(A.vs))
		transitions_to_add.append((edge.source,len(A.vs)))
		labels.append(edge["label"])
	A.add_vertex('err',1)
	A.add_edges(transitions_to_add,labels)
	A.delete_vertices(error_states)
	# print(d.DFA(A))
	return A
def complete_automata(A):
	transitions = []
	labels = []
	for st in A.vs:
		if st['name']!='err':
			events_en = {ev: st for (st,ev) in st['out']}
			for e in A.events.difference(events_en):
				transitions.append((st.index,len(A.vs)))
				labels.append(e)
	for e in A.events:
		transitions.append((len(A.vs),len(A.vs)))
		labels.append(e)
	A.add_vertex(str(len(A.vs)),0)
	A.add_edges(transitions,labels)
	return A
def weakest_assumption(M,P):
	comp = parallel_error(M,P)
	comp.Euo = M.Euo
	comp = backward_error_prop(comp)
	comp = d.composition.observer(comp)
	comp = min_error(comp)
	for st in comp.vs:
		if st['name']!='err':
			st['name'] = str(st.index)
	weak = complete_automata(comp)
	return weak


def duplicate_events(A):
	A = d.NFA(A)
	C = set(A.events)
	transitions = []
	labels = []
	for st in A.vs:
		if st['name']!='err':
			for (dst,ev) in st['out']:
				transitions.append((st.index,dst))
				labels.append(d.Event(ev.label+'_n'))
	A.add_edges(transitions,labels)
	A.Euc = C
	return A

def remove_duplicate_events(A):
	transitions = []
	labels = []
	for ts in A.es:
		if ts['label'].label.find("_n")!=-1:
			ts['label'] = d.Event(ts['label'].label[0:-2])
	A.generate_out()
	return A

# Human = d.read_fsm(path_script+"/human.fsm")
Human = d.read_fsm(path_script+"/human-dev.fsm")
Card = d.read_fsm(path_script+"/card-bal.fsm")
Oyster = d.read_fsm(path_script+"/oyster-bal.fsm")
GateIn = d.read_fsm(path_script+"/GateIn.fsm")
GateOut = d.read_fsm(path_script+"/GateOut.fsm")

Env = d.composition.parallel(GateIn,GateOut)
Prop = d.read_fsm(path_script+"/ColisionProperty-no-err.fsm")
Prop2 = d.read_fsm(path_script+"/ColisionProperty.fsm")


par = parallel(Human,Oyster,Card,GateIn,GateOut)
# d.write_fsm(path_script+"/par.fsm",par)
print(len(par.events))

sup = d.supervisor.supremal_sublanguage(par,Prop,prefix_closed=True,mode=d.supervisor.Mode.CONTROLLABLE_NORMAL)
# sup = d.supervisory_control.VLPPO.VLPPO.offline_VLPPO(par,Prop)
# print(sup)
# par = parallel(par,sup,Prop2)
d.write_fsm(path_script+"/sup.fsm",sup)
# d.write_fsm(path_script+"/par.fsm",par)



# weak = weakest_assumption(Env,Prop)


# d.write_fsm(path_script+"/weak.fsm",weak)

# weak = duplicate_events(weak)
# comp = parallel(Human,weak)
# comp = backward_error(comp)
# d.write_fsm(path_script+"/comp.fsm",comp)
# new_env = project(comp,Human)
# new_env = remove_duplicate_events(new_env)
# d.write_fsm(path_script+"/new_env.fsm",new_env)

# par = parallel(new_env,Env,Prop)
# d.write_fsm(path_script+"/par.fsm",par)


