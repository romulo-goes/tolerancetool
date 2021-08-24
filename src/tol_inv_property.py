import DESops as d
from itertools import product


#Get the successors of a given successor list and event
def Post(out_list,event):
	return [x[0] for x in out_list if x[1].label==event]


#Computes the empty controller for LTS T
#The empty controller selects empty tuples for each state in T
def Compute_empty_controller(T,Qinv):
	controller = dict()
	for st in range(len(T.vs)):
		controller[T.vs[st]['name']] = tuple()
	return controller

# Compute the finv for LTS T and invariant set Qinv; finv(q) = Ainv(q)
# It returns a controller as a dictionary where keys are state names and values are tuples with actions
# controler[state_name] = tuple(actions)
def Compute_inv_controller(T,Qinv):
	Qinv_id = {v.index for v in T.vs if v['name'] in Qinv}
	events = T.events
	controller = dict()
	for st in range(len(T.vs)):
		act = []
		if st in Qinv_id:
			for ev in events:
				# print(T.vs[st]['out'])
				post = Post(T.vs[st]['out'],ev.label)
				# print([T.vs[id]['name'] for id in post])
				if set(post).issubset(Qinv_id):
					act.append(ev.label)
			controller[T.vs[st]['name']] = tuple(act)
		else:
			controller[T.vs[st]['name']] = tuple()
	return controller

# Compute the least tolerant controller for LTS T, invariant set Qinv; finv(q) = Ainv(q), and minimum tolerance level d
# d is a list with transitions that must be tolerated, e.g., d = [(state_1, action_name, state_2)] where state_1,state_2 should be valid 
# It returns a controller as a dictionary where keys are state names and values are tuples with actions
# controler[state_name] = tuple(actions)
def Compute_tolerant_controller(T,Qinv,dist):
	Td = d.NFA(T)
	edges = []
	events = []
	for t in dist:
		# print(t[0],t[1],t[2])
		src = T.vs.select(name = t[0])
		tgt  = T.vs.select(name = t[2])
		if not src and not tgt:
			# print("Vertex name in ",t," disturbance list incorrect")
			return
		# print((src[0],tgt[0]))
		src = src[0].index
		tgt = tgt[0].index
		
		edges.append((src,tgt))
		events.append(d.Event(t[1]))
	# Td.add_edges(edges,events,fill_out=True)	
	# print(Td)
	# Need to compute Td. Add transitions d to T
	controller = Compute_inv_controller(Td,Qinv)
	return controller

#It calculates the controlled behavior of Env under control of controller
#It returns an NFA that represents the controlled system
def Control(Env, controller):
	C = d.automata.NFA()
	# print(names)
	edges = [] 
	for st in range(len(Env.vs)):
		src_index = st
		src_name = Env.vs[st]['name']
		if src_name in controller.keys():
			event = controller[src_name]
		else:
			continue
		for ev in event:
			post = Post(Env.vs[st]['out'],ev)
			for target in post:
				target_name = Env.vs[target]
				edges.append({"pair": (src_index, target), "label": d.Event(ev)})
	C.add_vertices(
            len(Env.vs),
            Env.vs['name']
        )
	C.add_edges(
            [e["pair"] for e in edges],
            [e["label"] for e in edges],
            fill_out=True,
        )
	C.events = Env.events
	return C


#Function to compute tolerance level of controller f, given LTS T and invariance set of states Qinv (string names of the states)
# T is an LTS (DFA or NFA)
# f is a dict defined as state: tuple of actions. For example f = {'1':(a,), '2': ('a','b')}
# Qinv is a list with the state names of invariant states
def Compute_tolerance_level(T,f,Qinv_name):
	Not_Qinv = [v.index for v in T.vs if v['name'] not in Qinv_name]
	Qinv = [v.index for v in T.vs if v['name'] in Qinv_name]
	Tinv = Extend_Env_Qinv(T,Qinv) #Compute T_{Qinv x Act x Qinv}
	Tinvf = Control(Tinv,f) #To identify the actions used by controller in each state
	inacc = d.basic_operations.unary.find_inacc(Tinvf) #Find the unreachable states
	Acc = [st.index for st in Tinvf.vs if st.index not in inacc] #Find the reachable states
	Tdelta = Extend_Env_Total(Tinvf,Tinv,Not_Qinv,Acc)
	# Delta = [(Tdelta.vs[e.source]['name'],e['label'],Tdelta.vs[e.target]['name']) for e in Tdelta.es if not T.es.select(_source_eq =e.source,_target_eq=e.target,label_eq=e['label'])]
	Delta = [(Tdelta.vs[e.source]['name'],e['label'],Tdelta.vs[e.target]['name']) for e in Tdelta.es if (e.target,e['label']) not in T.vs[e.source]['out']]
	return (Delta,Tdelta)


# It receives an NFA and a list of transition contraints 
# It return an NFA where its transition relation is defined by the intersection of the transition relation of the given NFA and the list of transition constraints
def Transition_contraint(T,trans_contraint):
	return

#Function to extend the environment with transitions in Qinv x Act x Qinv
def Extend_Env_Qinv(Env,Qinv):
	Ext = d.NFA(Env)
	events = list(Env.events)
	edges = [{"pair": (src, tgt), "label": e} for src in Qinv for tgt in Qinv for e in events if (tgt,e) not in Env.vs[src]['out']]
	Ext.add_edges(
	[e["pair"] for e in edges],
	[e["label"] for e in edges],
	fill_out=True,
	)
	# edge_pairs = list(product(Qinv,repeat=2))
	# edges = edge_pairs*len(events)
	# events = events*len(edge_pairs)
	# k = 5
	# for i in range(5):
	# 	for j in range(5):
	# 		edges = [{"pair": (src, tgt), "label": e} for src in Qinv[i*int(len(Qinv)/5):(i+1)*int(len(Qinv)/5)] for tgt in Qinv[j*int(len(Qinv)/5):(j+1)*len(Qinv)] for e in events if (tgt,e) not in Env.vs[src]['out']]
	# 		Ext.add_edges(
    #         [e["pair"] for e in edges],
    #         [e["label"] for e in edges],
    #         fill_out=True,
    #     	)
	
	# edges = [{"pair": (src, tgt), "label": e} for src in Qinv for tgt in Qinv for e in events if not Env.es.select(_source_eq =src,_target_eq=tgt,label_eq=e)]
	
	return Ext 

#Function to extend the environment with tolerable transitions in Q x Act x (Q-Qinv)
def Extend_Env_Total(Env,Env_ext,Unsafe,Acc):
	Ext = d.NFA(Env_ext)
	edges = []
	events = list(Ext.events)
	# Q = Unsafe+Acc
	Q = range(len(Env_ext.vs))
	# edge_pairs = list(product(Unsafe,Q))
	# edges_1 = edge_pairs*len(events)
	# events_1 = events*len(edge_pairs)
	# Ext.add_edges(
    #         edges_1,
    #         events_1,
    #         fill_out=True,
    #     )
	edges = [{"pair": (src, tgt), "label": e} for src in Unsafe for tgt in Q for e in events if (tgt,e) not in Env.vs[src]['out']]
    # left_out = []
	for id in Q:
		if id in Acc:
			control_action = {out[1] for out in Env.vs[id]['out']}
			not_used = Env.events - control_action
			edges.extend([{"pair": (id, uns), "label": e} for uns in Unsafe for e in not_used if (uns,e) not in Env.vs[id]['out']])
		elif id not in Unsafe:
			edges.extend([{"pair": (id, uns), "label": e} for uns in Unsafe for e in events if (uns,e) not in Env.vs[id]['out']])
	Ext.add_edges(
            [e["pair"] for e in edges],
            [e["label"] for e in edges],
            fill_out=True,
        )
	return Ext