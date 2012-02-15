import sys
import os
c = os.getcwd()
while c.find('prodRoot') != -1:
  c = os.path.dirname(c)
#print c
f = os.path.join(c,'prodRoot')
sys.path.insert(0, f)
sys.path.insert(0, os.path.join(f,'wwjufsdatabase'))
