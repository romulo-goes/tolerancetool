import json
import os
import DESops as d
import sys
import time
from xml.dom import minidom

#Getting absolute path to where script is being executed
path_script=os.path.dirname(os.path.realpath(__file__))
#Finding the absolute path to src folder
path_src = path_script[0:path_script.find('tolerancetool')]+'tolerancetool/src/'
#Add the path to src folder to PYTHONPATH so that we can import the module in src
sys.path.insert(1, path_src)
#
import tol_inv_property as t

Env = d.read_fsm(path_script+"/T1.fsm")
print("Printing LTS T\n",Env)
print("##################################")
print("Invariance set: ['1','2','4']")
print("##################################")
controller = {'1':('b',),'2':('b',),'4':('b',),'3':('none',)}
print("Controller for T\n",controller)
print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,controller,['1','2','4'])
print("Time to compute tolerance ",time.time()-start)
# print("Printing TDelta - the perturbed system with respect to the tolerance level")
# print(Tdelta)
# print("##################################")
# print("Printing Delta\n", Delta)
# print("##################################")
print("END OF EXAMPLE")

# ctr = t.Compute_tolerant_controller(Env,['1','2'],[('1','a','3'),('2','a','3')])
# print(ctr)
# sat = []
# for i in range(1,32768):
# 	mydoc = minidom.parse(path_script+'/vmt/T'+str(i)+'.log.xml')
# 	items = mydoc.getElementsByTagName('result')[0].firstChild.nodeValue
# 	if items == 'True':
# 		sat.append(i)
# subsets = []
# sat.reverse()
# print(len(sat))
# # tol={(0, 'b', 2)}
# for i in sat:
# 	f = open(path_script+'/perturbations/d'+str(i)+'.json')
# 	list = json.load(f)
# 	f.close()
# 	list = {tuple(el) for el in list}
# 	# print(list)
# 	# if tol == list:
# 		# print('Okay',i)
# 	for j in range(len(subsets)):
# 		if list.issubset(subsets[j]):
# 			break
# 	else:
# 		subsets.append(list)
# print(subsets)



