from libs.tree.treeItemDataWriter import storeItemData



def updateItem():
    import libs.services.services
    s = libs.services.services.services()
    h = s.getHtmlGen()
    
    h.genHead('hello world')

    f = s.getQuery()


    import libs.platform.ufsDbManagerInterface
    mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

    user = s.getUserAutoRedirect('/apps/tree/updateItem.py')
    if user is None:
        h.genEnd()
        return

    itemId = s.getParam('itemId')

    treeImportDb = s.getParam('treeImporterDb', 'treeImporterDb')
    treeNameDb = s.getParam('treeImporterNameDb', 'treeImporterNameDb')
    itemSequenceDb = s.getParam('treeImporterBigValueDb', 'treeImporterBigValueDb')
    i = s.getTreeItem(treeImportDb, treeNameDb,itemId,itemSequenceDb)
    
    if s.hasParam('itemName'):
        i.renameItemName(s.getParam('itemName'))

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

updateItem()