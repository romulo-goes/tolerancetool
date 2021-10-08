import subprocess
import time

path = subprocess.run(args = ["pwd"],stdout = subprocess.PIPE)
path = str(path.stdout)
path = path[2:len(path)-3]

start = time.time()
subprocess.run(args = ["../../FuseIC3","-f","2","vmt"])
print(time.time()-start)