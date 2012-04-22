'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
import localLibs.services.beanstalkdServices.TagProcessServiceBase as TagProcessServiceBase



gAutoArchiveFullPath = "D:\\userdata\\q19420\\My Documents\\Tencent Files\\10132994\\Image"
gWorkingDir = "D:/tmp/working/fileArchiveService"
g_default_target_dir = "D:/tmp/working/default_target_dir"


def ProcessTagged(tag = u"download", target_dir = g_default_target_dir,
                     workingDir = gWorkingDir):
    
    s1 = TagProcessServiceBase.TagProcessServiceBase()
    s1.addItem({"WorkingDir": workingDir,
               "TargetDir": target_dir, "tag":tag})

    
if __name__ == "__main__":
    ProcessTagged()