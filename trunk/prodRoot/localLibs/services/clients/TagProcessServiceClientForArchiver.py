'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
from localLibs.services.beanstalkdServices.TagProcessServiceV2 import TagProcessService
from localLibs.services.beanstalkdServices.AutoArchiveService import AutoArchiveService



gWorkingDir = "D:/tmp/working/tmp_generated_files"
g_default_target_dir = "D:/tmp/working/default_target_dir"


def ProcessTagged(tag = u"archive", target_dir = g_default_target_dir,
                     workingDir = gWorkingDir):
    
    auto_archive_tag_output_tube_name = "AutoArchiveService_"+str(uuid.uuid4())
    
    a = AutoArchiveService()
    a.addItem({"input_tube_name":auto_archive_tag_output_tube_name})
    
    s1 = TagProcessService()
    s1.addItem({"working_dir": workingDir,
               "target_dir": target_dir, "tag":tag, 
               "output_tube_name":auto_archive_tag_output_tube_name})

    
if __name__ == "__main__":
    ProcessTagged()