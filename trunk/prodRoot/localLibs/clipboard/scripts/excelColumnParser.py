z = {}
emptyCnt = 0
caseNum = 0
fieldList = []
for i in xl:
  if i == '':
    continue
  l = i.split(',')
  if len(l) > 1:
    caseNum = len(l)-1
  print caseNum
  if l[0] == '':
    l[0] = '%d'%emptyCnt
    emptyCnt += 1
  fieldList.append(l[0])
  z[l[0]] = l[1:]

print z
yl = []
for i in range(0,caseNum):
  paramCnt = 0
  for j in fieldList:
    #print '------------------------------------------------',j
    yl.append('##%s'%j)

    try:
      yl.append('@gPucchTestParameter[%d][%d] = "%s"'%(i, paramCnt, z[j][i]))
    except:
      print 'j:',j,',','i:',i
      print z[j]
      print z.keys()
      raise 'error'
    paramCnt += 1
