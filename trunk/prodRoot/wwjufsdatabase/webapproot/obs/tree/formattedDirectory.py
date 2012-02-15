import os

def basename(p):
  '''
  Here, whatever the directory is end with '/', the basename is always not ''.
  '''
  return os.path.basename(p)
  
  
  
def dirname(p):
  d = os.path.dirname(p)
  return d.replace('\\'.'/')