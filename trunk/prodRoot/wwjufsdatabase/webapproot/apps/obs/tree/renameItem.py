def renameItem():
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


    u = libs.platform.ufsDbManagerInterface.ufsUserExample(user)
    if f.has_key('treeImporterDb'):
      dbName = f['treeImporterDb'][0]
    else:
      dbName = 'treeImporterDb'
    db = mngr.getSimpleDb(u, dbName)
    nameDb = mngr.getSimpleDb(u, 'treeImporterNameDb')
    import libs.services.nameService
    nS = libs.services.nameService.nameService(nameDb)
    en = libs.platform.services.getEncodingService()
    renameItemId = en.de(f['itemId'][0])

    import libs.tree.namedTreeItem
    i = libs.tree.namedTreeItem.namedTreeItem(renameItemId, db, nS)

    #As the string passed from client will have a space before the text, remove it first using [1:]
    itemId = i.renameItemName(en.de(f['itemNewName'][0])[1:])
      
    '''
    Redirect to the item page
    '''
    h.redirect('/apps/test/mobileItem.py')
    h.genEnd()

renameItem()