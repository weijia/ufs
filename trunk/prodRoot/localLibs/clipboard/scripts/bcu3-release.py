def bcu3VerReplace(x):
  mapping={
  '{-TECH}':'-TDD',
  '{-tech}':'-tdd',
  'P.XX.YY':'1.03.00',
  'COREID':'q19420',
  'P.QQ.RR':'1.02.00'
  }
  y = x
  for i in mapping.keys():
    y = y.replace(i, mapping[i])
  return y

y = bcu3VerReplace(x)
t = (not (y == x))