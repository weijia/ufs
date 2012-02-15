x = x.replace('\r','')
lx = x.split('\n')
yl=[]
for i in lx:
 yl.append(i.split('\t')[0])
y = '\n'.join(yl)