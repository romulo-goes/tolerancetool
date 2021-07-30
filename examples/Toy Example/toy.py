
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
controller = {'1':('b',),'2':('b',),'3':('a',),'4':('b',)}
(Delta,Tdelta)=t.Compute_tolerance_level(Env,controller,['1','2','4'])
print(len(Tdelta.es))
print(Delta)