from DESops.basic_operations import composition
import DESops as d

#Get the successors of a given successor list and event
def Post(out_list,event):
	return [x[0] for x in out_list if x[1].label==event]

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
	Qinv = [v.index for v in Env.vs if v['name'] in Qinv_name]
	Tinv = Extend_Env_Qinv(T,Qinv) #Compute T_{Qinv x Act x Qinv}
	Tinvf = Control(Tinv,controller) #To identify the actions used by controller in each state
	inacc = d.basic_operations.unary.find_inacc(Tinvf) #Find the unreachable states
	Acc = [st.index for st in Tinvf.vs if st.index not in inacc] #Find the reachable states
	Tdelta = Extend_Env_Total(Tinvf,Tinv,Not_Qinv,Acc)
	Delta = [(Tdelta.vs[e.source]['name'],e['label'],Tdelta.vs[e.target]['name']) for e in Tdelta.es if not T.es.select(_source_eq =e.source,_target_eq=e.target,label_eq=e['label'])]
	return (Delta,Tdelta)


# It receives an NFA and a list of transition contraints 
# It return an NFA where its transition relation is defined by the intersection of the transition relation of the given NFA and the list of transition constraints
def Transition_contraint(T,trans_contraint):
	return

#Function to extend the environment with transitions in Qinv x Act x Qinv
def Extend_Env_Qinv(Env,Qinv):
	Ext = d.NFA(Env)
	events = Env.events
	edges = [{"pair": (src, tgt), "label": e} for src in Qinv for tgt in Qinv for e in events if not Env.es.select(_source_eq =src,_target_eq=tgt,label_eq=e)]
	Ext.add_edges(
            [e["pair"] for e in edges],
            [e["label"] for e in edges],
            fill_out=True,
        )
	return Ext 

#Function to extend the environment with tolerable transitions in Q x Act x (Q-Qinv)
def Extend_Env_Total(Env,Env_ext,Unsafe,Acc):
	Ext = d.NFA(Env_ext)
	edges = []
	events = Ext.events
	Q = Unsafe+Acc
	edges = [{"pair": (src, tgt), "label": e} for src in Unsafe for tgt in Q for e in events if not Ext.es.select(_source_eq =src,_target_eq=tgt,label_eq=e)]
    # left_out = []
	for id in Acc:
		control_action = {out[1] for out in Env.vs[id]['out']}
		not_used = Env.events - control_action
		edges.extend([{"pair": (id, uns), "label": e} for uns in Unsafe for e in not_used if not Ext.es.select(_source_eq =id,_target_eq=uns,label_eq=e)])
	Ext.add_edges(
            [e["pair"] for e in edges],
            [e["label"] for e in edges],
            fill_out=True,
        )
	return Ext

path = "/Users/romulo/Documents/romulo/Research/Postdoc/2021/Robustness/Examples/Toy example lncs/"
Env = d.read_fsm(path+"toy.fsm")
controller = {'1':('b',),'2':('b',),'3':('a',),'4':('b',)}

(Delta,Tdelta)=Compute_tolerance_level(Env,controller,['1','2','4'])
print(len(Tdelta.es))
print(Delta)