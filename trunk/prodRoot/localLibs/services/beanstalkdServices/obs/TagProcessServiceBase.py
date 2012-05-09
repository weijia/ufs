'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc


#from pprint import pprint

import localLibSys
from localLibs.services.clients.zippedCollectionListHandlerThumbClientV2 import AutoArchiveThumb
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp
import localLibs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform 
import wwjufsdatabase.libs.tag.tagSystemInterfaceV2 as tagSystem


        
class TagProcessServiceBase(beanstalkServiceApp):
    '''
    classdocs
    '''
    def __init__(self, tubeName = "TagProcessServiceBase"):
        super(TagProcessServiceBase, self).__init__(tubeName)

        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        
        #source_dir = item["SourceDir"]
        #misc.ensureDir(source_dir)
        
        tag = item["tag"]
        
        working_dir = item["WorkingDir"]
        misc.ensureDir(transform.transformDirToInternal(working_dir))
        
        target_dir = item["TargetDir"]
        misc.ensureDir(transform.transformDirToInternal(target_dir))
        
        import wwjufsdatabase.libs.services.servicesV2 as service
        req = service.req()
        t = tagSystem.getTagSysObj(req.getDbSys())
        e = t.getObjs(unicode(tag))
        for i in e:
            print i
            source_dir = transform.transformDirToInternal(i)
            
            AutoArchiveThumb(source_dir, target_dir, working_dir)
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        return True
                

if __name__ == "__main__":
    s = TagProcessServiceBase()
    s.startServer()