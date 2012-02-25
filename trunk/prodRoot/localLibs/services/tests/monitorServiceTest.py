'''
Created on 2012-02-20

@author: Richard
'''
import localLibSys
import localLibs.services.monitorService as monitorService
            
if __name__ == "__main__":
    s = monitorService.monitorService()
    s.addItem("d:/tmp/monitoring")