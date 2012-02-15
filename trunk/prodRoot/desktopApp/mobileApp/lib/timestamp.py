def timestamp():
  from time import gmtime, strftime, localtime
  t = strftime("%Y%m%d_%H%M%S", localtime())
  return t
