
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

Unsafe = [('2','a2'),('3','a3'),('4','a4'),('5','a5')]
Qinv = [v['name'] for v in Env.vs if v['name'] not in Unsafe]

f1 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1',),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m1',),('2','a5'):('m1',),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,f1,Qinv)
print(time.time() - start)
print(len(Tdelta.es),len(Delta))



f2 = {('1','a2'):('m1',),('1','a3'):('m1',),('1','a4'):('m1','m2'),('1','a5'):('m1',),('2','a2'):('a',),('2','a3'):('m1',),('2','a4'):('m2',),('2','a5'):('m1','m3'),('3','a2'):('m4',),('3','a3'):('a',),('3','a4'):('m2',),('3','a5'):('m3',),('4','a2'):('m4',),('4','a3'):('m5',),('4','a4'):('a',),('4','a5'):('m3',),('5','a2'):('m4',),('5','a3'):('m5',),('5','a4'):('m2',),('5','a5'):('a',)}
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,f2,Qinv)
print(time.time() - start)
print(len(Tdelta.es),len(Delta))

finv = {('1','a2'):('m1','m2','m4','m5'),('1','a3'):('m1','m2','m3','m5'),('1','a4'):('m1','m2','m3','m4'),('1','a5'):('m1','m3','m4','m5'),
('2','a2'):('a',),('2','a3'):('m1','m2','m3','m5'),('2','a4'):('m1','m2','m3','m4'),('2','a5'):('m1','m3','m4','m5'),
('3','a2'):('m1','m2','m4','m5'),('3','a3'):('a',),('3','a4'):('m1','m2','m3','m4'),('3','a5'):('m1','m3','m4','m5'),
('4','a2'):('m1','m2','m4','m5'),('4','a3'):('m1','m2','m3','m5'),('4','a4'):('a',),('4','a5'):('m1','m3','m4','m5'),
('5','a2'):('m1','m2','m4','m5'),('5','a3'):('m1','m2','m3','m5'),('5','a4'):('m1','m2','m3','m4'),('5','a5'):('a',)}
start = time.time()
(Delta,Tdelta)=t.Compute_tolerance_level(Env,finv,Qinv)
print(time.time() - start)
print(len(Tdelta.es),len(Delta))