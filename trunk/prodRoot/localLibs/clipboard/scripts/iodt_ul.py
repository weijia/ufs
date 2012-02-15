content = []
head = []
yl = []
for i in xl:
  n = i.split('\t')
  if len(n) > 1:
    head.append(n[0])
    casecnt = 0
    for j in n[1:]:
      try:
        content[casecnt].append(j)
      except:
        content.append([])
        content[casecnt].append(j)
      casecnt += 1
casecnt = 0
for k in content:
  fieldcnt = 0
  for m in k:
    yl.append('##'+head[fieldcnt])
    yl.append('@gPuschParam[%d][%d] = "%s"'%(casecnt,fieldcnt,m))
    fieldcnt += 1
  casecnt += 1