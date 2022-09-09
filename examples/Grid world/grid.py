
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
from math import pi as pi
from math import cos as cos
from math import sin as sin
from math import floor as floor
from math import sqrt as sqrt

def generate_model(N):
	angles = [0,pi/2, pi,3*pi/2]
	angles_str = ['0','pi2','pi','3pi2']
	action = ['M','L','R']
	with open(path_script+'/test_model2.fsm', "w") as f:
		f.write(str(N*N*4+1))
		f.write("\n\n")
		for x in range(1,N+1):
			for y in range(1,N+1):
				for i,t in enumerate(angles):
					st = ','.join([str(x),str(y),angles_str[i]])
					f.write('\t'.join([st,'0','3','\n']))
					# MOVE
					xp = int(round(x+cos(t)))
					yp = int(round(y+sin(t)))
					tp = t
					if xp>N or yp>N or xp<1 or yp<1:
						stp = 'Out'
						f.write('\t'.join(['M',stp,'c','o']))
						f.write("\n")
					else:
						stp = ','.join([str(xp),str(yp),angles_str[i]])
						f.write('\t'.join(['M',stp,'c','o']))
						f.write("\n")
					# RIGHT
					xp = x
					yp = y
					stp = ','.join([str(x),str(y),angles_str[(i-1)%4]])
					f.write('\t'.join(['R',stp,'c','o']))
					f.write("\n")
					# LEFT
					xp = x
					yp = y
					stp = ','.join([str(x),str(y),angles_str[(i+1)%4]])
					f.write('\t'.join(['L',stp,'c','o']))
					f.write("\n\n")
		f.write('\t'.join(['Out','0','0','\n']))

N = 50
generate_model(N)
# print(round(cos(3*pi/2)))
grid = d.read_fsm(path_script+"/test_model2.fsm")

# print([v['name'] for v in Env.vs if v['name'][1].find(v['name'][0])>=0])
Unsafe = ['Out']
Qinv = [v['name'] for v in grid.vs if v['name'] not in Unsafe]
# print("##################################")
# print("LTS transition set: ",len(Env.es))
# print("##################################")
f1 = {'1,1,0':(),'1,1,pi2':(),'1,1,pi':(),'1,1,3p2':(),
'1,2,0':(),'1,2,pi2':(),'1,2,pi':(),'1,2,3pi2':(),
'1,3,0':(),'1,3,pi2':(),'1,3,pi':(),'1,3,3pi2':(),
'1,4,0':(),'1,4,pi2':(),'1,4,pi':(),'1,4,3pi2':(),
'1,5,0':(),'1,5,pi2':(),'1,5,pi':(),'1,5,3pi2':(),
'1,6,0':(),'1,6,pi2':(),'1,6,pi':(),'1,6,3pi2':(),
'1,7,0':(),'1,7,pi2':(),'1,7,pi':(),'1,7,3pi2':(),
'1,8,0':(),'1,8,pi2':(),'1,8,pi':(),'1,8,3pi2':(),
'1,9,0':(),'1,9,pi2':(),'1,9,pi':(),'1,9,3pi2':(),
'1,10,0':(),'1,10,pi2':(),'1,10,pi':(),'1,10,3pi2':(),
'2,1,0':(),'2,1,pi2':(),'2,1,pi':(),'2,1,3pi2':(),
# '2,2,0':('M'),'2,2,pi2':('R'),'2,2,pi':(),'2,2,3pi2':(),
'2,2,0':(),'2,2,pi2':(),'2,2,pi':(),'2,2,3pi2':(),
# '2,3,0':('R'),'2,3,pi2':(),'2,3,pi':(),'2,3,3pi2':('M'),
'2,3,0':(),'2,3,pi2':(),'2,3,pi':(),'2,3,3pi2':(),
'2,4,0':(),'2,4,pi2':(),'2,4,pi':(),'2,4,3pi2':(),
'2,5,0':(),'2,5,pi2':(),'2,5,pi':(),'2,5,3pi2':(),
'2,6,0':(),'2,6,pi2':(),'2,6,pi':(),'2,6,3pi2':(),
'2,7,0':(),'2,7,pi2':(),'2,7,pi':(),'2,7,3pi2':(),
'2,8,0':(),'2,8,pi2':(),'2,8,pi':(),'2,8,3pi2':(),
'2,9,0':(),'2,9,pi2':(),'2,9,pi':(),'2,9,3pi2':(),
'2,10,0':(),'2,10,pi2':(),'2,10,pi':(),'2,10,3pi2':(),
'3,1,0':(),'3,1,pi2':(),'3,1,pi':(),'3,1,3pi2':(),
# '3,2,0':(),'3,2,pi2':('M'),'3,2,pi':('R'),'3,2,3pi2':(),
'3,2,0':(),'3,2,pi2':(),'3,2,pi':(),'3,2,3pi2':(),
# '3,3,0':(),'3,3,pi2':(),'3,3,pi':('M'),'3,3,3pi2':('R'),
'3,3,0':(),'3,3,pi2':(),'3,3,pi':(),'3,3,3pi2':(),
'3,4,0':(),'3,4,pi2':(),'3,4,pi':(),'3,4,3pi2':(),
'3,5,0':(),'3,5,pi2':(),'3,5,pi':(),'3,5,3pi2':(),
'3,6,0':(),'3,6,pi2':(),'3,6,pi':(),'3,6,3pi2':(),
'3,7,0':(),'3,7,pi2':(),'3,7,pi':(),'3,7,3pi2':(),
'3,8,0':(),'3,8,pi2':(),'3,8,pi':(),'3,8,3pi2':(),
'3,9,0':(),'3,9,pi2':(),'3,9,pi':(),'3,9,3pi2':(),
'3,10,0':(),'3,10,pi2':(),'3,10,pi':(),'3,10,3pi2':(),
'4,1,0':(),'4,1,pi2':(),'4,1,pi':(),'4,1,3pi2':(),
'4,2,0':(),'4,2,pi2':(),'4,2,pi':(),'4,2,3pi2':(),
'4,3,0':(),'4,3,pi2':(),'4,3,pi':(),'4,3,3pi2':(),
'4,4,0':(),'4,4,pi2':(),'4,4,pi':(),'4,4,3pi2':(),
'4,5,0':(),'4,5,pi2':(),'4,5,pi':(),'4,5,3pi2':(),
'4,6,0':(),'4,6,pi2':(),'4,6,pi':(),'4,6,3pi2':(),
'4,7,0':(),'4,7,pi2':(),'4,7,pi':(),'4,7,3pi2':(),
'4,8,0':(),'4,8,pi2':(),'4,8,pi':(),'4,8,3pi2':(),
'4,9,0':(),'4,9,pi2':(),'4,9,pi':(),'4,9,3pi2':(),
'4,10,0':(),'4,10,pi2':(),'4,10,pi':(),'4,10,3pi2':(),
'5,1,0':(),'5,1,pi2':(),'5,1,pi':(),'5,1,3pi2':(),
'5,2,0':(),'5,2,pi2':(),'5,2,pi':(),'5,2,3pi2':(),
'5,3,0':(),'5,3,pi2':(),'5,3,pi':(),'5,3,3pi2':(),
'5,4,0':(),'5,4,pi2':(),'5,4,pi':(),'5,4,3pi2':(),
'5,5,0':('L'),'5,5,pi2':('M'),'5,5,pi':('R'),'5,5,3pi2':(),
'5,6,0':('M'),'5,6,pi2':('R'),'5,6,pi':(),'5,6,3pi2':(),
'5,7,0':(),'5,7,pi2':(),'5,7,pi':(),'5,7,3pi2':(),
'5,8,0':(),'5,8,pi2':(),'5,8,pi':(),'5,8,3pi2':(),
'5,9,0':(),'5,9,pi2':(),'5,9,pi':(),'5,9,3pi2':(),
'5,10,0':(),'5,10,pi2':(),'5,10,pi':(),'5,10,3pi2':(),
'6,1,0':(),'6,1,pi2':(),'6,1,pi':(),'6,1,3pi2':(),
'6,2,0':(),'6,2,pi2':(),'6,2,pi':(),'6,2,3pi2':(),
'6,3,0':(),'6,3,pi2':(),'6,3,pi':(),'6,3,3pi2':(),
'6,4,0':(),'6,4,pi2':(),'6,4,pi':(),'6,4,3pi2':(),
'6,5,0':(),'6,5,pi2':(),'6,5,pi':('M'),'6,5,3pi2':('R'),
'6,6,0':('R'),'6,6,pi2':(),'6,6,pi':(),'6,6,3pi2':('M'),
'6,7,0':(),'6,7,pi2':(),'6,7,pi':(),'6,7,3pi2':(),
'6,8,0':(),'6,8,pi2':(),'6,8,pi':(),'6,8,3pi2':(),
'6,9,0':(),'6,9,pi2':(),'6,9,pi':(),'6,9,3pi2':(),
'6,10,0':(),'6,10,pi2':(),'6,10,pi':(),'6,10,3pi2':(),
'7,1,0':(),'7,1,pi2':(),'7,1,pi':(),'7,1,3pi2':(),
'7,2,0':(),'7,2,pi2':(),'7,2,pi':(),'7,2,3pi2':(),
'7,3,0':(),'7,3,pi2':(),'7,3,pi':(),'7,3,3pi2':(),
'7,4,0':(),'7,4,pi2':(),'7,4,pi':(),'7,4,3pi2':(),
'7,5,0':(),'7,5,pi2':(),'7,5,pi':(),'7,5,3pi2':(),
'7,6,0':(),'7,6,pi2':(),'7,6,pi':(),'7,6,3pi2':(),
'7,7,0':(),'7,7,pi2':(),'7,7,pi':(),'7,7,3pi2':(),
'7,8,0':(),'7,8,pi2':(),'7,8,pi':(),'7,8,3pi2':(),
'7,9,0':(),'7,9,pi2':(),'7,9,pi':(),'7,9,3pi2':(),
'7,10,0':(),'7,10,pi2':(),'7,10,pi':(),'7,10,3pi2':(),
'8,1,0':(),'8,1,pi2':(),'8,1,pi':(),'8,1,3pi2':(),
'8,2,0':(),'8,2,pi2':(),'8,2,pi':(),'8,2,3pi2':(),
'8,3,0':(),'8,3,pi2':(),'8,3,pi':(),'8,3,3pi2':(),
'8,4,0':(),'8,4,pi2':(),'8,4,pi':(),'8,4,3pi2':(),
'8,5,0':(),'8,5,pi2':(),'8,5,pi':(),'8,5,3pi2':(),
'8,6,0':(),'8,6,pi2':(),'8,6,pi':(),'8,6,3pi2':(),
'8,7,0':(),'8,7,pi2':(),'8,7,pi':(),'8,7,3pi2':(),
'8,8,0':(),'8,8,pi2':(),'8,8,pi':(),'8,8,3pi2':(),
'8,9,0':(),'8,9,pi2':(),'8,9,pi':(),'8,9,3pi2':(),
'8,10,0':(),'8,10,pi2':(),'8,10,pi':(),'8,10,3pi2':(),
'9,1,0':(),'9,1,pi2':(),'9,1,pi':(),'9,1,3pi2':(),
'9,2,0':(),'9,2,pi2':(),'9,2,pi':(),'9,2,3pi2':(),
'9,3,0':(),'9,3,pi2':(),'9,3,pi':(),'9,3,3pi2':(),
'9,4,0':(),'9,4,pi2':(),'9,4,pi':(),'9,4,3pi2':(),
'9,5,0':(),'9,5,pi2':(),'9,5,pi':(),'9,5,3pi2':(),
'9,6,0':(),'9,6,pi2':(),'9,6,pi':(),'9,6,3pi2':(),
'9,7,0':(),'9,7,pi2':(),'9,7,pi':(),'9,7,3pi2':(),
'9,8,0':(),'9,8,pi2':(),'9,8,pi':(),'9,8,3pi2':(),
'9,9,0':(),'9,9,pi2':(),'9,9,pi':(),'9,9,3pi2':(),
'9,10,0':(),'9,10,pi2':(),'9,10,pi':(),'9,10,3pi2':(),
'10,1,0':(),'10,1,pi2':(),'10,1,pi':(),'10,1,3pi2':(),
'10,2,0':(),'10,2,pi2':(),'10,2,pi':(),'10,2,3pi2':(),
'10,3,0':(),'10,3,pi2':(),'10,3,pi':(),'10,3,3pi2':(),
'10,4,0':(),'10,4,pi2':(),'10,4,pi':(),'10,4,3pi2':(),
'10,5,0':(),'10,5,pi2':(),'10,5,pi':(),'10,5,3pi2':(),
'10,6,0':(),'10,6,pi2':(),'10,6,pi':(),'10,6,3pi2':(),
'10,7,0':(),'10,7,pi2':(),'10,7,pi':(),'10,7,3pi2':(),
'10,8,0':(),'10,8,pi2':(),'10,8,pi':(),'10,8,3pi2':(),
'10,9,0':(),'10,9,pi2':(),'10,9,pi':(),'10,9,3pi2':(),
'10,10,0':(),'10,10,pi2':(),'10,10,pi':(),'10,10,3pi2':(),
'Out':()}
# start = time.time()
# (Delta,Tdelta)=t.Compute_tolerance_level(grid,f1,Qinv)
# Delta_full = [(Tdelta.vs[e.source]['name'],e['label'],Tdelta.vs[e.target]['name']) for e in Tdelta.es]
# end = time.time() - start
# print("Delta for f1 has ",len(Delta)," new transitions", len(grid.es))
# print("##################################")
# print("Time to compute delta: ",end)
# print("##################################")
n2id = dict()
for v in grid.vs:
	n2id[v['name']]= v.index
pert = []
d1 = 5
d3 = 5
for x in range(1,N+1):
	for y in range(1,N+1):	
		for d2 in range(1,d1+1):		
			if x+d2+1<=N:
				pert.append((','.join([str(x),str(y),'0']),'M',','.join([str(x+d2+1),str(y),'0'])))
			else:
				pert.append((','.join([str(x),str(y),'0']),'M','Out'))
			if x-d2-1>=1:
				pert.append((','.join([str(x),str(y),'pi']),'M',','.join([str(x-d2-1),str(y),'pi'])))
			else:
				pert.append((','.join([str(x),str(y),'pi']),'M','Out'))
			if y+d2+1<=N:
				pert.append((','.join([str(x),str(y),'pi2']),'M',','.join([str(x),str(y+d2+1),'pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'pi2']),'M','Out'))
			if y-d2-1>=1:
				pert.append((','.join([str(x),str(y),'3pi2']),'M',','.join([str(x),str(y-d2-1),'3pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'3pi2']),'M','Out'))
		for d2 in range(1,d3+1):
			#TURN L
			if x+d2<=N and y+d2<=N:
				pert.append((','.join([str(x),str(y),'0']),'L',','.join([str(x+d2),str(y+d2),'pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'0']),'L','Out'))
			if x+d2<=N and y-d2>=1:
				pert.append((','.join([str(x),str(y),'3pi2']),'L',','.join([str(x+d2),str(y-d2),'0'])))
			else:
				pert.append((','.join([str(x),str(y),'3pi2']),'L','Out'))
			if x-d2>=1 and y-d2>=1:
				pert.append((','.join([str(x),str(y),'pi']),'L',','.join([str(x-d2),str(y-d2),'3pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'pi']),'L','Out'))
			if x-d2>=1 and y+d2<=N:
				pert.append((','.join([str(x),str(y),'pi2']),'L',','.join([str(x-d2),str(y+d2),'pi'])))
			else:
				pert.append((','.join([str(x),str(y),'pi2']),'L','Out'))
			#TURN R
			if x+d2<=N and y+d2<=N:
				pert.append((','.join([str(x),str(y),'pi2']),'R',','.join([str(x+d2),str(y+d2),'0'])))
			else:
				pert.append((','.join([str(x),str(y),'pi2']),'R','Out'))
			if x+d2<=N and y-d2>=1:
				pert.append((','.join([str(x),str(y),'0']),'R',','.join([str(x+d2),str(y-d2),'3pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'0']),'R','Out'))
			if x-d2>=1 and y-d2>=1:
				pert.append((','.join([str(x),str(y),'3pi2']),'R',','.join([str(x-d2),str(y-d2),'pi'])))
			else:
				pert.append((','.join([str(x),str(y),'3pi2']),'R','Out'))
			if x-d2>=1 and y+d2<=N:
				pert.append((','.join([str(x),str(y),'pi']),'R',','.join([str(x-d2),str(y+d2),'pi2'])))
			else:
				pert.append((','.join([str(x),str(y),'pi']),'R','Out'))
# print(d)
# C = t.Control(grid,f1)
# print(C)
# print(len(Delta))
# print(set(pert).difference(set(Delta_full)))
# print(Qinv)
# if set(pert).issubset(set(Delta_full)):
print(len(pert))
start = time.time()
f = t.Compute_tolerant_controller(grid,Qinv,pert)
end = time.time() - start
print(end)
# start = time.time()
# (Delta,Tdelta)=t.Compute_tolerance_level(grid,f,Qinv)
# end = time.time() - start
# print(end)
# print(len(Delta))
# C = t.Control(grid,f)
# inacc = d.unary.find_inacc(C)
# C.delete_vertices(inacc)
# print(C)
# print(f)
# f = t.Compute_empty_controller(grid,Qinv)
# (Delta,Tdelta)=t.Compute_tolerance_level(grid,f,Qinv)
# print(len(Delta))
# f = t.Compute_inv_controller(grid,Qinv)
# (Delta,Tdelta)=t.Compute_tolerance_level(grid,f,Qinv)
# print(len(Delta))
# print(f)



{
'1,1,0': ('L', 'M', 'R'), '1,1,p2': ('L', 'R'), '1,1,p': ('L', 'R'), '1,1,3p2': ('L', 'M', 'R'), 
'2,1,0': ('L', 'M', 'R'), '2,1,p2': ('L', 'R'), '2,1,p': ('L', 'R'), '2,1,3p2': ('L', 'R'), 
'3,1,0': ('L', 'M', 'R'), '3,1,p2': ('L', 'M', 'R'), '3,1,p': ('L', 'R'), '3,1,3p2': ('L', 'R'),
'1,2,0': ('L', 'R'), '1,2,p2': ('L', 'R'), '1,2,p': ('L', 'R'), '1,2,3p2': ('L', 'M', 'R'), 
'2,2,0': ('L', 'R'), '2,2,p2': ('L', 'R'), '2,2,p': ('L', 'R'), '2,2,3p2': ('L', 'R'), 
'3,2,0': ('L', 'M', 'R'), '3,2,p2': ('L', 'M', 'R'), '3,2,p': ('L', 'M', 'R'), '3,2,3p2': ('L', 'R'), 
'1,3,0': ('L', 'R'), '1,3,p2': ('L', 'R'), '1,3,p': ('L', 'M', 'R'), '1,3,3p2': ('L', 'M', 'R'), 
'2,3,0': ('L', 'R'), '2,3,p2': ('L', 'M', 'R'), '2,3,p': ('L', 'M', 'R'), '2,3,3p2': ('L', 'M', 'R'), 
'3,3,0': ('L', 'R'), '3,3,p2': ('L', 'M', 'R'), '3,3,p': ('L', 'M', 'R'), '3,3,3p2': ('L', 'R'), 
'OUT': ()}