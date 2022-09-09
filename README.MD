It includes a prototype implementation of the tolerance tool.
The implementation assumes the user should provide the system modeled as an LTS, a controller, and an invariance property. 
The tool automatically computes the tolerance of the given controller. 
Moreover, the tool can also synthesize the most tolerant, the least tolerant, and the controller that achieves a given minimum threshold of tolerance.
We assume all the specifications of the models should be specified as a set of invariant states.


## System Requirements
This program requires Python 3.8. The program has been tested under
```
Python 3.8.10
python-igraph 0.9.6
pydash 5.1.0
libgmp3
```

## Install Instruction
This program relies on [MDESops](https://gitlab.eecs.umich.edu/M-DES-tools/desops) for LTS reachability analysis.
To install the tolerance tool, run the following commands.

```
cd /tolerancetool
./install.sh
source venv-tolerancetool/bin/activate
```

## API Usage
The remainder of this README explains how to run the tolerance tool manually to help you set up your own experiments.
The user can create a new project as follows:

1. Activated python environment and create a new folder of the system under model.
```
source venv-tolerancetool/bin/activate
cd /tolerancetool/examples
mkdir <project name>
cd <project name>
```

2. Create the LTS model for the system as an .fsm file using the following template:
```
<# states in the LTS>

<source state name>	0	<#transitions from this state>
<action>	<dest state name>	c	o
<action>	<dest state name>	c	o
... until all transitions are defined

<source state name>	0	<#transitions from this state>
<action>	<dest state name>	c	o
<action>	<dest state name>	c	o
... until all transitions are defined

... until all states are defined
```

3. Create a run.py file based on the following templates:
```
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

sys.path.insert(1, path_to_DESops)
# Import the DESops functions
import DESops as d

#It will read the fsm file that describes the LTS models
#Env is the environment model
Env = d.read_fsm(path_script+"/<name of the LTS model>.fsm")
#Ctr is a controller that restricts the behavior of Env
Ctr = d.read_fsm(path_script+"/<name of the LTS model>.fsm")
#Prop is a safety property
Prop = d.read_fsm(path_script+"/<name of the LTS model>.fsm")

#Computing the tolerance level of Env with respect to Ctr and Safety property Prop
trans2del = safe.tolerance_safety(Env,Ctr,Prop)
#trans2del returns a list of sets of transitions. Each set contains transitions to be removed from full environment
#The remaining transitions in the full environment represents a maximal perturbation in \Delta
print(trans2del)

```

4. Run the script run.py to obtain the results:
```
python3 run.py
```

5. For a concrete example run the file /tolerancetool/examples/Safety solutions/safety-test.py