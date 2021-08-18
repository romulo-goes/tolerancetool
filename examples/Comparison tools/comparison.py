
import os
import DESops as d
import sys
import time
#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
#
import tol_inv_property as t

Env = d.read_fsm(path_script+"/T.fsm")
print("Printing LTS T\n",Env)
print("##################################")
print("Invariance set: ['1','2']")
print("##################################")
controller = {'1':('b',),'2':('b',),'3':('none',)}
print("Controller for T\n",controller)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,controller,['1','2'])
print("Time to compute tolerance ",time.time()-start)
print("Printing TDelta - the perturbed system with respect to the tolerance level")
print(Tdelta)
print("##################################")
print("Printing Delta\n", Delta)
print("##################################")
print("END OF EXAMPLE")


# Computing the most and the least tolerant controller.
# Also, we compute a controller tolerant against deviation [('1','a','3'),('2','a','3')]
ctr = t.Compute_inv_controller(Env,['1','2'])
print(ctr)
ctr = t.Compute_empty_controller(Env,['1','2'])
print(ctr)
(Delta,Tdelta)=t.Compute_tolerance_level(Env,ctr,['1','2'])
print(Tdelta)
ctr = t.Compute_tolerant_controller(Env,['1','2'],[('1','a','3'),('2','a','3')])
print(ctr)
