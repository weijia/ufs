import localLibSys
from localLibs.thumb.thumbInterface import getThumb
import localLibs.utils.misc as misc
import localLibs.objSys.objectDatabaseV3 as objectDatabase
from localLibs.logSys.logSys import *
from ThumbCollector import InfoCollectorInterface

class FullContentCollector(InfoCollectorInterface):
    
    default_thumb_info_size = 100
    
    def __init__(self):
        super(FullContentCollector, self).__init__()
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
        full_path = obj_item.get_full_path()
        #########################################
        #Add file to storage
        #########################################
        added_size = trunk_storage.add_file(full_path)
        ####################################################
        #Add item info, it is not stored until finalize the current trunk
        ####################################################
        self.add_new_info(info_dict, obj_item.getObjUfsUrl(), {"content_path_in_storage":full_path})
        return added_size