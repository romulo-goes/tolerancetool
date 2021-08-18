
import os
import DESops as d
import sys
import time
from collections import deque


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
		# G_out_vertices = [
		#     {
		#         "name": (G1_x0["name"], G2_x0["name"]),
		#         "marked": G1_x0["marked"] and G2_x0["marked"],
		#     }
		# ]
		G_out_names = {G_out_vertices[i]["name"]: i for i in range(len(G_out_vertices))}
		G_out_edges = []  # type: List[Dict[str, Any]]

		queue = deque([(G1_x, G2_x) for G1_x in G1.vs for G2_x in G2.vs])

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
		        if e in active_both:
		            x1_dst = G1.vs[active_x1[e]]
		            x2_dst = G2.vs[active_x2[e]]
		        elif e in private_G1:
		            x1_dst = G1.vs[active_x1[e]]
		            x2_dst = x2
		        elif e in private_G2:
		            x1_dst = x1
		            x2_dst = G2.vs[active_x2[e]]
		        else:
		            continue

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


#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
import tol_inv_property as t

ego = d.read_fsm(path_script+"/ego_simpler.fsm")
adv = d.read_fsm(path_script+"/adv_simpler.fsm")
adv2 = d.read_fsm(path_script+"/adv_simpler_2.fsm")

Env = parallel(ego,adv,adv2)


# print(len([((str(i),'a'+str(j)),'a'+str(k)) for i in range(2,9) for j in range(2,9) for k in range(2,9) if (i==j or i==k)]))

# print([v['name'] for v in Env.vs if (v['name'][0][1].find(v['name'][0][0])>=0 or v['name'][1].find(v['name'][0][0])>=0)])
# Unsafe = [(str(i),'a'+str(j)) for i in range(2,9) for j in range(2,9) if i==j]		
# Unsafe = [(((str(i),'a'+str(j)),'b'+str(k)),'a'+str(l)) for i in range(2,9) for j in range(2,9) for k in range(2,9) for l in range(2,9) if (i==j or i==k or i==l)]
Unsafe = [((str(i),'a'+str(j)),'b'+str(k)) for i in range(2,9) for j in range(2,9) for k in range(2,9)  if (i==j or i==k)]
Qinv = [v['name'] for v in Env.vs if v['name'] not in Unsafe]
print("LTS T state set: ",len(Env.vs['name']))
print("LTS T state set: ",len(Env.es))
print("##################################")
print("Invariance set: ",len(Qinv))


# print("##################################")
# f1 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1',),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m1',),('2','a5'):('m1',),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
# print("##################################")
# print("Controller f1: ",f1)
# print("##################################")
# start = time.time()
# (Delta,Tdelta)=t.Compute_tolerance_level(Env,f1,Qinv)
# print("Time to compute delta: ",time.time() - start)
# print("##################################")
# print("Delta for f1 has ",len(Delta)," new transitions")
# print("##################################")


# f2 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1','m2'),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m2',),('2','a5'):('m1','m3'),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
# print("Controller f2: ",f2)
# print("##################################")
# start = time.time()
# (Delta,Tdelta)=t.Compute_tolerance_level(Env,f2,Qinv)
# print("Time to compute Delta: ",time.time() - start)
# print("##################################")
# print("Delta for f2 has ",len(Delta)," new transitions")
# print("##################################")



# finv = {('1','a2'):('m1','m2','m4','m5'),('1','a3'):('m1','m2','m3','m5'),('1','a4'):('m1','m2','m3','m4'),('1','a5'):('m1','m3','m4','m5'),
# ('2','a2'):('a',),('2','a3'):('m1','m2','m3','m5'),('2','a4'):('m1','m2','m3','m4'),('2','a5'):('m1','m3','m4','m5'),
# ('3','a2'):('m1','m2','m4','m5'),('3','a3'):('a',),('3','a4'):('m1','m2','m3','m4'),('3','a5'):('m1','m3','m4','m5'),
# ('4','a2'):('m1','m2','m4','m5'),('4','a3'):('m1','m2','m3','m5'),('4','a4'):('a',),('4','a5'):('m1','m3','m4','m5'),
# ('5','a2'):('m1','m2','m4','m5'),('5','a3'):('m1','m2','m3','m5'),('5','a4'):('m1','m2','m3','m4'),('5','a5'):('a',)}
finv =  t.Compute_inv_controller(Env,Qinv)
# print("Controller finv: ",finv)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,finv,Qinv)
print("Time to compute Delta: ",time.time() - start)
print("##################################")
print("Delta for finv has ",len(Delta)," new transitions")
print("##################################")

fem =  t.Compute_empty_controller(Env,Qinv)
# print("Controller fempty: ",fem)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,fem,Qinv)
print("Time to compute Delta: ",time.time() - start)
print("##################################")
print("Delta for fempty has ",len(Delta)," new transitions")
print("##################################")


# Computation of f1 based on synthesizing tolerant controllers with a minimum level of tolerance
# Defining minimum level of tolerance for f1
# d1 = [(('1', 'a2'),'m2',('2', 'a2')),(('1', 'a2'),'m3',('3', 'a3')),(('1', 'a2'),'m4',('4', 'a4')),(('1', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('1', 'a3'),'m2',('2', 'a2')),(('1', 'a3'),'m3',('3', 'a3')),(('1', 'a3'),'m4',('4', 'a4')),(('1', 'a3'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('1', 'a4'),'m2',('2', 'a2')),(('1', 'a4'),'m3',('3', 'a3')),(('1', 'a4'),'m4',('4', 'a4')),(('1', 'a4'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('1', 'a5'),'m2',('2', 'a2')),(('1', 'a5'),'m3',('3', 'a3')),(('1', 'a5'),'m4',('4', 'a4')),(('1', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('2', 'a3'),'m2',('2', 'a2')),(('2', 'a3'),'m3',('3', 'a3')),(('2', 'a3'),'m4',('4', 'a4')),(('2', 'a3'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('2', 'a4'),'m2',('2', 'a2')),(('2', 'a4'),'m3',('3', 'a3')),(('2', 'a4'),'m4',('4', 'a4')), #Srv can match any action ego takes
# (('2', 'a5'),'m3',('3', 'a3')),(('2', 'a5'),'m4',('4', 'a4')),(('2', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('3', 'a2'),'m1',('2', 'a2')),(('3', 'a2'),'m2',('2', 'a2')),(('3', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('3', 'a4'),'m1',('2', 'a2')),(('3', 'a4'),'m3',('3', 'a3')),(('3', 'a4'),'m4',('4', 'a4')),(('3', 'a4'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('3', 'a5'),'m1',('2', 'a2')),(('3', 'a5'),'m4',('4', 'a4')),(('3', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('4', 'a2'),'m1',('2', 'a2')),(('4', 'a2'),'m2',('2', 'a2')),(('4', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('4', 'a3'),'m1',('2', 'a2')),(('4', 'a3'),'m2',('2', 'a2')),(('4', 'a3'),'m3',('3', 'a3')), #Srv can match any action ego takes
# (('4', 'a5'),'m1',('2', 'a2')),(('4', 'a5'),'m2',('2', 'a2')),(('4', 'a5'),'m4',('4', 'a4')),(('4', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('5', 'a2'),'m1',('2', 'a2')),(('5', 'a2'),'m2',('2', 'a2')),(('5', 'a2'),'m3',('3', 'a3')),(('5', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
# (('5', 'a3'),'m1',('2', 'a2')),(('5', 'a3'),'m2',('2', 'a2')),(('5', 'a3'),'m3',('3', 'a3')), #Srv can match any action ego takes
# (('5', 'a4'),'m1',('2', 'a2')),(('5', 'a4'),'m3',('3', 'a3')),(('5', 'a4'),'m4',('4', 'a4')) #Srv can match any action ego takes
# ]

# f1 = t.Compute_tolerant_controller(Env,Qinv,d1)
# print(f1)

