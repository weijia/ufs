
def showItemWithoutJs():
    import libs.tree.jsTreeNamedItemFunc


    import libs.services.services
    s = libs.services.services.services()
    h = s.getHtmlGen()
    h.genHead('hello world')

    f = s.getQuery()


    import libs.platform.ufsDbManagerInterface
    mngr = libs.platform.ufsDbManagerInterface.ufsDbManager()

    user = s.getUserAutoRedirect('/apps/test/mobileItem.py')
    if user is None:
        h.genEnd()
        return
    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    if f.has_key('treeImporterDb'):
        dbName = f['treeImporterDb'][0]
    else:
        dbName = 'treeImporterDb'
    if u is None:
        raise 'user name is None'
    db = mngr.getSimpleDb(u, dbName)
    nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
    import libs.services.nameService
    nS = libs.services.nameService.nameService(nameDb)


    if f.has_key('treeRoot'):
      d = f['treeRoot'][0]
    else:
      d = '3fe6382b-0219-40c7-add3-2f3b60aeb368'
    bigValueDb = mngr.getSimpleDbWithBigValue(u, 'treeImporterBigValueDb')
    import libs.tree.namedTreeItem
    n = libs.tree.namedTreeItem.namedTreeItem(d, db, nS, bigValueDb)
    p = n.getContainer()
    if p is None:
      #print 'p is None'
      p = d

    
    #print p
    #print 'sparation---------------------------------------'

    pItem = libs.tree.namedTreeItem.namedTreeItem(p, db, nS)
    #print 'sparation---------------------------------------'

    #print pItem
    import libs.platform.services
    en = libs.platform.services.getEncodingService()

    h.write('parent:<a href="/apps/test/mobileItem.py?treeRoot=%(id)s">%(name)s</a>'%{'id':p,'name':en.en(pItem.getItemName())})
    #print 'sparation---------------------------------------'
    h.write(en.en(u'current:%s'%n.getItemName()))
    h.br()

    defaultStorageDbName = 'testStorageDb'

    storeDb = mngr.getStorageDb(u, defaultStorageDbName)


    sys_itemTextAttr = 'sys_item_text'

    dataId = db.getAttr(d, sys_itemTextAttr)
    submitUrl = '/apps/tree/updateItem.py'
    #h.write('data id is:'+dataId)
    #submitUrl = '/apps/test/testParam.py'
    if dataId is None:
        #Data does not exist
        h.genForm(submitUrl,[['t','itemName',en.en(n.getItemName())],['a','itemText'],['h','itemId',en.en(n.getItemAbsPath())],['h','oldItemName',en.en(n.getItemName())],['f','itemFile']])
    else:
        #Data exists
        h.genForm(submitUrl,[['t','itemName',en.en(n.getItemName())],['a','itemText',storeDb.getData(dataId)],['h','itemId',en.en(n.getItemAbsPath())],['h','oldItemName',en.en(n.getItemName())],['f','itemFile']])
    
    res = libs.tree.jsTreeNamedItemFunc.dirlist(n, '<a href="/apps/test/mobileItem.py?treeRoot=%(id)s">%(name)s</a>')
    #print 'sparation---------------------------------------'

    h.write('<ul>')
    h.write(res)
    h.write('</ul>')
    #print 'sparation---------------------------------------'
    h.genForm('/apps/tree/addItem.py',[['t','itemName'],['a','itemText'],['h','treeRoot',en.en(d)],['f','itemFile']])
    h.genEnd()
    
    
showItemWithoutJs()