yl = []
t = True
for i in xl:
  if i == '':
    continue
  xll = i.split('\t')
  if len(xll) <5:
    continue
  yl.append('\t'.join([xll[1], xll[4], xll[3], xll[2]]))