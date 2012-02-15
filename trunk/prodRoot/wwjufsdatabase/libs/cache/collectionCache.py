import libSys
import os
import uuid
import libs.utils.misc
import libs.ufsDb.dictShoveDb as dictShoveDb

childListInitialCnt = 30
class nullLog:
    def l(self, s):
        pass
import sys
        
        
class collectionCache:
    def __init__(self, collectionId):
        self.collectionId = collectionId
        self.childListContainerDb = dictShoveDb.getListDbForDirCacheDb('childListContainerDb')
        self.childListDb = dictShoveDb.getListDbForDirCacheDb('childListDb')


    def listNamedChildrenPerRangeWithoutAutoRefresh(self, start, cnt, log = nullLog()):
        '''
        start: from index 0
        '''
        res = ['start list']
        res = []
        childListContainerList = self.childListContainerDb[self.collectionId]
        log.l(str(childListContainerList)+','+self.collectionId)
        log.l('start:%d, cnt:%d'%(start,cnt))
        curListStart = 0
        for containerItem in childListContainerList:
            childListContainerId, childListLength = containerItem.split(',')
            childListLength = int(childListLength)
            log.l(childListContainerId+','+str(childListLength)+',----'+str(start)+',----'+str(cnt))
            if start <= curListStart+int(childListLength):
                #Find the first childList that will be displayed
                log.l("start to add items")
                childListContainer = self.childListDb[childListContainerId]
                cntInList = 0
                for childName in childListContainer:
                    log.l("adding res:"+childName)
                    log.l(str(curListStart)+','+str(cntInList)+',----'+str(start)+',----'+str(cnt))
                    if start <= curListStart+cntInList:
                        #res.append(str(curListStart+cntInList)+','+str(start+cnt))
                        res.append(childName)
                        log.l('adding:'+childName)
                    cntInList += 1
                    if start+cnt <= curListStart+cntInList:
                        #All requested cnt has been added, return it
                        log.l('returning last:'+str(res).encode("gbk","replace"))
                        return res
            
            curListStart = curListStart + int(childListLength)
        return res
    def listNamedChildrenPerRangeWithAutoRefresh(self, start, cnt, iter = None, log = nullLog()):
        '''
        iter should return unicode strings
        '''
        try:
            return self.listNamedChildrenPerRangeWithoutAutoRefresh(start, cnt, log)
        except KeyError:
            '''
            Currently, we rebuild the list whenever list container or list are not OK
            '''
            self.refreshWithoutCleanOld(iter, log)#Need to clean un-referenced items periodically and manually
            return self.listNamedChildrenPerRangeWithoutAutoRefresh(start, cnt, log)
    def refreshWithoutCleanOld(self, iter, log = nullLog()):
        childListContainerList = []
        curChildList = []
        curChildListUuid = unicode(uuid.uuid4())
        curElemInChildList = 0
        for i in iter:
            curChildList.append(i)
            log.l('adding:'+i)
            curElemInChildList += 1
            if curElemInChildList > childListInitialCnt:
                #Store into database
                self.childListDb[curChildListUuid] = curChildList
                childListContainerList.append(u"%s,%d"%(curChildListUuid,curElemInChildList))
                log.l('appending:%s'%str([curChildListUuid,curElemInChildList]))
                #Create a new child list
                curChildListUuid = unicode(uuid.uuid4())
                curElemInChildList = 0
                curChildList = []
        if 0 != curElemInChildList:
            #reminder,save them as well
            self.childListDb[curChildListUuid] = curChildList
            childListContainerList.append(u"%s,%d"%(curChildListUuid,curElemInChildList))
            log.l('appending:%s'%str([curChildListUuid,curElemInChildList]))
        #Scan complete, save childListContainer
        self.childListContainerDb[self.collectionId] = childListContainerList
        
        log.l('storing:%s to %s'%(str(childListContainerList),self.collectionId))