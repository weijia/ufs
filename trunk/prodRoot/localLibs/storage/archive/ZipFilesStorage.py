#import re
import localLibSys
#import wwjufsdatabase.libs.utils.simplejson as json
import wwjufsdatabase.libs.utils.transform as transform
#import localLibs.objSys.ufsObj as ufsObj
import wwjufsdatabase.libs.utils.fileTools as fileTools
import localLibs.utils.misc as misc
import localLibs.compress.zipClass as zipClass


from localLibs.logSys.logSys import *

gWorkingDir = "d:/tmp/working/zipfilestorage"

class StorageInterface(object):
    def __init__(self):
        pass
    
    def add_file(self, itemObj):
        pass
    
    def finalize_one_trunk(self):
        pass
    def get_storage_id(self):
        '''
        Used to identify this storage
        '''
        pass

    
class ZipFilesStorage(object):
    def __init__(self, trunk_data_path = gWorkingDir):
        super(ZipFilesStorage, self).__init__()
        self.trunk_data_path = trunk_data_path
        misc.ensureDir(self.trunk_data_path)
        ####################
        # The following var is not expected to be used in outside of this class
        self.zipFile = None
        self.zipFilePath = None
            
    def add_file(self, full_path):
        thumbnailZippedInfo = self.getZipFile().addfile(unicode(full_path), unicode(full_path))
        return thumbnailZippedInfo.compress_size

    def finalize_one_trunk(self):
        self.zipFile.close()
        #Set attribute so new zip will be created if this object is still in use
        self.zipFile = None
        return self.zipFilePath
    def get_storage_id(self):
        return "zip_file_storage://"+transform.transformDirToInternal(self.trunk_data_path)
    
    ################################################
    # The following functions are not recommended to be called from outside of this class
    def getZipFile(self):
        if self.zipFile is None:
            self.zipFilePath = transform.transformDirToInternal(
                fileTools.getTimestampWithFreeName(self.trunk_data_path, '.zip'))
            self.zipFile = zipClass.ZFile(self.zipFilePath, 'w')
        return self.zipFile
    