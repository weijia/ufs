'''
Created on Nov 2, 2011

@author: Richard
'''

import uuid

import localLibSys
import localLibs.localTasks.processorBaseV2 as processorBase
from localLibs.logSys.logSys import *

gAppUuid = 'ff97a8d4-9696-4920-a65b-ac8090245b9d'

class syncer(object):
    '''
    classdocs
    '''
    def __init__(self, taskId, srcCollectionFactory, 
                            destCollectionFactory, comparer, appUuid = gAppUuid):
        processorBase.processorBase.__init__(self, taskId, appUuid)
        self.appConfigObj = self.getAppCfg()
        self.comparer = comparer
        if self.appConfigObj is None:
            self.appConfigObj = {}
            self.appConfigObj["srcStateObjId"] = unicode(str(uuid.uuid4()))
            self.appConfigObj["destStateObjId"] = unicode(str(uuid.uuid4()))
            self.saveAppConfig()
        else:
            self.expectedDict = {}         
            self.checkParamInternal(self.expectedDict)

        #Set 2 collections
        self.src = srcCollectionFactory.getSrcCollection(self.appConfigObj["srcStateObjId"])
        self.dest = destCollectionFactory.getDestCollection(self.appConfigObj["destStateObjId"])
        ncl(self.appConfigObj)
        
    def syncFromSrc2Dest(self):
        for i in self.src.enumObjs():
            srcIdInCol = i.getIdInCol()
            if self.dest.exists(i):
                destObjUuid = self.dest.getObjUuid(srcIdInCol)
                if not self.comparer.isUpdated(i.getUuid(), destObjUuid):
                    continue
            self.dest.store(i)
            self.src.updateState()
        self.dest.enumEnd()            