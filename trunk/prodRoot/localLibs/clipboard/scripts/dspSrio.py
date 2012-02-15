def removeLeadingSpace(l):
  print l
  while l[0] == ' ' and len(l)>1:
    l = l[1:]
  return l

yl = []
for i in xl:
  if i.replace(' ','') == '':
    pass
    yl.append('')
  else:
    i = removeLeadingSpace(i)
    yl.append('#'+i)
    o = i.replace(';','#')
    o = o.replace('DspSrioWordWrite', 'writeFpga')
    o = o.replace('fpgasrioid', '$vFpgaSrioId')
    o = o.replace(',"', ',0x')
    o = o.replace('"', '')
    yl.append(o)