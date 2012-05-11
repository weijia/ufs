'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
from localLibs.services.beanstalkdServices.TagProcessServiceV2 import TagProcessService
from localLibs.services.beanstalkdServices.AutoExtractInfoWithThumbService import AutoExtractInfoWithThumbeService



gWorkingDir = "D:/tmp/working/fileArchiveService"
g_default_target_dir = "D:/tmp/working/default_target_dir"


def ProcessTagged(tag = u"useful", target_dir = g_default_target_dir,
                     workingDir = gWorkingDir):
    
    auto_ext_info_with_thumb_tube_name = "AutoExtractInfoWithThumbeService_"+str(uuid.uuid4())
    
    a = AutoExtractInfoWithThumbeService()
    a.addItem({"input_tube_name":auto_ext_info_with_thumb_tube_name})
    
    s1 = TagProcessService()
    s1.addItem({"working_dir": workingDir,
               "target_dir": target_dir, "tag":tag, 
               "output_tube_name":auto_ext_info_with_thumb_tube_name})

    
if __name__ == "__main__":
    ProcessTagged()