import sys
import os
c = os.getcwd()
r = 'prodRoot'
while c.find(r) != -1:
  c = os.path.dirname(c)
print c
sys.path.insert(0, os.path.join(c,r))
