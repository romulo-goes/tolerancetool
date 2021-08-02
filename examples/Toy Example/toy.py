
import os
import DESops as d
import sys
#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
#
import tol_inv_property as t

Env = d.read_fsm(path_script+"/toy.fsm")
print("Printing LTS T\n",Env)
print("##################################")
print("Invariance set: ['1','2','4']")
print("##################################")
controller = {'1':('b',),'2':('b',),'3':('none',),'4':('b',)}
print("Controller for T\n",controller)
print("##################################")
(Delta,Tdelta)=t.Compute_tolerance_level(Env,controller,['1','2','4'])
print("Printing TDelta - the perturbed system with respect to the tolerance level")
print(Tdelta)
print("##################################")
print("Printing Delta\n", Delta)
print("##################################")
print("END OF EXAMPLE")