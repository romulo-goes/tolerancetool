import os
import sys
import time
#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
# Import the tolerancetool functions
import tol_safety_property as safe
import tol_inv_property as inv

path_to_DESops = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/lib/'
print(path_to_DESops)
sys.path.insert(1, path_to_DESops)
# Import the DESops functions
import DESops as d

#It will read the fsm file that describes the LTS models
#Env is the environment model
Env = d.read_fsm(path_script+"/env.fsm")
#Ctr is a controller that restricts the behavior of Env
Ctr = d.read_fsm(path_script+"/machine.fsm")
#Prop is a safety property
Prop = d.read_fsm(path_script+"/property.fsm")

#Computing the tolerance level of Env with respect to Ctr and Safety property Prop
trans2del = safe.tolerance_safety(Env,Ctr,Prop)
#trans2del returns a list of sets of transitions. Each set contains transitions to be removed from full environment
#The remaining transitions in the full environment represents a maximal perturbation in \Delta
print(trans2del)