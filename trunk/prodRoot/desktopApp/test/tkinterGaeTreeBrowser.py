# File: hello1.py

import libSys
import desktopApp.mobileApp.lib.gaeItem
import desktopApp.mobileApp.lib.cfg
import os
import desktopApp.mobileApp.lib.treeLocator
    
if __name__ == '__main__':
    c = desktopApp.mobileApp.lib.cfg.cfg("tkTestCfg.txt")
    settings = c.getSettings()
    gAppBaseDir = settings.get('workingDir', 'd:\\tmp\\fileBrowser')


    if not os.path.exists(gAppBaseDir):
        os.makedirs(gAppBaseDir)

    i = desktopApp.mobileApp.lib.gaeItem.gaeItem('3fe6382b-0219-40c7-add3-2f3b60aeb368', 'username', 'passwd', gAppBaseDir, None)
    
    s = desktopApp.mobileApp.lib.treeLocator.tkFileSelector(i)
    
    c.save(settings)
    