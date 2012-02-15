import sys
import os
c = os.getcwd()
appRoot = 'directProxy'
while c.find(appRoot) != -1:
  c = os.path.dirname(c)
#print c
sys.path.insert(0, os.path.join(c,appRoot))
