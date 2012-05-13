'''
Created on 2012-02-13

@author: Richard
'''
import beanstalkc


#from pprint import pprint

import localLibSys
from localLibs.services.clients.zippedCollectionListHandlerThumbClientV2 import AutoArchiveThumb
from beanstalkServiceBaseV2 import beanstalkWorkingThread, beanstalkServiceApp, beanstalkServiceBase
import localLibs.utils.misc as misc
import wwjufsdatabase.libs.utils.transform as transform 
import wwjufsdatabase.libs.tag.tagSystemInterfaceV2 as tagSystem
from localLibs.logSys.logSys import *


        
class TagProcessService(beanstalkServiceApp):
    '''
    input: {"tag":"", "output_tube_name":"", "target_dir":"", "working_dir":""}
    '''
    def __init__(self, input_tube_name = None):
        super(TagProcessService, self).__init__(input_tube_name)
        self.processing_tag_dict = {}
        
    def processItem(self, job, item):
        #fullPath = transform.transformDirToInternal(item["fullPath"])
        #monitoringFullPath = transform.transformDirToInternal(item["monitoringPath"])
        
        #source_dir = item["SourceDir"]
        #misc.ensureDir(source_dir)
        
        tag = item["tag"]
        
        task_item = item
        
        if item.has_key("output_tube_name"):
            #################################
            # Adding tag processing task
            #################################
            task_item = item
            self.processing_tag_dict[tag] = item
            import wwjufsdatabase.libs.services.servicesV2 as service
            req = service.req()
            t = tagSystem.getTagSysObj(req.getDbSys())
            tagged_item_list = t.getObjs(unicode(tag))
        else:
            #################################
            # A new tag added for existing tag processing task
            #################################
            if self.processing_tag_dict.has_key(tag):
                #Task exist, add the new tagged elment for processing
                task_item = self.processing_tag_dict[tag]
                tagged_item_list = [transform.transformDirToInternal(item["url"])]
            else:
                #Not a valid item, return
                print "not a valid item or tag not have processor yet"
                job.delete()
                return False
            
            
        output_tube_name = task_item["output_tube_name"]
        
        working_dir = task_item["working_dir"]
        misc.ensureDir(transform.transformDirToInternal(working_dir))
        
        target_dir = task_item["target_dir"]
        misc.ensureDir(transform.transformDirToInternal(target_dir))
        
        
        b = beanstalkServiceBase(output_tube_name)

        for i in tagged_item_list:
            info(i)
            source_dir = transform.transformDirToInternal(i)
            
            b.addItem({"source_dir":source_dir, "working_dir": working_dir, "target_dir":target_dir})

        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True
                

if __name__ == "__main__":
    s = TagProcessService()
    s.startServer()