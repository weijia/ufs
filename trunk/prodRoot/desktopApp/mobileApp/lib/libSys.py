import sys
import os
c = os.getcwd()
sys.path.insert(0, os.path.join(c, 'lib'))
while c.find('wwjufsdatabase') != -1:
  c = os.path.dirname(c)
print c
sys.path.insert(0, os.path.join(c,'wwjufsdatabase'))

