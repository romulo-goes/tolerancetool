import os
import sys
import subprocess
import ctypes
#Getting absolute path to where script is being executed


path_script=os.path.dirname(os.path.realpath(__file__))
print("############## Running toy example in the paper (Example 3)####################")
subprocess.run(["python3", path_script+"/examples/Toy Example/toy.py"])
input("Press Enter to continue...")
print("############## Running motivating example in the paper ####################")
subprocess.run(["python3", path_script+"/examples/Surveillance Example/surv.py"])

# os.system('python3 /Users/romulo/Dropbox(University of Michigan)/Documents/Research/Postdoc/2021/Robustness/tolerancetool/examples/toy/toy.py')
