import localLibSys
from localLibs.thumb.thumbInterface import getThumb
import localLibs.utils.misc as misc
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp/working/thumbs"

class InfoCollectorInterface(object):
    def collect_info(self, item_obj, info_dict, trunk_storage):
        pass
    
    def add_new_info(self, info_dict, item_url, item_info_dict):
        if info_dict.has_key(item_url):
            info_dict[item_url] = dict(info_dict[item_url].items() + item_info_dict)
        else:
            info_dict[item_url] = item_info_dict
                
class ThumbCollector(InfoCollectorInterface):
    
    default_thumb_info_size = 100
    
    def __init__(self, working_dir = gWorkingDir):
        super(ThumbCollector, self).__init__()
        self.working_dir = working_dir
        misc.ensureDir(working_dir)
        self.dbInst = objectDatabase.objectDatabase()
        #self.trunk_storage = trunk_storage
        
        # TODO: Create a dict that can combine new dict to it.
        #self.collectionInfoDict = {}
        #self.additionalInfoDict = {}
        
        
    def collect_info(self, obj_item, info_dict, trunk_storage):
        '''
        Schema 1: return dict that contains compressed size, may need to scan all items
            in dict, such as thumb compressed size and file compressed size
        Schema 2: only return size, store collected info directly to trunk storage
        '''
        item_info_dict = obj_item.getItemInfo()
        fullPath = obj_item["fullPath"]
        mime_type = obj_item["mime_type"]
        #Add thumb info
        thumbFullPath = getThumb(fullPath, self.working_dir, mime_type)
        if not (thumbFullPath is None):
            thumbObj = self.dbInst.getFsObjFromFullPath(thumbFullPath)
            thumbUfsUrl = thumbObj.getObjUfsUrl()
            item_info_dict["thumbnailFullPath"] = thumbFullPath
            item_info_dict["thumbnailUuid"] = thumbObj["uuid"]
            item_info_dict["thumbnailUrl"] = thumbUfsUrl
            item_info_dict["thumbnailHeadMd5"] = thumbObj.headMd5()
            #Store thumbnail info
            info_dict[thumbUfsUrl] = thumbObj.getItemInfo()
            #########################################
            #Add thumb file to zip, it is not stored until finalize the current trunk
            #########################################
            added_size = trunk_storage.add_file(thumbFullPath)
            ####################################################
            #Add item info, it is not stored until finalize the current trunk
            ####################################################
            self.add_new_info(info_dict, obj_item.getObjUfsUrl(), item_info_dict)
            ncl(item_info_dict)
            return added_size
            
        else:
            ncl("No thumb generated", fullPath)
            return 0