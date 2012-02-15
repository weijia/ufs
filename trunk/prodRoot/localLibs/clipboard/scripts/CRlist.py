yl = []
t = True
for i in xl:
  if i == '':
    continue
  xll = i.split('\t')
  if len(xll) <5:
    t = False
    break
    print 'breaking'
  if False:
    if xll[3] == 'New Feature':
      yl.append('\t'.join(xll[1:5]))
  else:
    if xll[3] == 'Fault':
      se = xll[6][2:]
      yl.append('\t'.join([xll[1], xll[2], se, xll[4]]))