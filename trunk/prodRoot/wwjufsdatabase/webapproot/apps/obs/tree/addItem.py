from libs.tree.treeItemDataWriter import storeItemData



def addItem():
    import libs.services.services
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.genHead('hello world')


    f = s.getQuery()


    import libs.platform.ufsDbManagerInterface
    mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

    user = s.getUserAutoRedirect('/apps/tree/addItem.py')
    if user is None:
        h.end()
        return


    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    treeImportDb = s.getParam('treeImporterDb', 'treeImporterDb')
    treeNameDb = s.getParam('treeImporterNameDb', 'treeImporterNameDb')
    itemSequenceDb = s.getParam('treeImporterBigValueDb', 'treeImporterBigValueDb')

    testRoot = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
    treeRoot = f.get('treeRoot', [testRoot])[0]
    if treeRoot == '0':
      treeRoot = testRoot
      
    i = s.getTreeItem(treeImportDb, treeNameDb,treeRoot,itemSequenceDb)

    itemId = i.addNamedChild(s.getParam('itemName'), f.get('itemId', [None])[0])

    '''
    Store text if there is
    '''
    if s.hasParam('itemText'):
      if not s.getParam('itemText') == '':
        storeItemData(treeImportDb, itemId, s.getEncoder().en(s.getParam('itemText')),s, s.getParam('itemDataId'))

    '''
    Store file if there is
    '''
    if s.hasParam('itemFile'):
      h.write('has item file')
      dataFileContent = s.getRawParam('itemFile')
      if not (dataFileContent == ''):
        storeItemData(treeImportDb, itemId, dataFileContent,s, s.getParam('itemDataId'))

      
    '''
    Redirect to the item page
    '''
    h.redirect('/apps/test/mobileItem.py')
    h.genEnd()

addItem()