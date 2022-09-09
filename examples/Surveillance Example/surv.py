
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
import tol_inv_property as t

ego = d.read_fsm(path_script+"/ego_simpler.fsm")
adv = d.read_fsm(path_script+"/adv_simpler.fsm")

Env = d.composition.parallel(ego,adv)
d.write_fsm(path_script+'/srv-model.fsm',Env)

# print([v['name'] for v in Env.vs if v['name'][1].find(v['name'][0])>=0])
Unsafe = [('2','a2'),('3','a3'),('4','a4'),('5','a5')]
Qinv = [v['name'] for v in Env.vs if v['name'] not in Unsafe]
# print("LTS T state set: ",Env.vs['name'])
# print("##################################")
# print("Invariance set: ",Qinv)
print("##################################")
print("LTS transition set: ",len(Env.es))
print("##################################")
f1 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1',),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m1',),('2','a5'):('m1',),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
# print("##################################")
# print("Controller f1: ",f1)
# print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,f1,Qinv)
end = time.time() - start
print("Delta for f1 has ",len(Delta)," new transitions")
print("##################################")
print("Time to compute delta: ",end)
print("##################################")



f2 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1','m2'),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m2',),('2','a5'):('m1','m3'),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
# print("Controller f2: ",f2)
# print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,f2,Qinv)
end = time.time() - start
print("Delta for f2 has ",len(Delta)," new transitions")
print("##################################")
print("Time to compute Delta: ",end)
print("##################################")



# finv = {('1','a2'):('m1','m2','m4','m5'),('1','a3'):('m1','m2','m3','m5'),('1','a4'):('m1','m2','m3','m4'),('1','a5'):('m1','m3','m4','m5'),
# ('2','a2'):('a',),('2','a3'):('m1','m2','m3','m5'),('2','a4'):('m1','m2','m3','m4'),('2','a5'):('m1','m3','m4','m5'),
# ('3','a2'):('m1','m2','m4','m5'),('3','a3'):('a',),('3','a4'):('m1','m2','m3','m4'),('3','a5'):('m1','m3','m4','m5'),
# ('4','a2'):('m1','m2','m4','m5'),('4','a3'):('m1','m2','m3','m5'),('4','a4'):('a',),('4','a5'):('m1','m3','m4','m5'),
# ('5','a2'):('m1','m2','m4','m5'),('5','a3'):('m1','m2','m3','m5'),('5','a4'):('m1','m2','m3','m4'),('5','a5'):('a',)}
finv =  t.Compute_inv_controller(Env,Qinv)
# print("Controller finv: ",finv)
# print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,finv,Qinv)
end = time.time() - start
print("Delta for finv has ",len(Delta)," new transitions")
print("##################################")
print("Time to compute Delta: ",end)
print("##################################")

fem =  t.Compute_empty_controller(Env,Qinv)
# print("Controller fempty: ",fem)
# print("##################################")
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,fem,Qinv)
end = time.time() - start
print("Delta for fempty has ",len(Delta)," new transitions")
print("##################################")
print("Time to compute Delta: ",end)
print("##################################")
print("END OF SURV EXAMPLE")


# Computation of f1 based on synthesizing tolerant controllers with a minimum level of tolerance
# Defining minimum level of tolerance for f1
d1 = [(('1', 'a2'),'m2',('2', 'a2')),(('1', 'a2'),'m3',('3', 'a3')),(('1', 'a2'),'m4',('4', 'a4')),(('1', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('1', 'a3'),'m2',('2', 'a2')),(('1', 'a3'),'m3',('3', 'a3')),(('1', 'a3'),'m4',('4', 'a4')),(('1', 'a3'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('1', 'a4'),'m2',('2', 'a2')),(('1', 'a4'),'m3',('3', 'a3')),(('1', 'a4'),'m4',('4', 'a4')),(('1', 'a4'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('1', 'a5'),'m2',('2', 'a2')),(('1', 'a5'),'m3',('3', 'a3')),(('1', 'a5'),'m4',('4', 'a4')),(('1', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('2', 'a3'),'m2',('2', 'a2')),(('2', 'a3'),'m3',('3', 'a3')),(('2', 'a3'),'m4',('4', 'a4')),(('2', 'a3'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('2', 'a4'),'m2',('2', 'a2')),(('2', 'a4'),'m3',('3', 'a3')),(('2', 'a4'),'m4',('4', 'a4')), #Srv can match any action ego takes
(('2', 'a5'),'m3',('3', 'a3')),(('2', 'a5'),'m4',('4', 'a4')),(('2', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('3', 'a2'),'m1',('2', 'a2')),(('3', 'a2'),'m2',('2', 'a2')),(('3', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('3', 'a4'),'m1',('2', 'a2')),(('3', 'a4'),'m3',('3', 'a3')),(('3', 'a4'),'m4',('4', 'a4')),(('3', 'a4'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('3', 'a5'),'m1',('2', 'a2')),(('3', 'a5'),'m4',('4', 'a4')),(('3', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('4', 'a2'),'m1',('2', 'a2')),(('4', 'a2'),'m2',('2', 'a2')),(('4', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('4', 'a3'),'m1',('2', 'a2')),(('4', 'a3'),'m2',('2', 'a2')),(('4', 'a3'),'m3',('3', 'a3')), #Srv can match any action ego takes
(('4', 'a5'),'m1',('2', 'a2')),(('4', 'a5'),'m2',('2', 'a2')),(('4', 'a5'),'m4',('4', 'a4')),(('4', 'a5'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('5', 'a2'),'m1',('2', 'a2')),(('5', 'a2'),'m2',('2', 'a2')),(('5', 'a2'),'m3',('3', 'a3')),(('5', 'a2'),'m5',('5', 'a5')), #Srv can match any action ego takes
(('5', 'a3'),'m1',('2', 'a2')),(('5', 'a3'),'m2',('2', 'a2')),(('5', 'a3'),'m3',('3', 'a3')), #Srv can match any action ego takes
(('5', 'a4'),'m1',('2', 'a2')),(('5', 'a4'),'m3',('3', 'a3')),(('5', 'a4'),'m4',('4', 'a4')) #Srv can match any action ego takes
]

f1 = t.Compute_tolerant_controller(Env,Qinv,d1)
# print(f1)

