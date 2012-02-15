'''
Created on 2011-10-14

@author: Richard
'''
import xmlrpclib
import sys


def sync(folder, encZipFolder, passwd, workingDir, taskid):
    print folder, encZipFolder, passwd, workingDir, taskid
    proxy = xmlrpclib.ServerProxy("http://localhost:8807/xmlrpc")
    #argv1 task id, argv2 passwd
    
    targetUrl = proxy.addSync(taskid, folder, encZipFolder,
                              passwd, workingDir)
                            
    print targetUrl
    
if __name__ == '__main__':
    taskid = "helloworld"
    if len(sys.argv) > 2:
        taskid = sys.argv[2]
    sync("D:\\sys\\pidgin\\profile", "D:\\sys\\pidgin\\encZip", sys.argv[1], 'd:/tmp/fileman/working', taskid)