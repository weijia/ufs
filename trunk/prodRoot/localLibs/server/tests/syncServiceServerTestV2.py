import xmlrpclib
import sys

if __name__ == '__main__':
    proxy = xmlrpclib.ServerProxy("http://localhost:8807/xmlrpc")
    #argv1 task id, argv2 passwd
    taskid = "helloworld"
    if len(sys.argv) > 2:
        taskid = sys.argv[2]
    targetUrl = proxy.addSync(taskid, "D:\\sys\\pidgin\\profile", "D:\\sys\\pidgin\\encZip",
                              sys.argv[1], 'd:/tmp/fileman/working')
    print targetUrl