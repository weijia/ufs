#import libs.html.response
#import libs.platform.services


#import libs.services.services



import string
import uuid
def importFile(inputFile, root, db, nS, bigValueDb):
  import libs.tree.namedTreeItem
  mecacoreRoot = str(uuid.uuid4())
  mecacoreRootId = root.addNamedChild(mecacoreRoot+'mecacoreRoot')
  mecaCoreMain = libs.tree.namedTreeItem.namedTreeItem(mecacoreRootId, db, nS, bigValueDb)
  nameHash = {'Main': mecaCoreMain}#{Name: item ID}
  childHash = {'Main':[]}
  cnt = 0
  for i in inputFile.split('\n'):
    i = i.replace('\r','')
    cnt += 1
    if cnt > 10:
      pass#break#pass#return
    if i == '':
      continue
    if i[0] == ';':
      continue
    l = i.split('=')
    if len(l) == 1:
      l = i.split('+')
    left = string.strip(l[0])
    right = string.strip(l[1])
    if left[0]=='$':
      #$TDD Test Menu %1 = XXXXXX
      #$TDD Test Menu %2 = YYYYYY
      parent = string.strip(left.split('%')[0])[1:]
      child = string.strip(right)
      try:
        n = nameHash[parent].addNamedChild(child)#add the child
      except KeyError:
        print 'has no parent: %s'%parent
        continue
      print 'adding:',child,'<br/>'
      if childHash.has_key(parent):
        childHash[parent].append(n)#Will generate sequence later using this field
      else:
        childHash[parent] = [n]#Will generate sequence later
      nameHash[child] = libs.tree.namedTreeItem.namedTreeItem(n, db, nS, bigValueDb)
  #print childHash
  for i in childHash.keys():
    nameHash[i].updateSequence(childHash[i])
    #print childHash[i]
    
def importMecaCore():
    import libs.services.services
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.genHead('nobody')
    h.write('<body>')
    user = s.getUserAutoRedirect('/apps/moto/importMecacoreMenuDb.py')
    if user is None:
        h.write('user is None')
        h.genEnd()
        return
    f = s.getQuery()
    #print f
    if not f.has_key('uploadFile'):
      h.write("didn't have uploadFile filed")
      h.genForm('/apps/moto/importMecacoreMenuDb.py',[['f','uploadFile']])
    else:
      #Process the file
      h.write('has uploadFile')
      import libs.platform.ufsDbManagerInterface
      mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()
      u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
      print 'user is:%s'%u.getUserId()
      db = mngr.getSimpleDb(u, 'treeImporterDb')
      bigValueDb = mngr.getSimpleDbWithBigValue(u, 'treeImporterBigValueDb')
      nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
      import libs.services.nameService
      nS = libs.services.nameService.nameService(nameDb)
      testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
      h.write('nS is OK')
      import libs.tree.namedTreeItem
      root = libs.tree.namedTreeItem.namedTreeItem(testRoot, db, nS, bigValueDb)
      importFile(f['uploadFile'][0], root,db, nS, bigValueDb)

    print '</body>'
    h.genEnd()
    
    
importMecaCore()