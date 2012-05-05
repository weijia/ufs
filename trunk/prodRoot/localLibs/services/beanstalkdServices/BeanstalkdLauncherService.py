'''
Created on 2012-02-13

@author: Richard
'''
#import os
#import time
import beanstalkc
#import traceback
#import threading

import localLibSys
import wwjufsdatabase.libs.utils.simplejson as json
from beanstalkServiceBaseV2 import beanstalkServiceBase, gBeanstalkdLauncherServiceTubeName


        
class BeanstalkdLauncherService(beanstalkServiceBase):
    def __init__(self, tubeName = gBeanstalkdLauncherServiceTubeName):
        super(BeanstalkdLauncherService, self).__init__(tubeName)
        self.taskid_cmd_tube_name_dict = {}
    def startServer(self):
        print self.__class__, self.tubeName
        self.watchTube()
        #!!!Not working. Kick all items to active when start, as we bury them in the previous processing
        #kickedItemNum = beanstalk.kick(gMaxMonitoringItems)
        #print kickedItemNum
        while True:
            try:
                job = self.beanstalk.reserve()
            except:
                self.stop()
                return
            print "got job", job.body
            item = json.loads(job.body)
            if item.has_key("cmd"):
                if item["cmd"] == "registration":
                    if item.has_key("pid"):
                        if item.has_key("cmd_tube_name"):
                            if self.taskid_cmd_tube_name_dict.has_key(item["pid"]):
                                if self.taskid_cmd_tube_name_dict[item["pid"]] != item["cmd_tube_name"]:
                                    print "registered but not the same"
                                else:
                                    print "already registered, same tube name"
                            else:
                                self.taskid_cmd_tube_name_dict[item["pid"]] = item["cmd_tube_name"]
                        else:
                            print "not a correct registration, no cmd_tube_name"
                    else:
                        print "not a correct registration, no pid"
                elif item["cmd"] == "stop":
                    if item.has_key("pid"):
                        if self.taskid_cmd_tube_name_dict.has_key(item["pid"]):
                            self.put_item({"cmd":"quit"}, self.taskid_cmd_tube_name_dict[item["pid"]])
                        else:
                            print "no tube name registered for pid", item["pid"], self.taskid_cmd_tube_name_dict
                    else:
                        print "not a valid cmd", item
            
            job.delete()
            
    def send_stop_singals(self):
        for i in self.taskid_cmd_tube_name_dict:
            self.put_item({"cmd":"quit"}, self.taskid_cmd_tube_name_dict[i])


if __name__ == "__main__":
    s = BeanstalkdLauncherService(gBeanstalkdLauncherServiceTubeName)
    s.startServer()