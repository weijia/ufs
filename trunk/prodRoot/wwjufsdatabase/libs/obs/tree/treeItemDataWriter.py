import uuid

def storeItemData(dbName, itemId, itemData, sessionInst, dataId = None):
    defaultStorageDbName = sessionInst.getParam('itemStorageDb', 'testStorageDb')

    d = sessionInst.getStorage(defaultStorageDbName)
    if dataId is None:
        dataId = unicode(uuid.uuid4())

    db = sessionInst.getSimpleDb(dbName)

    d.storeData(dataId, itemData)
    sys_itemTextAttr = 'sys_item_text'
    att = db.getAttr(itemId, sys_itemTextAttr)

    db.update(itemId, sys_itemTextAttr, att, dataId)
