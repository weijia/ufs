'''
Created on 2012-02-20

@author: Richard
'''

import localLibSys
from localLibs.services.clients.zippedCollectionListHandlerThumbClientV2 import AutoArchiveThumb


gAutoArchiveFullPath = "D:\\userdata\\q19420\\My Documents\\Tencent Files\\10132994\\Image"
gWorkingDir = "D:/tmp/working/fileArchiveService"


if __name__ == "__main__":
    AutoArchiveThumb(gAutoArchiveFullPath, gWorkingDir)