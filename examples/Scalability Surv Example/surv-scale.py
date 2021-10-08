
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

Env = parallel(ego,adv)

Unsafe = [(str(i),'a'+str(j)) for i in range(2,9) for j in range(2,9) if i==j]		
# Unsafe = [(((str(i),'a'+str(j)),'b'+str(k)),'a'+str(l)) for i in range(2,9) for j in range(2,9) for k in range(2,9) for l in range(2,9) if (i==j or i==k or i==l)]
# Unsafe = [((str(i),'a'+str(j)),'b'+str(k)) for i in range(2,9) for j in range(2,9) for k in range(2,9)  if (i==j or i==k)]
Qinv = [v['name'] for v in Env.vs if v['name'] not in Unsafe]
print("##################################")
print("Example Scalability: 1 ego, 1 srv, 10 locations")
print("##################################")
print("LTS T state set: ",len(Env.vs['name']))
print("LTS T transition set: ",len(Env.es))
print("##################################")
print("Invariance set: ",len(Qinv))

finv =  t.Compute_inv_controller(Env,Qinv)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,finv,Qinv)
print("Time to compute Delta: ",time.time() - start)
print("##################################")
print("Delta for finv has ",len(Delta)," new transitions")
print("##################################")


print("##################################")
print("Example Scalability: 1 ego, 2 srv, 10 locations")
print("##################################")


Env = parallel(ego,adv,adv2)

# Unsafe = [(str(i),'a'+str(j)) for i in range(2,9) for j in range(2,9) if i==j]		
# Unsafe = [(((str(i),'a'+str(j)),'b'+str(k)),'a'+str(l)) for i in range(2,9) for j in range(2,9) for k in range(2,9) for l in range(2,9) if (i==j or i==k or i==l)]
Unsafe = [((str(i),'a'+str(j)),'b'+str(k)) for i in range(2,9) for j in range(2,9) for k in range(2,9)  if (i==j or i==k)]
Qinv = [v['name'] for v in Env.vs if v['name'] not in Unsafe]
print("LTS T state set: ",len(Env.vs['name']))
print("LTS T transition set: ",len(Env.es))
print("##################################")
print("Invariance set: ",len(Qinv))

finv =  t.Compute_inv_controller(Env,Qinv)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,finv,Qinv)
print("Time to compute Delta: ",time.time() - start)
print("##################################")
print("Delta for finv has ",len(Delta)," new transitions")
print("##################################")


