import localLibSys
from localLibs.thumb.thumbInterface import getThumb
from localLibs.logSys.logSys import *


class ThumbCollector(object):
    
    default_thumb_info_size = 100
    
    def __init(self, working_dir):
        self.working_dir = working_dir
    def collect_thumb(self, itemObj, trunk_storage):
        '''
        Schema 1: return dict that contains compressed size, may need to scan all items
            in dict, such as thumb compressed size and file compressed size
        Schema 2: only return size, store collected info directly to trunk storage
        '''
        infoDict = itemObj.getItemInfo()
        fullPath = itemObj["fullPath"]
        #Add thumb info
        thumbFullPath = getThumb(fullPath, self.working_dir)
        if not (thumbFullPath is None):
            thumbObj = self.dbInst.getFsObjFromFullPath(thumbFullPath)
            thumbUfsUrl = thumbObj.getObjUfsUrl()
            infoDict["thumbnailFullPath"] = thumbFullPath
            infoDict["thumbnailUuid"] = thumbObj["uuid"]
            infoDict["thumbnailUrl"] = thumbUfsUrl
            infoDict["thumbnailHeadMd5"] = thumbObj.headMd5()
            #Store thumbnail info
            trunk_storage.add_info(thumbUfsUrl, thumbObj.getItemInfo())
            #########################################
            #Add thumb file to zip, it is not stored until finalize the current trunk
            #########################################
            thumbnailZippedInfo = self.getZipFile().addfile(unicode(thumbFullPath), 
                                                            unicode(thumbFullPath))
            ####################################################
            #Add item info, it is not stored until finalize the current trunk
            ####################################################
            trunk_storage.add_info(itemObj.getObjUfsUrl(), infoDict)
            ncl(infoDict)
            
            return self.default_thumb_info_size*2 + thumbnailZippedInfo.compress_size
        else:
            cl("No thumb generated")
            return 0