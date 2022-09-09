import json
import os

# from igraph.datatypes import TriadCensus
import DESops as d
import sys
import time
# from DESops.automata.automata import State_or_StateSet
from itertools import combinations
# from DESops.basic_operations.construct_complement import construct_complement
from collections import deque


#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
#
# import tol_inv_property as t
import tol_safety_property as t

def parallel(*automata: d.NFA) -> d.NFA:
	"""
	Computes the parallel composition of 2 (or more) LTS in a BFS manner, and returns the resulting composition as a new Automata.
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
	"""
    Returns LTS where the err state becomes unreachable

    Returns: LTS with unreachable err state

    Parameters:
    A: LTS with err state
    """
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
		states = [(s,s['name'].index(st['name'])) for s in A.vs if st['name'] == s['name'][0]]
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
	"""
    Returns LTS where the err state becomes unreachable

    Returns: LTS with unreachable err state

    Parameters:
    A: LTS with err state
    """
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
	"""
    Returns LTS A with only one err (error) state. 
	LTS A might have multiple marked (error) states.
	Replaces the multiple error states by a single err state.

    Returns: LTS A with one single err state

    Parameters:
    A: LTS with possibly multiple err state
    """
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
	"""
    Returns a complete LTS A. An LTS with all transitions. 
	A new sink state is added to A where missing transitions are directed to this new state

    Returns: LTS A with all transitions

    Parameters:
    A: LTS to be completed
    """
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
	"""
    Returns the weakest assumption of Machine M and Property P

    Returns: LTS representing the weakest assumption of M and P

    Parameters:
    M: LTS representing the Machine
	P: LTS representing the safety property: it must have a single error state name err. Any trace that reaches err violates the property
    """
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
	"""
    Returns LTS A with duplicated controllable events event_n (event_new)

    Returns: LTS A

    Parameters:
    A: LTS
    """
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

def pre_computation(A):
	pre_list = []
	for i in range(len(A.vs)):
		pre = A.es.select(_target_eq = A.vs[i])
		pre = [(t.source,t['label'])for t in pre]
		pre_list.append(pre)
		A.vs["pre"] = pre_list
		
def Pre(states, A):
	Pre = states
	levels = [Pre]
	diff = states
	while diff:
		pre_1 = {st  for i in diff for (st,ev) in A.vs[i]['pre']}
		diff = pre_1.difference(Pre|{0})
		levels.append(pre_1)
		Pre = Pre|pre_1

def DFS_tree(A):
	"""
    Returns LTS A with parameters uncontrollable states and predecessors
    Returns: LTS A

    Parameters:
    A: LTS to add new paramenters
    """
	visited = []
	to_visit = []
	pre = [[] for i in range(len(A.vs))]
	unctr = [[] for i in range(len(A.vs))]
	constraints = [set() for i in range(len(A.vs))]
	to_visit.append(0)
	while to_visit:
		st = to_visit.pop(0)
		visited.append(st)
		for (tgt, ev) in A.vs[st]['out']:
			if tgt not in visited and tgt not in to_visit:
				to_visit.append(tgt)
			if (st,ev) not in pre[tgt]:
				pre[tgt].append((st,ev))
			if ev in A.Euc:
				unctr[tgt].append(st)
			# else:
			# 	env_src = A.vs[st]['name'][0]
			# 	if "err" in A.vs[tgt]['name']:
			# 		env_tgt = A.vs[tgt]['name'][0]
			# 		if (env_src,ev,env_tgt) not in constraints[tgt]:
			# 			constraints[tgt].add((env_src,ev,env_tgt))
			# 	else:
			# 		for j in range(n):
			# 			if (env_src,ev,str(j)) not in constraints[tgt]:
			# 				constraints[tgt].add((env_src,ev,str(j)))

	A.vs["pre"] = pre
	A.vs["uctr"] = unctr
	# A.vs["constraints"] = constraints

def backward_errors(A):
	"""
    Returns a list of set of transitions to be deleted from the Env_duplicated

    Returns: list(set of transitions)

    Parameters:
    A: LTS of Env_duplicated composed with the Weakest assumption 
    """
	# Getting the error states in A = Env_f||Weakest
	error_states = set([st.index for st in A.vs if 'err'in st['name']])
	#total_list_unreach holds the values of all possible set of unreachable states we must test to check the perturbation set
	total_list_unreach = []
	#list_unreach is a list of states we want to make unreachable. It starts with just the error states.
	#Note that the lists of unreachable states in list unreach might not be the same as the ones in total_list_unreach
	#We expand the set of unreachable states in list unreach to include the states that uncontrollably reach a states in list unreach 
	#For example, if state 1 reaches the err state via uncontrollable event b, then 1 must be included in the total list of unreach
	list_unreach = [list(error_states)]
	
	while list_unreach:
		
		unvisited = list_unreach.pop(0)
		unreach = set(unvisited)
		while unvisited:
			st = unvisited.pop(0)
			#Expand unvisted with states that reach st uncontrollably
			for new_st in A.vs[st]['uctr']:
				if new_st not in unvisited and new_st not in unreach:
					unreach.add(new_st)
					unvisited.append(new_st)
		#If the initial state was not added to unreach then we go to the next iteration, 
		#because we cannot make the initial state unreachable
		if 0 not in unreach:
			#Add the expanded list unreach to the total_list_unreach. Note that unreach \superseteq unvisited (before any pop)
			if unreach not in total_list_unreach:
				total_list_unreach.append(list(unreach))
			#Based on states in unreach, we do a one step predecessor
			#The idea is to replace a state in unreach making predecessors unreachable
			new_states = {src for st in unreach for (src, ev) in A.vs[st]['pre'] if (src not in unreach and src!=0)}
			#All possible combinations
			#Here we might be able to do better. For now, we try all possible combinations
			new_state_combinations= [set(t) for i in range(1,len(new_states)+1) for t in combinations(new_states, i)]
			#We take the union of the current unreach with every possible combination
			new_unreach = [list(t.union(unreach)) for t in new_state_combinations if list(t.union(unreach)) not in total_list_unreach] 
			# These are added to the list_unreach as possible states to make unreachable next
			if new_unreach:
				list_unreach.extend(new_unreach)
	#Set with all possible transition removals
	list_constraints = []
	for unr in total_list_unreach:
		# Copies the LTS
		Atrim = A.copy()
		# We delete the states in unr
		Atrim.delete_vertices(unr)
		# Delete any other unreachable state after deleting unr
		d.unary.trim(Atrim)
		# Set where we store the transitions to be deleted in this iteration
		constraints = set()
		for st in Atrim.vs:
			# Check comparing A and A trim based on their name and not index
			env_st = st["name"][0]
			# Find the same state in the not trimmed LTS
			st_A = A.vs.select(name=st["name"])
			st_A = st_A[0]
			# Get the list of successors for states st and st_A
			# We will compare what has been delete in the list of successors of st
			# after we deleted unr. 
			out_stA = [(A.vs[tgt]["name"], e) for (tgt,e) in st_A["out"]]
			out_st = [(Atrim.vs[tgt]["name"], e) for (tgt,e) in st["out"]]
			for (tgt,e) in out_stA:
				# When a transition is in the successors of st_A 
				# but not in the successors of st, it implies that a transition has been deleted
				# as to make a state in unr unreachable. We add the constraint of this transition
				# removal to contraints.
				if (tgt, e) not in out_st:
					if (st["name"][0],e,tgt[0]) not in constraints:
						constraints.add((st["name"][0],e,tgt[0]))
		# if the constraints have not been added yet. Add them to the list of constraints.
		if constraints not in list_constraints:
			list_constraints.append(constraints)
	return list_constraints


Env = d.read_fsm(path_script+"/env.fsm")
Machine = d.read_fsm(path_script+"/machine.fsm")
Prop = d.read_fsm(path_script+"/property.fsm")

weak = t.weakest_assumption(Machine,Prop)
weak = t.duplicate_events(weak)
comp = t.parallel(Env,weak)
t.Compute_pre_and_uctr(comp)
trans2del = t.backward_errors(comp)

trans2del = t.tolerance_safety(Env,Machine,Prop)
print(trans2del)
