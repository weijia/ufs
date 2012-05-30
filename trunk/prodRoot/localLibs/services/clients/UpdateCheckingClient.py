'''
Created on 2012-02-20

@author: Richard
'''

import uuid
import localLibSys
from localLibs.services.beanstalkdServices.UpdateCheckingService import UpdateCheckingService
from localLibs.services.beanstalkdServices.ReqDumpService import g_req_dump_service_tube_name


def check_updates():
    
    
    a = UpdateCheckingService()
    a.addItem({"full_path":"d:/tmp/update_checking", "black_list":[], 
                "target_tube_name":g_req_dump_service_tube_name, "state_collection_id":"test_update_checking"
                })

    
if __name__ == "__main__":
    check_updates()