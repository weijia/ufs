# File: hello1.py

import libSys
import desktopApp.mobileApp.lib.gaeItem
import desktopApp.mobileApp.lib.cfg
import os
import desktopApp.mobileApp.lib.treeLocator

def localFilesystemDecode(i):
    return i.decode('gb2312')
    
'''
>>> os.path.dirname("d:\\tmp\\hello\\")
'd:\\tmp\\hello'
>>> os.path.dirname("d:\\tmp\\hello")
'd:\\tmp'
>>> os.path.isdir("d:\\tmp\\hello")
False
>>> os.path.isdir("d:\\tmp\\hello\\")
False
>>> os.listdir("d:\\tmp")
['1', 'bbox', 'bld-pkg', 'btscoe_build.pl', 'btscoe_do_label.pl', 'build_commands-LTE2.0.txt', 'CCA_HAL_R20H_REL_04_txt_report.xls', 'CCA_LOG_R20H_REL_04_txt_report.xls', 'CCA_R2.0H_BLD-04.tar.gz', 'CCA_R2.0H_REL-04', 'cca_r2.0h_rel-main.cs', 'cr1346755.zip', 'cr_delta_1.03.00.out.q19420', 'dspmap', 'EXEC.catcr', 'fileBrowser', 'fullMakefile', 'gappproxy', 'git_repo', 'hapisb.ospf.bulid', 'ip.pl', 'Makefile', 'ospf.build', 'phy_eis.h', 'ramos', 'RSR10.1_Package_Info.xls', 'spel_CCA19.log', 'SwitchyOptions.bak', 'syncFile', 'tddtrial', 'tdd_r1.0_devintegration-multiue.cs', 'test.zip', 'test2', 'testzip.kk', 'TF#31point10_ant0_SF.dat', 'TF#31point10_ant1_SF.dat', 'token', 'ttyDownload.was', 'urllib', 'vxworks.h', 'w22792_tmp-ltedemo-tdd-r201-bld18.cs', 'w22792_tmp-ltedemo-tdd-r201-d17dp1704', 'WBTS-PHY-TDD_R2.0_REL-1.06.00_release_notes.doc', 'wxconsole', 'zch66bld01-2010-03-30-18-11-16.log', 'zch66bld01-2010-03-30-22-32-48.log', 'zch66bld01-2010-04-01-11-30-03.log', 'zch66bld01-2010-04-07-18-05-59.log', '~$a_0_0_07_release_notes_object_185.doc', '\xbc\xc6\xcb\xe3\xbb\xfa\xb3\xa3\xd3\xc3\xcb\xe3\xb7\xa8(PDG)', '\xbc\xc6\xcb\xe3\xbb\xfa\xb3\xa3\xd3\xc3\xcb\xe3\xb7\xa8(PDG).zip']
'''

class localTreeItem:
    def __init__(self, fullPath):
        self.fullPath = fullPath
        self.parentDir = os.path.dirname(self.fullPath)
        
    def getContainerItem(self):
        return self.parentDir

        
    def listNamedChildren(self):
        if not os.path.isdir(self.fullPath):
            return None
        res = {}
        d = os.listdir(self.fullPath)
        for i in d:
            res[os.path.join(self.fullPath, i)] = localFilesystemDecode(i)
        return res
        
    def child(self, fullPath):
        return localTreeItem(fullPath)
        
        
if __name__ == '__main__':

    i = localTreeItem("d:\\")    
    s = desktopApp.mobileApp.lib.treeLocator.tkFileSelector(i)

    