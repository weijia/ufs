'''
Created on 2012-05-30

@author: Richard
'''
from beanstalkServiceBaseV2 import beanstalkServiceApp

g_req_dump_service_tube_name = "req_dump_service_input_tube"

class ReqDumpService(beanstalkServiceApp):
    '''
    service request format:
    Depending on the input
    '''
        
    def processItem(self, job, item):
        job.delete()
        return False
        #Return true only when the item should be kept in the tube
        #return True

        
if __name__ == "__main__":
    s = ReqDumpService("req_dump_service_input_tube")
    s.startServer()