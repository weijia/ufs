def parse(headLine, lines, handlerObj):
  #Collect headers.
  heads = []
  fieldCnt = 0
  for i in lines[0:headLine]:

    ws = i.split(',')
    for k in ws:
      #print fieldCnt
      try:
        heads[fieldCnt] += k
      except IndexError:
        heads.append(k)
      fieldCnt += 1
  
  #Get datas
  
  for i in lines[headLine:]:
    if i.replace(' ','') == '':
      continue
    #print 'processing:', i
    j = i.split(',')
    fieldCnt = 0
    for k in j:
      #print 'processing value:',k
      try:
        head = heads[fieldCnt]
      except IndexError:
        head = 'no header'
      handlerObj.genItem(fieldCnt, head, k)
      fieldCnt += 1
    handlerObj.genLine()

      
class mecaCoreArrayGenerator:
  def __init__(self, arrayName):
    self.continueCountFlag = True
    self.arrayName = arrayName
    if self.continueCountFlag:
      self.elementCnt = None
    else:
      self.elementCnt = 0
    self.output = []
  def genItem(self, cnt, name, value):
    #Use the TF count for the test case number
    if self.continueCountFlag:
      if self.elementCnt is None:
        self.elementCnt = int(value)

    self.output.append('##'+name)
    self.output.append('%s[%d][%d] = "%s"'%(self.arrayName,self.elementCnt, cnt,value))

  def genLine(self):
    self.elementCnt += 1

m = mecaCoreArrayGenerator('@gpcfichParameter')

il = []

for i in x.split('\n'):
  i = i.replace('\r','')
  il.append(i)

  
parse(2, il, m)

y = '\n'.join(m.output)