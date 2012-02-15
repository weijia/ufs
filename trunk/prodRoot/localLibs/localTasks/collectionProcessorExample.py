import localLibs.localTasks.processorBase as processorBase


class encZipExtractor(processorBase.cacheCollectionProcessorBase):
    def __init__(self, taskId, appUuid, collectionId)
        processorBase.cacheCollectionProcessorBase.__init__(self, taskId, appUuid, collectionId)
        
    def subClassInitialCfg(self):
        '''
        Used by sub class to create config for itself.
        '''
        return {}

    def subClassProcessItem(self, processingObj):
        pass