import sys
import os
c = os.getcwd()#For python built in server, it will be server path
#print c
#For twisted server it will be where the script executed
while c.find('wwjufsdatabase') != -1:
  c = os.path.dirname(c)

sys.path.insert(0, os.path.join(c,'wwjufsdatabase'))